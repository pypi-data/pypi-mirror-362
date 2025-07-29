# SPDX-License-Identifier: LicenseRef-OQL-1.2

import subprocess
import sys


def test_cli_help_command():
    result = subprocess.run(
        [sys.executable, "-m", "PrintTolCalc.cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_cli_version_command():
    result = subprocess.run(
        [sys.executable, "-m", "PrintTolCalc.cli", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    output = result.stdout.strip()
    assert output.startswith("PrintTolCalc ")
    parts = output.split()
    assert len(parts) == 2
    version = parts[1].split(".")
    assert all(part.isdigit() for part in version)
