import asyncio
from QuantumCheck import HomeworkEvaluator

question_sets = {
    "python_beginner": "Write a Python function to calculate factorial.\nWrite a Python script to reverse a string.",
    "power_bi": "Create a Power BI report with a bar chart.\nExplain DAX measures for sales analysis.",
    "sql": "Write a SQL query to join two tables.\nWrite a SQL query for aggregate functions.",
    "ssis": "Design an SSIS package for data import.\nExplain SSIS control flow tasks."
}

answer_paths = {
    "python": ["../tests/answer/python1.zip"],
    "powerbi": ["../tests/answer/real.zip"],
    "sql": ["../tests/answer/sql3.zip"],
    "ssis": ["../tests/answer/answer.dtsx"]
}

question_type_mapping = {
    "python_beginner": "python",
    "power_bi": "powerbi",
    "sql": "sql",
    "ssis": "ssis"
}


def format_score(score):
    if score >= 90:
        return f"🟢 Excellent ({score}⭐)"
    elif score >= 75:
        return f"🟡 Good ({score})"
    elif score >= 50:
        return f"🟠 Pass ({score})"
    else:
        return f"🔴 Fail ({score})"
API_KEY = "<KEY>"
async def run_evaluation(evaluator, q_key, q_content, question_type, answer_path, index):
    try:
        evaluation = await evaluator.evaluate_from_content(
            question_content=q_content,
            answer_path=answer_path,
            api_key=API_KEY,
            question_type=question_type
        )
        score = evaluation.get("score", 0)
        return (q_key, index, "success", score)
    except Exception as e:
        return (q_key, index, "error", str(e))

async def main():
    evaluator = HomeworkEvaluator()
    tasks = []

    for q_key, q_content in question_sets.items():
        question_type = question_type_mapping[q_key]
        paths = answer_paths.get(question_type, [])
        if not paths:
            print(f"⚠️ No answer paths found for question type '{question_type}'")
            continue
        for i in range(10):  # run each set 10 times
            for path in paths:
                task = run_evaluation(evaluator, q_key, q_content, question_type, path, i + 1)
                tasks.append(task)

    results = await asyncio.gather(*tasks)

    # Group results by question key
    grouped = {}
    for q_key, index, status, output in results:
        if q_key not in grouped:
            grouped[q_key] = []
        grouped[q_key].append((index, status, output))

    # Sort and print all at once, grouped by question
    for q_key in grouped:
        print(f"\n📘 {q_key.upper()} Results")
        for index, status, output in sorted(grouped[q_key], key=lambda x: x[0]):
            if status == "success":
                print(f"  ⏱️ Run {index:02}: {format_score(output)}")
            else:
                print(f"  ⏱️ Run {index:02}: ❌ Error - {output}")

asyncio.run(main())
