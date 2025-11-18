# AI-Accelerated Rapid Development Workflow

> **Optimized for Solo Developer + Multiple AI Assistants**
>
> Problem: Traditional PR workflows create bottlenecks when one developer works with multiple AI agents, generating working software in <24 hours but drowning in branch/PR management.
>
> Solution: Streamlined trunk-based development with intelligent automation.

---

## The Problem

**Traditional workflow:**
```
AI 1 creates feature A → Branch A → PR A → Review → Merge
AI 2 creates feature B → Branch B → PR B → Review → Merge
AI 3 creates feature C → Branch C → PR C → Review → Merge
...
Result: 10+ open PRs, lost tasks, merge bottleneck
```

**You are both author AND reviewer** - pure overhead when CI ensures quality.

---

## The Solution: Speed-Optimized Workflow

### Core Principles

1. **CI is the Gatekeeper** - If tests pass, ship it
2. **Short-lived Branches** - Max 48 hours from creation to merge
3. **Auto-merge by Default** - Manual review only for critical changes
4. **Task-first, PR-second** - Track work in issues/tasks, not PR backlogs
5. **Batch Related Work** - Merge dependent PRs together
6. **Ruthless Cleanup** - Auto-close stale branches

---

## Workflow Types

### Type 1: Quick Wins (<2 hours, low risk)

**Use this for:** Bug fixes, docs, config changes, small features

```bash
# AI creates branch
git checkout -b fix/quick-bug-fix

# AI implements fix
# ... makes changes ...

# AI commits with auto-merge label
git commit -m "fix: resolve quick bug"
git push -u origin fix/quick-bug-fix

# Create PR with auto-merge label
gh pr create --title "fix: resolve quick bug" \
  --body "Quick fix that passes all CI checks" \
  --label "automerge:when-ci-passes"

# ✅ Auto-merges when CI passes (no manual review)
```

**Lifecycle:**
- Created → CI runs → ✅ Pass → Auto-merge → Branch deleted
- Total time: 5-15 minutes

---

### Type 2: Standard Features (2-24 hours, medium complexity)

**Use this for:** New features, refactoring, multi-file changes

```bash
# AI creates branch
git checkout -b feature/user-dashboard

# AI implements feature
# ... makes changes ...

# AI commits
git commit -m "feat: add user dashboard"
git push -u origin feature/user-dashboard

# Create PR with standard review
gh pr create --title "feat: add user dashboard" \
  --body "Implements user dashboard with analytics\n\nCloses #123" \
  --label "needs-review"

# You review when ready (not blocking)
# Meanwhile, AI continues on other tasks

# When ready: approve and auto-merge, OR let it auto-merge if labeled
```

**Lifecycle:**
- Created → CI runs → You review async → Merge
- Total time: 2-24 hours
- **Key:** Review happens async, doesn't block other AI work

---

### Type 3: Complex/Critical (>24 hours, high risk)

**Use this for:** Architecture changes, security, breaking changes

```bash
# AI creates branch
git checkout -b feature/major-refactor

# AI works incrementally with draft PR
gh pr create --draft --title "feat: major refactor" \
  --body "Work in progress - major architecture change"

# You review incrementally
# When ready, mark ready for review
gh pr ready

# Manual approval required
gh pr review --approve
gh pr merge --squash
```

**Lifecycle:**
- Created → Draft PR → Incremental commits → Review → Approve → Merge
- Total time: Variable
- **Key:** Explicit approval required

---

## Auto-Merge Configuration

### Labels that Trigger Auto-Merge

| Label | Behavior | Use When |
|-------|----------|----------|
| `automerge:when-ci-passes` | Merges immediately when all CI checks pass | Bug fixes, docs, low-risk changes |
| `automerge:after-24h` | Merges 24h after creation if CI passes | Standard features, gives time for second thought |
| `automerge:batch` | Waits for related PRs, merges together | Dependent changes across multiple PRs |
| `needs-review` | **Blocks** auto-merge, requires manual approval | Default for complex changes |

### How to Apply

**When creating PR:**
```bash
gh pr create --label "automerge:when-ci-passes"
```

**To existing PR:**
```bash
gh pr edit 123 --add-label "automerge:when-ci-passes"
```

**In PR description:**
```markdown
/automerge when-ci-passes
```

---

## Branch Lifecycle Management

### Automatic Cleanup

**Stale Branch Policy:**

| Age | Status | Action |
|-----|--------|--------|
| 0-48h | Active | No action |
| 48-72h | Warning | Bot comments: "Branch is 2 days old, merge or close soon" |
| 72h+ | Stale | Bot comments: "Will auto-close in 24h unless updated" |
| 96h+ | Closed | Auto-closes PR, deletes branch, extracts tasks to issue |

**Override stale automation:**
```bash
gh pr edit 123 --add-label "keep-alive"
```

---

## Task Tracking Integration

### Problem: Lost Tasks in Closed PRs

When PRs are abandoned, the work/tasks inside are lost.

### Solution: Automated Task Extraction

**Before closing a stale PR, automation:**

1. Scans PR description and comments for task lists
2. Extracts incomplete tasks
3. Creates a new issue: "Extracted tasks from PR #123"
4. Links back to original PR
5. Closes PR, deletes branch

**Example:**

PR #123 is stale with:
```markdown
- [x] Implement feature A
- [ ] Add tests for feature A
- [ ] Update docs
```

Automation creates Issue #124:
```markdown
# Extracted Tasks from PR #123

Original PR was closed due to inactivity. These tasks remain:

- [ ] Add tests for feature A (from PR #123)
- [ ] Update docs (from PR #123)

See original work: #123
```

---

## Batch Merge Workflow

### Problem: Related PRs Create Merge Conflicts

```
PR #100: Update API endpoint
PR #101: Update API tests (depends on #100)
PR #102: Update API docs (depends on #100)

Merging #100 creates conflicts in #101 and #102
```

### Solution: Batch Merge Labels

**Mark PRs as related:**
```bash
gh pr edit 100 --add-label "batch:api-update"
gh pr edit 101 --add-label "batch:api-update"
gh pr edit 102 --add-label "batch:api-update"
```

**Automation:**
1. Waits for ALL PRs with `batch:api-update` to pass CI
2. Rebases them in dependency order
3. Merges all together
4. Deletes all branches

**Or manually trigger:**
```bash
# Comment on any PR in the batch
/merge-batch api-update
```

---

## Daily Workflow for Solo Dev + AI

### Morning (15 min)
```bash
# Check what AI agents accomplished overnight
gh pr list --label "automerge:when-ci-passes"

# Review auto-merged PRs (just awareness)
gh pr list --state merged --limit 10

# Check anything that needs your review
gh pr list --label "needs-review"

# Prioritize tasks for AI agents today
gh issue list --label "priority:high"
```

### During Day (Continuous)
```bash
# AI 1 works on task A → auto-merges when done
# AI 2 works on task B → auto-merges when done
# AI 3 works on task C → needs your review

# You work on core architecture
# You review complex PRs async (not blocking)
```

### Evening (15 min)
```bash
# Review what shipped today
gh pr list --state merged --search "merged:>=2024-01-15"

# Check for stale branches
gh pr list --label "stale"

# Plan tomorrow's AI tasks
gh issue create --title "Task for AI: implement X"
```

### Weekly (30 min)
```bash
# Batch close stale PRs
gh pr list --label "stale" --json number --jq '.[].number' | xargs -I {} gh pr close {}

# Review metrics
gh run list --workflow="repo-metrics.yml"

# Adjust automation based on patterns
```

---

## Feature Flags for Incomplete Work

### Problem: Feature not done but need to merge to reduce PR backlog

### Solution: Feature flags

```typescript
// Use feature flags for work-in-progress
const FEATURE_FLAGS = {
  NEW_DASHBOARD: process.env.ENABLE_NEW_DASHBOARD === 'true', // default: false
  API_V2: process.env.ENABLE_API_V2 === 'true',
};

// Merge incomplete features disabled by default
if (FEATURE_FLAGS.NEW_DASHBOARD) {
  return <NewDashboard />;
}
return <OldDashboard />;
```

**Benefits:**
- Merge early, merge often
- Reduce PR backlog
- Enable features when ready
- A/B test in production

---

## PR Size Guidelines

### Target Sizes for Fast Merge

| Size | Lines Changed | Merge Time | Auto-Merge? |
|------|---------------|------------|-------------|
| XS | <10 | <5 min | ✅ Yes |
| S | 10-99 | <15 min | ✅ Yes |
| M | 100-499 | <1 hour | ⚠️ Maybe |
| L | 500-999 | <4 hours | ❌ No |
| XL | 1000+ | Manual | ❌ No |

**If PR is L or XL:**
1. Break into smaller PRs
2. Use feature flags
3. Use draft PR for incremental work

---

## Handling CI Failures

### Auto-Merge Behavior on Failure

```
PR created with "automerge:when-ci-passes"
  ↓
CI starts running
  ↓
CI fails ❌
  ↓
Auto-merge: BLOCKED
  ↓
Bot comments: "Auto-merge blocked. Fix CI to proceed."
  ↓
AI or you fix the issue
  ↓
Push new commit
  ↓
CI re-runs
  ↓
CI passes ✅
  ↓
Auto-merge: EXECUTES
```

**No manual intervention needed if AI fixes CI failures**

---

## Migration from Current State

### Step 1: Triage Existing PRs (One-time, 1 hour)

```bash
# Get all open PRs
gh pr list --limit 100

# For each PR, decide:
# 1. Merge now → Add "automerge:when-ci-passes"
# 2. Needs work → Add "needs-review"
# 3. Obsolete → Close, extract tasks
# 4. Batch merge → Add "batch:<name>"

# Example:
gh pr edit 45 --add-label "automerge:when-ci-passes"
gh pr edit 46 --add-label "batch:api-refactor"
gh pr close 47 --comment "Obsolete, extracted tasks to #200"
```

### Step 2: Enable Auto-Merge Workflows (5 min)

```bash
# Workflows are already created in .github/workflows/
# Just enable branch protection to allow auto-merge

# Settings → Branches → Branch protection rules → develop
# ✅ Require status checks to pass
# ✅ Require branches to be up to date
# ✅ Allow auto-merge
```

### Step 3: Update AI Agent Instructions (10 min)

Add to your AI prompts:

```markdown
When creating PRs:
- For bug fixes, docs, small features: Add label "automerge:when-ci-passes"
- For standard features: Add label "automerge:after-24h"
- For complex changes: Add label "needs-review"
- Always link to related issue: "Closes #123"
- Keep PRs small (<500 lines if possible)
```

### Step 4: Adopt New Daily Routine (Ongoing)

See "Daily Workflow" section above.

---

## Metrics to Track

### Measure Success

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **PR Merge Time** | <2 hours for small PRs | `gh pr list --state merged` |
| **Open PR Count** | <10 at any time | `gh pr list | wc -l` |
| **Stale PR Count** | <5 | `gh pr list --label stale | wc -l` |
| **Auto-merge Rate** | >70% of PRs | Weekly metrics workflow |
| **CI Pass Rate** | >90% | GitHub Actions insights |
| **Time to Ship** | <24h from idea to production | Track issue → merge time |

### Weekly Review

```bash
# Run weekly report
gh run view --workflow="weekly-commit-report.yml"

# Check auto-merge stats
gh pr list --state merged --search "merged:>=2024-01-08" --label "automerge:when-ci-passes" | wc -l
```

---

## Guardrails (Safety Checks)

### What Auto-Merge Will NOT Do

❌ Merge if ANY CI check fails
❌ Merge PRs labeled `needs-review` without approval
❌ Merge PRs targeting `main` (only `develop`)
❌ Merge PRs with unresolved review comments
❌ Merge PRs with merge conflicts
❌ Bypass security scans (CodeQL, Semgrep)

### Required CI Checks (Must Pass for Auto-Merge)

✅ All tests pass
✅ Code coverage >80% (if configured)
✅ CodeQL security scan passes
✅ Semgrep security scan passes
✅ Link checker passes (for docs)
✅ Conventional commit format
✅ PR description >50 characters

---

## Troubleshooting

### Issue: Too many auto-merges, not enough review

**Solution:**
```bash
# Change default to 24h delay
# In PR template, change default label to:
automerge:after-24h
```

### Issue: AI creating merge conflicts

**Solution:**
```bash
# Use batch merge for related work
# AI should coordinate:
gh pr edit 100 --add-label "batch:feature-x"
gh pr edit 101 --add-label "batch:feature-x"
```

### Issue: Important changes merged too fast

**Solution:**
```bash
# For critical files, require review
# Add to .github/CODEOWNERS:
/config/* @your-username
/security/* @your-username
```

### Issue: Want to disable auto-merge temporarily

**Solution:**
```bash
# Add label to PRs:
gh pr edit <number> --add-label "hold"

# Automation will skip these
```

---

## Best Practices

### ✅ DO

- Use auto-merge for >70% of your PRs (bug fixes, docs, small features)
- Keep PRs small (<500 lines changed)
- Link PRs to issues (track work in issues, not PR backlogs)
- Review auto-merged PRs async (for learning, not blocking)
- Use feature flags for incomplete work
- Close stale PRs ruthlessly (extract tasks first)
- Use batch merge for dependent PRs
- Trust your CI pipeline

### ❌ DON'T

- Create PRs without linking to issues/tasks
- Let PRs live >72 hours without activity
- Create XL PRs (>1000 lines) - break them up
- Disable CI checks to "move faster" (CI IS your safety net)
- Accumulate >15 open PRs (if you do, batch merge or close)
- Review every auto-merged PR before it merges (waste of time)

---

## Summary

**Old Way:**
- AI creates PR → you manually review → you manually merge → repeat
- Result: 20+ open PRs, lost tasks, slow shipping

**New Way:**
- AI creates PR with `automerge` label → CI passes → auto-merges
- You review complex PRs async, auto-merge handles 70%+ of work
- Result: <10 open PRs, no lost tasks, ship in hours not days

**Key Insight:**
> As a solo developer with AI assistants, the traditional PR review process is **pure overhead**. Your CI pipeline is your code reviewer. Trust it, automate it, ship faster.

---

**See Also:**
- `.github/workflows/auto-merge.yml` - Auto-merge implementation
- `.github/workflows/branch-lifecycle.yml` - Branch cleanup automation
- `.github/workflows/pr-batch-merge.yml` - Batch merge workflow
- `.github/workflows/task-tracker-integration.yml` - Task extraction
- `GIT_WORKFLOW.md` - Git branching strategy
- `BEST_PRACTICES.md` - General best practices

**Last Updated:** 2025-11-18
