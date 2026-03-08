# Root Directory Consolidation Plan

## Problem Statement

The repository root has sprawled from ~12 items to 26+ tracked items. This needs consolidation to maintain a clean, organized structure.

---

## Current State Analysis

### Tracked Root Items (26 total) → Actions

```
✗ .accesslint.yml        → move to .config/
✓ .config/               # keep
✓ .devcontainer/         # keep (symlink)
✗ .gitbook.yaml          → move to .config/
✓ .github/               # required
✓ .gitignore             # required
✗ .imgbotconfig          → move to .config/
✓ .pre-commit-config.yaml # keep (symlink)
✓ .vscode/               # keep (symlink)
✗ agents/                → DELETE (unnecessary symlink)
✗ AGENTS.md              → move to .ai/AGENTS.md
✗ CLAUDE.md              → move to .ai/, create symlink
✓ docs/                  # required
✗ GEMINI.md              → move to .ai/GEMINI.md
✓ LICENSE                # required
✗ metrics/               → move to docs/reports/
✗ netlify.toml           → DELETE (not used)
✓ package-lock.json      # required
✓ package.json           # required
✓ pyproject.toml         # required
✗ railway.json           → DELETE (not used)
✓ README.md              # required
✗ setup_week6.sh         → DELETE (temp script)
✓ src/                   # required
✗ template-config.yml    → move to .config/
✓ tests/                 # required
```

### Untracked Sprawl
- `automation/ml/` - empty directory (delete)

---

## Target State (12 root items)

```
.ai/                     # AI guidance files (new)
.config/                 # All configs consolidated
.github/                 # GitHub workflows, templates
.gitignore
CLAUDE.md                # Symlink → .ai/CLAUDE.md (Claude Code discovery)
docs/                    # All documentation
LICENSE
package.json             # + package-lock.json
.pre-commit-config.yaml  # Symlink → .config/pre-commit.yaml
pyproject.toml
README.md
src/
tests/
```

**Symlinks** (required for tool discovery):
- `CLAUDE.md` → `.ai/CLAUDE.md`
- `.pre-commit-config.yaml` → `.config/pre-commit.yaml`
- `.vscode` → `.config/vscode`
- `.devcontainer` → `.config/devcontainer`

---

## Phase 1: Move Config Files to .config/

| Source | Destination |
|--------|-------------|
| `.accesslint.yml` | `.config/accesslint.yml` |
| `.gitbook.yaml` | `.config/gitbook.yaml` |
| `.imgbotconfig` | `.config/imgbotconfig` |
| `template-config.yml` | `.config/template-config.yml` |

**Delete** (not actively used):
- `netlify.toml` - No active deployments
- `railway.json` - No active deployments

---

## Phase 2: Consolidate AI Guidance Files

**User Decision**: Create `.ai/` directory for AI guidance files with symlinks for tool discovery.

### Create Directory Structure

```
.ai/
├── CLAUDE.md        # Claude Code instructions
├── GEMINI.md        # Gemini instructions
├── AGENTS.md        # Codex/general agent instructions
└── README.md        # Explains the directory purpose
```

### Root Symlinks (for tool discovery)

| Symlink | Target | Reason |
|---------|--------|--------|
| `CLAUDE.md` → `.ai/CLAUDE.md` | Claude Code auto-discovers root CLAUDE.md |
| `GEMINI.md` → `.ai/GEMINI.md` | Gemini auto-discovers root GEMINI.md (optional) |

### Keep As-Is

| File | Location | Reason |
|------|----------|--------|
| `.github/copilot-instructions.md` | `.github/` | GitHub Copilot standard location |

### Migration Steps

1. Create `.ai/` directory
2. Move `CLAUDE.md` → `.ai/CLAUDE.md`
3. Move `GEMINI.md` → `.ai/GEMINI.md`
4. Move `AGENTS.md` → `.ai/AGENTS.md`
5. Create symlink `CLAUDE.md` → `.ai/CLAUDE.md` (required for Claude Code)
6. Optionally create symlink `GEMINI.md` → `.ai/GEMINI.md`
7. Create `.ai/README.md` explaining the directory

---

## Phase 3: Remove Unnecessary Items

| Action | Item | Reason |
|--------|------|--------|
| Remove symlink | `agents/` → `src/ai_framework/agents` | Unnecessary indirection |
| Delete | `setup_week6.sh` | Temporary development script |
| Delete | `automation/` (untracked) | Empty directory |

---

## Phase 4: Relocate Metrics

Move `metrics/` → `docs/reports/metrics/`

Contents:
- `health/latest.json` - Health metrics data

---

## Phase 5: Update References

Files that may reference moved items:
- `CLAUDE.md` - Check for any references
- `.github/workflows/*.yml` - Check for config paths
- `README.md` - Check for links

---

## Verification

```bash
# Count root items (target: ~12 visible + symlinks)
ls -1 | wc -l

# Verify symlinks work
ls -la CLAUDE.md .pre-commit-config.yaml .vscode .devcontainer

# Confirm CLAUDE.md symlink resolves
cat CLAUDE.md | head -5

# Run pre-commit to ensure configs still work
pre-commit run --all-files

# Check for broken references
git grep -l "agents/\|netlify\|railway" -- ':!.git' ':!*.md'

# Verify .ai/ structure
ls -la .ai/
```

---

## Commits

```
chore: create .ai/ directory for AI guidance files

  - Move CLAUDE.md, GEMINI.md, AGENTS.md to .ai/
  - Create symlink CLAUDE.md → .ai/CLAUDE.md
  - Add .ai/README.md explaining directory purpose

chore: move config files to .config/

  - Move .accesslint.yml, .gitbook.yaml, .imgbotconfig
  - Move template-config.yml

chore: remove unused files and symlinks

  - Delete agents/ symlink (unnecessary)
  - Delete setup_week6.sh (temp script)
  - Delete netlify.toml, railway.json (not used)

chore: move metrics to docs/reports/
```

---

## Risk Assessment

**Low Risk**:
- Moving config files to `.config/`
- Removing `agents` symlink, `setup_week6.sh`
- Deleting unused `netlify.toml`, `railway.json`
- Moving `metrics/`

**Medium Risk**:
- Creating `.ai/` with symlinked `CLAUDE.md` - Claude Code must still discover it

**Mitigation**:
- Test that `cat CLAUDE.md` works via symlink before committing
- Run `pre-commit run --all-files` to verify config moves
- CI will validate nothing is broken

---

## Investigation Results

1. **AGENTS.md**: Root version (44 lines) contains "Repository Guidelines" with project structure and dev commands. Move to `.ai/AGENTS.md` as Codex-style agent instructions.

2. **template-config.yml**: No references found. Safe to move to `.config/`.

3. **Deployment configs**: No references found. **User confirmed not used - DELETE both.**

4. **agents symlink**: No references found. Safe to remove.

---

## User Decisions

✓ **AI files**: Create `.ai/` directory with symlinks for tool discovery
✓ **Deployment configs**: Delete both (not used)
