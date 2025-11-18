# AI Rapid Development - Quick Reference

> **For solo developers working with multiple AI assistants**
> Fast-track your PR workflow with intelligent automation

---

## 🚀 Quick Start

### For AI Assistants Creating PRs

```bash
# Quick fix/small feature (auto-merge immediately)
gh pr create \
  --title "fix: your fix here" \
  --body "Description" \
  --label "automerge:when-ci-passes"

# Standard feature (auto-merge after 24h)
gh pr create \
  --title "feat: your feature" \
  --body "Description\n\nCloses #123" \
  --label "automerge:after-24h"

# Complex change (needs review)
gh pr create \
  --title "refactor: major change" \
  --body "Description" \
  --label "needs-review"

# Related PRs (batch merge)
gh pr create \
  --title "feat: API endpoint" \
  --body "Description" \
  --label "batch:api-refactor"
```

---

## 🏷️ Labels Quick Reference

| Label | Effect | Use When |
|-------|--------|----------|
| `automerge:when-ci-passes` | ⚡ Merges immediately when CI ✅ | Bug fixes, docs, small features |
| `automerge:after-24h` | ⏰ Merges 24h after creation | Standard features |
| `automerge:batch` | 🔗 Waits for related PRs | Dependent changes |
| `batch:<name>` | 🔗 Groups related PRs | API updates, refactors |
| `needs-review` | 🛑 Blocks auto-merge | Complex/critical changes |
| `keep-alive` | ♾️ Prevents stale closure | Long-running work |
| `hold` | 🛑 Temporarily blocks merge | Need to pause |
| `do-not-extract-tasks` | 🚫 Skip task extraction on close | Obsolete work |

---

## ⏱️ PR Lifecycle Timeline

```
0h    PR Created
      ↓
      CI runs
      ↓
      ✅ CI passes + "automerge:when-ci-passes" → MERGED
      OR
      ⏳ Wait for label trigger...
      ↓
24h   "automerge:after-24h" → MERGED
      ↓
48h   ⚠️  Stale warning (if no activity)
      ↓
72h   🚨 Final warning
      ↓
96h   🔒 Auto-closed + task extraction
```

---

## 💬 Comment Commands

| Command | Action | Where |
|---------|--------|-------|
| `/merge-batch api-update` | Trigger batch merge | Any PR in batch |
| `/automerge` | Enable auto-merge | Any open PR |

---

## 📊 Daily Dashboard (15 min/day)

### Morning
```bash
# What auto-merged overnight?
gh pr list --state merged --search "merged:>=yesterday"

# What needs your review?
gh pr list --label "needs-review"

# Any stale warnings?
gh pr list --label "stale:warning"

# Open PR count (keep <10)
gh pr list | wc -l
```

### Evening
```bash
# Today's velocity
gh pr list --state merged --search "merged:>=today"

# Clean up stale PRs
gh pr list --label "stale:final-warning"
```

---

## 🎯 Target Metrics

| Metric | Target | Check With |
|--------|--------|------------|
| Open PRs | <10 | `gh pr list \| wc -l` |
| PR merge time | <2h | Auto-merged PRs |
| Stale PRs | <5 | `gh pr list --label stale` |
| Auto-merge rate | >70% | Weekly report |

---

## 🚦 Decision Tree

```
New PR needed?
  ↓
Is it quick (<2h) and low-risk?
  YES → automerge:when-ci-passes ⚡
  NO ↓
Is it related to open PRs?
  YES → batch:<name> 🔗
  NO ↓
Is it standard feature?
  YES → automerge:after-24h ⏰
  NO ↓
Is it complex/critical?
  YES → needs-review 🛑
```

---

## 🔥 Common Scenarios

### Scenario 1: 10+ Open PRs (Overwhelmed)

**Solution: Batch Close/Merge**

```bash
# Find old PRs
gh pr list --json number,createdAt | jq -r '.[] | select(.createdAt < "2024-01-10") | .number'

# Review each:
# - Obsolete? Close manually
# - Ready? Add automerge:when-ci-passes
# - Related? Add batch:<name>

# Example:
gh pr edit 45 --add-label "automerge:when-ci-passes"
gh pr edit 46 47 48 --add-label "batch:feature-x"
gh pr close 49 --comment "Obsolete work"
```

### Scenario 2: Related PRs Creating Conflicts

**Solution: Batch Merge**

```bash
# Label all related PRs
gh pr edit 100 101 102 --add-label "batch:api-update"

# Wait for all to pass CI, then:
# Comment on any PR: /merge-batch api-update

# Or manually trigger:
# Actions → Batch Merge → Run → Enter: batch:api-update
```

### Scenario 3: Important Change Merged Too Fast

**Solution: Post-Merge Review**

```bash
# Review what auto-merged
gh pr view 123

# If issue found, create fix PR or revert
gh pr comment 123 --body "Found issue: <explanation>"
git revert <commit>
```

### Scenario 4: Feature Not Done But Need to Reduce PR Backlog

**Solution: Feature Flags**

```typescript
// Merge with feature disabled
const FEATURE_FLAGS = {
  NEW_DASHBOARD: false,  // Not ready yet
};

if (FEATURE_FLAGS.NEW_DASHBOARD) {
  return <NewDashboard />;
}
```

```bash
# Label and merge
gh pr edit 150 --add-label "automerge:when-ci-passes"
```

---

## ⚙️ Configuration Changes

### Enable Auto-Merge in Repo Settings

1. Settings → General → Pull Requests
2. ✅ Allow auto-merge
3. ✅ Automatically delete head branches

### Update Branch Protection (Optional)

Settings → Branches → Add rule for `develop`:
- ✅ Require status checks: `CodeQL`, `Semgrep`, `Tests`
- ✅ Require branches up to date
- ⬜ Require pull request reviews (optional for solo dev)

### Create Labels

```bash
# Auto-merge labels
gh label create "automerge:when-ci-passes" --color "0E8A16" --description "Auto-merge when CI passes"
gh label create "automerge:after-24h" --color "1D76DB" --description "Auto-merge 24h after creation"
gh label create "automerge:batch" --color "5319E7" --description "Batch merge with related PRs"

# Stale labels
gh label create "stale:warning" --color "FEF2C0" --description "PR inactive 48+ hours"
gh label create "stale:final-warning" --color "FF9800" --description "PR will be closed soon"

# Control labels
gh label create "keep-alive" --color "006B75" --description "Prevent stale auto-closure"
gh label create "hold" --color "D93F0B" --description "Temporarily block merge"
gh label create "do-not-extract-tasks" --color "E99695" --description "Skip task extraction"

# Task labels
gh label create "extracted-tasks" --color "C5DEF5" --description "Tasks extracted from closed PR"
gh label create "needs-triage" --color "FBCA04" --description "Needs review and prioritization"
```

---

## 🆘 Troubleshooting

### Auto-merge not working?

```bash
# Check PR details
gh pr view 123

# Requirements:
# ✅ Not a draft
# ✅ CI all passed
# ✅ No merge conflicts
# ✅ Has automerge:* label
# ✅ No 'hold' or 'needs-review' label (unless approved)

# Manual trigger:
gh pr merge 123 --auto --squash
```

### Too many stale PRs?

```bash
# Find all stale
gh pr list --label "stale:warning,stale:final-warning"

# Batch decision:
for pr in $(gh pr list --label stale --json number -q '.[].number'); do
  echo "PR #$pr"
  gh pr view $pr
  read -p "Action? (m=merge, c=close, k=keep, s=skip): " action
  case $action in
    m) gh pr edit $pr --add-label "automerge:when-ci-passes" ;;
    c) gh pr close $pr ;;
    k) gh pr edit $pr --add-label "keep-alive" ;;
    *) echo "Skipped" ;;
  esac
done
```

### Lost track of tasks?

```bash
# Find extracted task issues
gh issue list --label "extracted-tasks"

# Manually extract from old PR
gh workflow run task-extraction.yml -f pr_number=123
```

---

## 📚 Related Docs

- **Full Guide**: `AI_RAPID_WORKFLOW.md`
- **Git Workflow**: `GIT_WORKFLOW.md`
- **Best Practices**: `BEST_PRACTICES.md`
- **CLAUDE.md**: Main AI assistant guide

---

## 🎓 Philosophy

> **For solo dev + AI:**
> - CI is your code reviewer
> - PRs are a means to ship, not a process to follow
> - Speed > bureaucracy (but quality via automation)
> - Track work in issues, not PR backlogs
> - Merge often, ship fast, fix forward

---

**Last Updated:** 2025-11-18
**Version:** 1.0.0
