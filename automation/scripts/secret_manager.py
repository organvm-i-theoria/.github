#!/usr/bin/env python3
"""
Universal Secret Manager for GitHub Copilot Automation

Securely retrieves secrets from 1Password CLI instead of environment variables.
Prevents plaintext secrets in files or environment.

Supported secret types:
- GitHub tokens (personal access tokens, app tokens)
- API keys (third-party services)
- Passwords (databases, services)
- SSH keys
- Certificates
- Any other sensitive credentials

Usage:
    from secret_manager import get_secret, get_github_token
    
    # GitHub token
    token = get_github_token()
    
    # Generic secret
    api_key = get_secret("my-api-key-item", "credential")
    
    # Database password
    db_pass = get_secret("prod-database", "password")
"""

import os
import subprocess
import sys
from typing import Optional


def get_secret(
    item_name: str,
    field: str = "password",
    vault: str = "Private"
) -> Optional[str]:
    """
    Get any secret from 1Password CLI.

    Args:
        item_name: Name of the 1Password item
        field: Field to retrieve (password, username, credential, etc.)
        vault: Vault name (default: Private)

    Returns:
        The secret value, or None if not found

    Security:
        - Secret retrieved from encrypted 1Password vault
        - Only exists in memory during execution
        - No plaintext files created
        - Auto-cleared when process exits

    Examples:
        >>> api_key = get_secret("datadog-api-key", "credential")
        >>> db_password = get_secret("postgres-prod", "password")
        >>> ssh_key = get_secret("deploy-key", "private key")
    """
    try:
        # Try 1Password CLI first
        cmd = ["op", "item", "get", item_name, "--fields", field]
        if vault != "Private":
            cmd.extend(["--vault", vault])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        secret = result.stdout.strip()
        if secret:
            return secret
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return None


def get_secret_with_fallback(
    item_name: str,
    field: str = "password",
    env_var: Optional[str] = None,
    vault: str = "Private"
) -> Optional[str]:
    """
    Get secret from 1Password CLI with environment variable fallback.

    Args:
        item_name: Name of the 1Password item
        field: Field to retrieve
        env_var: Environment variable to check as fallback
        vault: Vault name

    Returns:
        The secret value, or None if not found

    Examples:
        >>> token = get_secret_with_fallback(
        ...     "github-token",
        ...     "password",
        ...     env_var="GITHUB_TOKEN"
        ... )
    """
    # Try 1Password CLI first
    secret = get_secret(item_name, field, vault)
    if secret:
        return secret

    # Fallback to environment variable
    if env_var:
        secret = os.environ.get(env_var)
        if secret:
            return secret

    return None


def ensure_secret(
    item_name: str,
    field: str = "password",
    env_var: Optional[str] = None,
    vault: str = "Private"
) -> str:
    """
    Get secret or exit if not available.

    Args:
        item_name: Name of the 1Password item
        field: Field to retrieve
        env_var: Environment variable to check as fallback
        vault: Vault name

    Returns:
        The secret value (guaranteed)

    Raises:
        SystemExit: If secret cannot be retrieved
    """
    secret = get_secret_with_fallback(item_name, field, env_var, vault)
    if not secret:
        print(f"❌ Secret '{item_name}' not found", file=sys.stderr)
        print("", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print("  1. Store in 1Password:", file=sys.stderr)
        print(f'     op item create --category=password --title="{item_name}" '
              f'--vault="{vault}" {field}="your-secret"', file=sys.stderr)
        print("", file=sys.stderr)
        if env_var:
            print("  2. Export environment variable:", file=sys.stderr)
            print(f'     export {env_var}="your-secret"', file=sys.stderr)
            print("", file=sys.stderr)
        sys.exit(1)
    return secret


def get_github_token(item_name: str = "batch-label-deployment-011726") -> Optional[str]:
    """
    Get GitHub token from 1Password CLI.

    Args:
        item_name: Name of the 1Password item containing the token

    Returns:
        The GitHub token, or None if not found

    Security:
        - Token retrieved from encrypted 1Password vault
        - Only exists in memory during execution
        - No plaintext files created
        - Auto-cleared when process exits
    """
    try:
        # Try 1Password CLI first
        result = subprocess.run(
            ["op", "item", "get", item_name, "--fields", "password"],
            capture_output=True,
            text=True,
            check=True
        )
        token = result.stdout.strip()
        if token:
            return token
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fallback to environment variable (for CI/CD or manual export)
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token

    # No token found
    print("❌ GitHub token not found", file=sys.stderr)
    print("", file=sys.stderr)
    print("Options:", file=sys.stderr)
    print("  1. Store in 1Password:", file=sys.stderr)
    print(
        f'     op item create --category=password --title="{item_name}" --vault="Private" password="ghp_xxx"', file=sys.stderr)
    print("", file=sys.stderr)
    print("  2. Export environment variable:", file=sys.stderr)
    print('     export GITHUB_TOKEN="ghp_xxx"', file=sys.stderr)
    print("", file=sys.stderr)
    return None


def ensure_github_token(item_name: str = "batch-label-deployment-011726") -> str:
    """
    Get GitHub token or exit if not available.

    Args:
        item_name: Name of the 1Password item containing the token

    Returns:
        The GitHub token (guaranteed)

    Raises:
        SystemExit: If token cannot be retrieved
    """
    token = get_github_token(item_name)
    if not token:
        sys.exit(1)
    return token


if __name__ == "__main__":
    # Test the secret manager
    token = get_github_token()
    if token:
        print("✅ Token retrieved successfully")
        print(f"   Length: {len(token)} characters")
        print(f"   Prefix: {token[:7]}...")
    else:
        print("❌ Failed to retrieve token")
        sys.exit(1)
