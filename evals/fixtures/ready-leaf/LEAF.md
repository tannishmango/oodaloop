# Add `is_null` expression

Intent: support `{"is_null": expression}` and return true only when the evaluated
operand is null.

Invariants: preserve every existing operator and error behavior. Do not change the
query shape or add dependencies.

Allowed scope: `candidate/miniquery.py` plus focused tests.

Proof: run the existing deterministic tests and add visible cases for null and
non-null fields. The implementation must remain stdlib-only.
