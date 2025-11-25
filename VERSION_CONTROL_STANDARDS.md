# Version Control Standards

Organization-wide standards for version control, branching, tagging, and release management.

## Table of Contents

- [Semantic Versioning](#semantic-versioning)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Git History as Version Trail](#git-history-as-version-trail)
- [Tag Standards](#tag-standards)
- [Branch Types](#branch-types)
- [Commit Guidelines](#commit-guidelines)
- [Integration with Existing Standards](#integration-with-existing-standards)

---

## Semantic Versioning

### Version Format

All releases MUST follow semantic versioning: **MAJOR.MINOR.PATCH**

```
v1.0.0
v1.0.1
v1.1.0
v2.0.0
```

### Version Increment Rules

| Change Type | Version Component | Example | When to Use |
|-------------|------------------|---------|-------------|
| Breaking Changes | MAJOR | v1.0.0 → v2.0.0 | API changes, removed features, incompatible changes |
| New Features | MINOR | v1.0.0 → v1.1.0 | New functionality, backward-compatible additions |
| Bug Fixes | PATCH | v1.0.0 → v1.0.1 | Bug fixes, security patches, backward-compatible fixes |

### Pre-release Versions

For development and testing phases:

```
v1.0.0-alpha.1
v1.0.0-beta.1
v1.0.0-rc.1
v1.0.0
```

See [SEMANTIC_VERSIONING.md](SEMANTIC_VERSIONING.md) for detailed guidelines.

---

## Branch Naming Conventions

### Standard Format

Branches MUST follow a hierarchical naming structure that visually represents development order and product lifecycle:

```
<lifecycle-phase>/<feature-type>/<component>/<subcomponent>
```

### Lifecycle Phases

Primary branch prefixes indicate the product lifecycle phase:

- `develop/` - Active development features
- `experimental/` - Proof-of-concept and experimentation
- `production/` - Production-ready features
- `maintenance/` - Maintenance and support
- `deprecated/` - Features being phased out
- `archive/` - Historical reference branches

### Feature Types (Second Level)

- `feature/` - New feature development
- `bugfix/` - Non-critical bug fixes
- `hotfix/` - Critical production fixes
- `enhancement/` - Improvements to existing features
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions or improvements
- `chore/` - Maintenance tasks

### Examples

```bash
# Active development of a new user interface feature
develop/feature/user-interface/authentication-flow

# Production feature for payment system
production/feature/payment-gateway/stripe-integration

# Experimental AI feature with multiple components
experimental/feature/ai-assistant/natural-language-processing

# Maintenance work on legacy API
maintenance/bugfix/api-v1/rate-limiting

# Documentation for a specific component
develop/docs/deployment-guide/kubernetes-setup

# Archive of old version
archive/v1/feature/legacy-authentication
```

### Multi-Component Features

For complex features spanning multiple components:

```bash
develop/feature/dashboard-redesign/frontend
develop/feature/dashboard-redesign/backend
develop/feature/dashboard-redesign/api

# Or with deeper hierarchy
production/feature/payment-system/checkout/ui-components
production/feature/payment-system/checkout/validation-logic
```

### Branch Naming Rules

1. Use lowercase letters only
2. Use hyphens (not underscores or spaces) to separate words
3. Be descriptive but concise
4. Maximum 4 levels deep in hierarchy
5. Avoid generic names like "fix" or "update"
6. Include ticket/issue numbers when applicable: `develop/feature/AUTH-123-oauth-integration`

### Legacy Branch Names

**AVOID** version-numbered branches like `v2`, `v3` as primary development branches. Instead:

```bash
# Instead of:
v2
v3-rewrite

# Use:
develop/feature/api-v2/endpoints
experimental/feature/architecture-v3/microservices
```

---

## Git History as Version Trail

### Principle

Git commit history serves as the **detailed version trail** of the project. Each commit represents a point in the project's evolution.

### Guidelines

1. **Commit Frequently**: Small, atomic commits create a clear trail
2. **Descriptive Messages**: Each commit message should explain what and why
3. **Conventional Commits**: Follow conventional commit format for automation
4. **Never Rewrite Public History**: Preserve the integrity of the version trail
5. **Tag Releases**: Use annotated tags for all releases

### Viewing Version History

```bash
# View commit history
git log --oneline --graph --all --decorate

# View history for specific file
git log --follow -- path/to/file

# View changes between versions
git log v1.0.0..v2.0.0

# Find when a bug was introduced
git bisect start
```

### Commit Message as Documentation

Each commit message becomes part of the version documentation:

```bash
# Good commit messages become version trail entries
git commit -m "feat(auth): add OAuth2 authentication flow

Implements OAuth2 authentication with support for Google and GitHub
providers. This enables users to sign in with their existing accounts.

Closes #123"
```

---

## Tag Standards

### Release Tags

All releases MUST be tagged with annotated tags following semantic versioning:

```bash
# Create annotated release tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag to remote
git push origin v1.0.0

# Push all tags
git push origin --tags
```

### Tag Format

```
v<MAJOR>.<MINOR>.<PATCH>[-<pre-release>]

Examples:
v1.0.0
v1.0.1
v1.1.0
v2.0.0
v1.0.0-alpha.1
v1.0.0-beta.1
v1.0.0-rc.1
```

### Tag Guidelines

1. **Always Use Annotated Tags**: Include message with release information
2. **Never Delete Published Tags**: Tags are permanent version markers
3. **Tag on Main Branch**: Production releases tagged on main/master only
4. **Pre-release Tags**: Use for alpha, beta, and RC versions on appropriate branches
5. **Include Changelog**: Reference or include changelog in tag message

### Tag Message Template

```bash
git tag -a v1.2.0 -m "Release v1.2.0

Features:
- Added user authentication system
- Implemented dashboard redesign
- Added export functionality

Bug Fixes:
- Fixed memory leak in data processor
- Resolved login timeout issue

Breaking Changes:
- API endpoint /users now requires authentication

See CHANGELOG.md for full details."
```

---

## Branch Types

### Main Branches

#### `main` (or `master`)
- **Purpose**: Production-ready code
- **Lifetime**: Permanent
- **Protection**: Highest level
- **Tagging**: All production releases tagged here
- **Deployment**: Auto-deploys to production

#### `develop`
- **Purpose**: Integration branch for active development
- **Lifetime**: Permanent
- **Protection**: High level
- **Deployment**: Auto-deploys to staging
- **Source for**: Feature branches

### Supporting Branches

#### Feature Branches (`<lifecycle>/feature/<name>`)
- **Purpose**: New features and enhancements
- **Created from**: `develop`
- **Merged to**: `develop`
- **Lifetime**: Temporary (delete after merge)
- **Naming**: `develop/feature/component-name`

#### Hotfix Branches (`production/hotfix/<name>`)
- **Purpose**: Critical production fixes
- **Created from**: `main`
- **Merged to**: Both `main` and `develop`
- **Lifetime**: Temporary (delete after merge)
- **Naming**: `production/hotfix/critical-security-fix`

#### Release Branches (`release/v<version>`)
- **Purpose**: Release preparation and stabilization
- **Created from**: `develop`
- **Merged to**: Both `main` and `develop`
- **Lifetime**: Temporary (delete after release)
- **Naming**: `release/v1.2.0`

### Long-Lived Maintenance Branches

For supporting older versions:

```bash
# Maintenance branches for specific versions
maintenance/v1-maintenance
maintenance/v2-maintenance

# Or with more detail
maintenance/v1.x/security-patches
maintenance/v2.x/bug-fixes
```

**Purpose**: Provide bug fixes and security patches for older major versions

**Guidelines**:
1. Create when a new major version is released
2. Only accept critical bug fixes and security patches
3. Never add new features
4. Tag patch releases: v1.2.3, v1.2.4, etc.

### Archive Branches

For historical reference:

```bash
# Archive old development branches
archive/v1/original-implementation
archive/legacy/old-authentication-system
archive/experimental/failed-ml-approach

# Archive completed project phases
archive/phase1/initial-mvp
archive/phase2/feature-expansion
```

**Purpose**: Preserve historical development without cluttering active branches

**Guidelines**:
1. Move old work that's no longer actively maintained
2. Never delete - keep for historical reference
3. Clearly mark in branch name
4. Document reason for archival in README or commit message

---

## Commit Guidelines

All commits MUST follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

- `feat`: New feature (MINOR version bump)
- `fix`: Bug fix (PATCH version bump)
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test changes
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks
- `revert`: Revert previous commit

### Breaking Changes

Mark breaking changes with `!` or `BREAKING CHANGE:` footer (MAJOR version bump):

```bash
feat!: redesign API authentication

BREAKING CHANGE: Authentication now requires OAuth2 tokens
instead of API keys. All clients must migrate.
```

See [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for detailed commit guidelines.

---

## Integration with Existing Standards

This document consolidates and extends the following existing standards:

- **[SEMANTIC_VERSIONING.md](SEMANTIC_VERSIONING.md)**: Detailed versioning and automated release information
- **[GIT_WORKFLOW.md](GIT_WORKFLOW.md)**: Comprehensive Git workflow and branching strategies
- **[CHANGELOG.md](CHANGELOG.md)**: Automated changelog generation and maintenance
- **[BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md)**: Branch protection rules and enforcement

### Key Differences from Existing Docs

1. **Branch Naming**: Introduces lifecycle-phase prefix system for visual ordering
2. **Archive Strategy**: Formalizes archive branch naming and usage
3. **Maintenance Branches**: Defines long-lived maintenance branch strategy
4. **History as Trail**: Emphasizes Git history as primary version documentation

### Migration Path

**For Existing Repositories**:

1. Continue using current main/develop branches
2. Adopt new naming convention for new feature branches
3. Create maintenance branches when releasing new major versions
4. Archive old branches following new naming conventions
5. Update branch protection rules to recognize new patterns

**For New Repositories**:

1. Start with main and develop branches
2. Use lifecycle-phase naming from day one
3. Set up automated tagging and changelog generation
4. Configure branch protection rules

---

## Quick Reference

### Creating a New Feature

```bash
# Update develop
git checkout develop
git pull origin develop

# Create feature branch with lifecycle phase
git checkout -b develop/feature/user-profile/avatar-upload

# Work and commit
git add .
git commit -m "feat(profile): add avatar upload functionality"

# Push and create PR
git push -u origin develop/feature/user-profile/avatar-upload
```

### Creating a Release

```bash
# Create release branch
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# Prepare release (version bumps, changelog updates)
# Make final adjustments

# Merge to main
git checkout main
git merge --no-ff release/v1.2.0

# Tag release
git tag -a v1.2.0 -m "Release version 1.2.0"

# Push
git push origin main --tags

# Merge back to develop
git checkout develop
git merge --no-ff release/v1.2.0
git push origin develop

# Delete release branch
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

### Creating Maintenance Branch

```bash
# When releasing v2.0.0, create maintenance branch for v1.x
git checkout v1.9.0  # Last v1 release
git checkout -b maintenance/v1-maintenance
git push -u origin maintenance/v1-maintenance

# Apply security patches to v1.x
git checkout maintenance/v1-maintenance
git checkout -b maintenance/v1.x/security-patch-openssl
# Make fixes
git commit -m "fix(security): update OpenSSL dependency"
# Merge and tag v1.9.1
```

### Archiving Old Branch

```bash
# Rename to archive
git branch -m old-feature-branch archive/v1/old-feature-implementation
git push origin archive/v1/old-feature-implementation

# Or create new archive branch
git checkout old-feature-branch
git checkout -b archive/experimental/ml-approach-2023
git push -u origin archive/experimental/ml-approach-2023

# Delete old branch
git push origin --delete old-feature-branch
```

---

## Enforcement

These standards are enforced through:

1. **Branch Protection Rules**: Configured in repository settings
2. **GitHub Actions**: Automated validation of branch names and commit messages
3. **PR Templates**: Require adherence to conventions
4. **Code Review**: Manual verification during review process
5. **Pre-commit Hooks**: Local validation before commits

---

## Related Documentation

- [SEMANTIC_VERSIONING.md](SEMANTIC_VERSIONING.md) - Detailed semantic versioning guide
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md) - Complete Git workflow documentation
- [CHANGELOG.md](CHANGELOG.md) - Changelog format and maintenance
- [RELEASE_PROCESS.md](RELEASE_PROCESS.md) - Release creation and management
- [BRANCH_STRATEGY.md](BRANCH_STRATEGY.md) - Comprehensive branching strategies
- [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md) - Branch protection configuration

---

**Last Updated**: 2025-11-25
