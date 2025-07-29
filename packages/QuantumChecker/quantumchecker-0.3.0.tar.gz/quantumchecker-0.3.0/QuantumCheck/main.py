import logging
import os
import zipfile
from datetime import datetime
from typing import List, Dict
from .python_evaluator import PythonEvaluator
from .sql_evaluator import SQLEvaluator
from .powerbi_evaluator import PowerBIEvaluator
from .ssis_evaluator import SSISEvaluator
import asyncio

_logger_cache = {}

class HomeworkEvaluator:
    EVALUATOR_REGISTRY = {
        "python": PythonEvaluator,
        "sql": SQLEvaluator,
        "powerbi": PowerBIEvaluator,
        "ssis": SSISEvaluator
    }

    EXTENSION_TO_TYPE = {
        ".py": "python",
        ".sql": "sql",
        ".pbit": "powerbi",
        ".pdf": "powerbi",
        ".dtsx": "ssis",
        ".DTSX": "ssis",
        ".txt": "text",
        ".md": "text"
    }

    API_NAME_MAPPING = {
        "python": "Google Gemini API",
        "sql": "Google Gemini API",
        "powerbi": "Google Gemini API",
        "ssis": "Google Gemini API",
        "text": "Google Gemini API"
    }

    def __init__(self, log_level: int = logging.INFO):
        self.log_level = log_level
        self._successful_key_cache = {}
        self._rate_limit_delay = {}
        self._invalid_key_cache = set()
        self._lock = asyncio.Lock()
        self._last_request_time = None

    def _get_logger(self, log_type: str) -> logging.Logger:
        log_name = f"{log_type}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        if log_name not in _logger_cache:
            logger = logging.getLogger(log_name)
            logger.setLevel(self.log_level)
            if not logger.handlers:
                handler = logging.StreamHandler()
                handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
                logger.addHandler(handler)
            _logger_cache[log_name] = logger
        return _logger_cache[log_name]

    def parse_questions(self, content: str) -> List[str]:
        logger = self._get_logger("QuantumCheck.main")
        questions = [q.strip() for q in content.split("\n\n") if q.strip()]
        if not questions:
            raise ValueError("No valid questions found in content")
        return questions

    def _detect_zip_content_type(self, zip_path: str, logger: logging.Logger) -> str:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            extensions = {os.path.splitext(name)[1].lower() for name in zip_ref.namelist()}
            file_types = [self.EXTENSION_TO_TYPE.get(ext, "text") for ext in extensions if ext]
            if "python" in file_types:
                return "python"
            elif "sql" in file_types:
                return "sql"
            elif "powerbi" in file_types:
                return "powerbi"
            elif "ssis" in file_types:
                return "ssis"
            else:
                return "text"

    async def evaluate_from_content(
        self,
        question_content: str,
        answer_path: str,
        api_keys: List[str],
        question_type: str,
        retry_count: int = 0
    ) -> Dict[str, any]:
        async with self._lock:
            now = datetime.now()
            if self._last_request_time:
                elapsed = (now - self._last_request_time).total_seconds()
                if elapsed < 30:
                    await asyncio.sleep(30 - elapsed)
            self._last_request_time = datetime.now()

            try:
                questions = self.parse_questions(question_content)
            except ValueError as e:
                logger = self._get_logger("QuantumCheck.main")
                return {
                    "score": 0,
                    "feedback": f"Error parsing question content: {str(e)}",
                    "issues": [str(e)],
                    "recommendations": [],
                    "used_api_key_index": None,
                    "used_api_name": None
                }

            answer_path = answer_path.strip()
            _, ext = os.path.splitext(answer_path)
            ext = ext.lower()

            if ext == ".zip":
                logger = self._get_logger("zip")
                file_type = self._detect_zip_content_type(answer_path, logger)
            else:
                file_type = self.EXTENSION_TO_TYPE.get(ext, "text")
                logger = self._get_logger(file_type)

            eval_type = question_type if question_type in self.EVALUATOR_REGISTRY else file_type

            if not os.path.exists(answer_path):
                return {
                    "score": 0,
                    "feedback": f"Answer file not found: {answer_path}",
                    "issues": [f"Answer file not found: {answer_path}"],
                    "recommendations": [],
                    "used_api_key_index": None,
                    "used_api_name": None
                }

            evaluator_class = self.EVALUATOR_REGISTRY.get(eval_type, PythonEvaluator)
            last_error_messages = []

            available_keys = [(i + 1, key) for i, key in enumerate(api_keys) if key not in self._invalid_key_cache]

            cached_key_idx = self._successful_key_cache.get(eval_type)
            if cached_key_idx is not None and cached_key_idx < len(api_keys):
                cached_key = api_keys[cached_key_idx]
                if cached_key not in self._invalid_key_cache:
                    available_keys.insert(0, (cached_key_idx + 1, cached_key))

            if not available_keys:
                return {
                    "score": 0,
                    "feedback": "No valid API keys available.",
                    "issues": ["All API keys are invalid or rate-limited."],
                    "recommendations": [],
                    "used_api_key_index": None,
                    "used_api_name": None
                }

            for idx, key in available_keys:
                if key in self._rate_limit_delay:
                    delay_until = self._rate_limit_delay[key]
                    current_time = datetime.now()
                    delay_until_time = datetime.fromtimestamp(delay_until)
                    if current_time < delay_until_time:
                        continue
                    else:
                        del self._rate_limit_delay[key]

                evaluator = evaluator_class(key)
                api_name = getattr(evaluator, 'get_api_name', lambda: self.API_NAME_MAPPING.get(eval_type, "Unknown API"))()

                try:
                    evaluation = evaluator.evaluate(questions, answer_path, temp_dir=f"temp_extract_{os.getpid()}_{idx}")
                    feedback = evaluation.get("feedback", "").lower()
                    issues = " ".join(evaluation.get("issues", [])).lower()

                    if any(phrase in feedback or phrase in issues for phrase in ["api key not valid", "api_key_invalid"]):
                        last_error_messages.append(f"API key #{idx} invalid.")
                        self._invalid_key_cache.add(key)
                        continue

                    if any(phrase in feedback or phrase in issues for phrase in ["429", "too many requests", "rate limit"]):
                        last_error_messages.append(f"API key #{idx} rate limited.")
                        self._rate_limit_delay[key] = datetime.now().timestamp() + 300
                        continue

                    if any(phrase in feedback or phrase in issues for phrase in ["503", "service unavailable"]):
                        last_error_messages.append(f"API key #{idx} service unavailable.")
                        self._rate_limit_delay[key] = datetime.now().timestamp() + 7200
                        continue

                    if evaluation.get("score", 0) == 0 and "evaluation not returned" in feedback:
                        last_error_messages.append(f"API key #{idx} returned invalid evaluation.")
                        continue

                    self._successful_key_cache[eval_type] = idx - 1
                    return {
                        "score": evaluation.get("score", 0),
                        "feedback": evaluation.get("feedback", "No feedback provided"),
                        "issues": evaluation.get("issues", []),
                        "recommendations": evaluation.get("recommendations", []),
                        "used_api_key_index": idx,
                        "used_api_name": api_name
                    }

                except Exception as e:
                    last_error_messages.append(f"Exception with key #{idx}: {str(e)}")
                    if "429" in str(e) or "rate limit" in str(e).lower():
                        self._rate_limit_delay[key] = datetime.now().timestamp() + 300
                    elif "503" in str(e) or "service unavailable" in str(e).lower():
                        self._rate_limit_delay[key] = datetime.now().timestamp() + 7200
                    continue

            if retry_count < 3 and self._rate_limit_delay:
                next_available_ts = min(self._rate_limit_delay.values())
                wait_time = max(0, next_available_ts - datetime.now().timestamp())
                await asyncio.sleep(wait_time + 1)
                return await self.evaluate_from_content(
                    question_content=question_content,
                    answer_path=answer_path,
                    api_keys=api_keys,
                    question_type=question_type,
                    retry_count=retry_count + 1
                )

            return {
                "score": 0,
                "feedback": "Evaluation failed with all API keys." if retry_count >= 3 else "All API keys are temporarily unavailable.",
                "issues": last_error_messages if last_error_messages else ["All API keys failed to evaluate the submission."],
                "recommendations": [],
                "used_api_key_index": None,
                "used_api_name": None
            }
