"""'linton publish' tests.

Copyright (c) Reuben Thomas 2024.
Released under the GPL version 3, or (at your option) any later version.
"""

from collections.abc import Callable
from pathlib import Path

from pytest import CaptureFixture
from testutils import Case, dir_test, make_tests

from linton import main


test_files_dir = Path(__file__).parent.resolve() / "test-files"

pytestmark = make_tests(
    main,
    test_files_dir,
    Case(
        "from-init",
        ["publish", str(test_files_dir / "publish/from-init/input")],
    ),
)


def test_publish(
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
