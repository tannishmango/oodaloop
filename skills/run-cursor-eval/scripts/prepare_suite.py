#!/usr/bin/env python3
"""Materialize the configured Cursor evaluation matrix without grading leakage."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def export_harness(ref, destination):
    archive = destination.parent / "harness.tar"
    with archive.open("wb") as stream:
        subprocess.run(["git", "archive", ref, "commands", "skills", "rules", "agents", "foundation", "templates"], cwd=ROOT, stdout=stream, check=True)
    destination.mkdir()
    with tarfile.open(archive) as bundle:
        bundle.extractall(destination)
    archive.unlink()


def init_workspace(path):
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "-c", "user.name=OODALOOP Eval", "-c", "user.email=eval@invalid", "commit", "-q", "-m", "seed fixture"], cwd=path, check=True)


def resolve_ref(ref):
    if ref is None:
        return None
    return subprocess.run(
        ["git", "rev-parse", f"{ref}^{{commit}}"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()


def iter_matrix(scenarios, conditions, repetitions):
    reps = int(repetitions)
    if reps < 1:
        raise SystemExit("repetitions must be >= 1")
    for scenario in scenarios:
        for condition in conditions:
            for rep in range(1, reps + 1):
                yield scenario, condition, rep


def durable_suite_dir(suite_id, output_dir=None):
    base = Path(output_dir) if output_dir is not None else ROOT / "evals" / "runs"
    candidate = base / suite_id
    if not candidate.exists():
        candidate.mkdir(parents=True)
        return candidate
    suffix = 2
    while True:
        candidate = base / f"{suite_id}-{suffix}"
        if not candidate.exists():
            candidate.mkdir(parents=True)
            return candidate
        suffix += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()
    config = json.loads((ROOT / "evals" / "config.json").read_text(encoding="utf-8"))
    public_dir = ROOT / "evals" / "scenarios" / "public"
    scenarios = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(public_dir.glob("*.json"))]
    if config["scenarios"] != "all":
        allowed = set(config["scenarios"])
        scenarios = [item for item in scenarios if item["id"] in allowed]
    suite_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suite_dir = durable_suite_dir(suite_id, args.output_dir)
    cells = []
    for scenario, condition, rep in iter_matrix(scenarios, config["conditions"], config["repetitions"]):
        cell_id = f"{scenario['id']}--{condition['id']}--{rep}"
        cell_dir = suite_dir / cell_id
        cell_dir.mkdir(parents=True, exist_ok=True)
        workspace_parent = Path(tempfile.mkdtemp(prefix=f"oodaloop-eval-{cell_id}-"))
        workspace = workspace_parent / "workspace"
        workspace.mkdir()
        shutil.copytree(ROOT / "evals" / "seed_project", workspace / "candidate", ignore=shutil.ignore_patterns("__pycache__"))
        overlay = ROOT / "evals" / "fixtures" / scenario["fixture"]
        if overlay.is_dir():
            shutil.copytree(overlay, workspace, dirs_exist_ok=True)
        elif scenario["fixture"] != "canonical":
            raise SystemExit(f"missing fixture overlay: {scenario['fixture']}")
        instructions = ["Complete the following task in this repository.", "", scenario["task"]]
        if condition["ref"] is not None:
            export_harness(condition["ref"], workspace / ".harness")
            instructions += ["", "OODALOOP is the active harness for this condition.", "Start at `.harness/commands/oodaloop-start.md` and follow the referenced harness skills exactly."]
        (workspace / "AGENT_TASK.md").write_text("\n".join(instructions) + "\n", encoding="utf-8")
        init_workspace(workspace)
        (cell_dir / "events.jsonl").touch()
        cell = {"cell_id": cell_id, "scenario_id": scenario["id"], "condition": condition["id"], "condition_ref": condition["ref"], "condition_sha": resolve_ref(condition["ref"]), "workspace": str(workspace), "repetition": rep}
        (cell_dir / "cell.json").write_text(json.dumps(cell, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        cells.append(cell)
    suite = {"schema_version": 1, "suite_id": suite_id, "model": config["model"], "repetitions": config["repetitions"], "parallelism": config["parallelism"], "cells": cells}
    (suite_dir / "suite.json").write_text(json.dumps(suite, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(suite_dir)


if __name__ == "__main__":
    main()
