# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Repository Purpose

Organization-level `.github` repository for {{ORG_NAME}} providing:

- Default community health files inherited by all org repositories
- {{WORKFLOW_COUNT}} GitHub Actions workflows
- {{AGENT_COUNT}} production AI agents in `src/ai_framework/`
- GitHub Copilot customizations (instructions, prompts, chatmodes, collections)

## Essential Commands

### Setup

```bash
pip install -e ".[dev]"
pre-commit install
```

### Testing

```bash
# Full test suite with coverage (58% minimum required)
python -m pytest --cov=src/automation

# Single test file
python -m pytest tests/test_specific.py -v

# Run by marker
python -m pytest -m unit        # Unit tests only
python -m pytest -m integration # Integration tests
python -m pytest -m critical    # Critical tests
```

### Linting and Code Quality

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Python linting with ruff
ruff check .
ruff format .

# Type checking
mypy src/automation/

# Security scanning
bandit -r src/automation/scripts/
```

### Version Management

```bash
# Check version (in pyproject.toml)
grep "^version" pyproject.toml  # Currently 1.0.0

# Bump and sync versions
npm run version:bump:minor
npm run version:sync
```

## Architecture Overview

> **Note**: The nested `.github/.github/` structure is intentional and correct
> for organization-level `.github` repositories. GitHub looks for workflows in
> `.github/workflows/` relative to the repository root.

```
.github/
├── .config/               # ALL configs (devcontainer, vscode, jules, pre-commit)
├── .github/workflows/     # {{WORKFLOW_COUNT}} automation workflows
│   └── reusable/          # {{REUSABLE_TEMPLATE_COUNT}} reusable workflow templates
├── docs/                  # ALL documentation (304+ files)
│   ├── archive/           # Historical reports
│   ├── guides/            # How-to guides (includes extended CLAUDE.md)
│   └── registry/          # Workflow registry
├── src/
│   ├── ai_framework/      # AI agents, chatmodes, prompts
│   │   ├── agents/        # {{AGENT_COUNT}} production AI agents (*.agent.md)
│   │   ├── chatmodes/     # {{CHATMODE_COUNT}} chatmodes (*.chatmode.md)
│   │   ├── collections/   # Collection definitions
│   │   └── prompts/       # Prompt templates (*.prompt.md)
│   └── automation/        # Python automation scripts
│       ├── scripts/       # {{SCRIPT_COUNT}} Python automation scripts
│       │   └── utils/     # Utility scripts (update-action-pins.py, etc.)
│       └── project_meta/  # Project metadata and context handoffs
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml         # Python config (deps, pytest, coverage, ruff, mypy)
└── package.json           # npm config (version scripts)
```

## Key Patterns

### Workflow SHA Pinning

All GitHub Actions are SHA-pinned with ratchet comments:

```yaml
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # ratchet:actions/checkout@v4
```

Update pins with:
`python src/automation/scripts/utils/update-action-pins.py --recursive`

### Centralized Version Management

Workflows use repository variables with fallbacks:

```yaml
python-version: ${{ vars.PYTHON_VERSION_DEFAULT || '3.12' }}
node-version: ${{ vars.NODE_VERSION_DEFAULT || '20' }}
```

### FUNCTIONcalled Metadata

Workflows can have `.meta.json` sidecars with layer classification:

- `core` - Foundation, CI, reusable workflows
- `interface` - User-facing workflows
- `logic` - Validation workflows
- `application` - Deployment, release workflows

## Commit Convention

**Strictly enforced** via pre-commit hooks and CI:

```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
```

Examples:

- `feat(workflows): add auto-labeling for new PRs`
- `fix(ci): resolve CodeQL security alerts`
- `docs: update installation guide`

## Pre-commit Troubleshooting

If `mypy` fails on `types-all` dependency:

1. Remove `types-all` from `.config/pre-commit-rapid.yaml`
1. Run `pre-commit clean && pre-commit install`

If `mdformat` has dependency conflicts:

1. Ensure rev is `0.7.17` with `mdformat-gfm>=0.3.5`
1. Run
   `pre-commit autoupdate --repo https://github.com/executablebooks/mdformat`

## Key Files

| File                                                 | Purpose                                                    |
| ---------------------------------------------------- | ---------------------------------------------------------- |
| `pyproject.toml`                                     | Python config (deps, pytest, coverage, ruff, mypy, bandit) |
| `.pre-commit-config.yaml`                            | Quality hooks (symlink to .config/pre-commit.yaml)         |
| `src/automation/scripts/utils/update-action-pins.py` | SHA pin updater                                            |
| `.github/WORKFLOW_STANDARDS.md`                      | Workflow conventions                                       |
| `docs/guides/CLAUDE.md`                              | Extended AI assistant guide with workflow catalog          |

## Runtime Requirements

- Python >= 3.9 (prefer 3.12)
- Node.js >= 20.0.0
- Dependencies: PyYAML, requests, PyGithub, jsonschema

## Branch Naming

Allowed patterns:

- `<lifecycle>/<type>/<component>` (e.g., `develop/feature/user-auth`)
- `fix/<description>` (e.g., `fix/workflow-bug`)
- `release/v<semver>` (e.g., `release/v1.2.0`)
- `dependabot/*` (automated dependency updates)

Lifecycles: develop, experimental, production, maintenance, deprecated, archive
Types: feature, bugfix, hotfix, enhancement, refactor, docs, test, chore

## Test Markers

```bash
pytest -m unit          # Unit tests
pytest -m integration   # Integration tests
pytest -m critical      # Critical functionality
pytest -m month1        # Month 1 core workflow tests
pytest -m month2        # Month 2 feature tests (Slack, ML)
pytest -m month3        # Month 3 advanced automation tests
pytest -m security      # Security-focused tests
```

<!-- ORGANVM:AUTO:START -->
## System Context (auto-generated — do not edit)

**Organ:** ORGAN-I (Theory) | **Tier:** infrastructure | **Status:** LOCAL
**Org:** `organvm-i-theoria` | **Repo:** `.github`

### Edges
- **Produces** → `ORGAN-IV, ORGAN-V`: unspecified (event: `distribution-completed`)
- **Produces** → `unspecified`: unspecified (event: `press-release`)
- **Produces** → `unspecified`: unspecified (event: `grant-update`)
- **Produces** → `ORGAN-V`: unspecified (event: `newsletter-published`)

### Siblings in Theory
`recursive-engine--generative-entity`, `organon-noumenon--ontogenetic-morphe`, `auto-revision-epistemic-engine`, `narratological-algorithmic-lenses`, `call-function--ontological`, `sema-metra--alchemica-mundi`, `system-governance-framework`, `cognitive-archaelogy-tribunal`, `a-recursive-root`, `radix-recursiva-solve-coagula-redi`, `nexus--babel-alexandria-`, `reverse-engine-recursive-run`, `4-ivi374-F0Rivi4`, `cog-init-1-0-`, `collective-persona-operations` ... and 4 more

### Governance
- Foundational theory layer. No upstream dependencies.

*Last synced: 2026-03-08T20:11:34Z*

## Session Review Protocol

At the end of each session that produces or modifies files:
1. Run `organvm session review --latest` to get a session summary
2. Check for unimplemented plans: `organvm session plans --project .`
3. Export significant sessions: `organvm session export <id> --slug <slug>`
4. Run `organvm prompts distill --dry-run` to detect uncovered operational patterns

Transcripts are on-demand (never committed):
- `organvm session transcript <id>` — conversation summary
- `organvm session transcript <id> --unabridged` — full audit trail
- `organvm session prompts <id>` — human prompts only


## Active Directives

| Scope | Phase | Name | Description |
|-------|-------|------|-------------|
| system | any | prompting-standards | Prompting Standards |
| system | any | research-standards-bibliography | APPENDIX: Research Standards Bibliography |
| system | any | research-standards | METADOC: Architectural Typology & Research Standards |
| system | any | sop-ecosystem | METADOC: SOP Ecosystem — Taxonomy, Inventory & Coverage |
| system | foundation | agent-seeding-and-workforce-planning | agent-seeding-and-workforce-planning |
| system | any | autopoietic-systems-diagnostics | SOP: Autopoietic Systems Diagnostics (The Mirror of Eternity) |
| system | any | cicd-resilience-and-recovery | SOP: CI/CD Pipeline Resilience & Recovery |
| system | any | cross-agent-handoff | SOP: Cross-Agent Session Handoff |
| system | any | document-audit-feature-extraction | SOP: Document Audit & Feature Extraction |
| system | any | essay-publishing-and-distribution | SOP: Essay Publishing & Distribution |
| system | any | market-gap-analysis | SOP: Full-Breath Market-Gap Analysis & Defensive Parrying |
| system | foundation | ontological-renaming | ontological-renaming |
| system | any | pitch-deck-rollout | SOP: Pitch Deck Generation & Rollout |
| system | any | promotion-and-state-transitions | SOP: Promotion & State Transitions |
| system | foundation | readme-and-documentation | readme-and-documentation |
| system | any | repo-onboarding-and-habitat-creation | SOP: Repo Onboarding & Habitat Creation |
| system | any | research-to-implementation-pipeline | SOP: Research-to-Implementation Pipeline (The Gold Path) |
| system | any | security-and-accessibility-audit | SOP: Security & Accessibility Audit |
| system | any | session-self-critique | session-self-critique |
| system | any | source-evaluation-and-bibliography | SOP: Source Evaluation & Annotated Bibliography (The Refinery) |
| system | any | stranger-test-protocol | SOP: Stranger Test Protocol |
| system | any | strategic-foresight-and-futures | SOP: Strategic Foresight & Futures (The Telescope) |
| system | any | typological-hermeneutic-analysis | SOP: Typological & Hermeneutic Analysis (The Archaeology) |
| unknown | any | gpt-to-os | SOP_GPT_TO_OS.md |
| unknown | any | index | SOP_INDEX.md |
| unknown | any | obsidian-sync | SOP_OBSIDIAN_SYNC.md |

Linked skills: cross-agent-handoff, evaluation-to-growth, planning-and-roadmapping, repo-onboarding-and-habitat-creation, structural-integrity-audit


**Prompting (Anthropic)**: context 200K tokens, format: XML tags, thinking: extended thinking (budget_tokens)

<!-- ORGANVM:AUTO:END -->


## ⚡ Conductor OS Integration
This repository is a managed component of the ORGANVM meta-workspace.
- **Orchestration:** Use `conductor patch` for system status and work queue.
- **Lifecycle:** Follow the `FRAME -> SHAPE -> BUILD -> PROVE` workflow.
- **Governance:** Promotions are managed via `conductor wip promote`.
- **Intelligence:** Conductor MCP tools are available for routing and mission synthesis.
