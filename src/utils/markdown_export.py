def export_use_cases_to_markdown(results):
    import datetime
    import json

    timestamp = datetime.datetime.now()

    with open("use_cases.md", "w", encoding="utf-8") as f:
        f.write("# Web Scraping Agent\n")
        f.write(f"Generated on: {timestamp}\n\n")

        for case in results:
            f.write(f"## {case['test_name']}\n\n")

            f.write("### Input URL\n")
            f.write(case["url"] + "\n\n")

            f.write("### Researcher Output\n```\n")
            f.write(case["researcher_output"])
            f.write("\n```\n\n")

            f.write("### Evaluator Output\n```\n")
            f.write(json.dumps(case["evaluator_output"], indent=4))
            f.write("\n```\n\n")
