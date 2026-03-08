# Plan: Loosen Branch Protection for Solo Dev + AI Workflow

## Context

The repo's branch protection is configured for a multi-person team with formal code review. The actual workforce is one person + AI agents. Rules like "2 required reviewers" and "required signatures" actively block the workflow (e.g., can't squash commits, AI commits are unsigned).

## Current vs Proposed

| Rule | Current | Proposed | Rationale |
|------|---------|----------|-----------|
| Required reviews | 2 approvers, code owner, dismiss stale, last push approval | **Remove entirely** | Can't review your own PRs; AI can't approve |
| Required signatures | Yes | **No** | AI agent commits are unsigned |
| Merge queue | Yes | **Remove** | No concurrent PRs to serialize |
| Force pushes | Blocked | **Allow** | Enables squash/rebase after push |
| Conversation resolution | Required | **Remove** | Unnecessary friction for solo |
| Required status checks | 3 checks, strict (must be up-to-date) | **Keep 3 checks, non-strict** | Checks are valuable; strict mode forces constant rebasing |
| Linear history | Yes | **Keep** | Clean history is still good |
| Enforce admins | Off | **Keep off** | Escape hatch for emergencies |
| Allow deletions | No | **Keep no** | Protect against accidents |

## Implementation

Single `gh api` call to update branch protection on `main`:

**File**: No files modified — this is a GitHub API settings change.

**Command**:
```bash
gh api repos/ivviiviivvi/.github/branches/main/protection \
  --method PUT \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": false,
    "contexts": ["CI / CI Status Check", "CI / Lint Code", "Security Scan / Secret Detection"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": true,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": false,
  "required_signatures": false
}
EOF
```

Note: `required_pull_request_reviews: null` removes the PR review requirement entirely. `restrictions: null` means no push restrictions (anyone with write access can push).

The merge queue is a separate setting controlled by rulesets — since no rulesets were found, it may be set at the org level or via the branch protection "merge queue" checkbox. We'll check after applying.

## Verification

1. Run the `gh api` command
2. Verify with `gh api repos/ivviiviivvi/.github/branches/main/protection` that settings took effect
3. Test: `git commit --allow-empty -m "test" && git push --force-with-lease` to confirm force push works
4. Test: push a commit directly to main without a PR to confirm no review requirement
