"""Linton 'publish' subcommand

© Reuben Thomas <rrt@sc3d.org> 2024-2025
Released under the GPL version 3, or (at your option) any later version.
"""

import argparse
import os
import subprocess
import sys

from linton.warnings_util import die


def run(args: argparse.Namespace) -> None:
    """'publish' command handler"""
    cmd = ["nancy"]

    # Deal with --update
    if args.update:
        args.force = True
        cmd.append("--update")

    # Check output either does not exist, or is an empty directory, unless
    # --force given
    if os.path.exists(args.output) and not (
        os.path.isdir(args.output) and len(os.listdir(args.output)) == 0
    ):
        if args.force:
            cmd.append("--delete")
        else:
            die(f"output {args.output} exists and is not an empty directory")

    try:
        # Render the project files to the output
        subprocess.check_output(cmd + [args.document_root, args.output])

        # Check links unless disabled
        output_dir = args.output
        if not output_dir.endswith("/"):
            output_dir += "/"
        if not args.no_check_links:
            subprocess.check_call(["linkchecker", output_dir])
    except subprocess.CalledProcessError as err:
        if err.stderr is not None:
            print(err.stderr.decode("iso-8859-1"), file=sys.stderr)
        die(f"Error code {err.returncode} running: {' '.join(map(str, err.cmd))}")


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "publish",
        help="convert a directory of Markdown files and other resources into a web site",
        epilog="The output DIRECTORY cannot be a subdirectory of the input directory.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite output directory even if it is not empty",
    )
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="update an existing site, writing only changed files (implies --force)",
    )
    parser.add_argument(
        "--base-url",
        metavar="URL",
        help="base URL of web site relative to root of server [default: %(default)s]",
        default="/",
    )
    parser.add_argument(
        "--no-check-links",
        action="store_true",
        help="don't check hyperlinks in the generated site",
    )
    parser.add_argument(
        "document_root", metavar="DIRECTORY", help="directory containing source files"
    )
    parser.add_argument("output", metavar="DIRECTORY", help="output directory")
    parser.set_defaults(func=run)
