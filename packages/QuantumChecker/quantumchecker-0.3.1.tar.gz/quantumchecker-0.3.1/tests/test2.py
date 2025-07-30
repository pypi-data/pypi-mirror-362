import asyncio
from QuantumCheck import HomeworkEvaluator

async def main():
    evaluator = HomeworkEvaluator()

    question_content = """
    Q1: Write a Python function that calculates the factorial of a number.

    Q2: What is the difference between a list and a tuple in Python?
    """

    answer_path = "answer/python1.zip"

    question_type = "python"

    result = await evaluator.evaluate_from_content(
        question_content=question_content,
        answer_path=answer_path,
        api_key="AIzaSyC2B_Q38DkCl6O8y4b5hAWEpb6aJHW6FcY",
        question_type=question_type
    )

    result2 = await evaluator.evaluate_from_content(
        question_content=question_content,
        answer_path=answer_path,
        api_key="AIzaSyC2B_Q38DkCl6O8y4b5hAWEpb6aJHW6FcY",
        question_type=question_type
    )

    print("Evaluation Result:")
    print(result["score"])
    print(result["feedback"])

    print("Evaluation Result:")
    print(result2["score"])
    print(result2["feedback"])


if __name__ == "__main__":
    asyncio.run(main())
