"""Fixed and fixed-seed cases. Expected values are computed only by the oracle."""
from __future__ import annotations

import random


TABLES = {
    "people": [{"id": 1, "team": "a", "score": 7}, {"id": 2, "team": "b", "score": None}, {"id": 3, "team": "a", "score": 4}],
    "teams": [{"id": "a", "label": "Alpha"}, {"id": "c", "label": "Gamma"}],
}


def fixed_cases():
    f = lambda name: {"field": name}
    lit = lambda value: {"literal": value}
    return [
        {"name": "filter-project-order-limit", "tables": TABLES, "query": {"from": {"table": "people", "as": "p"}, "where": {"gt": [f("p.score"), lit(3)]}, "select": {"id": f("p.id"), "next": {"add": [f("p.score"), lit(1)]}}, "order_by": [{"field": "next", "direction": "desc"}], "limit": 1}},
        {"name": "group-and-null", "tables": TABLES, "query": {"from": {"table": "people", "as": "p"}, "group_by": [f("p.team")], "aggregate": {"rows": {"op": "count"}, "known": {"op": "count", "expr": f("p.score")}, "total": {"op": "sum", "expr": f("p.score")}}, "select": {"team": f("group0"), "rows": f("rows"), "known": f("known"), "total": f("total")}, "order_by": [{"field": "team"}]}},
        {"name": "left-join", "tables": TABLES, "query": {"from": {"table": "people", "as": "p"}, "join": {"type": "left", "table": "teams", "as": "t", "on": [f("p.team"), f("t.id")]}, "select": {"id": f("p.id"), "label": f("t.label")}, "order_by": [{"field": "id"}]}},
        {"name": "empty-aggregate", "tables": {"people": []}, "query": {"from": {"table": "people", "as": "p"}, "aggregate": {"rows": {"op": "count"}, "total": {"op": "sum", "expr": f("p.score")}}}},
        {"name": "invalid-limit", "tables": TABLES, "query": {"from": {"table": "people"}, "limit": -1}, "error": True},
        {"name": "unknown-field", "tables": TABLES, "query": {"from": {"table": "people", "as": "p"}, "select": {"x": f("p.missing")}}, "error": True},
    ]


def generated_cases(seed=20260816, count=24):
    randomizer = random.Random(seed)
    cases = []
    for index in range(count):
        rows = [{"id": n, "value": randomizer.choice([None, randomizer.randint(-9, 20)])} for n in range(randomizer.randint(0, 12))]
        threshold = randomizer.randint(-5, 15)
        cases.append({"name": f"generated-{index:02d}", "tables": {"items": rows}, "query": {"from": {"table": "items", "as": "i"}, "where": {"gt": [{"field": "i.value"}, {"literal": threshold}]}, "select": {"id": {"field": "i.id"}, "value": {"field": "i.value"}}, "order_by": [{"field": "value"}, {"field": "id", "direction": "desc"}], "limit": randomizer.randint(0, 8)}})
    return cases


def all_cases():
    return fixed_cases() + generated_cases()

