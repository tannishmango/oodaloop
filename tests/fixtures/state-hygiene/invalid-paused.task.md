# Task: invalid-paused-fixture

## Phase: act
Started: 2026-04-21
Updated: 2026-04-21

## Objective
Fixture with an incomplete Paused section (missing Strategy field). Validator must reject with paused-completeness error.

## Plan
### T1: Example task
**Depends on**: none
**Acceptance**: example
**Proof Plan**: manual

## Paused
Reason: Example blocking discovery.
Blocked-during: T1: Example task
Completed-before-pause: none
Child-objective: Resolve the blocker.
Child-slug: invalid-paused-child
Paused-at: 2026-04-21
Resume-instructions: Resume T1 after child completes.

Mode: direct
