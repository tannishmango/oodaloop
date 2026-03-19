# Code Design Principles

Concrete design criteria for evaluating implementation quality. Used by the assess checkpoint in the decide phase. Every principle here should be assessable against actual code -- if you can't point at a file and say whether it's violated, the principle is too abstract.

## Contents

- [Structural Limits](#structural-limits) - File length, function length, nesting depth, parameter count thresholds with review/refactor triggers
- [Composition](#composition) - Single responsibility, narrow interfaces, grow by addition not inflation
- [Coupling and Cohesion](#coupling-and-cohesion) - Dependency direction, hidden coupling detection, cohesion test, feature envy
- [Data Over Branching](#data-over-branching) - Replace if/elif chains with lookup tables, registries, data-driven dispatch
- [Naming](#naming) - Intent over implementation, scope-scaled length, naming difficulty as design signal
- [Error Handling](#error-handling) - Handle at the right level, fail fast on programmer errors, graceful on environmental
- [DRY Without Brittleness](#dry-without-brittleness) - Rule of Three, premature abstraction as coupling, extraction must simplify both sites
- [Scalability Patterns](#scalability-patterns) - Extension points, registries, grow by composition not module inflation
- [Red Flags](#red-flags) - 9 concrete anti-patterns: God objects, shotgun surgery, copy-paste variants, circular deps, etc.
- [Assessment Stance](#assessment-stance) - Not style enforcement; the question is "easier or harder to change next time?"

---

## Structural Limits

| Signal | Threshold | What it means |
|--------|-----------|---------------|
| File length | >500 lines: review | >750 lines: likely doing too much | The file has accumulated multiple responsibilities or is missing extraction opportunities. |
| Function/method length | >40 lines: review | >80 lines: split | Long functions conflate steps that should be composed. |
| Nesting depth | >3 levels: review | >5 levels: refactor | Deep nesting hides control flow. Extract, invert conditions, or use early returns. |
| Parameter count | >4 parameters: review | >6: introduce structure | Many parameters signal a missing object, config, or context. |
| Class/module public surface | >10 public methods: review | Too many entry points means the abstraction boundary is wrong. |

These are heuristics, not laws. A 600-line file that's a well-structured data model may be fine. A 200-line file with 6 levels of nesting is not. Context overrides thresholds. But the assessor must flag the threshold and state why context justifies the exception.

---

## Composition

**Do one thing well; compose cleanly.** System capability grows from composition of focused components, not from expanding existing ones.

- Each function, class, or module has a single reason to change. If describing what it does requires "and," it has two jobs.
- Interfaces between components should be narrow and explicit. A function's signature should tell you what it needs and what it produces.
- When a change requires touching many files, either the change is cross-cutting (acceptable) or the abstraction boundaries are wrong (refactor).
- Prefer pure transformations over side-effecting procedures. When side effects are necessary, isolate them at the boundaries.
- Grow by adding new components, not by making existing components bigger. If a feature extends a file by 100+ lines, ask whether a new file with a clear interface would be better.

---

## Coupling and Cohesion

**Minimize coupling between modules. Maximize cohesion within them.**

- **Dependency direction matters.** Depend on stable things. Concrete implementations depend on abstractions, not the reverse. Business logic should not import infrastructure details.
- **No hidden coupling.** If changing module A forces a change in module B, the coupling should be visible in the interface, not buried in implicit conventions or shared mutable state.
- **Cohesion test.** If you delete a function from a module, do the remaining functions still make sense together? If removing one function makes others pointless, the module is cohesive. If they're unrelated, it's a junk drawer.
- **Feature envy.** A function that mostly operates on another module's data belongs in that module. Move it.

---

## Data Over Branching

**Put variability into data structures before adding conditional logic.**

- When you see a chain of if/elif or a switch with logic per case, ask: can this be a lookup table, a registry, or a data-driven dispatch?
- Configuration and policy should live in data (dicts, configs, schemas), not in branching code. Branching code is harder to extend, harder to test, and harder to read.
- When a new variant requires adding a new branch to existing code rather than adding a new entry to a data structure, the design is closed where it should be open.

---

## Naming

**Names reveal intent, not implementation.**

- A reader should understand what a function does from its name and signature without reading the body.
- Avoid encoding type, scope, or convention into names (no `strName`, `m_count`, `IInterface`). The type system carries this.
- Name length should scale with scope. Loop variables can be short. Module-level functions should be descriptive.
- If naming something is hard, the thing probably isn't well-defined yet. Refine the concept before naming it.

---

## Error Handling

**Handle errors at the level that has enough context to do something useful.**

- Don't catch exceptions just to log and re-raise. Either handle them or let them propagate.
- Don't return error codes when exceptions are the language idiom (and vice versa). Match the ecosystem.
- Fail fast and loud on programmer errors (assertions, type violations). Fail gracefully on environmental errors (network, disk, user input).
- Error messages should say what went wrong, what was expected, and what the caller can do about it.

---

## DRY Without Brittleness

**Duplication is cheaper than the wrong abstraction.**

- The Rule of Three: tolerate duplication until you've seen the pattern three times. Two instances might be coincidence. Three is a pattern worth extracting.
- Premature abstraction creates coupling between things that happen to look similar today but diverge tomorrow. When that happens, the abstraction becomes a constraint.
- When extracting, the abstraction should make both call sites simpler. If it makes them more complex (more parameters, more configuration, more special cases), the extraction was wrong.

---

## Scalability Patterns

**Code should grow by composition, not by inflation.**

- When a module keeps growing with each feature, it's missing an extension point. Identify what varies and make it pluggable.
- Registries, plugins, middleware chains, and strategy patterns let new behavior join without modifying existing code.
- If the codebase has no pattern for extensibility in a given area, introducing one during a task is a valid design improvement -- not scope creep. But flag it as a design decision.

---

## Red Flags

These should always be flagged by the assessor. They may be acceptable in context, but they must be acknowledged, never silently passed.

| Red flag | What to look for |
|----------|-----------------|
| **God object** | One class/module that everything depends on. Changes to it ripple everywhere. |
| **Shotgun surgery** | A single logical change requires edits across many unrelated files. |
| **Primitive obsession** | Business concepts represented as raw strings, ints, or dicts instead of named types. |
| **Leaky abstraction** | Callers need to know implementation details to use the interface correctly. |
| **Dead code** | Functions, classes, imports, or branches that are never executed. |
| **Copy-paste variants** | Two or more code blocks that are 80%+ identical with minor variations. |
| **Magic numbers/strings** | Literals embedded in logic without named constants or explanation. |
| **Circular dependencies** | Module A imports B which imports A (directly or transitively). |
| **Test-only interfaces** | Public methods or parameters that exist only to make testing possible, not for real callers. |

---

## Assessment Stance

The assessor is not a style guide enforcer. The question is never "does this follow a rule?" It's: **does this implementation make the codebase easier or harder to change next time?**

Good code is code that:
- Can be understood without the author present
- Can be extended without modifying existing working code
- Fails in ways that are diagnosable
- Grows by addition, not by inflation

When flagging an issue, always state: (1) what the specific concern is, (2) what the concrete impact would be if left as-is, and (3) a suggested alternative. Do not flag style preferences as design issues.
