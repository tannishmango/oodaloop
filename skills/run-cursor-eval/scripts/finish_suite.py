#!/usr/bin/env python3
"""Grade every prepared cell and write a vector comparison."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from evals.oracle.scenario_cases import grade_scenario
from evals.runner.trajectory import assess_anchor, read_events


def load_candidate(path):
    spec = importlib.util.spec_from_file_location("eval_candidate", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load candidate: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def factual_events(cell_dir, workspace):
    path = cell_dir / "events.jsonl"
    events = read_events(path)
    names = {item["event"] for item in events}
    entered = (workspace / ".oodaloop").exists()
    if "route" not in names:
        events.append({"schema_version": 1, "run_id": cell_dir.name, "scenario_id": cell_dir.name.split("--", 1)[0], "sequence": len(events), "event": "route", "data": {"route": "OODALOOP" if entered else "NORMAL"}})
    if entered and "framework_state_created" not in names:
        events.append({"schema_version": 1, "run_id": cell_dir.name, "scenario_id": cell_dir.name.split("--", 1)[0], "sequence": len(events), "event": "framework_state_created", "data": {}})
    return events


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("suite_dir", type=Path)
    args = parser.parse_args()
    suite = json.loads((args.suite_dir / "suite.json").read_text(encoding="utf-8"))
    anchors = {item["id"]: item for item in json.loads((ROOT / "evals" / "scenarios" / "grading" / "anchors.json").read_text(encoding="utf-8"))}
    results = []
    for cell in suite["cells"]:
        cell_dir = args.suite_dir / cell["cell_id"]
        workspace = Path(cell["workspace"])
        try:
            semantic = grade_scenario(load_candidate(workspace / "candidate" / "miniquery.py").execute, cell["scenario_id"])
            protocol_error = None
        except Exception as error:
            semantic = {"passed": False, "cases_passed": 0, "cases_total": 0, "cases": []}
            protocol_error = f"{type(error).__name__}: {error}"
        trajectory = assess_anchor(anchors[cell["scenario_id"]], factual_events(cell_dir, workspace), semantic["passed"])
        result = {"schema_version": 1, "run_id": cell["cell_id"], "condition": cell["condition"], "scenario_id": cell["scenario_id"], "semantic": semantic, "trajectory": trajectory, "protocol_error": protocol_error}
        (cell_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        results.append(result)
    output = {"schema_version": 1, "suite_id": suite["suite_id"], "model": suite["model"], "results": results}
    path = args.suite_dir / "comparison.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
