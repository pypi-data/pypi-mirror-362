import json
import logging
import os
import re
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List
from pdf2image import convert_from_path
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests
from dotenv import load_dotenv
from PIL import Image
import io
import base64


def prompt_text_powerbi(combined_content: str) -> str:
    return f"""
    Evaluate the following Power BI DAX question-answer pairs for correctness, clarity, and appropriateness.
    Provide an overall score out of 100 and concise feedback. Focus on DAX logic and structure.
    Structure the response as:
    OVERALL SCORE: [SCORE]/100
    [FEEDBACK]

    {combined_content}
    """


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("../powerbi_evaluator.log"), logging.StreamHandler()]
)


class GeminiFlashModel:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY") or api_key
        if not api_key:
            raise ValueError("API key not found in .env file or environment variables.")
        self.api_key = api_key
        self.model_name = model_name
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=4, max=10),
        retry=retry_if_exception_type((requests.exceptions.RequestException,))
    )
    def evaluate(self, question_answer_pairs: List[Dict[str, str]]) -> Dict[str, any]:
        logger.info("Starting evaluation of %d Power BI question-answer pairs", len(question_answer_pairs))
        combined_content = "\n\n".join(
            f"Question {i}:\n{qa['question']}\n\nAnswer {i}:\n{qa['answer']}\n"
            for i, qa in enumerate(question_answer_pairs, 1)
        )
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt_text_powerbi(combined_content)}]}]}
        response = requests.post(f"{self.endpoint}?key={self.api_key}", headers=headers, json=data)
        if response.status_code != 200:
            logger.error("API request failed: Status %d, Response: %s", response.status_code, response.text)
            raise Exception(f"API call failed: {response.status_code} - {response.text}")
        response_data = response.json()
        if not response_data.get("candidates"):
            logger.error("API response missing candidates: %s", response_data)
            raise ValueError("No candidates in API response")
        generated_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        return self._parse_response(generated_text)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=4, max=10),
        retry=retry_if_exception_type((requests.exceptions.RequestException,))
    )
    def evaluate_visuals(self, question: str, image_folder: str) -> Dict[str, any]:
        folder_path = Path(image_folder)
        images = list(folder_path.glob("*.png"))[:3]
        if not images:
            raise ProcessingError(f"No PNG images found in {image_folder}")
        prompt = (
            "Evaluate the Power BI report visuals based on the provided task. The visuals are professional dashboards designed for enterprise use.\n\n"
            f"Task: {question}\n\n"
            f"Screenshots: {[str(img.name) for img in images]}\n\n"
            "Evaluate based on the following criteria, assigning a score out of 100:\n"
            "- Clarity (30%): Are visuals clear, with readable labels, titles, and legends?\n"
            "- Appropriateness (30%): Are chart types (e.g., bar, line, pie) suitable for the data and task?\n"
            "- Color Usage (20%): Are colors consistent, accessible, and visually appealing? Consider contrast and colorblind accessibility.\n"
            "- Interactivity (20%): Do visible slicers, filters, or tooltips enhance usability and data exploration?\n\n"
            "Provide a score for overall quality, considering the enterprise context. Avoid overly harsh penalties for minor issues.\n"
            "Provide concise, supportive feedback for beginners, highlighting strengths and areas for improvement.\n\n"
            "Structure the response as:\n"
            "Score: [SCORE]/100\n"
            "Feedback: [FEEDBACK]"
        )
        parts = [{"text": prompt}]
        for img in images:
            with Image.open(img) as pil_img:
                pil_img.thumbnail((1024, 1024))
                img_buffer = io.BytesIO()
                pil_img.save(img_buffer, format="PNG")
                parts.append({
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                    }
                })
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": parts}]}
        response = requests.post(f"{self.endpoint}?key={self.api_key}", headers=headers, json=data)
        if response.status_code != 200:
            logger.error("API request failed: Status %d, Response: %s", response.status_code, response.text)
            raise Exception(f"API call failed: {response.status_code} - {response.text}")
        response_data = response.json()
        if not response_data.get("candidates"):
            logger.error("API response missing candidates: %s", response_data)
            raise ValueError("No candidates in API response")
        output_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        score_match = re.search(r"Score:\s*(\d+)(?:/100)?", output_text)
        feedback_match = re.search(r"Feedback:\s*(.*)", output_text, re.DOTALL)
        return {
            "score": int(score_match.group(1)) if score_match else 0,
            "feedback": feedback_match.group(1).strip() if feedback_match else "No visual feedback generated"
        }

    def _parse_response(self, text: str) -> Dict[str, any]:
        result = {"score": 0, "feedback": "Evaluation not returned by API.", "issues": [], "recommendations": []}
        try:
            lines = text.split("\n")
            score_found = False
            feedback_lines = []
            for line in lines:
                line = line.strip()
                if not score_found and line.startswith("OVERALL SCORE:") and "/100" in line:
                    try:
                        result["score"] = int(line.split(":")[1].split("/")[0].strip())
                        score_found = True
                    except ValueError:
                        result["issues"].append("Failed to parse score from API response")
                        continue
                elif score_found:
                    feedback_lines.append(line)
            if feedback_lines:
                result["feedback"] = "\n".join(feedback_lines).strip()
            return result
        except Exception as e:
            result["issues"].append(str(e))
            return result


class PowerBIProcessor:
    def extract_datamodel(self, pbit_file_path: str) -> Dict:
        if not os.path.exists(pbit_file_path):
            raise ProcessingError(f"PBIT file not found: {pbit_file_path}")
        folder_path = os.path.dirname(pbit_file_path)
        file_name = os.path.splitext(os.path.basename(pbit_file_path))[0]
        zip_file = os.path.join(folder_path, f"{file_name}.zip")
        export_path = os.path.join(folder_path, "export")
        self._cleanup(zip_file, export_path)
        try:
            os.rename(pbit_file_path, zip_file)
            if not zipfile.is_zipfile(zip_file):
                raise ProcessingError(f"File is not a valid ZIP: {zip_file}")
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(export_path)
            schema_path = os.path.join(export_path, "DataModelSchema")
            txt_path = os.path.join(export_path, "DataModelSchema.txt")
            os.rename(schema_path, txt_path)
            with open(txt_path, "r", encoding="utf-16-le") as file:
                return json.load(file)
        except UnicodeDecodeError as e:
            logger.error("Failed to decode DataModelSchema: %s", str(e))
            raise ProcessingError(f"Invalid encoding in DataModelSchema: {e}")
        except Exception as e:
            raise ProcessingError(f"Failed to extract DataModelSchema: {e}")
        finally:
            self._cleanup(zip_file, export_path)

    def extract_model_data(self, data: Dict) -> Dict:
        try:
            tables = data.get("model", {}).get("tables", [])
            relationships = data.get("model", {}).get("relationships", [])
            return {
                "Calculated Measures": self._get_measures(tables),
                "Tables": self._get_tables_and_columns(tables),
                "Relationships": self._get_relationships(relationships)
            }
        except Exception as e:
            raise ProcessingError(f"Failed to extract model data: {e}")

    def process_pdf(self, pdf_path: str, output_dir: str = "outputimages", num_pages: int = 3) -> List[str]:
        try:
            if not os.path.exists(pdf_path):
                raise ProcessingError(f"PDF file not found: {pdf_path}")
            os.makedirs(output_dir, exist_ok=True)
            pages = convert_from_path(pdf_path, first_page=1, last_page=num_pages)
            image_paths = []
            for i, page in enumerate(pages):
                image_path = os.path.join(output_dir, f"page_{i + 1}.png")
                page.save(image_path, "PNG")
                image_paths.append(image_path)
            os.remove(pdf_path)
            return image_paths
        except Exception as e:
            raise ProcessingError(f"Failed to process PDF: {e}")

    def extract_zip(self, zip_path: str, extract_path: str) -> tuple[str, str | None]:
        try:
            if not os.path.exists(zip_path):
                raise ProcessingError(f"ZIP file not found: {zip_path}")
            if not zipfile.is_zipfile(zip_path):
                raise ProcessingError(f"File is not a valid ZIP: {zip_path}")
            os.makedirs(extract_path, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)
            pbit_files = list(Path(extract_path).glob("*.pbit"))
            pdf_files = list(Path(extract_path).glob("*.pdf"))
            if not pbit_files:
                raise ProcessingError("ZIP file must contain at least one .pbit file")
            if len(pbit_files) > 1:
                raise ProcessingError("ZIP file contains multiple .pbit files")
            pdf_path = str(pdf_files[0]) if pdf_files else None
            return str(pbit_files[0]), pdf_path
        except Exception as e:
            raise ProcessingError(f"Failed to extract ZIP file: {e}")

    @staticmethod
    def _get_measures(tables: List[Dict]) -> List[Dict]:
        measures = []
        for table in tables:
            if "measures" in table:
                for measure in table["measures"]:
                    measures.append({
                        "Table": table["name"],
                        "Name": measure["name"],
                        "Expression": " ".join(measure.get("expression", "")) if isinstance(measure.get("expression"), list) else measure.get("expression", ""),
                        "FormatString": measure.get("formatString", "")
                    })
        return measures

    @staticmethod
    def _get_tables_and_columns(tables: List[Dict]) -> List[Dict]:
        table_info = []
        for table in tables:
            columns = [
                {
                    "Column Name": col["name"],
                    "Data Type": col.get("dataType", "Unknown"),
                    "Source Column": col.get("sourceColumn", "N/A"),
                    "Calculated": col.get("type") == "calculated"
                }
                for col in table.get("columns", [])
            ]
            expressions = [part["source"]["expression"] for part in table.get("partitions", []) if part["source"].get("expression")]
            table_info.append({"Table Name": table["name"], "Columns": columns, "Expressions": expressions})
        return table_info

    @staticmethod
    def _get_relationships(relationships: List[Dict]) -> List[Dict]:
        return [
            {
                "From Table": rel["fromTable"],
                "From Column": rel["fromColumn"],
                "To Table": rel["toTable"],
                "To Column": rel["toColumn"],
                "Join Behavior": rel.get("joinOnDateBehavior", "N/A")
            }
            for rel in relationships
        ]

    @staticmethod
    def _cleanup(*paths: str):
        for path in paths:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path, ignore_errors=True)


class PowerBIEvaluator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = GeminiFlashModel(api_key)
        self.processor = PowerBIProcessor()

    def evaluate(self, questions: List[str], answer_path: str, temp_dir: str = "temp_extract") -> Dict[str, any]:
        try:
            _, ext = os.path.splitext(answer_path)
            ext = ext.lower()
            extract_path = temp_dir
            pbit_path = None
            pdf_path = None
            if ext == ".zip":
                pbit_path, pdf_path = self.processor.extract_zip(answer_path, extract_path)
            elif ext == ".pbit":
                pbit_path = answer_path
                pdf_path = None
            else:
                logger.error("Invalid file type for Power BI: %s", answer_path)
                return {
                    "score": 0,
                    "feedback": f"Invalid file type: {ext}. Expected .pbit or .zip",
                    "issues": ["Invalid file type"],
                    "recommendations": [],
                    "dax_score": 0,
                    "visual_score": 0
                }
            try:
                data_model = self.processor.extract_datamodel(pbit_path)
                model_data = self.processor.extract_model_data(data_model)
                answers = [json.dumps(model_data)] * len(questions)
                dax_result = self.model.evaluate([{"question": q, "answer": a} for q, a in zip(questions, answers)])
                result = {
                    "score": 0,
                    "feedback": f"DAX Feedback:\n{dax_result['feedback']}",
                    "issues": dax_result["issues"],
                    "recommendations": dax_result["recommendations"],
                    "dax_score": dax_result["score"],
                    "visual_score": 0
                }
                if pdf_path:
                    try:
                        image_paths = self.processor.process_pdf(pdf_path, output_dir=os.path.join(temp_dir, "outputimages"))
                        visual_result = self.model.evaluate_visuals(questions[0], os.path.join(temp_dir, "outputimages"))
                        result["score"] = int(0.7 * dax_result["score"] + 0.3 * visual_result["score"])
                        result["visual_score"] = visual_result["score"]
                        result["feedback"] += f"\n\nVisual Feedback:\n{visual_result['feedback']}"
                        result["issues"].extend([f"Visual: {i}" for i in visual_result.get("issues", [])])
                        result["recommendations"].extend(visual_result.get("recommendations", []))
                    except ProcessingError as e:
                        logger.warning("Failed to process PDF, proceeding with DAX evaluation only: %s", str(e))
                        result["score"] = dax_result["score"]
                        result["issues"].append(f"Visual evaluation skipped: {str(e)}")
                        result["recommendations"].append("Ensure a valid PDF is provided for visual evaluation if intended")
                else:
                    result["score"] = dax_result["score"]
                    result["feedback"] += "\n\nVisual Feedback:\nNo visuals provided for evaluation."
                    result["issues"].append("No PDF provided for visual evaluation")
                    result["recommendations"].append("Include a PDF with report visuals for complete evaluation")
                logger.info("[DAX] Score: %d/100", result["dax_score"])
                logger.info("[Visual] Score: %d/100", result["visual_score"])
                logger.info("[Final] Score (70%% DAX, 30%% Visuals): %d/100", result["score"])
                return result
            finally:
                self.processor._cleanup(extract_path, os.path.join(temp_dir, "outputimages"))
        except Exception as e:
            logger.exception("Failed to evaluate Power BI file %s: %s", answer_path, str(e))
            self.processor._cleanup(extract_path, os.path.join(temp_dir, "outputimages"))
            return {
                "score": 0,
                "feedback": f"Error processing file: {str(e)}",
                "issues": [str(e)],
                "recommendations": ["Check file formats and API connectivity", "Review logs for detailed errors"],
                "dax_score": 0,
                "visual_score": 0
            }


class ProcessingError(Exception):
    pass
