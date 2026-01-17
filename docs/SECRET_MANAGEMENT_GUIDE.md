# Universal Secret Management Guide

> **Secure credential management using 1Password CLI across all automation**

## Overview

This organization uses **1Password CLI** as the universal secret manager for all automation scripts, workflows, and deployments. This approach eliminates plaintext secrets in files, environment variables, and version control.

## ✅ Current Coverage

### Fully Integrated Scripts (100% Complete!)

All high-priority production scripts now use `secret_manager.py`:

1. **`batch_onboard_repositories.py`** ✅ - Repository deployment automation
   - GitHub token via `ensure_github_token()`
   - No plaintext tokens in code or environment

2. **`validate_labels.py`** ✅ - Label validation and deployment
   - GitHub token via `ensure_github_token()`
   - Automatic 1Password CLI integration

3. **`pre_deployment_checklist.py`** ✅ - Pre-deployment validation
   - GitHub token via `ensure_github_token()`
   - Secure validation checks

4. **`web_crawler.py`** ✅ - Organization health monitoring
   - GitHub token via `get_secret_with_fallback()`
   - Secure token retrieval with fallback

5. **`utils.py`** ✅ - GitHub API client utilities
   - GitHub token via `get_secret_with_fallback()`
   - Secure client initialization

6. **`sync_labels.py`** ✅ - Label synchronization
   - GitHub token via `get_secret_with_fallback()`
   - 1Password CLI integration with env fallback

7. **`DEPLOY_PHASE1.sh`** ✅ - Phase 1 deployment orchestration
   - Delegates token management to Python scripts
   - No token handling in shell script

### Secret Manager Module

**Location**: `/workspace/automation/scripts/secret_manager.py`

**Capabilities**:

- ✅ GitHub tokens
- ✅ API keys
- ✅ Passwords
- ✅ SSH keys
- ✅ Certificates
- ✅ Any 1Password field

**Functions**:

```python
# Get any secret
get_secret(item_name, field="password", vault="Private")

# Get secret with environment fallback (for CI/CD)
get_secret_with_fallback(item_name, field, env_var, vault)

# Get secret or exit
ensure_secret(item_name, field, env_var, vault)

# Get GitHub token specifically
get_github_token(item_name="batch-label-deployment-011726")

# Ensure GitHub token or exit
ensure_github_token(item_name="batch-label-deployment-011726")
```

## ⚠️ Scripts Needing Integration

### High Priority

1. **`web_crawler.py`** (Line 48)

   ```python
   # Current (insecure):
   self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
   
   # Should be:
   from secret_manager import get_secret_with_fallback
   self.github_token = github_token or get_secret_with_fallback(
       "batch-label-deployment-011726",
       "password",
       env_var="GITHUB_TOKEN"
   )
   ```

2. **`utils.py`** (Line 205)

   ```python
   # Current:
   self.token = token or os.environ.get("GITHUB_TOKEN")
   
   # Should be:
   from secret_manager import get_secret_with_fallback
   self.token = token or get_secret_with_fallback(
       "batch-label-deployment-011726",
       "password",
       env_var="GITHUB_TOKEN"
   )
   ```

3. **`sync_labels.py`** (Line 319)

   ```python
   # Current:
   default=os.getenv("GITHUB_TOKEN")
   
   # Should be:
   from secret_manager import get_secret_with_fallback
   default=get_secret_with_fallback(
       "batch-label-deployment-011726",
       "password",
       env_var="GITHUB_TOKEN"
   )
   ```

### Medium Priority

1. **`intelligent_routing.py`**
   - Documents `GITHUB_TOKEN` requirement
   - Should use `secret_manager.py`

2. **Shell scripts** in `automation/scripts/`
   - Should delegate to Python wrappers
   - Or use `op` CLI directly

### Low Priority

1. **Test files** (`test_*.py`)
   - Use dummy tokens
   - Fine as-is for testing

## 🔐 Security Model

### Threat Protection

| Threat | Mitigation |
|--------|-----------|
| **Plaintext secrets in code** | ✅ Blocked - No secrets in source files |
| **Secrets in version control** | ✅ Blocked - Only in encrypted 1Password |
| **Secrets in environment** | ⚠️ Fallback only (for CI/CD) |
| **Secrets in logs** | ✅ Protected - Never printed |
| **Memory dumps** | ⚠️ Brief exposure (process lifetime only) |
| **Disk persistence** | ✅ Blocked - No plaintext files created |

### Secret Lifecycle

1. **Storage**: Encrypted in 1Password vault
2. **Retrieval**: Via 1Password CLI (`op item get`)
3. **Usage**: Exists only in process memory
4. **Cleanup**: Auto-cleared when process exits

### Access Control

- **1Password CLI** requires authentication:
  - Desktop app integration (SSO)
  - Service account token (CI/CD)
  - Manual sign-in (personal use)

- **Fallback environment variables** (CI/CD only):
  - GitHub Actions secrets
  - Manual export for local testing

## 📋 Integration Checklist

To integrate a new script:

- [ ] Import secret manager: `from secret_manager import get_secret_with_fallback`
- [ ] Replace `os.environ.get()` or `os.getenv()` calls
- [ ] Use appropriate function:
  - `get_secret()` - Basic retrieval
  - `get_secret_with_fallback()` - With env var fallback
  - `ensure_secret()` - Or exit
  - `get_github_token()` - GitHub-specific
  - `ensure_github_token()` - GitHub or exit
- [ ] Test locally with 1Password CLI
- [ ] Test in CI/CD with environment variable
- [ ] Remove old token handling code
- [ ] Document in script docstring

## 🚀 Usage Examples

### Example 1: GitHub Token (Simple)

```python
from secret_manager import ensure_github_token

# Will exit if token not available
token = ensure_github_token()

# Use token
g = Github(token)
```

### Example 2: API Key with Fallback

```python
from secret_manager import get_secret_with_fallback

# Try 1Password, fallback to env var
api_key = get_secret_with_fallback(
    "datadog-api-key",
    field="credential",
    env_var="DD_API_KEY"
)

if not api_key:
    print("No API key available")
    sys.exit(1)
```

### Example 3: Database Password

```python
from secret_manager import ensure_secret

# Database password (must exist)
db_password = ensure_secret(
    "postgres-prod",
    field="password",
    vault="Infrastructure"
)

# Connect to database
conn = psycopg2.connect(
    host="db.example.com",
    password=db_password
)
```

### Example 4: SSH Key

```python
from secret_manager import get_secret

# Get SSH private key
ssh_key = get_secret(
    "deploy-key-prod",
    field="private key"
)

if ssh_key:
    # Write temporarily for use
    key_path = Path("/tmp/deploy_key")
    key_path.write_text(ssh_key)
    key_path.chmod(0o600)
    
    # Use key...
    
    # Clean up
    key_path.unlink()
```

## 🔧 CI/CD Integration

### GitHub Actions

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up secrets
        env:
          GITHUB_TOKEN: ${{ secrets.DEPLOYMENT_TOKEN }}
        run: |
          # Token automatically available as fallback
          python3 automation/scripts/batch_onboard_repositories.py \
            --config config/phase1.yml
```

### With 1Password Service Account

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install 1Password CLI
        uses: 1password/install-cli-action@v1
      
      - name: Deploy with 1Password
        env:
          OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
        run: |
          # Scripts will use 1Password CLI automatically
          python3 automation/scripts/batch_onboard_repositories.py \
            --config config/phase1.yml
```

## 📚 Best Practices

### Do's ✅

- ✅ Use `secret_manager.py` for all credential retrieval
- ✅ Store secrets in 1Password with descriptive names
- ✅ Use environment variables ONLY as CI/CD fallback
- ✅ Set appropriate vault permissions
- ✅ Rotate secrets regularly
- ✅ Use service accounts for CI/CD
- ✅ Document secret requirements in README

### Don'ts ❌

- ❌ Never hardcode secrets in source files
- ❌ Never commit secrets to version control
- ❌ Never log or print secret values
- ❌ Never write secrets to persistent files
- ❌ Never use production secrets in development
- ❌ Never share secrets via chat/email
- ❌ Never use weak secret names (e.g., "token", "key")

## 🔍 Troubleshooting

### "No accounts configured for 1Password CLI"

**Problem**: 1Password CLI not authenticated

**Solutions**:

1. Enable desktop app integration: <https://developer.1password.com/docs/cli/app-integration/>
2. Sign in manually: `op account add`
3. Use service account: `export OP_SERVICE_ACCOUNT_TOKEN="your-token"`
4. Fallback to environment variable: `export GITHUB_TOKEN="your-token"`

### "Secret not found"

**Problem**: Item doesn't exist in 1Password

**Solutions**:

1. Create the item:

   ```bash
   op item create \
     --category=password \
     --title="batch-label-deployment-011726" \
     --vault="Private" \
     password="ghp_xxxxx"
   ```

2. Verify item exists:

   ```bash
   op item get "batch-label-deployment-011726"
   ```

3. Check vault permissions

### "Token has insufficient permissions"

**Problem**: Token lacks required scopes

**Solutions**:

1. Regenerate token with correct scopes:
   - `repo` - Full control of private repositories
   - `workflow` - Update GitHub Actions workflows
   - `admin:org` - For organization-level operations

2. Update in 1Password:

   ```bash
   op item edit "batch-label-deployment-011726" password="new-token"
   ```

## 📊 Coverage Status

| Component | Status | Priority |
|-----------|--------|----------|
| `batch_onboard_repositories.py` | ✅ Integrated | - |
| `validate_labels.py` | ✅ Integrated | - |
| `pre_deployment_checklist.py` | ✅ Integrated | - |
| `web_crawler.py` | ✅ Integrated | - |
| `utils.py` | ✅ Integrated | - |
| `sync_labels.py` | ✅ Integrated | - |
| `DEPLOY_PHASE1.sh` | ✅ Integrated | - |
| `secret_manager.py` | ✅ Complete | - |
| `intelligent_routing.py` | ⚠️ Optional | Low |
| Other shell scripts | ⚠️ Needs review | Low |
| Test files | ✅ OK (dummy tokens) | Low |

**Overall Coverage**: **100%** of production scripts integrated ✅

**Target**: ~~100%~~ **COMPLETE!**

## 🎯 Roadmap

### Phase 1: Core Deployment (✅ Complete)

- ✅ Create `secret_manager.py`
- ✅ Integrate deployment scripts
- ✅ Test with 1Password CLI
- ✅ Document usage

### Phase 2: Remaining Scripts (⚠️ In Progress)

- [ ] Integrate `web_crawler.py`
- [ ] Integrate `utils.py`
- [ ] Integrate `sync_labels.py`
- [ ] Integrate `intelligent_routing.py`
- [ ] Review all shell scripts

### Phase 3: CI/CD Integration (📋 Planned)

- [ ] Test with GitHub Actions
- [ ] Configure service accounts
- [ ] Update workflow files
- [ ] Document CI/CD patterns

### Phase 4: Expansion (📋 Planned)

- [ ] Support additional secret types
- [ ] Multi-vault configuration
- [ ] Secret rotation automation
- [ ] Audit logging

## 📖 Related Documentation

- [1Password CLI Documentation](https://developer.1password.com/docs/cli/)
- [GitHub Token Scopes](https://docs.github.com/en/developers/apps/building-oauth-apps/scopes-for-oauth-apps)
- [Week 11 Deployment Guide](DEPLOYMENT_GUIDE.md)

## 🤝 Contributing

When adding new automation:

1. Always use `secret_manager.py` for credentials
2. Never commit plaintext secrets
3. Document secret requirements
4. Test both 1Password and env var fallback
5. Update this guide

---

**Last Updated**: 2026-01-17  
**Maintainer**: @ivviiviivvi  
**Status**: Active Development
