import asyncio
import logging
import random
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
from QuantumCheck import HomeworkEvaluator
from backoff import on_exception, expo
from google.api_core.exceptions import TooManyRequests


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("evaluation.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


question_sets = {
    "python_beginner": "Your Python beginner questions content here...",
    "power_bi": "Your Power BI questions content here...",
    "sql": "Your SQL questions content here...",
    "ssis": "Your SSIS questions content here..."
}

answer_paths = {
    "python": ["../tests/answer/python1.zip"],
    "power_bi": ["../tests/answer/real.zip"],
    "sql": ["../tests/answer/sql3.zip"],
    "ssis":["../tests/answer/answer.dtsx"]
}

question_type_mapping = {
    "python_beginner": "python",
    "power_bi": "power_bi",
    "sql": "sql",
    "ssis": "ssis"
}

api_keys = []


evaluator = HomeworkEvaluator(log_level=logging.INFO)

@on_exception(expo, TooManyRequests, max_tries=5, max_time=300)
async def evaluate_async(question_text: str, answer_path: str, api_keys: List[str], question_type: str) -> Dict:
    """Wrap the async evaluate function with exponential backoff for rate limit errors."""
    try:
        return await evaluator.evaluate_from_content(
            question_content=question_text,
            answer_path=answer_path,
            api_keys=api_keys,
            question_type=question_type
        )
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}")
        return {
            "score": 0,
            "feedback": f"Evaluation failed: {str(e)}",
            "issues": [str(e)],
            "recommendations": [],
            "used_api_key_index": None,
            "used_api_name": None
        }

async def main(num_requests: int = 10, max_workers: int = 6):
    resource_exhausted_count = 0
    logger.info(f"Starting evaluation with {num_requests} requests and {max_workers} workers")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        loop = asyncio.get_running_loop()
        tasks = []

        for i in range(num_requests):
            question_key = random.choice(list(question_sets.keys()))
            question_text = question_sets[question_key]
            question_type = question_type_mapping.get(question_key, "python")
            answer_path = random.choice(answer_paths.get(question_type, answer_paths["python"]))

            logger.info(f"Scheduling Request #{i + 1} for '{question_key}' with '{answer_path}'")
            task = loop.create_task(evaluate_async(question_text, answer_path, api_keys, question_type))
            tasks.append((i + 1, task))


        results = []
        for i, task in tasks:
            try:
                result = await task
                if "resource exhausted" in str(result.get("feedback", "")).lower():
                    resource_exhausted_count += 1
                results.append((i, result))
            except Exception as e:
                logger.error(f"Request #{i} failed with error: {str(e)}")
                if "resource exhausted" in str(e).lower():
                    resource_exhausted_count += 1
                results.append((i, {
                    "score": 0,
                    "feedback": f"Request failed: {str(e)}",
                    "issues": [str(e)],
                    "recommendations": [],
                    "used_api_key_index": None,
                    "used_api_name": None
                }))

    logger.info("All evaluations completed")

    for i, result in results:
        score = result.get("score", 0)
        feedback = result.get("feedback", "")
        used_key_index = result.get("used_api_key_index", "N/A")
        used_api_name = result.get("used_api_name", "N/A")

        feedback_words = feedback.split()
        partial_feedback = " ".join(feedback_words[:40]) + ("..." if len(feedback_words) > 10 else "")

        if score == 0 and "failed" in feedback.lower():
            logger.error(f"Request #{i} failed with error: {feedback}")
            print(f"X Request #{i} failed with error: {feedback}")
        else:
            logger.info(f"Request #{i} succeeded: Score = {score}, API Index = {used_key_index}, API Name = {used_api_name}")
            print(f"O Request #{i} succeeded: Score = {score}, API Index = {used_key_index}, API Name = {used_api_name}")
            print(f"   Feedback preview: {partial_feedback}\n")

    logger.info(f"Total 'resource exhausted' errors encountered: {resource_exhausted_count}")
    print(f"Total 'resource exhausted' errors encountered: {resource_exhausted_count}")

if __name__ == "__main__":
    try:
        asyncio.run(main(num_requests=100, max_workers=20))
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        print(f"Fatal error in main: {e}")