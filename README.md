# ivviiviivvi Organization Policies

This repository contains community health files and organization-wide policies for the ivviiviivvi GitHub organization.

## 📚 Documentation

### Core Policies

- **[SECURITY.md](SECURITY.md)** - Security vulnerability reporting and response procedures
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributing to our projects
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community standards and enforcement (Contributor Covenant 2.1)
- **[SUPPORT.md](SUPPORT.md)** - How to get help and support resources
- **[GOVERNANCE_ANALYSIS.md](GOVERNANCE_ANALYSIS.md)** - Governance framework and decision-making processes

### Technical Documentation

- **[docs/TEAM_STRUCTURE.md](docs/TEAM_STRUCTURE.md)** - Team organization, permissions, and CODEOWNERS
- **[docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md)** - Branch protection rules and workflows

### Templates

#### Issue Templates (`.github/ISSUE_TEMPLATE/`)
- `bug_report.yml` - Bug report template
- `feature_request.yml` - Feature request template
- `security_vulnerability.yml` - Security vulnerability template
- `task.yml` - Task/work item template
- `documentation.yml` - Documentation request template
- `config.yml` - Issue template configuration

#### Discussion Templates (`.github/DISCUSSION_TEMPLATE/`)
- `announcements.yml` - Official announcements
- `ideas.yml` - Feature ideas and suggestions
- `q-and-a.yml` - Q&A discussions
- `show-and-tell.yml` - Community showcases
- `general.yml` - General discussions

#### Pull Request Template
- **[PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)** - PR checklist and guidelines

### Configuration Files

- **[CODEOWNERS](.github/CODEOWNERS)** - Code ownership by team
- **[dependabot.yml](.github/dependabot.yml)** - Automated dependency updates (7 ecosystems)
- **[labels.yml](.github/labels.yml)** - Standardized label definitions
- **[.pre-commit-config.yaml](.pre-commit-config.yaml)** - Pre-commit hook configuration

## 🔄 Workflows

Automated GitHub Actions workflows in `.github/workflows/`:

- **ci.yml** - Comprehensive CI pipeline (lint, test, security)
- **security-scan.yml** - Secret and vulnerability scanning
- **stale.yml** - Stale issue and PR management
- **welcome.yml** - Welcome new contributors
- **label-sync.yml** - Synchronize labels across repositories

## 🏗️ Repository Structure

```
.github/
├── ISSUE_TEMPLATE/           # Issue templates
│   ├── bug_report.yml
│   ├── feature_request.yml
│   ├── security_vulnerability.yml
│   ├── task.yml
│   ├── documentation.yml
│   └── config.yml
├── DISCUSSION_TEMPLATE/      # Discussion templates
│   ├── announcements.yml
│   ├── ideas.yml
│   ├── q-and-a.yml
│   ├── show-and-tell.yml
│   └── general.yml
├── workflows/                # GitHub Actions workflows
│   ├── ci.yml
│   ├── security-scan.yml
│   ├── stale.yml
│   ├── welcome.yml
│   └── label-sync.yml
├── CODEOWNERS                # Code ownership
├── dependabot.yml            # Dependency updates
├── labels.yml                # Label configuration
└── PULL_REQUEST_TEMPLATE.md  # PR template
├── SECURITY.md               # Security policy
├── CONTRIBUTING.md           # Contribution guidelines
├── CODE_OF_CONDUCT.md        # Community standards
├── SUPPORT.md                # Support resources
├── GOVERNANCE_ANALYSIS.md    # Governance framework
├── README.md                 # This file
├── .pre-commit-config.yaml   # Pre-commit hooks
└── docs/                     # Additional documentation
    ├── TEAM_STRUCTURE.md     # Team organization
    └── BRANCH_PROTECTION.md  # Branch protection rules
```

## 🚀 Quick Start

### For Contributors

1. **Read the docs**: Start with [CONTRIBUTING.md](CONTRIBUTING.md)
2. **Set up your environment**: Follow development setup instructions
3. **Install pre-commit hooks**: `pip install pre-commit && pre-commit install`
4. **Create a branch**: `git checkout -b feature/your-feature`
5. **Make changes**: Follow our code style guidelines
6. **Submit a PR**: Use the PR template

### For Maintainers

1. **Review policies**: Familiarize yourself with [GOVERNANCE_ANALYSIS.md](GOVERNANCE_ANALYSIS.md)
2. **Set up teams**: Follow [docs/TEAM_STRUCTURE.md](docs/TEAM_STRUCTURE.md)
3. **Apply branch protection**: See [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md)
4. **Sync labels**: Run label sync workflow or use `scripts/sync_labels_gh.sh`

## 🔒 Security

**Found a security vulnerability?**

**DO NOT create a public issue.** Follow our [Security Policy](SECURITY.md) to report privately:

- Email: security@ivviiviivvi.com
- GitHub Security Advisory: [Create Advisory](https://github.com/ivviiviivvi/.github/security/advisories/new)

**Response Timeline:**
- 24 hours: Acknowledgment
- 72 hours: Initial assessment
- 7 days: Detailed response
- 30 days: Fix deployed (critical issues)

## 🤝 Community

### Getting Help

- **Questions**: [GitHub Discussions](https://github.com/ivviiviivvi/.github/discussions)
- **Documentation**: [docs/](docs/)
- **Support**: [SUPPORT.md](SUPPORT.md)
- **Email**: support@ivviiviivvi.com

### Contributing

We welcome contributions from the community! Please see:

- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community standards
- [Good First Issues](https://github.com/search?q=org%3Aivviiviivvi+label%3A%22good+first+issue%22+state%3Aopen&type=issues)

### Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

Report violations to: conduct@ivviiviivvi.com

## 📊 Labels

We use a standardized label system across all repositories:

**Priority:** critical, high, medium, low  
**Type:** bug, enhancement, documentation, security, task, question  
**Status:** triage, in-progress, blocked, needs-review, approved  
**Category:** github-actions, configuration, dependencies, automated

See [labels.yml](.github/labels.yml) for complete definitions.

## 🔄 Automation

### Dependabot

Automated dependency updates configured for:
- GitHub Actions (weekly, Monday 9am)
- pip/Python (weekly, Monday 9am)
- npm/Node.js (weekly, Monday 9am)
- Docker (weekly, Monday 9am)
- Go modules (weekly, Monday 9am)
- Terraform (weekly, Monday 9am)

### Stale Management

- Issues/PRs marked stale after 60 days of inactivity
- Closed 14 days after being marked stale
- Exemptions: security, priority: critical/high, pinned

### Label Sync

- Syncs labels from `.github/labels.yml`
- Runs on push to main and weekly
- Ensures consistency across all repositories

## 📝 License

Organization policies and documentation are available under the [MIT License](LICENSE).

Individual repositories may use different licenses - check each repository's LICENSE file.

## 📞 Contact

- **General**: info@ivviiviivvi.com
- **Security**: security@ivviiviivvi.com
- **Support**: support@ivviiviivvi.com
- **Governance**: governance@ivviiviivvi.com
- **Conduct**: conduct@ivviiviivvi.com

---

**Last Updated**: January 12, 2026  
**Maintained by**: @ivviiviivvi/leadership
