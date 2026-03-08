# Fix All 176+ Security Scanning Alerts

## Context

The repo has 176 code scanning alerts (Semgrep, CodeQL, Trivy) and 7 secret scanning alerts. The bulk (155) are Semgrep warnings for shell/script injection in GitHub Actions workflows where `${{ github.event.* }}` is interpolated directly into `run:` or `script:` blocks. The rest are container CVEs, docker-compose hardening, cleartext logging, and minor findings.

## Alert Inventory

| Group | Tool / Rule | Count | Files |
|-------|------------|-------|-------|
| A | Semgrep `run-shell-injection` | 111 | ~44 workflow files |
| B | Semgrep `github-script-injection` | 11 | 4 workflow files |
| C | Semgrep `no-new-privileges` + `writable-filesystem` | 28 | 3 docker-compose files |
| D | Semgrep misc (curl-pipe-bash, missing-integrity, http) | 5 | 4 files |
| E | CodeQL `clear-text-logging-sensitive-data` | 4 | 3 Python files |
| F | CodeQL `incomplete-url-substring-sanitization` | 5 | 3 test files |
| G | Trivy container CVEs | 12 | 1 workflow file |
| H | Secret scanning (OpenVSX tokens) | 7 | git history only |
| **Total** | | **183** | |

## Implementation

### Phase 1: Critical — Cleartext Logging + Secrets (11 alerts)

**Group E: Mask sensitive data (4 alerts, 3 files)**

| File | Line | Issue | Fix |
|------|------|-------|-----|
| `src/automation/scripts/utils/validate-tokens.py` | 181 | Prints raw token value: `result['token']` | Mask: `token[:4]...token[-4:]` |
| `src/automation/scripts/utils/validate-tokens.py` | 128, 183 | Prints token scopes | Mask in CI: check `os.getenv('CI')` |
| `src/automation/deployment/deploy.py` | 163 | Prints missing secret name | Use `::add-mask::` or redact |
| `src/automation/scripts/batch_onboard_repositories.py` | 115 | Logs full validation errors | Log only error count |

**Group H: Secret scanning (7 alerts)**

All 7 are `openvsx_access_token` in `.specstory/history/` files (already deleted from working tree, only in git history). Resolution:
- Dismiss all 7 via API as `revoked`
- Ensure `.specstory/` is in `.gitignore`

### Phase 2: Shell & Script Injection (122 alerts, ~48 files)

**Group A: `run-shell-injection` (111 alerts)**

Mechanical fix — move `${{ github.event.* }}` and `${{ inputs.* }}` from `run:` blocks into step-level `env:` vars:

```yaml
# BEFORE (vulnerable):
run: |
  CONFIG="${{ github.event.inputs.config_file }}"

# AFTER (safe):
env:
  CONFIG_FILE: ${{ github.event.inputs.config_file }}
run: |
  CONFIG="$CONFIG_FILE"
```

Process files in this order:
1. **Reusable workflows** (8 files, ~46 alerts) — `reusable/specialized-testing.yml` (18), `reusable/ci-pipeline.yml` (11), `reusable/github-cli-pr-ops.yml` (5), `reusable/nodejs-setup-build.yml` (4), `reusable/python-setup-test.yml` (3), `reusable/artifact-management.yml` (2), `reusable/docker-build-push.yml` (2), `reusable/security-scanning.yml` (1)
2. **Active workflows** (~28 files, ~45 alerts) — all remaining `.github/workflows/*.yml`
3. **Composite actions** (3 files, ~4 alerts) — `.github/actions/*/action.yml`
4. **Workflow templates** (~7 files, ~16 alerts) — `src/automation/workflow-templates/`, `docs/workflow-templates/`, `.github/workflow-templates/`

**Group B: `github-script-injection` (11 alerts, 4 files)**

Move `${{ github.event.* }}` out of `script:` blocks into `env:`, use `process.env.*`:

```yaml
# BEFORE:
script: |
  const dryRun = '${{ github.event.inputs.dry_run }}' === 'true';

# AFTER:
env:
  DRY_RUN: ${{ github.event.inputs.dry_run }}
script: |
  const dryRun = process.env.DRY_RUN === 'true';
```

Files: `nightly-cleanup.yml` (5), `draft-to-ready-automation.yml` (3), `auto-batch-prs.yml` (2), `auto-merge.yml` (1)

### Phase 3: Docker-Compose Hardening (28 alerts, 3 files)

Add `security_opt: ["no-new-privileges:true"]` to all 14 services (resolves 14 alerts).
Add `read_only: true` + `tmpfs` to non-workspace services only (resolves 10 alerts).
For 4 workspace services: add `# nosemgrep: writable-filesystem-service` (dev containers need write access).

Files:
- `.config/devcontainer/docker-compose.yml` — 4 services (workspace, db, redis, mailhog)
- `.config/devcontainer/templates/fullstack/docker-compose.yml` — 5 services (workspace, postgres, redis, mailhog, adminer)
- `.config/devcontainer/templates/datascience/docker-compose.yml` — 5 services (workspace, postgres, redis, mlflow, adminer)

### Phase 4: Container CVEs (12 alerts, 1 file)

Update base image versions in `.github/workflows/docker-build-push.yml`:

| Current | Updated | Reason |
|---------|---------|--------|
| `node:18-alpine` | `node:22-alpine` | Node 18 EOL; fixes npm/tar/glob/cross-spawn CVEs |
| `python:3.11-slim` | `python:3.12-slim` | 3.11 security-only maintenance |
| `golang:1.21-alpine` | `golang:1.23-alpine` | 1.21 EOL; fixes OpenSSL CVEs |
| `rust:1.75-alpine` | `rust:1.85-alpine` | Outdated; fixes OpenSSL CVEs |

### Phase 5: Remaining Findings (10 alerts, ~6 files)

**Group D misc (5 alerts):**
- 2 HTML `missing-integrity`: Add SRI `integrity=` + `crossorigin="anonymous"` to Chart.js CDN scripts in `src/automation/dashboard/index.html` and `predictive-analytics.html`
- 2 `curl-pipe-bash`: In `.config/devcontainer/templates/dotfiles-enabled/setup.sh` — download to temp file then execute instead of piping
- 1 `http-not-https`: In `src/automation/scripts/web_crawler.py` — add `# nosemgrep` suppression (HTTP adapter mount needed for redirect handling)

**Group F URL validation (5 alerts, 3 test files):**
- Use `urllib.parse.urlparse()` instead of `in` / `startswith()` for URL checks in:
  - `tests/unit/test_web_crawler_security.py:90-92`
  - `tests/unit/test_web_crawler_coverage.py:493`
  - `tests/unit/test_resolve_link_placeholders.py:530`

## Commit Strategy

Single branch, one commit per phase:

1. `fix(security): mask cleartext token logging + resolve secret scanning alerts`
2. `fix(ci): remediate shell injection in reusable workflows`
3. `fix(ci): remediate shell injection in active workflows and templates`
4. `fix(ci): remediate github-script injection in 4 workflows`
5. `fix(docker): harden docker-compose services + update base images`
6. `fix(security): add SRI integrity, fix curl-pipe-bash, URL validation`

## Verification

1. YAML syntax: `python3 -c "import yaml; yaml.safe_load(open(f))"` for each modified file
2. Python lint: `ruff check . && ruff format --check .`
3. Tests: `python -m pytest tests/ -x`
4. Push and monitor: alert count should drop to near 0 after Semgrep/CodeQL re-scan
5. Spot-check: trigger 2-3 `workflow_dispatch` workflows to verify env var passing works
