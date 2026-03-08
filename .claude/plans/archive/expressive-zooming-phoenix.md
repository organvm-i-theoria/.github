# Plan: Address Issues in PRs #284, #285, and #287

## Summary
Three open PRs are blocked by a combination of workflow bugs and validation issues. The workflow bugs in `auto-merge.yml` and `pr-task-catcher.yml` are blocking multiple PRs.

---

## Issue Analysis

### PR #284 - slack-github-action v1.26.0 → v2.1.1 (Dependabot)
| Aspect | Details |
|--------|---------|
| **Files Changed** | `.github/workflows/reusable-notify.yml` (1 file) |
| **Breaking Changes** | None - v1→v2 is backward compatible |
| **Blockers** | Branch naming validation fails (`dependabot/` not in allowed prefixes) |
| **Other Failures** | Claude review (missing API key), badge management (peter-evans action), cascading from validation |

### PR #285 - Workflow Metrics Update
| Aspect | Details |
|--------|---------|
| **Files Changed** | `metrics/metrics-summary.md`, `metrics/workflow-metrics.json` |
| **Content Issues** | None - legitimate metrics update |
| **Blockers** | Workflow bugs in `auto-merge.yml` and `pr-task-catcher.yml` |
| **Status** | Behind main (needs rebase after fixes) |

### PR #287 - Live Demo Badge (Simulation Mode)
| Aspect | Details |
|--------|---------|
| **Files Changed** | `README.md` (adds badge) |
| **Content Issues** | Badge links to non-functional simulation URL |
| **Blockers** | Same workflow bugs as PR #285 |
| **Action** | Fix - remove simulation badge or point to real resource |

---

## Root Cause: Workflow Bugs

### Bug 1: `auto-merge.yml` line 75 - JavaScript Syntax Error
```javascript
// CURRENT (fails when not workflow_dispatch):
prNumber = ${{ github.event.inputs.pr_number }};
// Expands to: prNumber = ;  ← Invalid JS

// FIX:
prNumber = ${{ github.event.inputs.pr_number || 'null' }};
// Or use: prNumber = context.payload.inputs?.pr_number;
```

### Bug 2: `auto-merge.yml` lines 584-586 - Malformed Object
```javascript
// CURRENT (syntax error):
tree: parentCommit.tree.sha
})).data.tree.sha,
parents: [mergeSha]

// FIX:
tree: parentCommit.tree.sha,
parents: [mergeSha]
```

### Bug 3: `pr-task-catcher.yml` - Output Format Issue
Lines 92-100 may have issues when `UNCHECKED_TASKS` is empty, causing heredoc format errors.

---

## Implementation Plan

### Phase 1: Fix Workflow Bugs (Required First)
These fixes unblock PRs #285 and #287.

**File: `.github/workflows/auto-merge.yml`**

1. **Line 75** - Fix undefined variable:
   ```yaml
   # Change:
   prNumber = ${{ github.event.inputs.pr_number }};
   # To:
   prNumber = '${{ github.event.inputs.pr_number }}' || null;
   ```
   Then parse it properly in JS.

2. **Lines 584-586** - Remove malformed code:
   ```javascript
   // Delete line 585: })).data.tree.sha,
   // Result should be:
   tree: parentCommit.tree.sha,
   parents: [mergeSha]
   ```

**File: `.github/workflows/pr-task-catcher.yml`**

3. **Lines 96-100** - Handle empty heredoc safely:
   ```bash
   # Add check before heredoc
   if [ -n "$UNCHECKED_TASKS" ]; then
     {
       echo "unchecked_tasks<<TASK_LIST_EOF"
       printf '%s\n' "$UNCHECKED_TASKS"
       echo "TASK_LIST_EOF"
     } >> $GITHUB_OUTPUT
   else
     echo "unchecked_tasks=" >> $GITHUB_OUTPUT
   fi
   ```

### Phase 2: Handle PR #284 (Dependabot slack-github-action)
**Options:**
- **A) Allow Dependabot branches** - Update `validate-version-control.yml` to skip validation for `dependabot/*` branches
- **B) Close and manually update** - Close PR, manually update the action SHA

**Recommended: Option A** - Dependabot branches should be allowed since they're automated and follow their own conventions.

### Phase 3: Handle PR #285 (Metrics Update)
After workflow fixes:
1. Update branch from main: `gh pr update-branch 285`
2. Wait for checks to pass
3. Merge the PR

### Phase 4: Fix PR #287 (Live Demo Badge)
**Action: Close PR - non-functional content**

The PR adds this badge to README.md:
```markdown
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Available-brightgreen?style=for-the-badge)](https://demo-ivviiviivvi-.github.agentsphere.dev)
```

Since this badge points to a non-existent URL and has no real value, the fix is to close the PR entirely:
```bash
gh pr close 287 --comment "Closing - badge links to non-functional simulation URL. The entire purpose of this PR was to add this badge, which provides no value without real deployment."
git push origin --delete agentsphere/add-live-demo-badge
```

**Alternative** (if we want to keep the PR structure): Edit the branch to remove the badge and update PR description, but this defeats the purpose since the PR's only change IS the badge.

---

## Files to Modify

| File | Changes |
|------|---------|
| `.github/workflows/auto-merge.yml` | Fix JS syntax errors (lines 75, 584-586) |
| `.github/workflows/pr-task-catcher.yml` | Fix heredoc output format (lines 96-100) |
| `.github/workflows/validate-version-control.yml` | Add Dependabot branch exception |
| PR #287 | Close PR and delete branch (non-functional badge) |

---

## Verification

1. **After workflow fixes:**
   ```bash
   # Trigger workflow manually to test
   gh workflow run auto-merge.yml
   gh workflow run pr-task-catcher.yml
   ```

2. **For PR #284:**
   ```bash
   gh pr checks 284 --watch
   ```

3. **For PR #285:**
   ```bash
   gh pr update-branch 285
   gh pr checks 285 --watch
   gh pr merge 285 --squash
   ```

4. **For PR #287:**
   ```bash
   # Close PR since badge points to non-existent URL
   gh pr close 287 --comment "Closing - badge links to non-functional simulation URL."
   git push origin --delete agentsphere/add-live-demo-badge
   ```

---

## Decisions Made

1. **PR #287**: Fix by closing PR (badge points to non-existent URL, no value to merge)
2. **Dependabot handling**: Allow `dependabot/*` branches in validation workflow
