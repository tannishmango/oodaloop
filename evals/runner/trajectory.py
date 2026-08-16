"""Reduce factual events to a comparison vector and check only anchor invariants."""
from __future__ import annotations

import json
from collections import Counter


def read_events(path):
    with open(path, encoding="utf-8") as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    if [item["sequence"] for item in events] != list(range(len(events))):
        raise ValueError("event sequence must be contiguous")
    return events


def vector(events):
    counts = Counter(item["event"] for item in events)
    route = next((item.get("data", {}).get("route") for item in events if item["event"] == "route"), None)
    metrics = {}
    for item in events:
        if item["event"] == "metric": metrics.update(item.get("data", {}))
    return {"route": route, "framework_entered": bool(counts["framework_state_created"]), "leaf_count": counts["leaf_started"], "post_plan_split_count": counts["post_plan_split"], "surprise_count": counts["surprise"], "reentry_count": counts["reentry"], "reviewer_calls": counts["reviewer_call"], "child_nodes": counts["child_created"], "user_questions": counts["user_question"], "proof_attempts": counts["proof_attempt"], "tool_calls": counts["tool_call"], **metrics}


def assess_anchor(anchor, events, semantic_passed):
    facts = vector(events)
    kind = anchor["anchor"]
    checks = {"semantic_success": bool(semantic_passed)}
    if kind == "normal":
        checks.update({"route_normal": facts["route"] in (None, "NORMAL"), "no_framework_state": not facts["framework_entered"], "no_reviewer_call": facts["reviewer_calls"] == 0})
    elif kind == "oodaloop":
        checks["framework_entered"] = facts["route"] == "OODALOOP" or facts["framework_entered"]
    elif kind == "leaf_ready":
        checks.update({"fresh_executor_semantic_success": bool(semantic_passed), "no_user_correction": facts["user_questions"] == 0})
    elif kind == "no_silent_drift":
        surfaced = [item["sequence"] for item in events if item["event"] in ("surprise", "reentry")]
        protected = set(anchor.get("protected_paths", []))
        writes = [item["sequence"] for item in events if item["event"] == "tool_call" and item.get("data", {}).get("operation") == "write" and item.get("data", {}).get("path") in protected]
        checks["contradiction_before_protected_write"] = not writes or bool(surfaced and min(surfaced) < min(writes))
    return {"passed": all(checks.values()), "checks": checks, "facts": facts}

