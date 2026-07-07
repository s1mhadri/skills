---
name: tutorial-creator
description: Create polished concept-learning and implementation-prep tutorials as matching Markdown and HTML artifacts, with an independent Markdown verification pass when warranted. Use when Codex needs to turn any topic, concept, issue, ticket, feature request, implementation plan, or coding task into a tutorial that teaches the mental model, practical adoption path, step-by-step practice or implementation, validation ladder, risks, caveats, explanations, and further-reading links.
---

# Tutorial Creator

## Overview

Turn the user's input into a tutorial that prepares another person to understand a subject deeply enough to use it in real work. A good tutorial must transfer judgment, not only steps: teach the mental model, the adoption strategy, the tradeoffs, the validation path, and the risks before or while showing examples.

Produce Markdown as the source of truth, then create matching HTML with the optional renderer or the bundled HTML template.

Keep the skill generic. Do not force software-project language onto every subject. For code tutorials, talk about modules, tests, dependencies, and integration seams. For non-code tutorials, translate the same intent into the subject's natural form: concepts, decisions, workflows, examples, exercises, evidence, mistakes, constraints, and readiness checks.

## Workflow

1. Clarify only when missing information would make the tutorial misleading. Otherwise, state reasonable assumptions in the tutorial.
2. Gather context from the repo, ticket, issue, docs, or user-provided material. For changing technologies, prefer current official documentation and cite useful external references. Record the docs or versions that materially affect correctness.
3. Decide the tutorial mode:
   - Use **concept-first** mode when the user wants to learn a topic, concept, tool, domain, pattern, or practice before applying it.
   - Use **existing-project implementation** mode when the input is an issue, feature, ticket, repo change, or project-specific plan.
   - Use **greenfield demo** mode only when a standalone learning project, practice scenario, or worked example is appropriate or explicitly requested. Even then, include notes for adapting the lesson to an existing codebase, workflow, project, or decision context.
4. Decide whether the scope needs chapters:
   - Use chapters when the topic has multiple milestones, concepts, subsystems, or implementation phases.
   - Use a single tutorial file when the topic can be taught cleanly in one sequence.
5. Create the output folder at `.scratch/tutorial/<topic-slug>/`.
6. Read `assets/tutorial-format.md`, then write Markdown files first:
   - Multi-chapter tutorials: `index.md`, `01-<chapter-slug>.md`, `02-<chapter-slug>.md`, etc.
   - Single-file tutorials: `<topic-slug>.md`.
7. Run the Markdown verification gate:
   - For multi-chapter tutorials, implementation-prep tutorials, changing technologies, high-impact topics, or any tutorial with code/commands, run a standalone verification subagent before creating HTML when subagent tools are available and allowed.
   - For small single-file concept tutorials, run the verifier when available, allowed, and useful; otherwise self-review against the same rubric.
   - Give the verifier only the task context and Markdown source files. Do not give it your private diagnosis, intended fixes, or generated HTML.
   - Ask the verifier to report blocking issues, non-blocking suggestions, and evidence. It must not edit files.
   - Fix valid blocking issues in Markdown, then rerun verification or self-check the changed areas. Do not generate final HTML while known blocking issues remain.
8. Create matching HTML:
   - If Python is available, run `python3 <skill-dir>/scripts/render_tutorial.py .scratch/tutorial/<topic-slug>` to generate matching `.html` files.
   - If Python is not available, copy `assets/tutorial-template.html` once per Markdown file and manually replace the template placeholders with the title, header navigation, footer navigation, and HTML content derived from that Markdown file.
9. Review the Markdown and HTML outputs for parity, completeness, ordering, broken links, malformed code fences, step quality, conceptual coverage, integration guidance, risk coverage, and validation quality.

## Markdown Verification Gate

Use a standalone verification subagent when subagent tools are available, allowed, and the tutorial is not trivial. The verifier is a reviewer, not a co-author. It must judge whether the Markdown tutorial is ready to become the source of truth. If a subagent cannot be used, perform the same rubric locally and state that fallback in the final response.

Use this prompt shape, adapted to the current task:

```text
Review the Markdown tutorial files in <tutorial-folder> as source-of-truth learning material.

Audience and purpose: <summarize the intended learner and why they need the tutorial>.
Topic/context: <summarize the topic, repo/issue/docs if relevant, and assumptions>.

Do not edit files. Do not review generated HTML. Return a concise review with:
1. Blocking issues: misinformation, unsafe advice, broken code/commands, missing mental model, missing adoption map, missing validation, bad sequencing, wrong audience fit, missing risk coverage for sensitive/high-impact topics, or anything that would mislead a reader.
2. Non-blocking suggestions: useful improvements that are not required for correctness.
3. Evidence: file paths, headings, snippets, or missing sections that justify each issue.
4. Verdict: pass if no blocking issues remain; otherwise fail.

Check the tutorial against this rubric:
- Audience fit
- Mental model before mechanics
- Real-work adoption map
- Decision quality and alternatives
- Step size and sequencing
- Technical or factual correctness
- Validation ladder
- Risk and safety coverage
- Troubleshooting guidance
- Readiness check
- Generic fit for the subject's natural artifacts
- Markdown quality: headings, links, code fences, chapter order, missing files
```

Treat verifier feedback as input, not authority. Apply feedback when it identifies real reader harm, correctness risk, missing required structure, or broken verification. Reject or defer feedback that is only stylistic, contradicts user requirements, or would overfit the tutorial to an unrelated use case. Record unresolved non-blocking suggestions only when useful.

Blocking issues include:

- Incorrect, stale, or unsupported facts, APIs, commands, formulas, process claims, or references.
- Tutorial structure that prevents the reader from understanding the mental model before acting.
- Missing adoption map for implementation-prep or real-work tutorials.
- Missing validation ladder, readiness check, or troubleshooting for non-trivial tutorials.
- High-impact risk coverage that appears too late or is absent.
- Steps that are too large to learn from, cannot be verified, or would fail when followed.
- Code, commands, exercises, links, or file paths that are broken or internally inconsistent.

## Tutorial Structure

Start each Markdown file with one H1 title. For multi-chapter tutorials, include the chapter number in the title.

For multi-chapter tutorials, create `index.md` as the combined entry page. Use it to explain the tutorial goal, audience, assumptions, prerequisites, chapter sequence, and expected final outcome. Link to every chapter file. Keep it concise; the detailed instruction belongs in the chapter files.

Before writing tutorial Markdown, read `assets/tutorial-format.md` and follow its format. It is the maintained source for the tutorial skeleton and the placement of mental model, adoption map, decisions, risk checklist, validation ladder, troubleshooting, readiness check, and further reading.

For concept-learning and implementation-prep tutorials, the overview or first chapter must include the relevant version of these sections:

- **Mental model**: the core concepts, vocabulary, data flow, lifecycle, state model, boundaries, process, or cause-and-effect relationships the reader must understand before acting.
- **Adoption map**: how the idea is applied in real work. For software, explain where the implementation belongs in a codebase, what seams or interfaces to look for, what should stay decoupled, and how to avoid turning a demo shape into accidental architecture. For non-code topics, explain where the concept fits in the workflow, what decisions it informs, what artifacts or evidence it changes, and what should not be conflated.
- **Decision record**: the important choices, realistic alternatives, and why the tutorial chooses one approach.
- **Risk checklist**: privacy, security, data retention, safety, migrations, performance, operations, cost, compatibility, or user-impacting risks when relevant. Put high-impact risks near the beginning, not only as final caveats.
- **Validation ladder**: the ordered checks that prove progress. For software, include fast local checks, unit tests, integration tests, end-to-end/manual verification, and failure symptoms. For non-code topics, include self-checks, worked examples, scenario exercises, review questions, observable evidence, and common wrong answers.
- **Readiness check**: how the reader can tell they understand enough to apply the concept to a feature, issue, project, discussion, or decision.

Each chapter must finish at a usable, testable, or verifiable stopping point. Prefer chapters that complete one coherent learning or implementation slice: a reader should be able to finish the chapter, run the relevant check or exercise, and verify that the concept, workflow, or system works before moving on. Do not cut a chapter off where the reader cannot check whether they understood or changed the right thing.

Omit empty subsections only when they would add no value. Keep every step focused on one thing; split a step if it mixes setup, design, implementation, and validation.

## Writing Standards

- Teach application patterns used in good projects and real work, not toy examples, unless the user explicitly asks for a beginner-only version.
- Teach the concept before the mechanics when the reader needs a mental model to make safe implementation decisions.
- Bias tutorials toward real-work transfer. If a standalone project, scenario, or example is used for learning, explicitly label it as a learning harness and explain how the pattern maps into an existing codebase, workflow, project, or decision context.
- Use the subject's natural artifacts. Code topics may need files, commands, tests, APIs, and diagrams. Product, design, writing, research, operations, or domain topics may need examples, decision tables, checklists, exercises, review prompts, process maps, or critique rubrics instead.
- Prefer clear, maintainable code with separation of concerns, good naming, meaningful validation, error handling, and tests when relevant.
- For software tutorials, prefer deep modules over shallow modules. Teach small interfaces with meaningful behavior behind them, placed at clean seams, instead of pass-through wrappers that expose as much complexity as they hide. Explain the interface, implementation, seam, and adapter choices when they matter.
- Explain what is being done in every step, not just the command or code to run. Include enough context for the reader to understand the concept, the application boundary being changed, and the consequences of the change.
- Explain code before or after showing it. Call out important lines, control flow, data boundaries, dependencies, failure modes, and how the code participates in the larger implementation.
- Avoid large code blocks inside a single step. Prefer patch-sized snippets with local explanations: add this import, create this interface, insert this cleanup block, then verify. When a larger implementation must be shown, split it by responsibility, explain each chunk, and provide the full file only as an optional end-of-step reference.
- Include reasoning for meaningful decisions: library choice, file placement, API shape, state model, validation strategy, error handling, performance tradeoffs, and testing approach.
- Include realistic alternatives for meaningful decisions and explain why the tutorial does not choose them.
- Prefer end-to-end tests, exercises, or verification workflows for each chapter because they prove the learning slice works through the subject's natural interface. Use unit tests when the chapter is specifically about isolated software logic, edge cases, fast feedback around a deep module, or behavior that cannot be exercised reliably end to end.
- Include a validation ladder. For coding tutorials, use fast checks, unit tests, integration checks, end-to-end/manual checks, expected outcomes, common failures, and evidence that the chapter is complete. For non-code tutorials, use exercises, scenario checks, compare-and-contrast examples, review prompts, rubrics, and evidence the reader can inspect.
- Treat external resources, handles, network connections, files, cameras, subprocesses, locks, and transactions as lifecycle hazards. Teach ownership, cleanup, failure paths, retries, cancellation, and shutdown behavior when they appear.
- For changing dependencies, APIs, models, schemas, or services, state the version or documentation source used, avoid unqualified `latest` dependencies unless intentionally teaching that tradeoff, and explain pinning or upgrade strategy.
- For privacy, security, identity, user data, money, medical, legal, or production operations topics, include the risk model before implementation steps and revisit it where code changes affect the risk.
- Include a troubleshooting matrix for non-trivial tutorials. Use columns or bullets for symptom, likely cause, and fix.
- Make each paragraph earn its place. Remove filler, generic encouragement, and background that does not help the reader act or understand.
- Use external references only where they add useful learning, context, or verification. Prefer official docs, repo files, standards, tickets, or reputable references over generic search-result pages.
- Keep Markdown and HTML content aligned by editing Markdown first. Then regenerate HTML with the renderer when available, or update the template-based HTML manually and verify it still matches the Markdown.
- Ensure every HTML code block displays line numbers. When manually filling the template, preserve the `.code-block`, `.code-line`, `.line-number`, and `.line-code` structure used by the renderer.
- Use only Previous, Home, and Next buttons for repeated page navigation. Do not repeat a full list of chapter links at the top of each chapter page.

## Output Rules

- Always place artifacts under `.scratch/tutorial/<topic-slug>/`.
- Use lowercase hyphenated slugs.
- Generate one `.html` file for every `.md` tutorial file.
- For multi-chapter tutorials, include both `index.md` and `index.html` as the combined overview page.
- For multi-chapter tutorials, every HTML page must include Previous, Home, and Next navigation controls in both the header and footer. Use disabled spacing where a previous or next page does not exist, and keep Home in the middle.
- Keep filenames ordered and stable so chapters sort correctly.
- In the final response, list the created Markdown and HTML files, mention any assumptions or external references used, and summarize the verification result. If a verification subagent was not used for a non-trivial tutorial, state why and what self-review was performed instead.

## Renderer

Use `scripts/render_tutorial.py` after writing or editing tutorial Markdown when Python is available:

```bash
python3 skills/tutorial-creator/scripts/render_tutorial.py .scratch/tutorial/<topic-slug>
```

The script renders every `.md` file in the topic folder to a same-named `.html` file with `assets/tutorial-template.html`, a shared stylesheet, header navigation, and footer navigation. It intentionally treats Markdown as the canonical content, so the companion files stay synchronized.

## HTML Template

Use `assets/tutorial-template.html` when the renderer cannot run or when manual HTML creation is required. Copy it to the target `.html` filename and replace:

- `{{title}}` with the page title.
- `{{header_nav}}` with Previous, Home, and Next buttons for multi-chapter tutorials, or an empty string for single-page tutorials.
- `{{footer_nav}}` with the same Previous, Home, and Next buttons.
- `{{body}}` with HTML converted from the matching Markdown file.

Keep the template structure intact unless the user asks for a different visual style. If manually filling the template, compare the finished HTML against the Markdown section by section before final delivery. Render fenced code blocks with line numbers using this structure:

```html
<pre class="code-block"><code class="language-python"><span class="code-line"><span class="line-number">1</span><span class="line-code">print("hello")</span></span></code></pre>
```
