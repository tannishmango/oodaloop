from __future__ import annotations

import ast
import json
import tempfile
import unittest
from pathlib import Path

from evals.oracle.cases import all_cases, generated_cases
from evals.oracle.scenario_cases import grade_scenario
from evals.runner.run import grade
from evals.runner.telemetry import EventWriter
from evals.runner.trajectory import assess_anchor, read_events, vector
from evals.seed_project import miniquery


ROOT = Path(__file__).parents[1]
REPO_ROOT = ROOT.parent


class FoundationTests(unittest.TestCase):
    def test_canonical_passes_fixed_and_generated_oracle(self):
        result = grade(miniquery.execute)
        self.assertTrue(result["passed"])
        self.assertEqual(result["cases_total"], 30)

    def test_generation_is_deterministic(self):
        self.assertEqual(generated_cases(), generated_cases())
        self.assertEqual([case["name"] for case in all_cases()][-1], "generated-23")

    def test_oracle_rejects_behavioral_mutant(self):
        result = grade(lambda query, tables: [])
        self.assertFalse(result["passed"])
        self.assertLess(result["cases_passed"], result["cases_total"])

    def test_scenario_extensions_are_hidden_and_executable(self):
        result = grade_scenario(miniquery.execute, "ready-leaf")
        self.assertFalse(result["passed"])
        self.assertEqual(result["cases_total"], 31)
        self.assertEqual(result["cases"][-1]["name"], "scenario-is-null-expression")

    def test_oracle_is_not_self_referential(self):
        tree = ast.parse((ROOT / "seed_project" / "miniquery.py").read_text())
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        self.assertFalse(any("oracle" in ast.unparse(node) for node in imports))

    def test_six_public_scenarios_have_separate_grading(self):
        public = [json.loads(path.read_text()) for path in sorted((ROOT / "scenarios" / "public").glob("*.json"))]
        grading = json.loads((ROOT / "scenarios" / "grading" / "anchors.json").read_text())
        self.assertEqual(len(public), 6)
        self.assertEqual({item["id"] for item in public}, {item["id"] for item in grading})
        self.assertTrue(all("anchor" not in item and "invariants" not in item for item in public))

    def test_cursor_default_matrix_and_model_are_pinned(self):
        config = json.loads((ROOT / "config.json").read_text())
        self.assertEqual(config["scenarios"], "all")
        self.assertEqual([item["id"] for item in config["conditions"]], ["host-native", "main", "pr1"])
        self.assertEqual(config["model"]["id"], "grok-4.6")
        self.assertEqual(config["model"]["reasoning_effort"], "high")
        self.assertFalse(config["model"]["fast_mode"])
        self.assertFalse(config["model"]["allow_auto"])
        self.assertTrue((REPO_ROOT / "commands" / "oodaloop-eval.md").is_file())
        self.assertTrue((REPO_ROOT / "skills" / "run-cursor-eval" / "SKILL.md").is_file())

    def test_telemetry_is_append_only_and_sequenced(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            writer = EventWriter(path, "run", "scenario")
            writer.append("route", route="NORMAL")
            writer.append("proof_attempt", passed=True)
            records = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual([item["sequence"] for item in records], [0, 1])
            self.assertEqual(records[0]["data"], {"route": "NORMAL"})
            self.assertEqual(vector(read_events(path))["proof_attempts"], 1)

    def test_surprise_anchor_rejects_silent_protected_write(self):
        anchor = {"anchor": "no_silent_drift", "protected_paths": ["core.py"]}
        silent = [{"sequence": 0, "event": "tool_call", "data": {"operation": "write", "path": "core.py"}}]
        surfaced = [{"sequence": 0, "event": "surprise", "data": {}}, {"sequence": 1, "event": "tool_call", "data": {"operation": "write", "path": "core.py"}}]
        self.assertFalse(assess_anchor(anchor, [], True)["passed"])
        self.assertFalse(assess_anchor(anchor, silent, True)["passed"])
        self.assertTrue(assess_anchor(anchor, surfaced, True)["passed"])


if __name__ == "__main__": unittest.main()
