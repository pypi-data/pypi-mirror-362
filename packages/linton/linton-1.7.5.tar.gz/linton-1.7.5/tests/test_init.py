"""'linton init' tests.

Copyright (c) Reuben Thomas 2024.
Released under the GPL version 3, or (at your option) any later version.
"""

from collections.abc import Callable
from pathlib import Path

from pytest import CaptureFixture
from testutils import Case, dir_test, make_tests

from linton import main


pytestmark = make_tests(
    main,
    Path(__file__).parent.resolve() / "test-files",
    Case(
        "default",
        ["init"],
    ),
)


def test_init(
    function: Callable[[list[str]], None],
    case: Case,
    fixture_dir: Path,
    capsys: CaptureFixture[str],
    regenerate_expected: bool,
) -> None:
    dir_test(
        function,
        case,
        fixture_dir,
        capsys,
        regenerate_expected,
    )
