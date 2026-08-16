"""Independent executable oracle for the tiny relational specification."""
from __future__ import annotations

from functools import cmp_to_key


class QueryError(ValueError):
    pass


def _field(row, name):
    if name not in row:
        raise QueryError(f"unknown field: {name}")
    return row[name]


def _expr(node, row):
    if not isinstance(node, dict) or len(node) != 1:
        raise QueryError("malformed expression")
    kind, value = next(iter(node.items()))
    if kind == "literal":
        return value
    if kind == "field":
        return _field(row, value)
    if kind == "not":
        return not bool(_expr(value, row))
    if kind == "coalesce":
        for item in value:
            result = _expr(item, row)
            if result is not None:
                return result
        return None
    if kind not in {"eq", "lt", "gt", "and", "or", "add"} or not isinstance(value, list) or len(value) != 2:
        raise QueryError(f"unknown or malformed operator: {kind}")
    left, right = (_expr(item, row) for item in value)
    if kind == "and":
        return bool(left) and bool(right)
    if kind == "or":
        return bool(left) or bool(right)
    if kind in {"eq", "lt", "gt"} and (left is None or right is None):
        return False
    if kind == "eq":
        return left == right
    if kind == "lt":
        return left < right
    if kind == "gt":
        return left > right
    if left is None or right is None:
        return None
    if not isinstance(left, (int, float)) or isinstance(left, bool) or not isinstance(right, (int, float)) or isinstance(right, bool):
        raise QueryError("add requires numbers")
    return left + right


def _source(query, tables):
    source = query.get("from")
    if not isinstance(source, dict) or set(source) - {"table", "as"} or "table" not in source:
        raise QueryError("malformed from")
    name, alias = source["table"], source.get("as", source["table"])
    if name not in tables:
        raise QueryError(f"unknown table: {name}")
    return [{f"{alias}.{key}": value for key, value in item.items()} for item in tables[name]]


def _join(rows, join, tables):
    if not isinstance(join, dict) or join.get("type", "inner") not in {"inner", "left"}:
        raise QueryError("malformed join")
    name, alias = join.get("table"), join.get("as", join.get("table"))
    if name not in tables or not isinstance(join.get("on"), list) or len(join["on"]) != 2:
        raise QueryError("malformed join")
    right_rows = [{f"{alias}.{key}": value for key, value in item.items()} for item in tables[name]]
    right_fields = {key for row in right_rows for key in row}
    output = []
    for left in rows:
        matches = []
        for right in right_rows:
            merged = {**left, **right}
            a, b = (_expr(item, merged) for item in join["on"])
            if a is not None and b is not None and a == b:
                matches.append(merged)
        output.extend(matches or ([{**left, **{key: None for key in right_fields}}] if join.get("type", "inner") == "left" else []))
    return output


def _aggregate(rows, query):
    group_nodes = query.get("group_by", [])
    aggregate = query.get("aggregate")
    if aggregate is None:
        return rows
    if not isinstance(aggregate, dict):
        raise QueryError("malformed aggregate")
    groups = {}
    for row in rows:
        key = tuple(_expr(node, row) for node in group_nodes)
        groups.setdefault(key, []).append(row)
    if not group_nodes and not groups:
        groups[()] = []
    output = []
    for key, members in groups.items():
        item = {f"group{index}": value for index, value in enumerate(key)}
        for name, definition in aggregate.items():
            if not isinstance(definition, dict) or definition.get("op") not in {"count", "sum"}:
                raise QueryError("unknown aggregate")
            values = members if "expr" not in definition else [_expr(definition["expr"], row) for row in members]
            if definition["op"] == "count":
                item[name] = len(values) if "expr" not in definition else sum(value is not None for value in values)
            else:
                numbers = [value for value in values if value is not None]
                if any(not isinstance(value, (int, float)) or isinstance(value, bool) for value in numbers):
                    raise QueryError("sum requires numbers")
                item[name] = sum(numbers)
        output.append(item)
    return output


def execute(query, tables):
    if not isinstance(query, dict) or not isinstance(tables, dict):
        raise QueryError("query and tables must be objects")
    allowed = {"from", "join", "where", "group_by", "aggregate", "select", "order_by", "limit"}
    if set(query) - allowed:
        raise QueryError("unknown query member")
    rows = _source(query, tables)
    if "join" in query:
        rows = _join(rows, query["join"], tables)
    if "where" in query:
        rows = [row for row in rows if _expr(query["where"], row) is True]
    rows = _aggregate(rows, query)
    if "select" in query:
        if not isinstance(query["select"], dict):
            raise QueryError("malformed select")
        rows = [{name: _expr(node, row) for name, node in query["select"].items()} for row in rows]
    order = query.get("order_by", [])
    if order:
        def compare(a, b):
            for item in order:
                name, direction = item.get("field"), item.get("direction", "asc")
                if name not in a or name not in b or direction not in {"asc", "desc"}:
                    raise QueryError("malformed order_by")
                av, bv = a[name], b[name]
                result = 0 if av == bv else (1 if av is None else -1 if bv is None else (-1 if av < bv else 1))
                if result:
                    return result if direction == "asc" else -result
            return 0
        rows = sorted(rows, key=cmp_to_key(compare))
    if "limit" in query:
        if not isinstance(query["limit"], int) or isinstance(query["limit"], bool) or query["limit"] < 0:
            raise QueryError("limit must be a non-negative integer")
        rows = rows[:query["limit"]]
    return rows

