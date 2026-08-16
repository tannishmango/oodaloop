"""Canonical passing implementation. It intentionally does not import the oracle."""
from __future__ import annotations

from functools import cmp_to_key


class QueryError(ValueError):
    pass


def _value(term, row):
    if not isinstance(term, dict) or len(term) != 1:
        raise QueryError("bad expression")
    op, arg = next(iter(term.items()))
    if op == "literal": return arg
    if op == "field":
        if arg not in row: raise QueryError(f"unknown field: {arg}")
        return row[arg]
    if op == "not": return not bool(_value(arg, row))
    if op == "coalesce":
        return next((v for v in (_value(x, row) for x in arg) if v is not None), None)
    if op not in ("eq", "lt", "gt", "and", "or", "add") or not isinstance(arg, list) or len(arg) != 2:
        raise QueryError(f"bad operator: {op}")
    a, b = _value(arg[0], row), _value(arg[1], row)
    if op == "and": return bool(a) and bool(b)
    if op == "or": return bool(a) or bool(b)
    if op in ("eq", "lt", "gt") and (a is None or b is None): return False
    if op == "eq": return a == b
    if op == "lt": return a < b
    if op == "gt": return a > b
    if a is None or b is None: return None
    if any(not isinstance(x, (int, float)) or isinstance(x, bool) for x in (a, b)): raise QueryError("add requires numbers")
    return a + b


def execute(query, tables):
    if not isinstance(query, dict) or not isinstance(tables, dict): raise QueryError("bad input")
    if set(query) - {"from", "join", "where", "group_by", "aggregate", "select", "order_by", "limit"}: raise QueryError("unknown query member")
    source = query.get("from")
    if not isinstance(source, dict) or "table" not in source or set(source) - {"table", "as"}: raise QueryError("bad from")
    table = source["table"]
    if table not in tables: raise QueryError("unknown table")
    alias = source.get("as", table)
    rows = [{f"{alias}.{k}": v for k, v in item.items()} for item in tables[table]]
    if "join" in query:
        join = query["join"]
        if not isinstance(join, dict) or join.get("type", "inner") not in ("inner", "left") or join.get("table") not in tables or not isinstance(join.get("on"), list) or len(join["on"]) != 2: raise QueryError("bad join")
        ja = join.get("as", join["table"])
        rights = [{f"{ja}.{k}": v for k, v in item.items()} for item in tables[join["table"]]]
        fields = {k for r in rights for k in r}
        joined = []
        for left in rows:
            found = []
            for right in rights:
                both = dict(left, **right)
                a, b = (_value(x, both) for x in join["on"])
                if a is not None and b is not None and a == b: found.append(both)
            joined += found or ([dict(left, **{k: None for k in fields})] if join.get("type", "inner") == "left" else [])
        rows = joined
    if "where" in query: rows = [r for r in rows if _value(query["where"], r) is True]
    if "aggregate" in query:
        definitions = query["aggregate"]
        if not isinstance(definitions, dict): raise QueryError("bad aggregate")
        groups = {}
        keys = query.get("group_by", [])
        for row in rows: groups.setdefault(tuple(_value(x, row) for x in keys), []).append(row)
        if not keys and not groups: groups[()] = []
        reduced = []
        for key, members in groups.items():
            out = {f"group{i}": v for i, v in enumerate(key)}
            for name, definition in definitions.items():
                if not isinstance(definition, dict) or definition.get("op") not in ("count", "sum"): raise QueryError("bad aggregate")
                values = members if "expr" not in definition else [_value(definition["expr"], r) for r in members]
                if definition["op"] == "count": out[name] = len(values) if "expr" not in definition else len([v for v in values if v is not None])
                else:
                    values = [v for v in values if v is not None]
                    if any(not isinstance(v, (int, float)) or isinstance(v, bool) for v in values): raise QueryError("sum requires numbers")
                    out[name] = sum(values)
            reduced.append(out)
        rows = reduced
    if "select" in query:
        if not isinstance(query["select"], dict): raise QueryError("bad select")
        rows = [{name: _value(term, row) for name, term in query["select"].items()} for row in rows]
    if query.get("order_by"):
        def compare(a, b):
            for rule in query["order_by"]:
                field, direction = rule.get("field"), rule.get("direction", "asc")
                if field not in a or field not in b or direction not in ("asc", "desc"): raise QueryError("bad order")
                av, bv = a[field], b[field]
                n = 0 if av == bv else (1 if av is None else -1 if bv is None else (-1 if av < bv else 1))
                if n: return n if direction == "asc" else -n
            return 0
        rows = sorted(rows, key=cmp_to_key(compare))
    if "limit" in query:
        limit = query["limit"]
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0: raise QueryError("bad limit")
        rows = rows[:limit]
    return rows

