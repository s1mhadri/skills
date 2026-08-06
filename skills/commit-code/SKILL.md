---
name: commit-code
description: Commit the current code changes to the active Git repository in small, atomic, semantically-scoped commits when explicitly requested by the user.
---

Commit the unstaged and staged changes in the active repository.

## Authorization

Invoking this skill is itself the user's authorization — proceed directly, don't ask for confirmation.

## Rules

- Never override system/developer/security/sandbox/permission/org restrictions — if one blocks committing, explain it instead of proceeding.
- Never commit secrets, credentials, generated artifacts, or ignorable files (build output, `.env`, lockfile noise).
- Never drop unrelated changes silently — every concern gets its own commit (see grouping).
- An explicit user request overrides a repo-local "don't commit" instruction — commit anyway and note the override in your report.
- Don't push unless separately asked.

## Grouping into commits

Each commit = one coherent, revertible unit of work, grouped by *what changed*, not by file or domain — a feature and a refactor sharing a config area are still two commits.

Hard order — always enumerate before staging:

1. **Enumerate.** Before any `git add`, read the full diff (`git diff` + `git diff --staged`) and list each concern as a `type: subject` line. The *subject* defines the concern: same type with a different subject (`feat: X` / `feat: Y`) is still two commits, while different types are an even stronger split signal. State this list in your response as the plan — files/hunks, order — before staging begins.
2. **Stage per concern** with `git add -p`, splitting at the hunk level; sharing a file never merges two concerns.
3. **Merge only for a hard dependency** — keep pieces together only if splitting would break the build (e.g. a function and its caller).
4. **Order for validity** — every intermediate checkout must build; dependencies before dependents.
5. **Entangled hunks** that can't be cleanly attributed to one concern (e.g. a cross-cutting rename) get bundled with the closest commit, with a note in its body explaining why.

## Commit messages

Conventional Commits, imperative mood, concise subject, no trailing period:

```text
<type>(<scope>): <subject>

- Main change
- Notable detail
- Validation, if relevant
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `build`, `ci`, `perf`, `style`.

Add a body when the change isn't self-explanatory, noting any bundled entangled change. Use a heredoc for real newlines, not `\n`:

```bash
git commit -F - <<'EOF'
<type>(<scope>): <subject>

- Main change
EOF
```

## After committing, report

- Each commit: hash + subject + one-line rationale.
- Any bundled entangled changes and why.
- Any changes left uncommitted and why.