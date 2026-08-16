from __future__ import annotations

import ast
import importlib.util
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
        self.assertEqual(config["model"]["cursor_task_model"], "cursor-grok-4.6-high")
        skill = (REPO_ROOT / "skills" / "run-cursor-eval" / "SKILL.md").read_text()
        self.assertIn("cursor-grok-4.6-high", skill)
        self.assertIn("not `cursor-grok-4.6-xhigh`", skill)
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

    def test_start_skill_routes_before_initialization(self):
        skill = (REPO_ROOT / "skills" / "start" / "SKILL.md").read_text()
        self.assertIn("Route before touching OODALOOP state", skill)
        self.assertIn("If either answer is yes, choose **NORMAL**.", skill)
        self.assertIn("do not recommend `/oodaloop-quick` as a substitute framework path", skill)
        self.assertIn("Only after choosing OODALOOP", skill)
        self.assertNotIn("Cannot start OODALOOP flow without initialization.", skill)
        self.assertNotIn("### 1. Ensure state exists", skill)

    def test_surprise_anchor_rejects_silent_protected_write(self):
        anchor = {"anchor": "no_silent_drift", "protected_paths": ["core.py"]}
        silent = [{"sequence": 0, "event": "tool_call", "data": {"operation": "write", "path": "core.py"}}]
        surfaced = [{"sequence": 0, "event": "surprise", "data": {}}, {"sequence": 1, "event": "tool_call", "data": {"operation": "write", "path": "core.py"}}]
        self.assertFalse(assess_anchor(anchor, [], True)["passed"])
        self.assertFalse(assess_anchor(anchor, silent, True)["passed"])
        self.assertTrue(assess_anchor(anchor, surfaced, True)["passed"])

    def test_prepare_suite_multiplies_cells_by_repetitions(self):
        path = REPO_ROOT / "skills" / "run-cursor-eval" / "scripts" / "prepare_suite.py"
        spec = importlib.util.spec_from_file_location("prepare_suite", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        scenarios = [{"id": "alpha"}, {"id": "beta"}]
        conditions = [{"id": "host"}, {"id": "main"}]
        once = [f"{scenario['id']}--{condition['id']}--{rep}" for scenario, condition, rep in module.iter_matrix(scenarios, conditions, 1)]
        self.assertEqual(len(once), 4)
        self.assertEqual(len(set(once)), 4)
        self.assertTrue(all(item.endswith("--1") for item in once))
        thrice = [f"{scenario['id']}--{condition['id']}--{rep}" for scenario, condition, rep in module.iter_matrix(scenarios, conditions, 3)]
        self.assertEqual(len(thrice), 12)
        self.assertEqual(len(set(thrice)), 12)
        for scenario in scenarios:
            for condition in conditions:
                copies = [item for item in thrice if item.startswith(f"{scenario['id']}--{condition['id']}--")]
                self.assertEqual(copies, [f"{scenario['id']}--{condition['id']}--{rep}" for rep in (1, 2, 3)])
        source = path.read_text(encoding="utf-8")
        self.assertIn('iter_matrix(scenarios, config["conditions"], config["repetitions"])', source)
        with self.assertRaises(SystemExit):
            list(module.iter_matrix(scenarios, conditions, 0))
        with self.assertRaises(SystemExit):
            list(module.iter_matrix(scenarios, conditions, -2))

    def test_eval_run_outputs_are_durable_and_agent_readable(self):
        gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        cursorignore = (REPO_ROOT / ".cursorignore").read_text(encoding="utf-8")
        self.assertIn("evals/runs/*", gitignore)
        self.assertIn("!evals/runs/README.md", gitignore)
        self.assertNotIn("evals/runs", cursorignore)
        self.assertTrue((REPO_ROOT / "evals" / "runs" / "README.md").is_file())
        prepare = (REPO_ROOT / "skills" / "run-cursor-eval" / "scripts" / "prepare_suite.py").read_text(encoding="utf-8")
        self.assertIn('ROOT / "evals" / "runs"', prepare)
        self.assertIn("suite_dir = durable_suite_dir(suite_id, args.output_dir)", prepare)
        self.assertNotIn("oodaloop-eval-{suite_id}-", prepare)
        self.assertNotIn(".archive", prepare)
        skill = (REPO_ROOT / "skills" / "run-cursor-eval" / "SKILL.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "evals" / "README.md").read_text(encoding="utf-8")
        self.assertIn("evals/runs/", skill)
        self.assertIn("evals/runs/", readme)
        self.assertIn("Never copy suites to `.archive/`", skill)
        self.assertIn("## Re-run policy", skill)
        self.assertIn("Do not re-run the full matrix", skill)
        self.assertIn("could this change alter routing, init", skill)
        self.assertNotIn("Archive under `.archive/", skill)
        self.assertNotIn("Archive under `.archive/", readme)

    def test_durable_suite_dir_uses_output_dir_and_keeps_workspaces_in_tempfile(self):
        path = REPO_ROOT / "skills" / "run-cursor-eval" / "scripts" / "prepare_suite.py"
        spec = importlib.util.spec_from_file_location("prepare_suite", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            first = module.durable_suite_dir("suite", parent)
            self.assertEqual(first, parent / "suite")
            self.assertTrue(first.is_dir())
            second = module.durable_suite_dir("suite", parent)
            self.assertEqual(second, parent / "suite-2")
            self.assertTrue(second.is_dir())
        source = path.read_text(encoding="utf-8")
        self.assertIn("workspace_parent = Path(tempfile.mkdtemp", source)
        self.assertIn("suite_dir = durable_suite_dir", source)


if __name__ == "__main__": unittest.main()
