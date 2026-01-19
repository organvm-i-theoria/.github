#!/usr/bin/env python3
"""
Test suite for branch deletion audit system.
Validates that the logging and recovery scripts work correctly.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def test_log_script_exists():
    """Test that the log script exists and is executable."""
    script_path = Path(".github/scripts/log-branch-deletion.sh")
    assert script_path.exists(), "Log script not found"
    assert os.access(script_path, os.X_OK), "Log script not executable"
    print("✓ Log script exists and is executable")


def test_recover_script_exists():
    """Test that the recover script exists and is executable."""
    script_path = Path(".github/scripts/recover-branch.sh")
    assert script_path.exists(), "Recovery script not found"
    assert os.access(script_path, os.X_OK), "Recovery script not executable"
    print("✓ Recovery script exists and is executable")


def test_audit_directory_exists():
    """Test that the audit directory exists."""
    audit_dir = Path(".github/branch-deletion-audit")
    assert audit_dir.exists(), "Audit directory not found"
    assert audit_dir.is_dir(), "Audit path is not a directory"
    print("✓ Audit directory exists")


def test_audit_readme_exists():
    """Test that audit README exists."""
    readme = Path(".github/branch-deletion-audit/README.md")
    assert readme.exists(), "Audit README not found"
    print("✓ Audit README exists")


def test_log_script_syntax():
    """Test that the log script has valid bash syntax."""
    returncode, _, stderr = run_command("bash -n .github/scripts/log-branch-deletion.sh")
    assert returncode == 0, f"Log script syntax error: {stderr}"
    print("✓ Log script has valid syntax")


def test_recover_script_syntax():
    """Test that the recover script has valid bash syntax."""
    returncode, _, stderr = run_command("bash -n .github/scripts/recover-branch.sh")
    assert returncode == 0, f"Recovery script syntax error: {stderr}"
    print("✓ Recovery script has valid syntax")


def test_log_script_with_test_data():
    """Test logging a branch deletion (using main branch for metadata)."""
    # Create a test audit log
    returncode, stdout, stderr = run_command(
        '.github/scripts/log-branch-deletion.sh "test-branch-audit" "999" "test-run"'
    )
    
    # Should succeed even if branch doesn't exist remotely
    assert returncode == 0, f"Log script failed: {stderr}"
    print("✓ Log script executes successfully")
    
    # Check that audit file was created
    audit_files = list(Path(".github/branch-deletion-audit").glob("*.jsonl"))
    assert len(audit_files) > 0, "No audit files created"
    print(f"✓ Audit file created: {audit_files[0].name}")
    
    # Validate JSON format
    with open(audit_files[0], 'r') as f:
        lines = f.readlines()
        last_line = lines[-1]
        try:
            record = json.loads(last_line)
            assert "branch" in record, "Missing 'branch' field"
            assert "tip_sha" in record, "Missing 'tip_sha' field"
            assert "timestamp" in record, "Missing 'timestamp' field"
            assert "pr_number" in record, "Missing 'pr_number' field"
            assert record["branch"] == "test-branch-audit", "Wrong branch name"
            assert record["pr_number"] == "999", "Wrong PR number"
            print("✓ Audit log has valid JSON format")
            print(f"  Branch: {record['branch']}")
            print(f"  SHA: {record['tip_sha']}")
            print(f"  PR: #{record['pr_number']}")
        except json.JSONDecodeError as e:
            raise AssertionError(f"Invalid JSON in audit log: {e}")
    
    return audit_files[0], record


def test_recover_script_finds_branch(audit_file, record):
    """Test that recovery script can find the logged branch."""
    branch_name = record["branch"]
    returncode, stdout, stderr = run_command(
        f'.github/scripts/recover-branch.sh "{branch_name}"'
    )
    
    assert returncode == 0, f"Recovery script failed: {stderr}"
    assert branch_name in stdout, "Branch name not in output"
    assert record["tip_sha"] in stdout or "already-deleted" in stdout, "SHA not in output"
    print(f"✓ Recovery script found branch: {branch_name}")


def test_cleanup_test_data(audit_file):
    """Clean up test data."""
    # Remove test audit log entries
    with open(audit_file, 'r') as f:
        lines = f.readlines()
    
    # Filter out test entries
    cleaned_lines = [l for l in lines if '"test-branch-audit"' not in l]
    
    if len(cleaned_lines) == 0:
        # If file is empty, remove it
        audit_file.unlink()
        print(f"✓ Removed empty audit file: {audit_file.name}")
    else:
        # Write back cleaned lines
        with open(audit_file, 'w') as f:
            f.writelines(cleaned_lines)
        print(f"✓ Cleaned test data from: {audit_file.name}")


def main():
    """Run all tests."""
    print("Branch Deletion Audit System Test Suite")
    print("=" * 50)
    
    try:
        # Basic existence tests
        test_log_script_exists()
        test_recover_script_exists()
        test_audit_directory_exists()
        test_audit_readme_exists()
        
        # Syntax validation
        test_log_script_syntax()
        test_recover_script_syntax()
        
        # Functional tests
        audit_file, record = test_log_script_with_test_data()
        test_recover_script_finds_branch(audit_file, record)
        
        # Cleanup
        test_cleanup_test_data(audit_file)
        
        print("=" * 50)
        print("✅ All tests passed!")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
