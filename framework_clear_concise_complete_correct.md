# Writing Framework: Clear, Concise, Complete, and Correct

## Purpose

Use this framework when deciding whether technical writing needs more detail.

The goal is **clear, concise, complete, and correct** — in that order only when necessary, not as a rigid priority. Concision is valuable, but not when it removes information the reader needs to understand, trust, use, or safely act on the material.

A useful rule:

> **Keep detail when removing it would make the reader more likely to misunderstand, make the wrong decision, take the wrong action, or need to ask a predictable follow-up question. Otherwise, remove it.**

---

## The Four Cs

### 1. Clear

The reader should be able to understand the intended meaning without reconstructing it.

Check for:

- Unambiguous terminology.
- Explicit subjects and relationships.
- Logical ordering.
- Concrete wording instead of vague abstractions.
- Enough context to understand references such as "this," "it," or "the change."
- Examples when an abstract explanation is harder to understand than a concrete one.

**Test:** Could a technically competent reader reasonably interpret this another way?

If yes, add or change detail until the ambiguity is gone.

---

### 2. Concise

Every sentence should earn its place.

Remove:

- Repetition.
- Background the intended audience already knows.
- Obvious implications.
- Decorative language.
- Multiple explanations of the same point.
- Implementation detail that does not affect the reader's task.

Prefer:

- One precise sentence over several approximate ones.
- Specific nouns and verbs.
- Tables or lists when they reduce repeated prose.
- Examples that replace lengthy explanation.

**Test:** If this sentence disappeared, would the reader lose information they need?

If no, delete it.

---

### 3. Complete

Include everything the reader needs for the document's purpose — not everything that could possibly be known about the subject.

Completeness is **purpose-relative**.

For a technical document, ask whether the reader has enough information to:

1. Understand what is being described.
2. Understand why it matters, when that matters.
3. Perform the intended task.
4. Make the intended decision.
5. Understand important constraints and exceptions.
6. Recognize failure modes that are reasonably foreseeable.
7. Know what to do next.

Do not confuse completeness with exhaustive coverage.

**Test:** What predictable question would the reader ask immediately after reading this?

If the answer is necessary to use the document correctly, include it.

---

### 4. Correct

Technical writing must be factually and operationally correct.

Check:

- Facts and claims.
- Terminology.
- Examples.
- Commands, configuration, and code.
- Version-specific behavior.
- Preconditions and assumptions.
- Scope and exceptions.
- Causal explanations.

Do not add plausible detail merely to make a document feel complete. If a detail is uncertain, verify it or explicitly mark the uncertainty.

**Test:** Could this detail cause the reader to do something wrong?

If yes, verify it before publishing.

---

# The Concision–Completeness Decision Framework

When deciding whether to keep an extra detail, classify it by the value it provides.

## Keep the detail if it does any of these

### 1. Prevents a likely misunderstanding

Keep it when the shorter version has a plausible incorrect interpretation.

Examples:

- Clarifying that a setting applies to one environment, not all environments.
- Distinguishing "restart" from "rebuild."
- Explaining that a default applies only when another value is absent.

### 2. Prevents a likely operational mistake

Keep it when omitting the detail could cause a bad command, configuration, deployment, migration, or recovery action.

Operationally important details include:

- Preconditions.
- Ordering.
- Required permissions.
- Scope.
- Destructive consequences.
- Rollback requirements.
- Idempotency.
- Known failure modes.

### 3. Explains a non-obvious decision

Keep enough rationale to explain **why this approach exists**, especially when a reasonable engineer might otherwise change it.

Good technical rationale answers:

- Why this instead of the obvious alternative?
- What constraint drove the choice?
- What failure mode does this avoid?
- What tradeoff was accepted?

Avoid documenting rationale that is merely historical trivia.

### 4. Handles an important exception

Keep an exception when it is:

- Common.
- Easy to miss.
- High-impact.
- Relevant to the intended audience.
- Likely to invalidate the main instruction.

Do not enumerate every theoretical edge case.

### 5. Makes the document independently usable

Keep information that otherwise forces the reader to search elsewhere for a necessary piece of context.

A document does not need to contain everything. It should, however, contain enough to complete its stated purpose without unnecessary detective work.

### 6. Establishes a boundary

Technical instructions often need explicit boundaries:

- Applies to X, not Y.
- Supported from version X onward.
- Safe only in environment Z.
- Do not perform this during normal production traffic.

Boundaries are usually worth the extra words because they prevent overgeneralization.

---

# Remove the detail if it only does these things

### 1. Proves that the author knows the subject

Expertise should appear in the quality of the explanation, not in unnecessary depth.

### 2. Repeats information already established

Do not restate a constraint, definition, or conclusion unless repetition serves a specific navigational purpose.

### 3. Explains obvious mechanics

If the intended audience already understands the mechanism, skip it unless the mechanism affects the decision or operation.

### 4. Documents every possible edge case

Technical documents become less useful when low-probability cases obscure the normal path.

Document unusual cases separately when they deserve treatment.

### 5. Adds historical detail with no current consequence

"The system used to work this way" is useful only when that history explains current behavior, constraints, or decisions.

### 6. Provides multiple examples that prove the same point

Usually one good example is enough. Add another only when it demonstrates a materially different case.

---

# The Information Value Test

For each sentence, ask:

> **What changes for the reader because this sentence exists?**

A useful answer should fall into one of these categories:

| Value | Keep? |
|---|---|
| Prevents misunderstanding | Usually yes |
| Prevents an operational mistake | Yes |
| Provides required context | Yes |
| Documents an important constraint | Yes |
| Explains a non-obvious decision | Usually yes |
| Covers a meaningful exception | Usually yes |
| Gives a useful example | Usually |
| Provides historical context | Only if relevant |
| Repeats an earlier point | Usually no |
| Shows expertise | No |
| Adds trivia | No |
| Covers a remote hypothetical | Usually no |

---

# The Compression Test

When a passage feels too long, do **not** immediately delete details.

Compress in this order:

1. Remove repetition.
2. Remove unnecessary qualifiers.
3. Replace verbose constructions with precise wording.
4. Combine closely related sentences.
5. Convert repeated prose into a list or table.
6. Move secondary detail into a note, appendix, or linked reference.
7. Only then remove substantive information.

The objective is to reduce **words**, not necessarily **information**.

---

# The Layering Pattern

When information is useful but not universally needed, layer it.

### Layer 1 — Main path

Give the information every reader needs.

### Layer 2 — Important context

Include constraints, rationale, exceptions, and details needed by a meaningful subset of readers.

### Layer 3 — Deep detail

Move exhaustive reference material, historical background, edge cases, and implementation specifics elsewhere when they would interrupt the main flow.

This produces concise writing without sacrificing completeness.

A good technical document often looks like:

> **What to do → why it matters → important constraints → details for unusual cases**

---

# Audience and Document Type Matter

The same information can be necessary in one document and excessive in another.

### Runbook

Optimize for execution.

Include:

- Preconditions.
- Exact commands or actions.
- Expected results.
- Failure handling.
- Rollback.
- Safety boundaries.

Minimize theory unless it affects execution.

### Architecture / design document

Optimize for understanding and future decision-making.

Include:

- Context.
- Constraints.
- Alternatives considered when relevant.
- Tradeoffs.
- Decision rationale.
- Consequences.
- Important rejected options.

### Reference documentation

Optimize for retrieval.

Include:

- Precise definitions.
- Complete supported options.
- Defaults.
- Constraints.
- Examples.
- Version/scope information.

Avoid long narrative explanations.

### PR / code review

Optimize for reviewability.

Explain:

- What changed.
- Why it changed.
- Non-obvious behavior.
- Risks and tradeoffs.
- Testing and operational impact.

Do not reproduce code behavior the diff already makes obvious.

### Incident / postmortem

Optimize for understanding and prevention.

Include:

- Timeline.
- Impact.
- Trigger.
- Contributing factors.
- Detection.
- Resolution.
- Corrective actions.

Avoid irrelevant chronology and blame-oriented detail.

---

# The Predictable Follow-Up Test

Before deleting a detail, ask:

> **If I remove this, what is the most likely question a competent reader will ask next?**

If the answer is:

- "Nothing important" → remove it.
- "Something useful but optional" → consider moving it to a note or reference.
- "Something required to proceed" → keep it.
- "Something required to avoid a mistake" → definitely keep it.

This is one of the most practical ways to resolve the concise/complete conflict.

---

# The Reader-Work Budget

Every omission transfers work from the writer to the reader.

That can be appropriate, but it should be deliberate.

A concise document is not necessarily a good document if the reader must:

- Search multiple documents for missing context.
- Infer unstated assumptions.
- Reverse-engineer why a choice was made.
- Experiment to discover prerequisites.
- Guess which exceptions matter.

Prefer **writer effort** when the information is stable, important, and broadly useful.

Prefer **reader lookup** when the information is:

- Voluminous.
- Frequently changing.
- Easily discoverable.
- Only relevant to a small subset of readers.

---

# A Practical Editing Pass

Use this sequence when editing technical writing:

## Pass 1 — Purpose

Write down the document's job in one sentence.

If a sentence does not serve that job, challenge its presence.

## Pass 2 — Reader

Identify:

- Who is reading?
- What do they already know?
- What are they trying to accomplish?
- What could they get wrong?

## Pass 3 — Critical information

Mark:

- Required actions.
- Constraints.
- Decisions.
- Exceptions.
- Failure modes.
- Assumptions.

These are the details most likely to be lost during editing.

## Pass 4 — Compression

Remove repetition and compress wording without removing the marked information.

## Pass 5 — Completeness

Ask:

> Could the intended reader successfully use this without asking a predictable, important follow-up question?

If not, add the missing information.

## Pass 6 — Correctness

Verify facts, commands, examples, versions, assumptions, and operational consequences.

## Pass 7 — Final deletion

Look for anything that remains only because it is interesting, impressive, historical, or familiar to the author.

Delete it unless it serves the reader.

---

# Default Rule for Technical Writing

When in doubt:

> **Be as concise as possible without making the reader supply information that the document reasonably should provide.**

Or, more operationally:

> **Do not optimize for minimum word count. Optimize for minimum reader effort while preserving correctness.**

That is the practical resolution of the concise-versus-complete conflict.

---

# Quick Checklist

Before publishing, ask:

- [ ] Is the purpose obvious?
- [ ] Is the intended audience clear?
- [ ] Can the main point be understood without inference?
- [ ] Does every important instruction include its necessary constraints?
- [ ] Are important exceptions covered?
- [ ] Could omission cause a likely mistake?
- [ ] Could a reasonable reader ask a predictable follow-up question?
- [ ] Have repetition and unnecessary wording been removed?
- [ ] Have deep details been layered rather than deleted?
- [ ] Are facts, examples, commands, and assumptions correct?
- [ ] Is the document complete **for its purpose**, rather than exhaustive?
- [ ] Does the final version minimize reader effort?

## One-sentence standard

**Clear enough to understand, concise enough to navigate, complete enough to use, and correct enough to trust.**
