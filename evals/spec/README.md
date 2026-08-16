# Tiny relational substrate

Candidates expose `execute(query, tables)`. `tables` maps table names to lists of
JSON objects. A query is JSON and is evaluated in this order:

1. `from` selects a table and optionally names its alias.
2. `join` performs an `inner` or `left` equality join.
3. `where` retains rows for which an expression is exactly `true`.
4. `group_by` and `aggregate` produce grouped rows. Without `group_by`, an
   aggregate produces one row, including for empty input.
5. `select` produces output objects.
6. `order_by` sorts output rows, with null after non-null in ascending order.
7. `limit` retains the first non-negative number of rows.

Field expressions are `{"field":"alias.name"}`. Literals are
`{"literal": value}`. Supported operations are `eq`, `lt`, `gt`, `and`, `or`,
`not`, `add`, and `coalesce`. Comparisons involving null are false. Arithmetic
involving null produces null. Aggregates are `count` (all rows or non-null
expression values) and `sum` (non-null values; zero when none).

Unknown tables, fields, operators, aggregate kinds, negative limits, malformed
queries, and non-numeric addition/sum raise `QueryError`.

The contract is deliberately compact and implementation-independent. The
reference oracle and canonical implementation are separate code paths.

