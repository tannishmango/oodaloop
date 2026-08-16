"""Append-only, observational JSONL trajectory events."""
from __future__ import annotations

import json


class EventWriter:
    def __init__(self, path, run_id, scenario_id):
        self.path, self.run_id, self.scenario_id, self.sequence = path, run_id, scenario_id, 0

    def append(self, event, **data):
        record = {"schema_version": 1, "run_id": self.run_id, "scenario_id": self.scenario_id, "sequence": self.sequence, "event": event, "data": data}
        with open(self.path, "a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
        self.sequence += 1
        return record

