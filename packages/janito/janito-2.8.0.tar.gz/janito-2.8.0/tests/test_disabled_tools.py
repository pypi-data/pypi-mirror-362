#!/usr/bin/env python3
"""Test script to verify disabled tools functionality."""

import tempfile
import os
import subprocess
import sys
from pathlib import Path


def test_disabled_tools_cli():
    """Test the --set disabled_tools=... CLI functionality."""
    print("Testing disabled tools CLI functionality...")

    # Test 1: Set disabled tools
    print("\n1. Testing --set disabled_tools=...")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "janito",
            "--set",
            "disabled_tools=create_file,read_files",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"ERROR: Failed to set disabled tools: {result.stderr}")
        return False

    print("✓ Successfully set disabled tools")

    # Test 2: Show config to verify disabled tools
    print("\n2. Testing --show-config shows disabled tools")
    result = subprocess.run(
        [sys.executable, "-m", "janito", "--show-config"],
        capture_output=True,
        text=True,
    )

    if "Disabled tools:" not in result.stdout:
        print("ERROR: Disabled tools not shown in config")
        return False

    if "create_file" not in result.stdout or "read_files" not in result.stdout:
        print("ERROR: Expected disabled tools not found in config")
        return False

    print("✓ Disabled tools correctly shown in config")

    # Test 3: List tools should exclude disabled ones
    print("\n3. Testing --list-tools excludes disabled tools")
    result = subprocess.run(
        [sys.executable, "-m", "janito", "--list-tools"], capture_output=True, text=True
    )

    if "create_file" in result.stdout or "read_files" in result.stdout:
        print("ERROR: Disabled tools still appear in --list-tools")
        return False

    print("✓ Disabled tools correctly excluded from --list-tools")

    # Test 4: Clear disabled tools
    print("\n4. Testing clearing disabled tools")
    result = subprocess.run(
        [sys.executable, "-m", "janito", "--set", "disabled_tools="],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"ERROR: Failed to clear disabled tools: {result.stderr}")
        return False

    print("✓ Successfully cleared disabled tools")

    # Test 5: Verify tools are available again
    print("\n5. Testing tools are available after clearing")
    result = subprocess.run(
        [sys.executable, "-m", "janito", "--list-tools"], capture_output=True, text=True
    )

    if "create_file" not in result.stdout or "read_files" not in result.stdout:
        print("ERROR: Tools not restored after clearing disabled list")
        return False

    print("✓ Tools correctly restored after clearing disabled list")

    return True


if __name__ == "__main__":
    success = test_disabled_tools_cli()
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
