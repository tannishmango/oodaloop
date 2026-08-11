# State-hygiene validator fixtures

The pre-commit hook validates only cheap, factual restartability contracts.

## Current commit-time coverage

`valid.task.md` exercises:
- valid phase vocabulary (`observe|orient|decide|act|loop`),
- phase → minimum-evidence pairing,
- compact `## Waiting` field presence,
- parent-chain cycle detection when parent fixtures are present.

The hook intentionally does **not** validate:
- plan quality,
- surprise significance,
- REFINE vs RESCOPE,
- model/labor strategy,
- recursion depth,
- semantic review quality.

Those are agent judgments or obsolete process concepts, not factual schema contracts.

## Legacy fixtures

Files named around `mode`, `paused`, or `depth-consent` were created for the previous process model. They are retained temporarily as historical/manual artifacts while the fixture directory is pruned; they are not part of the current commit-time contract.

Do not add new validators to preserve those concepts.

## Harness

```bash
# From repo root

git add tests/fixtures/state-hygiene/valid.task.md
.githooks/pre-commit  # should pass

git restore --staged tests/fixtures/state-hygiene/
```

Future malformed fixtures should test only durable factual invariants (for example invalid phase/evidence pairing, incomplete Waiting records, or parent cycles).
