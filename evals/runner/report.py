"""Turn a graded suite into a human-readable REPORT.md."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONDITION_ORDER = ("host-native", "main", "pr1")
SCENARIO_ORDER = ("small-local", "broad-explicit", "small-consequential", "ready-leaf", "no-surprise", "latent-coupling")
PAIR_ORDER = ("routing", "handoff", "surprise")


def load_reading():
    return json.loads((ROOT / "evals" / "scenarios" / "grading" / "reading.json").read_text(encoding="utf-8"))


def failed_checks(result):
    return [name for name, ok in result["trajectory"]["checks"].items() if not ok]


def extra_case_failed(result):
    cases = result["semantic"].get("cases") or []
    extras = [case for case in cases if str(case.get("name", "")).startswith("scenario-") and not case.get("passed")]
    return extras[0]["name"] if extras else None


def explain_check(reading, name):
    text = reading["checks"].get(name)
    if text is None:
        return f"Failed an undocumented check `{name}`."
    return text


def imply(reading, result):
    if result.get("protocol_error"):
        return f"The cell crashed before grading ({result['protocol_error']})."
    bits = []
    facts = result["trajectory"]["facts"]
    failed = set(failed_checks(result))
    if facts.get("user_questions") and not result["semantic"]["passed"]:
        bits.append("Stopped to ask the user (often: run `/oodaloop-init`) and never finished the task.")
    elif facts.get("user_questions"):
        bits.append("Asked the user a question during the run.")
    extra = extra_case_failed(result)
    if extra == "scenario-ne-expression":
        bits.append("Core library still worked, but `ne` was not implemented.")
    elif extra == "scenario-is-null-expression":
        bits.append("Core library still worked, but `is_null` was not implemented.")
    elif extra == "scenario-error-prefix":
        bits.append("Core library still worked, but the `miniquery:` error prefix was not applied.")
    elif not result["semantic"]["passed"] and "semantic_success" in failed:
        passed, total = result["semantic"]["cases_passed"], result["semantic"]["cases_total"]
        bits.append(f"Correctness tests failed ({passed}/{total}).")
    failed.discard("semantic_success")
    if failed & {"no_framework_state", "route_normal"}:
        bits.append("Entered OODALOOP on a task that should have stayed ordinary.")
        failed -= {"no_framework_state", "route_normal"}
    if "contradiction_surfaced" in failed:
        bits.append(explain_check(reading, "contradiction_surfaced"))
        failed -= {"contradiction_surfaced", "contradiction_before_protected_write"}
    scenario = reading["scenarios"].get(result["scenario_id"], {})
    if result["condition"] == "host-native" and result["scenario_id"] == "small-consequential" and "framework_entered" in failed:
        return scenario.get("host_native_trajectory") or " ".join(bits)
    for name in sorted(failed):
        bits.append(explain_check(reading, name))
    return " ".join(bits) if bits else "Matched both the hidden correctness tests and this task's behavioral probe."


def group_results(results):
    grouped = defaultdict(list)
    for result in results:
        grouped[(result["scenario_id"], result["condition"])].append(result)
    return grouped


def scoreboard_line(results):
    n = len(results)
    sem = sum(1 for item in results if item["semantic"]["passed"] and not item.get("protocol_error"))
    traj = sum(1 for item in results if item["trajectory"]["passed"] and not item.get("protocol_error"))
    proto = sum(1 for item in results if item.get("protocol_error"))
    return n, sem, traj, proto


def render(comparison, reading):
    results = comparison["results"]
    model = comparison.get("model") or {}
    suite_id = comparison.get("suite_id", "unknown")
    grouped = group_results(results)
    conditions = [item for item in CONDITION_ORDER if any(result["condition"] == item for result in results)]
    scenarios = [item for item in SCENARIO_ORDER if any(result["scenario_id"] == item for result in results)]
    lines = [
        f"# Eval suite `{suite_id}`",
        "",
        "## What this run is",
        "",
        "Isolated agents each received **one coding task** in a throwaway repo. A **cell** is one attempt: one task × one harness × one repetition. Nothing from grading, oracles, or other cells is in that repo.",
        "",
        f"Model: {model.get('display_name', model.get('id', 'unknown'))}, reasoning {model.get('reasoning_effort', 'unknown')}, Fast {'on' if model.get('fast_mode') else 'off'} (`{model.get('cursor_task_model', 'unspecified')}`). {len(results)} cells.",
        "",
        "## How to read a cell",
        "",
        "- **Code worked (semantic):** hidden tests of the library, plus one extra check for the feature this task asked for. Pass means they actually did the work without breaking miniquery.",
        "- **Behaved as probed (trajectory):** not “did they follow OODALOOP ceremony.” Each task probes one behavior (stay ordinary / enter the framework / notice a contradiction). Pass means they matched **that** probe.",
        "- These scores are independent. Working code can still fail trajectory (over-routed, or invented a product contract with no framework). Correct routing can still fail semantic (asked for init and never implemented).",
        "",
        "Harnesses:",
    ]
    for condition in conditions:
        meta = reading["conditions"][condition]
        lines.append(f"- **{meta['label']}** (`{condition}`): {meta['means']}")
    lines += ["", "## Scoreboard", "", "| Harness | Code worked | Behaved as probed | Protocol errors |", "|---|---:|---:|---:|"]
    by_condition = defaultdict(list)
    for result in results:
        by_condition[result["condition"]].append(result)
    for condition in conditions:
        n, sem, traj, proto = scoreboard_line(by_condition[condition])
        label = reading["conditions"][condition]["label"]
        lines.append(f"| {label} | {sem}/{n} | {traj}/{n} | {proto} |")
    lines += ["", "Protocol error = the cell crashed before grading (missing file, import blow-up). That is data, not a skipped row.", ""]
    for pair in PAIR_ORDER:
        named = [item for item in scenarios if reading["scenarios"][item]["pair"] == pair]
        if not named:
            continue
        lines += [f"## {reading['pairs'][pair]}", ""]
        for scenario_id in named:
            spec = reading["scenarios"][scenario_id]
            lines += [
                f"### {spec['title']} (`{scenario_id}`)",
                "",
                f"**We asked:** {spec['we_asked']}",
                "",
                f"**Good looks like:** {spec['success_means']}",
                "",
            ]
            for condition in conditions:
                cells = grouped.get((scenario_id, condition), [])
                if not cells:
                    continue
                n, sem, traj, proto = scoreboard_line(cells)
                label = reading["conditions"][condition]["label"]
                lines.append(f"**{label}:** code {sem}/{n}, behavior {traj}/{n}" + (f", {proto} crashed" if proto else "") + ".")
                misses = [item for item in cells if not item["trajectory"]["passed"] or not item["semantic"]["passed"] or item.get("protocol_error")]
                if not misses:
                    lines.append("All repetitions matched the probe.")
                else:
                    for item in misses:
                        lines.append(f"- `{item['run_id']}`: {imply(reading, item)}")
                lines.append("")
    failures = [item for item in results if not item["semantic"]["passed"] or not item["trajectory"]["passed"] or item.get("protocol_error")]
    lines += ["## Every miss, in English", ""]
    if not failures:
        lines.append("None.")
    else:
        for item in failures:
            label = reading["conditions"][item["condition"]]["label"]
            title = reading["scenarios"][item["scenario_id"]]["title"]
            lines.append(f"- **{title} / {label}** `{item['run_id']}`: {imply(reading, item)}")
    lines += [
        "",
        "## Do not conclude",
        "",
        "Do not invent a single winner score. Do not treat host-native misses on “must enter OODALOOP” tasks as a product bug. Do not treat one repetition as a stability estimate. Raw `comparison.json` is the machine record; this file is what to read and what to say to a human.",
        "",
    ]
    return "\n".join(lines)


def write_report(suite_dir):
    suite_dir = Path(suite_dir)
    comparison = json.loads((suite_dir / "comparison.json").read_text(encoding="utf-8"))
    if "suite_id" not in comparison:
        suite_path = suite_dir / "suite.json"
        if suite_path.is_file():
            comparison["suite_id"] = json.loads(suite_path.read_text(encoding="utf-8"))["suite_id"]
        else:
            comparison["suite_id"] = suite_dir.name
    text = render(comparison, load_reading())
    path = suite_dir / "REPORT.md"
    path.write_text(text, encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("suite_dir", type=Path)
    args = parser.parse_args()
    print(write_report(args.suite_dir))


if __name__ == "__main__":
    main()
