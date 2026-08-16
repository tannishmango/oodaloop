"""Grade any candidate module with an execute(query, tables) function."""
from __future__ import annotations

import argparse
import importlib
import json
import uuid

from evals.oracle.cases import all_cases
from evals.oracle.reference import QueryError, execute as oracle_execute


def grade(candidate_execute):
    details = []
    for case in all_cases():
        expected_error = case.get("error", False)
        try:
            expected = oracle_execute(case["query"], case["tables"])
            oracle_error = False
        except QueryError:
            expected, oracle_error = None, True
        try:
            actual = candidate_execute(case["query"], case["tables"])
            candidate_error = False
        except Exception:
            actual, candidate_error = None, True
        passed = oracle_error == candidate_error == expected_error and (candidate_error or actual == expected)
        details.append({"name": case["name"], "passed": passed})
    count = sum(item["passed"] for item in details)
    return {"passed": count == len(details), "cases_passed": count, "cases_total": len(details), "cases": details}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default="evals.seed_project.miniquery")
    parser.add_argument("--condition", choices=("host-native", "pre-redesign", "main", "pr1", "future"), required=True)
    parser.add_argument("--scenario", default="semantic-substrate")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    candidate = importlib.import_module(args.candidate)
    result = {"schema_version": 1, "run_id": args.run_id or str(uuid.uuid4()), "condition": args.condition, "scenario_id": args.scenario, "semantic": grade(candidate.execute), "trajectory": None}
    rendered = json.dumps(result, sort_keys=True, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as stream: stream.write(rendered + "\n")
    print(rendered)
    return 0 if result["semantic"]["passed"] else 1


if __name__ == "__main__": raise SystemExit(main())

