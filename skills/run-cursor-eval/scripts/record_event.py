#!/usr/bin/env python3
"""Append one factual event to a prepared cell."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def value(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cell_dir", type=Path)
    parser.add_argument("event")
    parser.add_argument("data", nargs="*")
    args = parser.parse_args()
    path = args.cell_dir / "events.jsonl"
    existing = path.read_text(encoding="utf-8").splitlines()
    cell = json.loads((args.cell_dir / "cell.json").read_text(encoding="utf-8"))
    payload = {}
    for item in args.data:
        if "=" not in item:
            raise SystemExit(f"expected key=value: {item}")
        key, raw = item.split("=", 1)
        payload[key] = value(raw)
    record = {"schema_version": 1, "run_id": cell["cell_id"], "scenario_id": cell["scenario_id"], "sequence": len(existing), "event": args.event, "data": payload}
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
