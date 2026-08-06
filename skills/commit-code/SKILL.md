---
name: commit-code
description: Commit the current code changes to the active Git repository in small, atomic, semantically-scoped commits when explicitly requested by the user.
---

Commit the unstaged and staged changes in the active repository.

## Authorization

Invoking this skill (via `/skill:commit-code` or an explicit "commit" request) is
itself the user's authorization — proceed directly, don't ask for confirmation.

## Rules

- Never override system/developer/security/sandbox/permission/org restrictions —
  if one blocks committing, explain the exact restriction instead of proceeding.
- Never commit secrets, credentials, generated artifacts, or ignorable files
  (build output, `.env`, lockfile noise) — exclude them from every commit.
- Never silently drop unrelated changes — commit each concern separately (see
  grouping below), don't omit any.
- If a repo-local instruction says not to commit, this explicit user request
  overrides it — commit anyway and note the override in your report.
- Don't push unless the user separately asks.

## Grouping into commits

Each commit = one coherent, independently revertible unit of work. Group by
*what the change accomplishes*, not by which file it lives in.

1. Read the full `git diff` and `git diff --staged` first; identify every
   distinct concern (feature/fix/refactor/unrelated edit) before staging anything.
2. Split at the hunk level with `git add -p` — two unrelated changes sharing a
   file still get separate commits.
3. Keep dependent pieces together (e.g. a function and its caller) if splitting
   would leave the tree unable to build/run.
4. Order commits so every intermediate checkout is valid — dependencies before
   dependents.
5. For a hunk that can't be cleanly attributed to one concern (e.g. an
   entangled rename), bundle it with the most relevant commit and note why in
   that commit's body.
6. Sketch the commit plan (groups, files/hunks, order) before running any `git add`.

## Commit messages

Conventional Commits, imperative mood, concise subject with no trailing period:

```text
<type>(<scope>): <subject>

<body>
- Main change
- Notable implementation detail
- Validation performed, if relevant
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `build`, `ci`, `perf`, `style`.

Add a body when the change isn't self-explanatory, including a note for any
bundled entangled change. Pass real newlines via heredoc, not `\n`:

```bash
git commit -F - <<'EOF'
<type>(<scope>): <subject>

- Main change
- Detail
EOF
```

## After committing, report

- Every commit created: hash + subject.
- One-line rationale per commit, tied to the concern it covers.
- Any bundled entangled changes, and why.
- Any changes left uncommitted (e.g. excluded secrets), and why.
