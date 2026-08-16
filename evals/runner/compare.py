"""Compare result vectors without collapsing them to an invented scalar score."""
from __future__ import annotations

import argparse, json


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("results", nargs="+")
    args = parser.parse_args(argv)
    records = [json.load(open(path, encoding="utf-8")) for path in args.results]
    fields = ("condition", "scenario_id", "semantic")
    print(json.dumps([{field: record.get(field) for field in fields} | {"trajectory": record.get("trajectory")} for record in records], indent=2, sort_keys=True))


if __name__ == "__main__": main()

