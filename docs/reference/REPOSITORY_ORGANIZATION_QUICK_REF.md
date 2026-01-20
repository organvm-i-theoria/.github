# Repository Organization Quick Reference

> **Quick reference for repository structure and file organization standards**

## 🎯 Quick Links

- 📖 [Full Standards Document](./REPOSITORY_STRUCTURE.md)
- ✅ [Validation Script](../../scripts/validate-repository-structure.sh)
- 🔧 [VERSION_CONTROL_STANDARDS.md](./VERSION_CONTROL_STANDARDS.md)
- 📝 [CONTRIBUTING.md](../../docs/governance/CONTRIBUTING.md)

---

## Essential File Checklist

### ✅ Required at Root
```
✓ README.md          # Repository overview
✓ LICENSE            # License terms
✓ .gitignore         # Ignore rules
```

### ⚠️ Recommended at Root
```
! CONTRIBUTING.md    # or docs/governance/CONTRIBUTING.md
! CODE_OF_CONDUCT.md # or docs/governance/CODE_OF_CONDUCT.md
! SECURITY.md        # or docs/governance/SECURITY.md
! CHANGELOG.md       # Version history
! VERSION            # Current version (if using semver)
```

---

## Standard Directory Structure

```
repository/
├── .github/              # GitHub config
│   ├── workflows/        # Actions
│   ├── ISSUE_TEMPLATE/   # Issue templates
│   └── CODEOWNERS        # Code owners
├── docs/                 # Documentation
│   ├── guides/           # How-tos
│   ├── reference/        # Technical docs
│   └── governance/       # Policies
├── src/                  # Source code
├── tests/                # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/              # Build/deploy scripts
├── reports/              # Generated reports
└── archive/              # Deprecated content
```

---

## File Naming Quick Rules

| Type | Convention | Examples |
|------|-----------|----------|
| **Main docs** | ALL_CAPS.md | README.md, CONTRIBUTING.md |
| **Guides** | kebab-case.md | getting-started.md, api-guide.md |
| **Code (TS/JS)** | camelCase / PascalCase | userService.ts, UserController.ts |
| **Code (Python)** | snake_case | user_service.py, data_processor.py |
| **Constants** | SCREAMING_SNAKE_CASE | MAX_RETRY_COUNT, API_URL |
| **Config** | kebab-case | .pre-commit-config.yaml |

---

## Common Anti-Patterns

### ❌ DON'T
```
repository/
├── STATUS_WEEK1.md           # Status files at root
├── DEPLOYMENT_NOTES.md       # Deployment logs at root
├── test-results-12345.json   # Test results at root
├── TEMP_FIX.md               # Temporary files at root
└── old_backup/               # Backup folders at root
```

### ✅ DO
```
repository/
├── README.md
├── docs/
│   └── reports/
│       ├── status-2025-01.md
│       └── deployment-phase1.md
├── reports/
│   └── test-results/
│       └── 2025-01-20.json
└── archive/
    └── old_backup/
```

---

## Quick Decision Tree

### Where should this file go?

```
Is it essential for repo discovery?
├─ YES → Root level (README.md, LICENSE)
└─ NO → Is it documentation?
    ├─ YES → docs/ subdirectory
    └─ NO → Is it a report/status?
        ├─ YES → reports/ or docs/reports/
        └─ NO → Is it source code?
            ├─ YES → src/ or language-specific dir
            └─ NO → Is it a test?
                ├─ YES → tests/
                └─ NO → Is it a build script?
                    ├─ YES → scripts/
                    └─ NO → Is it configuration?
                        ├─ YES → Root (dotfiles) or config/
                        └─ NO → Is it deprecated?
                            ├─ YES → archive/
                            └─ NO → Reconsider if needed!
```

---

## GitHub-Specific Structure

### `.github/` Directory
```
.github/
├── workflows/                    # GitHub Actions (REQUIRED)
│   ├── ci.yml
│   └── deploy.yml
├── ISSUE_TEMPLATE/               # Issue templates
│   ├── bug_report.yml
│   ├── feature_request.yml
│   └── config.yml
├── PULL_REQUEST_TEMPLATE.md      # Single PR template
│   or
├── PULL_REQUEST_TEMPLATE/        # Multiple PR templates
│   ├── default.md
│   └── hotfix.md
├── DISCUSSION_TEMPLATE/          # Discussion templates
├── CODEOWNERS                    # Code ownership
├── dependabot.yml                # Dependency updates
├── labels.yml                    # Label definitions
└── copilot-instructions.md       # AI instructions
```

---

## Documentation Structure

### `docs/` Directory
```
docs/
├── README.md                 # Documentation index
├── guides/                   # How-to guides
│   ├── getting-started.md
│   ├── installation.md
│   └── deployment.md
├── reference/                # Technical reference
│   ├── api-reference.md
│   └── configuration.md
├── architecture/             # Architecture docs
│   ├── overview.md
│   └── decisions/            # ADRs
├── governance/               # Policies
│   ├── SECURITY.md
│   ├── CODE_OF_CONDUCT.md
│   └── CONTRIBUTING.md
└── assets/                   # Images & diagrams
    ├── images/
    └── diagrams/
```

---

## Validation Commands

### Validate Repository Structure
```bash
# Run validation script
./scripts/validate-repository-structure.sh

# Check specific requirements
test -f README.md && echo "✓ README exists" || echo "✗ README missing"
test -f LICENSE && echo "✓ LICENSE exists" || echo "✗ LICENSE missing"
test -f .gitignore && echo "✓ .gitignore exists" || echo "✗ .gitignore missing"
```

### Common Cleanup Commands
```bash
# Move status files to reports
mkdir -p reports/status
mv *STATUS*.md reports/status/ 2>/dev/null || true

# Move monitoring files
mkdir -p reports/monitoring
mv MONITORING_*.md reports/monitoring/ 2>/dev/null || true

# Move deployment files
mkdir -p docs/deployment
mv DEPLOYMENT_*.md docs/deployment/ 2>/dev/null || true

# Move phase completion files
mkdir -p docs/reports
mv PHASE*_COMPLETE.md docs/reports/ 2>/dev/null || true
```

---

## Language-Specific Layouts

### Python
```
python-project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       └── module.py
├── tests/
├── pyproject.toml
└── requirements.txt
```

### Node.js
```
nodejs-project/
├── src/
├── tests/
├── package.json
├── package-lock.json
└── tsconfig.json
```

### Go
```
go-project/
├── cmd/
│   └── app/
│       └── main.go
├── pkg/
├── internal/
├── go.mod
└── go.sum
```

---

## .gitignore Essentials

```gitignore
# Dependencies
node_modules/
venv/
.venv/

# Build outputs
dist/
build/
target/
*.pyc
__pycache__/

# IDE
.vscode/
.idea/
*.swp

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Reports (keep templates only)
coverage/
reports/*.json
!reports/README.md

# Logs
*.log
logs/
```

---

## Pre-commit Configuration

Add structure validation to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-structure
        name: Validate Repository Structure
        entry: scripts/validate-repository-structure.sh
        language: system
        pass_filenames: false
```

---

## CI/CD Integration

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
        run: ./scripts/validate-repository-structure.sh
```

---

## Quick Tips

### 1. Keep Root Clean
- **Maximum 15 files** at root level
- Move reports to `reports/` or `docs/reports/`
- Archive old content in `archive/`

### 2. Use README Files
- Add README.md to every significant directory
- Explain purpose, structure, and usage
- Link to related documentation

### 3. Consistent Naming
- Choose one convention per file type
- Use kebab-case for multi-word files
- CAPS for important docs (README, LICENSE)

### 4. Automate Validation
- Run validation script in CI/CD
- Add pre-commit hooks
- Document violations in issues

### 5. Progressive Cleanup
- Don't reorganize everything at once
- Move files in batches
- Update references as you go
- Document changes in CHANGELOG

---

## Common Questions

**Q: Where do I put temporary analysis files?**  
A: Use `docs/reports/` or better yet, keep them local and gitignore them.

**Q: Should I commit build artifacts?**  
A: No. Add them to `.gitignore` and regenerate during CI/CD.

**Q: Where do weekly status updates go?**  
A: `reports/status/YYYY-MM-DD.md` or `docs/reports/status-YYYY-MM-DD.md`

**Q: Can I have multiple CONTRIBUTING.md files?**  
A: One at root OR one in `docs/governance/`. Link from README if elsewhere.

**Q: What about language-specific structure?**  
A: Follow community conventions (e.g., Go's `cmd/`, `pkg/`, `internal/`)

---

## Resources

- 📖 [Full Standards](./REPOSITORY_STRUCTURE.md)
- 🔧 [Validation Script](../../scripts/validate-repository-structure.sh)
- 📝 [Version Control Standards](./VERSION_CONTROL_STANDARDS.md)
- 🔒 [Security Best Practices](../SECURITY_BEST_PRACTICES.md)
- 🤝 [Contributing Guidelines](../governance/CONTRIBUTING.md)

---

**Need Help?**  
- Open an issue with label `question` or `documentation`
- Check [SUPPORT.md](../SUPPORT.md) for contact options
- Review [full standards document](./REPOSITORY_STRUCTURE.md)

---

*Last Updated: 2026-01-20 | Version: 1.0.0*
