# SPDX-License-Identifier: LicenseRef-OQL-1.2

import sys
from unittest import mock
from PrintTolCalc import cli
import pytest


def test_cli_runs_without_error(capsys):
    test_args = ["prog", "--help"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as e:
            cli.main()
        assert e.value.code == 0
        out = capsys.readouterr().out
        assert "usage" in out.lower()


def test_cli_version_output(capsys):
    test_args = ["prog", "--version"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as e:
            cli.main()
        assert e.value.code == 0
        out = capsys.readouterr().out.strip()
        assert out.startswith("PrintTolCalc ")
        assert len(out.split()) == 2
        assert all(part.isdigit() for part in out.split()[1].split("."))
