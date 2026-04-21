# Task: valid-fixture

## Phase: act
Started: 2026-04-21
Updated: 2026-04-21

## Objective
A fully valid task file exercising every section type used by the validator.

## Observations
### O1: Fixture
This file is a validator test harness fixture. It is not a real OODALOOP task.

## Requirements
### R1: Coverage
Covers: valid Mode, complete Paused section, correct phase↔section pairing (act → Plan present), no Parent reference (depth 0).

## Scope
- **In**: validator pass
- **Out**: nothing
- **Deferred**: nothing

## Assessment
### Situational interpretation
Fixture only.
### Viable approaches
N/A
### Risks and assumptions
None.
### Constraints
None.
### Recommendation
N/A

## Plan
### T1: Example task
**Depends on**: none
**Acceptance**: example
**Proof Plan**: manual

## Paused
Reason: Example blocking discovery that cannot be deferred.
Blocked-during: T1: Example task
Completed-before-pause: none
Child-objective: Resolve the example blocker before resuming T1.
Child-slug: valid-child
Strategy: in-chat
Paused-at: 2026-04-21
Resume-instructions: After child completes, resume T1 from the top.

Mode: direct
