# Plan: Org-Level `.github` Template Deployment Across 7 Organs

## Context

The organvm system has **two parallel template systems** that need to become one:

1. **organvm template system** — `organvm.env` / `organvm.config.json` / `organvm.env.local` — resolves org names via env vars (`${ORGAN_PREFIX}-i-theoria`, etc.)
2. **`.github` template system** — `template-config.yml` + `setup_template.py` — resolves org-specific values via mustache-style variables (`{{ORG_NAME}}`, `{{ORG_DISPLAY_NAME}}`, `{{NPM_SCOPE}}`, etc.)

The user's `.github` repo at `ivviiviivvi/.github` is exceptional and far exceeds what the planning corpus anticipated:
- 127 workflow YAML files (SHA-pinned)
- 18 issue templates
- Enterprise-grade community health files (CONTRIBUTING 3,000+ words, SECURITY with response SLAs)
- AI framework (agents, chatmodes, prompts)
- `profile/README.md` for org-level GitHub page
- Sophisticated `template-config.yml` + `setup_template.py` for parameterized deployment

**The problem:** The orgs don't exist yet on GitHub (verified — all 7 `organvum-*` names return 404). The planning corpus budgets ~105K TE for "org About sections" but has no specification for org-level `.github` repos. The `.github` repo is currently in `ivviiviivvi` (old ORGAN-I name) and has a few remaining hardcoded values.

**The question:** When and how to introduce this infrastructure across all 7 organizations.

---

## Strategic Recommendation: Phase 0, Immediately After Org Creation

The `.github` repo is **foundational infrastructure** — it should be the first repo in each org. The sequencing:

```
Phase -1 (PENDING — human task):
  Step 1: Rename ivviiviivvi → organvum-i-theoria (the .github repo comes along)
  Step 2: Rename omni-dromenon-machina → organvum-ii-poiesis
  Step 3: Rename labores-profani-crux → organvum-iii-ergon
  Step 4: Create organvum-iv-taxis, v-logos, vi-koinonia, vii-kerygma

Phase 0 (THIS PLAN — right after orgs exist):
  Step A: Fix remaining hardcoded values in the template source
  Step B: Harmonize template-config.yml with organvm.config.json
  Step C: Generate 7 per-organ template-config.yml variants
  Step D: Stratify workflows by organ type
  Step E: Deploy .github repos to all 7 orgs
  Step F: Customize profile/README.md per organ

Bronze Sprint (after .github deployed):
  Flagship READMEs inherit community health from org-level .github
  → No need to add CODE_OF_CONDUCT, CONTRIBUTING, SECURITY per-repo
  → Issue templates and PR templates available immediately
  → Workflows available for adoption
```

**Why Phase 0, not later:**
- GitHub's `.github` repo feature provides org-wide defaults — every repo in the org inherits community health files, templates, and workflow templates automatically
- Deploying `.github` first means Bronze Sprint flagship repos inherit infrastructure from day 1
- The `profile/README.md` is the org's public face — it should exist before any repos are publicized
- The `10-repository-standards.md` spec requires `.github/` in all repos — org-level defaults satisfy this requirement centrally

---

## Step A: Fix Remaining Hardcoded Values in Template Source

The `.github` repo is already well-parameterized but has 3 files with hardcoded org names:

| File | Current | Fix |
|------|---------|-----|
| `LICENSE` | `Copyright (c) 2025 ivi374forivi` | → `Copyright (c) 2025 {{ORG_DISPLAY_NAME}}` |
| `GOVERNANCE.md` | References "ivi374forivi organization" | → `{{ORG_NAME}}` |
| `CONTRIBUTORS.md` | References `[@ivi374forivi]` | → `{{ORG_NAME}}` |

These are edits to the existing `ivviiviivvi/.github` repo (which becomes `organvum-i-theoria/.github` after rename).

---

## Step B: Merge Template Systems Into `organvm.config.json`

**Decision:** Extend `organvm.config.json` to be the **single config file** for everything — org naming, `.github` template fields, feature flags, teams, emails. The existing `.github` repo's `template-config.yml` system is consumed by this unified config.

**Extend `.config/organvm.config.json` with new fields per organ:**

```jsonc
{
  "organ_prefix": "${ORGAN_PREFIX}",
  "shared": {
    "email_domain": "organvum.org",           // NEW
    "default_branch": "main",                  // NEW
    "license_default": "MIT",                  // NEW
    "personal_account": "4444J99",             // NEW (from organvm.env.local)
    "owner_display_name": "...",               // NEW — for LICENSE copyright
    "discord_invite": "...",                   // NEW — if applicable
    "teams": {                                 // NEW — shared team name pattern
      "leadership": "${ORGAN_PREFIX}-leads",
      "engineering": "${ORGAN_PREFIX}-engineering",
      "devops": "${ORGAN_PREFIX}-devops",
      "security": "${ORGAN_PREFIX}-security"
    }
  },
  "orgs": {
    "ORGAN-I": {
      "suffix": "i-theoria",
      "env_var": "ORGAN_I_ORG",
      "domain": "Theory",
      "etymology": "θεωρία — contemplation, theory",
      "display_name": "ORGAN I: Theoria",      // NEW
      "license": "MIT",                         // NEW — from 10-repository-standards.md §2.3
      "profile_tagline": "Epistemological frameworks and recursive systems", // NEW — from roadmap
      "features": {                             // NEW — workflow feature flags (for Phase 2+)
        "ai_agents": true,
        "advanced_ci": true,
        "security_scanning": true,
        "automated_releases": false,
        "demo_sandbox": false,
        "documentation_site": true,
        "ml_workflows": true
      }
    }
    // ... same pattern for ORGAN-II through VII
  }
}
```

**What this replaces:** The `.github` repo's `template-config.yml` + `setup_template.py` will read from `organvm.config.json` instead. One source of truth, one config file, one system.

**Generator script:** `scripts/generate-github-configs.py` reads `organvm.config.json` and produces per-organ `template-config.yml` files that the existing `setup_template.py` can consume. This is a bridge — it translates the unified config into the format the `.github` repo's existing tooling expects.

---

## Step C: Minimal Core Deployment (Phase 0)

**Decision:** Deploy only community health infrastructure now. Defer all 127 workflows to Phase 2/3.

**What gets deployed per org in Phase 0:**

| Component | Included | Notes |
|---|---|---|
| `profile/README.md` | YES | Org-specific, generated from `organvm.config.json` |
| `CODE_OF_CONDUCT.md` | YES | Identical across all 7 orgs (Contributor Covenant v2.1) |
| `CONTRIBUTING.md` | YES | Shared base with organ-specific adaptations (code vs docs vs art) |
| `SECURITY.md` | YES | Shared structure, org-specific contact email |
| `SUPPORT.md` | YES | Shared structure, org-specific links |
| `GOVERNANCE.md` | YES | Parameterized from template |
| `LICENSE` | YES | Per-organ license type from `organvm.config.json` |
| `FUNDING.yml` | YES | Shared across all orgs |
| `.github/ISSUE_TEMPLATE/` | YES | Shared 18 templates (reduce to essential ~6 for minimal core) |
| `.github/PULL_REQUEST_TEMPLATE.md` | YES | Shared across all orgs |
| `.github/CODEOWNERS` | YES | Per-organ team routing |
| `CLAUDE.md` | YES | Per-organ AI context (domain-specific) |
| `.github/workflows/` | NO | **Deferred to Phase 2/3** |
| `src/ai_framework/` | NO | **Deferred** |
| `src/automation/` | NO | **Deferred** |
| `docs/` (the 304 doc files) | NO | **Deferred** |
| `.config/` (linting, semgrep, etc.) | NO | **Deferred** |

**Reduced issue template set for minimal core (~6 essential):**
1. `bug_report.yml` — universal
2. `feature_request.yml` — universal
3. `documentation.yml` — universal
4. `question.md` — universal
5. `task.yml` — universal
6. `config.yml` — contact links / external links

The full 18 templates can be rolled out when workflows are deployed in Phase 2/3.

**Feature flags are recorded in `organvm.config.json` now** (see Step B) but not acted upon until Phase 2/3.

---

## Step D: Per-Organ `profile/README.md`

Each org gets a unique profile README reflecting its domain. The structure is shared; the content is organ-specific:

```markdown
# {{ORG_DISPLAY_NAME}}

> {{ORGAN_ETYMOLOGY}}

{{ORGAN_DESCRIPTION — 2-3 sentences from registry portfolio_angle}}

## Repositories

{{Auto-generated or curated list of repos in this org}}

## Part of the organvm System

This organization is **Organ {{N}}** of 7 in the [organvm](https://github.com/organvum-iv-taxis/orchestration-start-here) creative-institutional system.

{{Links to other 6 orgs}}
```

---

## Step E: Deployment Sequence

For each of the 7 orgs (after they exist on GitHub):

1. **ORGAN-I** (`organvum-i-theoria`): The `.github` repo already exists here (it comes along with the rename from `ivviiviivvi`). Fix hardcoded values, run `setup_template.py` with ORGAN-I config. This is the **pilot deployment**.

2. **ORGAN-II through VII**: Fork/clone from the template source. Generate per-organ `template-config.yml`. Run `setup_template.py`. Push as `.github` repo in each org.

**Pilot-first approach:** ORGAN-I is the test case because the repo already exists there. Validate that inherited community health files, issue templates, and profile README all work correctly. Then replicate to remaining 6 orgs.

---

## Files to Create/Modify

### In the planning corpus (`ingesting-organ-document-structure/`)

| File | Action | Purpose |
|------|--------|---------|
| `.config/organvm.config.json` | **EXTEND** | Add `shared` block, per-organ `display_name`, `license`, `profile_tagline`, `features` |
| `scripts/generate-github-configs.py` | **CREATE** | Reads `organvm.config.json`, generates per-organ `template-config.yml` for `.github` repo's `setup_template.py` |
| `.github-template/profile/README.md` | **CREATE** | Parameterized org profile README template with `{{ORG_DISPLAY_NAME}}`, `{{ORGAN_ETYMOLOGY}}`, cross-links |
| `.github-template/minimal-core/` | **CREATE** | The minimal-core file set (community health + templates) ready for per-org generation |

### In the remote `.github` repo (`ivviiviivvi/.github`)

| File | Action | Purpose |
|------|--------|---------|
| `LICENSE` | **EDIT** | `ivi374forivi` → `{{ORG_DISPLAY_NAME}}` |
| `GOVERNANCE.md` | **EDIT** | `ivi374forivi organization` → `{{ORG_NAME}}` |
| `CONTRIBUTORS.md` | **EDIT** | `[@ivi374forivi]` → `{{ORG_NAME}}` |

### Not created (planning doc avoided per MG4)

No new planning/specification document (`github-org-infrastructure.md`) will be created. The plan lives in `organvm.config.json` (the config IS the spec) and this plan file. Per the meta-review's declaration: no more planning documents.

---

## Verification

1. After fixing hardcoded values: grep the `.github` repo for `ivi374forivi` — should be 0 hits outside of git history
2. After generating configs: validate each `template-config.yml` against the `template-config.yml` schema in the original repo
3. After deploying to ORGAN-I (pilot): visit `https://github.com/organvum-i-theoria` and verify profile README displays
4. After deploying to ORGAN-I: create a test repo in the org and verify it inherits CODE_OF_CONDUCT, CONTRIBUTING, SECURITY, issue templates
5. After deploying to all 7 orgs: verify each org's profile page shows correct organ description and cross-links

---

## Decisions Made

1. **Deployment scope:** Minimal core first (community health + profile + templates). 127 workflows deferred to Phase 2/3.
2. **Template system:** Merge into unified `organvm.config.json`. Single source of truth for everything.

## Execution Dependency

**This plan is blocked on Phase -1 (human task):** The 7 orgs must exist on GitHub before `.github` repos can be deployed. Steps A-B (parameterization + config extension) can proceed now. Steps C-E (generation + deployment) require the orgs to exist.

**Suggested execution order:**
1. Steps A + B now (local work, no GitHub dependency)
2. Human does Phase -1 (rename 3 orgs, create 4 new)
3. Steps C + D + E immediately after orgs exist
