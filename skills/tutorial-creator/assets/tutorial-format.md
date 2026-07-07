# Tutorial Markdown Format

Use this format when writing tutorial Markdown files. Adapt headings to the subject, but preserve the intent: concept first, real-work transfer, focused practice or implementation, and verifiable understanding.

## Multi-Chapter Tutorial

Create `index.md` as the entry page. Keep it concise; detailed teaching belongs in chapter files.

```markdown
# Tutorial Title

## Goal

Explain what the reader will understand or be able to do by the end.

## Audience

State who the tutorial is for and what they already know.

## Assumptions

List the assumptions that materially affect correctness, safety, tooling, context, or scope.

## Prerequisites

List only prerequisites required to succeed.

## Mental Model

Summarize the core vocabulary, moving parts, lifecycle, process, boundaries, or cause-and-effect relationships the reader needs before acting.

## Adoption Map

Explain how the concept applies in real work. For software, map it to codebase boundaries, modules, interfaces, dependencies, and ownership. For non-code topics, map it to workflows, documents, decisions, evidence, people, or constraints.

## Chapter Sequence

1. [Chapter 1: Meaningful Chapter Title](01-meaningful-chapter-title.md)
2. [Chapter 2: Meaningful Chapter Title](02-meaningful-chapter-title.md)

## Final Outcome

Describe the finished artifact, capability, decision, workflow, or understanding.

## References

Link only references that materially help the reader verify, deepen, or apply the tutorial.
```

## Chapter Or Single-File Tutorial

Use this shape for each chapter. For a single-file tutorial, use the same structure but omit chapter numbering if it would feel awkward.

```markdown
# Chapter 1: Meaningful Chapter Title

## Goal

Explain what the reader will understand, decide, produce, or be able to do after this chapter.

## Mental Model

Teach the concept before the mechanics. Explain vocabulary, data flow, lifecycle, state model, process, boundaries, or cause-and-effect relationships.

## Adoption Map

Explain where this chapter's idea fits in real work:

- For software: codebase location, seams, interfaces, dependencies, data ownership, failure boundaries, and coupling to avoid.
- For non-code topics: workflow location, artifacts changed, decisions informed, people involved, evidence needed, and concepts not to conflate.

## Decisions And Tradeoffs

Explain meaningful alternatives, why this tutorial chooses one, and when a different choice would be better.

## Risk Checklist

Call out relevant privacy, security, safety, data, legal, operational, compatibility, cost, performance, or user-impacting risks before the reader acts.

## Prerequisites

List only prerequisites that materially affect this chapter.

## Practice Or Implementation Steps

### Step 1: One focused action

#### What to do

Give the exact instruction, exercise, implementation step, decision task, or practice scenario.

#### What is happening

Explain what this step changes, creates, configures, proves, or helps the reader understand.

#### Explanation

Explain important code, commands, examples, calculations, diagrams, decisions, artifacts, or reasoning. If the step includes code, call out important lines, control flow, data boundaries, dependencies, and failure modes. If there is no code, explain the subject's natural artifact or example instead.

#### Context and reasoning

Explain why this step is appropriate for real work, what constraints matter, and what tradeoffs the reader is accepting.

#### Integration notes

Explain how to apply this step in an existing codebase, workflow, project, document, team process, or decision context. Omit only when the step is purely conceptual and has no adoption implications.

#### Validation

Give the command, test, inspection, exercise, expected output, observable behavior, rubric, or worked-example result that proves this step worked. Include common failure symptoms, misconceptions, or wrong answers and what they usually mean.

#### Caveats and notes

Call out edge cases, common mistakes, limitations, and safety concerns.

Repeat focused steps as needed. Split steps when one step mixes setup, design, implementation, validation, and troubleshooting.

## Validation Ladder

List the checks that prove progress from fastest to most realistic:

- Fast local/self-check
- Focused unit or concept check
- Integration, scenario, or workflow check
- End-to-end/manual check
- Evidence that confirms the chapter is complete

Use software tests for code tutorials. Use exercises, scenario checks, compare-and-contrast examples, review prompts, critique rubrics, or observable evidence for non-code tutorials.

## Troubleshooting

Use a concise matrix or bullets:

- Symptom: What the reader observes.
- Likely cause: What usually caused it.
- Fix: What to do next.

## Readiness Check

List concrete checks that show the reader is ready to apply the concept to a feature, issue, project, workflow, discussion, or decision. Prefer checks that require explanation, diagnosis, application, comparison, or judgment.

## Further Reading

Link official docs, source files, issues, standards, references, or deeper explanations that materially help the reader.
```

## Format Rules

- Keep Markdown as the source of truth.
- Use one H1 per file.
- Omit sections only when they add no value for the topic.
- Rename headings only when the subject's natural language is clearer, but keep the same teaching purpose.
- Prefer focused snippets and examples over large dumps. If a full file or full artifact is necessary, provide it only after explaining the smaller pieces.
- Put high-impact risks early, not only in final caveats.
- End every chapter at a usable, testable, or verifiable stopping point.
