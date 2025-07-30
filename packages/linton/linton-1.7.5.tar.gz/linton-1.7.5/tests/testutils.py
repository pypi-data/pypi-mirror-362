"""Linton tests utility routines.

Copyright (c) Reuben Thomas 2023.
Released under the GPL version 3, or (at your option) any later version.
"""

import contextlib
import filecmp
import io
import re
import shutil
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
from pytest import CaptureFixture, mark, param


@dataclass
class Case:
    name: str
    args: list[str]
    error: int | None = None


# See https://stackoverflow.com/questions/4187564
def dirs_equal(a: Path, b: Path) -> bool:
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        filecmp.dircmp(a, b).report_full_closure()
    match = re.search("Differing files|Only in", stdout.getvalue())
    if match is None:
        return True
    print(stdout.getvalue())
    return False


def dir_test(
    function: Callable[[list[str]], None],
    case: Case,
    fixture_dir: Path,
    capsys: CaptureFixture[str],
    regenerate_expected: bool,
) -> None:
    subcommand_name = case.args[0]
    expected_dir = fixture_dir / subcommand_name / case.name / "expected"
    expected_stderr = fixture_dir / subcommand_name / case.name / "expected-stderr.txt"
    patched_argv = [subcommand_name, *(sys.argv[1:])]
    # FIXME: when we can assume Python ≥ 3.12, use
    # `TemporaryDirectory(delete="DEBUG" not in os.environ)`
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "output"
        full_args = [*case.args, str(output_dir)]
        if case.error is None:
            with patch("sys.argv", patched_argv):
                function(full_args)
            if regenerate_expected:
                shutil.copytree(output_dir, expected_dir, dirs_exist_ok=True)
            else:
                assert dirs_equal(output_dir, expected_dir)
        else:
            with pytest.raises(SystemExit) as e:
                with patch("sys.argv", patched_argv):
                    function(full_args)
            assert e.value.code == case.error
        if regenerate_expected:
            with open(expected_stderr, "w", encoding="utf-8") as f:
                f.write(capsys.readouterr().err)
        else:
            assert (
                capsys.readouterr().err
                == open(expected_stderr, encoding="utf-8").read()
            )


def make_tests(
    function: Callable[..., Any],
    fixture_dir: Path,
    *tests: Case,
) -> Any:
    ids = []
    test_cases = []
    for t in tests:
        ids.append(t.name)
        test_cases.append(t)
    return mark.parametrize(
        "function,case,fixture_dir",
        [param(function, case, fixture_dir) for case in test_cases],
        ids=ids,
    )
