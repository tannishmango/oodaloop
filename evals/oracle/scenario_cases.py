"""Hidden scenario-specific checks layered on the stable substrate oracle."""
from __future__ import annotations

from evals.runner.run import grade


TABLES = {"items": [{"id": 1, "value": None}, {"id": 2, "value": 3}]}


def _extension_case(candidate_execute, query, expected):
    try:
        actual = candidate_execute(query, TABLES)
        return actual == expected
    except Exception:
        return False


def grade_scenario(candidate_execute, scenario_id):
    result = grade(candidate_execute)
    extra = []
    select = lambda expression: {"from": {"table": "items", "as": "i"}, "select": {"result": expression}, "order_by": [{"field": "result"}]}
    if scenario_id in {"small-local", "no-surprise"}:
        query = select({"ne": [{"field": "i.value"}, {"literal": 3}]})
        extra.append({"name": "scenario-ne-expression", "passed": _extension_case(candidate_execute, query, [{"result": False}, {"result": True}])})
    elif scenario_id == "ready-leaf":
        query = select({"is_null": {"field": "i.value"}})
        extra.append({"name": "scenario-is-null-expression", "passed": _extension_case(candidate_execute, query, [{"result": False}, {"result": True}])})
    elif scenario_id == "broad-explicit":
        try:
            candidate_execute({"from": {"table": "items"}, "limit": -1}, TABLES)
            passed = False
        except Exception as error:
            passed = str(error).startswith("miniquery:")
        extra.append({"name": "scenario-error-prefix", "passed": passed})
    result["cases"].extend(extra)
    result["cases_passed"] += sum(item["passed"] for item in extra)
    result["cases_total"] += len(extra)
    result["passed"] = result["cases_passed"] == result["cases_total"]
    return result
