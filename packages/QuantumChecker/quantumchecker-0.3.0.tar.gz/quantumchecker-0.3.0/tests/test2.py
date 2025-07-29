import asyncio
from QuantumCheck import HomeworkEvaluator

async def main():
    evaluator = HomeworkEvaluator()

    question_content = """
    Q1: Write a Python function that calculates the factorial of a number.

    Q2: What is the difference between a list and a tuple in Python?
    """

    answer_path = "answer/python1.zip"
    api_keys = []

    question_type = "python"

    result = await evaluator.evaluate_from_content(
        question_content=question_content,
        answer_path=answer_path,
        api_keys=api_keys,
        question_type=question_type
    )

    print("Evaluation Result:")
    print(result["score"])
    print(result["feedback"])


if __name__ == "__main__":
    asyncio.run(main())
