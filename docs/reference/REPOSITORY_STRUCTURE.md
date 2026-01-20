# Repository Structure and Organization Standards

> **Organization-wide standards for repository folder structure, file naming, and content placement**

**Version**: 1.0.0  
**Last Updated**: 2026-01-20  
**Status**: ✅ Active Standard  

## Table of Contents

- [Overview](#overview)
- [Core Principles](#core-principles)
- [Directory Structure](#directory-structure)
- [File Naming Conventions](#file-naming-conventions)
- [Content Placement Guidelines](#content-placement-guidelines)
- [Special Directories](#special-directories)
- [Best Practices](#best-practices)
- [Anti-Patterns](#anti-patterns)
- [Enforcement](#enforcement)

---

## Overview

This document establishes organization-wide standards for repository structure, ensuring consistency, maintainability, and discoverability across all projects.

### Goals

1. **Consistency**: Predictable structure across all repositories
2. **Discoverability**: Easy to find files and understand organization
3. **Maintainability**: Clear separation of concerns
4. **Automation-friendly**: Structure supports tooling and CI/CD
5. **Scalability**: Accommodates growth without reorganization

### Scope

These standards apply to:
- All organization repositories
- New repository creation
- Repository migrations
- Documentation updates

---

## Core Principles

### 1. Separation of Concerns

Files should be organized by **purpose** and **audience**:
- Source code in `src/` or language-specific directories
- Documentation in `docs/`
- Configuration in `.github/` or root
- Build artifacts excluded via `.gitignore`

### 2. Hierarchical Organization

```
Repository Root
├── Core Files (README, LICENSE, etc.)
├── Configuration Files (dotfiles)
├── Source Directories (code, docs, tests)
└── Metadata Directories (.github, .config)
```

### 3. Progressive Disclosure

- Root level: Essential information for quick understanding
- First-level directories: Major functional areas
- Deeper levels: Detailed organization within areas

### 4. Convention Over Configuration

Use standard names that tools expect:
- `README.md` for repository overview
- `LICENSE` for licensing information
- `CONTRIBUTING.md` for contribution guidelines
- `.github/workflows/` for GitHub Actions

---

## Directory Structure

### Standard Repository Layout

```
repository-name/
├── .github/                    # GitHub-specific configurations
│   ├── workflows/              # GitHub Actions workflows
│   ├── ISSUE_TEMPLATE/         # Issue templates
│   ├── PULL_REQUEST_TEMPLATE/  # PR templates (can be single file)
│   ├── DISCUSSION_TEMPLATE/    # Discussion templates
│   ├── actions/                # Custom actions (optional)
│   ├── scripts/                # GitHub-specific scripts
│   ├── CODEOWNERS              # Code ownership rules
│   ├── dependabot.yml          # Dependabot configuration
│   ├── labels.yml              # Label definitions
│   └── copilot-instructions.md # Copilot custom instructions
│
├── .devcontainer/              # Development container configuration
│   ├── devcontainer.json       # Main config
│   └── Dockerfile              # Container definition (if custom)
│
├── .vscode/                    # VS Code settings (optional, can be .gitignored)
│   ├── settings.json           # Workspace settings
│   ├── extensions.json         # Recommended extensions
│   └── launch.json             # Debug configurations
│
├── docs/                       # Documentation
│   ├── README.md               # Documentation index
│   ├── guides/                 # User and developer guides
│   ├── api/                    # API documentation
│   ├── architecture/           # Architecture documentation
│   ├── reference/              # Reference documentation
│   ├── governance/             # Policies and governance
│   │   ├── SECURITY.md         # Security policy
│   │   ├── CODE_OF_CONDUCT.md  # Code of conduct
│   │   └── CONTRIBUTING.md     # Contribution guidelines
│   └── assets/                 # Images, diagrams, etc.
│
├── src/                        # Source code (language-specific alternatives below)
│   ├── main/                   # Main application code
│   ├── lib/                    # Libraries and utilities
│   └── config/                 # Application configuration
│
├── tests/                      # Test files
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── e2e/                    # End-to-end tests
│   └── fixtures/               # Test fixtures and data
│
├── scripts/                    # Build, deployment, and utility scripts
│   ├── build.sh                # Build scripts
│   ├── deploy.sh               # Deployment scripts
│   └── setup.sh                # Setup and initialization
│
├── config/                     # Application configuration files
│   ├── production/             # Production configs
│   ├── staging/                # Staging configs
│   └── development/            # Development configs
│
├── .schema-org/                # Schema.org structured data (if applicable)
│   ├── organization.json       # Organization schema
│   └── repository.json         # Repository schema
│
├── reports/                    # Generated reports and artifacts
│   ├── coverage/               # Test coverage reports
│   ├── audit/                  # Audit reports
│   └── performance/            # Performance reports
│
├── archive/                    # Archived/deprecated content
│   └── README.md               # Explanation of archived content
│
├── README.md                   # Repository overview (REQUIRED)
├── LICENSE                     # License file (REQUIRED)
├── CHANGELOG.md                # Version history
├── VERSION                     # Current version (if using semver)
├── .gitignore                  # Git ignore rules
├── .gitattributes              # Git attributes
└── package.json / pyproject.toml / etc. # Language-specific manifests
```

### Language-Specific Variations

#### Python Projects
```
python-project/
├── src/
│   └── package_name/           # Python package
│       ├── __init__.py
│       └── module.py
├── tests/
├── pyproject.toml              # Project metadata and dependencies
├── requirements.txt            # Alternative dependency specification
└── setup.py                    # Build script (if needed)
```

#### Node.js Projects
```
nodejs-project/
├── src/                        # Source TypeScript/JavaScript
├── dist/                       # Compiled output (gitignored)
├── tests/
├── package.json                # NPM package definition
├── package-lock.json           # Dependency lock file
└── tsconfig.json               # TypeScript configuration
```

#### Go Projects
```
go-project/
├── cmd/                        # Command-line applications
│   └── app-name/
│       └── main.go
├── pkg/                        # Public library code
├── internal/                   # Private application code
├── api/                        # API definitions (OpenAPI, gRPC)
├── go.mod                      # Go module definition
└── go.sum                      # Dependency checksums
```

#### Java/Maven Projects
```
java-project/
├── src/
│   ├── main/
│   │   ├── java/
│   │   └── resources/
│   └── test/
│       ├── java/
│       └── resources/
├── target/                     # Build output (gitignored)
└── pom.xml                     # Maven configuration
```

---

## File Naming Conventions

### General Rules

1. **Use descriptive names**: `user-authentication.md` not `doc1.md`
2. **Be consistent**: Choose one style and stick to it within a project
3. **Use appropriate case**:
   - **kebab-case** for URLs and multi-word files: `api-reference.md`
   - **PascalCase** for classes: `UserController.ts`
   - **camelCase** for variables/functions: `getUserById()`
   - **SCREAMING_SNAKE_CASE** for constants: `MAX_RETRY_COUNT`
   - **snake_case** for Python modules: `data_processor.py`

### Documentation Files

| File Type | Naming Convention | Example |
|-----------|------------------|---------|
| Main docs | ALL_CAPS.md | `README.md`, `CONTRIBUTING.md` |
| Guides | kebab-case.md | `getting-started.md` |
| Reference | kebab-case.md | `api-reference.md` |
| Architecture | CAPS or kebab-case | `ARCHITECTURE.md` or `system-design.md` |

### Special Files (Always ROOT Level)

| File | Purpose | Required |
|------|---------|----------|
| `README.md` | Repository overview | ✅ Yes |
| `LICENSE` | License terms | ✅ Yes |
| `CONTRIBUTING.md` | Contribution guide | ⚠️ Recommended |
| `CODE_OF_CONDUCT.md` | Community standards | ⚠️ Recommended |
| `SECURITY.md` | Security policy | ⚠️ Recommended |
| `CHANGELOG.md` | Version history | ⚠️ Recommended |
| `VERSION` | Current version | ⬜ Optional |
| `.gitignore` | Git ignore rules | ✅ Yes |

### Configuration Files

- **Dotfiles at root**: `.gitignore`, `.gitattributes`, `.editorconfig`
- **Hidden directories for tools**: `.github/`, `.vscode/`, `.devcontainer/`
- **Language configs at root**: `package.json`, `pyproject.toml`, `go.mod`

### Status and Report Files

❌ **AVOID at root**:
- `STATUS_*.md`
- `REPORT_*.md`
- `*_COMPLETE.md`
- `MONITORING_*.md`

✅ **USE instead**:
- `docs/reports/status-YYYY-MM-DD.md`
- `reports/monitoring/week-11.md`
- `docs/deployment/phase-1-complete.md`

---

## Content Placement Guidelines

### Root Directory

**ONLY include**:
- Essential discovery files (README, LICENSE)
- Critical policies (SECURITY, CODE_OF_CONDUCT, CONTRIBUTING)
- Language/tool manifests (package.json, Cargo.toml)
- Essential configuration (dotfiles)
- Version/changelog files (VERSION, CHANGELOG.md)

**NEVER include**:
- Temporary files
- Build artifacts
- Development notes
- Detailed documentation (use `docs/`)
- Status reports (use `reports/` or `docs/reports/`)

### Documentation Directory (`docs/`)

```
docs/
├── README.md                   # Documentation index/guide
├── guides/                     # How-to guides and tutorials
│   ├── getting-started.md
│   ├── installation.md
│   └── deployment.md
├── reference/                  # Technical reference
│   ├── api.md
│   └── configuration.md
├── architecture/               # System design and architecture
│   ├── overview.md
│   └── decisions/              # Architecture Decision Records (ADRs)
├── governance/                 # Policies and procedures
│   ├── SECURITY.md
│   ├── CODE_OF_CONDUCT.md
│   └── CONTRIBUTING.md
└── assets/                     # Images, diagrams
    ├── images/
    └── diagrams/
```

### GitHub Directory (`.github/`)

```
.github/
├── workflows/                  # GitHub Actions workflows
│   ├── ci.yml
│   ├── cd.yml
│   └── security.yml
├── ISSUE_TEMPLATE/             # Issue templates
│   ├── bug_report.yml
│   ├── feature_request.yml
│   └── config.yml
├── PULL_REQUEST_TEMPLATE.md    # PR template (single file at this level)
│   or
├── PULL_REQUEST_TEMPLATE/      # Multiple PR templates (directory)
│   ├── default.md
│   └── hotfix.md
├── actions/                    # Custom composite actions
│   └── custom-action/
│       └── action.yml
├── scripts/                    # GitHub-specific utility scripts
├── CODEOWNERS                  # Code ownership
├── dependabot.yml              # Dependency updates
└── copilot-instructions.md     # AI assistant instructions
```

### Test Directory (`tests/`)

```
tests/
├── unit/                       # Unit tests
│   └── test_module.py
├── integration/                # Integration tests
│   └── test_api.py
├── e2e/                        # End-to-end tests
│   └── test_workflow.py
├── fixtures/                   # Test data
│   └── sample_data.json
├── conftest.py                 # Pytest configuration (Python)
└── README.md                   # Testing documentation
```

---

## Special Directories

### Archive Directory

**Purpose**: Store deprecated or historical content that might be referenced later

```
archive/
├── README.md                   # Explains what's archived and why
├── deprecated-feature/         # Old features
└── old-docs/                   # Superseded documentation
```

**Guidelines**:
- Always include README explaining archive purpose
- Include date of archival
- Link to replacements if applicable
- Consider deleting after defined retention period

### Reports Directory

**Purpose**: Store generated reports, metrics, and automated output

```
reports/
├── README.md                   # Report index and retention policy
├── coverage/                   # Test coverage reports
├── security/                   # Security scan results
├── performance/                # Performance metrics
└── audit/                      # Compliance audits
```

**Guidelines**:
- Typically gitignored (except samples)
- Include retention policy in README
- Automate cleanup with scripts or CI
- Store historical reports if needed for compliance

### Scripts Directory

**Purpose**: Utility scripts for build, deployment, and maintenance

```
scripts/
├── README.md                   # Script documentation
├── build/                      # Build scripts
├── deploy/                     # Deployment scripts
├── setup/                      # Environment setup
└── utils/                      # Utility scripts
```

**Guidelines**:
- Make scripts executable: `chmod +x script.sh`
- Include usage documentation in script headers
- Use consistent naming: `verb-noun.sh` (e.g., `deploy-production.sh`)
- Add README with script inventory

---

## Best Practices

### 1. Keep Root Clean

✅ **DO**:
```
repository/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── .gitignore
├── package.json
├── docs/
└── src/
```

❌ **DON'T**:
```
repository/
├── README.md
├── STATUS_UPDATE_JAN.md
├── DEPLOYMENT_NOTES_V2.md
├── TEMP_FIX.md
├── old_version_backup/
├── test_results_12345.json
└── ... (50+ files at root)
```

### 2. Use README Files as Guides

Place `README.md` in every significant directory to explain:
- Purpose of the directory
- Structure and organization
- How to use the contents
- Links to related resources

### 3. Separate Source from Configuration

```
✅ Good:
project/
├── src/              # Application code
├── config/           # Configuration files
└── .env.example      # Environment template

❌ Bad:
project/
├── src/
│   ├── config.json   # Mixed with code
│   └── app.js
```

### 4. Version Everything Important

- Use `VERSION` file or manifest for version tracking
- Tag releases with semantic versions
- Maintain `CHANGELOG.md` for user-facing changes
- Link documentation to specific versions

### 5. Document Structure Changes

When reorganizing:
1. Create migration guide in `docs/migration/`
2. Update all documentation with new paths
3. Add redirects or notes in old locations
4. Announce changes in CHANGELOG

### 6. Automate Validation

Create validation scripts:
```bash
# scripts/validate-structure.sh
#!/bin/bash
# Validates repository structure against standards

# Check required files
for file in README.md LICENSE .gitignore; do
  if [ ! -f "$file" ]; then
    echo "ERROR: Required file missing: $file"
    exit 1
  fi
done

# Check directory structure
for dir in docs tests; do
  if [ ! -d "$dir" ]; then
    echo "WARNING: Recommended directory missing: $dir"
  fi
done

echo "Structure validation passed!"
```

---

## Anti-Patterns

### ❌ Root Directory Clutter

**Problem**: Too many files at root level  
**Solution**: Move to appropriate subdirectories

```
❌ Bad:
├── README.md
├── STATUS_WEEK1.md
├── STATUS_WEEK2.md
├── DEPLOYMENT_LOG.md
├── MEETING_NOTES.md
├── TEMP_ANALYSIS.md
└── ... (30+ markdown files)

✅ Good:
├── README.md
└── docs/
    ├── reports/
    │   ├── status-2025-01.md
    │   └── status-2025-02.md
    └── meetings/
        └── 2025-01-15-planning.md
```

### ❌ Mixed Concerns

**Problem**: Mixing source, docs, configs in same directory  
**Solution**: Clear separation

```
❌ Bad:
src/
├── app.js
├── README.md
├── app.test.js
├── config.json
└── deployment-guide.md

✅ Good:
src/
└── app.js
tests/
└── app.test.js
docs/
└── deployment-guide.md
config/
└── app.json
```

### ❌ Deep Nesting

**Problem**: Too many levels of directories  
**Solution**: Flatten when possible

```
❌ Bad:
docs/guides/user/getting-started/installation/prerequisites/system-requirements.md

✅ Good:
docs/guides/installation-prerequisites.md
```

### ❌ Inconsistent Naming

**Problem**: Mixed naming conventions  
**Solution**: Choose one and stick to it

```
❌ Bad:
docs/
├── Getting_Started.md
├── api-reference.md
├── SystemDesign.md
└── troubleshooting guide.md

✅ Good:
docs/
├── getting-started.md
├── api-reference.md
├── system-design.md
└── troubleshooting-guide.md
```

### ❌ Version Control Artifacts

**Problem**: Committing generated or temporary files  
**Solution**: Use comprehensive .gitignore

```
❌ Bad:
git status:
  node_modules/
  .env
  dist/
  coverage/
  .DS_Store
  *.log

✅ Good:
.gitignore:
  node_modules/
  .env
  dist/
  coverage/
  .DS_Store
  *.log
```

---

## Enforcement

### Pre-commit Validation

Add structure validation to pre-commit hooks:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-structure
        name: Validate Repository Structure
        entry: scripts/validate-structure.sh
        language: system
        pass_filenames: false
```

### CI/CD Checks

```yaml
# .github/workflows/structure-validation.yml
name: Structure Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate structure
        run: ./scripts/validate-structure.sh
```

### Documentation Updates

When structure changes:
1. Update this document
2. Update repository README
3. Update CONTRIBUTING.md
4. Create migration guide if needed
5. Announce in CHANGELOG

---

## References

- [GitHub Community Health Files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions)
- [Conventional Repository Structure](https://github.com/golang-standards/project-layout)
- [The Twelve-Factor App](https://12factor.net/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-20 | Initial comprehensive standards document |

---

**Questions or Feedback?**  
Open an issue or discussion in the repository to suggest improvements to these standards.
