"""Linton 'serve' subcommand

© Reuben Thomas <rrt@sc3d.org> 2024-2025
Released under the GPL version 3, or (at your option) any later version.
"""

import argparse
import glob
import os
import subprocess
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import quote

from xdg import Mime


def denancify(name: Path) -> Path:
    suffixes = name.suffixes
    if len(suffixes) > 0 and ".nancy" in suffixes[-2:]:
        suffixes.remove(".nancy")
        while name.suffix:
            name = name.with_suffix("")
        return name.with_suffix("".join(suffixes))
    return name


def run(args: argparse.Namespace) -> None:
    """'serve' command handler"""

    class HTTPRequestHandler(BaseHTTPRequestHandler):
        def serve_file(self, filename: Path, content: bytes) -> None:
            mime_type = str(Mime.get_type2(filename).canonical())
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.end_headers()
            self.wfile.write(content)

        def maybe_serve_file(
            self, filename: Path, filenames: list[str], url_path: str
        ) -> bool:
            # If the name is a directory, try serving its "index.html"
            if filename.is_dir():
                self.send_response(301)
                self.send_header(
                    "Location",
                    os.path.join(quote(args.base_url), quote(url_path), "index.html"),
                )
                self.end_headers()
                return True

            # First, try reading a plain file.
            if filename.name in filenames:
                with open(filename, "rb") as fh:
                    output = fh.read()
                self.serve_file(filename, output)
                return True

            # Next, look for a Nancy source file to expand.
            suffix = filename.suffix
            nancy_suffix = f".nancy{suffix}"
            nancy_source = filename.with_suffix(nancy_suffix)
            if nancy_source.name in filenames:
                output = self.run_command(
                    [
                        "nancy",
                        args.document_root,
                        "-",
                        f"--path={Path(url_path).parent / nancy_source.name}",
                    ],
                )
                if output is None:
                    return True
                self.serve_file(Path(nancy_source), output)
                return True

            return False

        def run_command(self, cmd: list[str]) -> bytes | None:
            try:
                res = subprocess.run(cmd, capture_output=True, check=True)
                return res.stdout
            except subprocess.CalledProcessError as e:
                self.send_response(500)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(
                    b"<html><head><title>Internal error</title><body><h1>Internal error</h1><pre>"
                    + e.stderr
                    + b"</pre></body></html>"
                )

        def do_GET(self) -> None:
            """GET handler"""
            url_path = urllib.parse.unquote(
                urllib.parse.urlparse(self.path.removeprefix(args.base_url)).path
            )

            # First, try the literal file name and its templated version.
            input_path = Path(args.document_root) / url_path
            if self.maybe_serve_file(
                input_path, os.listdir(input_path.parent), url_path
            ):
                return

            # If that doesn't work, find all files whose names containing
            # commands in the same directory, and expand a file containing
            # each of them to find its expanded name, in case one expands to
            # the name we want.
            with TemporaryDirectory() as tmpdir:
                filename_file_url = Path(os.path.dirname(url_path)) / "filelist.nancy"
                filename_file = Path(tmpdir) / filename_file_url
                os.makedirs(filename_file.parent, exist_ok=True)
                for filename in glob.glob(b"*$*", root_dir=bytes(input_path.parent)):
                    with open(filename_file, "wb") as f:
                        f.write(filename)
                    output_file = self.run_command(
                        [
                            "nancy",
                            os.pathsep.join([args.document_root, tmpdir]),
                            "-",
                            f"--path={filename_file_url}",
                        ],
                    )
                    if output_file is None:
                        return
                    output_name = denancify(Path(output_file.decode("utf-8")))
                    if input_path.name == str(output_name) and self.maybe_serve_file(
                        input_path.parent / denancify(Path(filename.decode("utf-8"))),
                        [os.fsdecode(filename)],
                        url_path,
                    ):
                        return

            # Otherwise, file is not found
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><head><title>No such page</title><body>No such page</body></html>"
            )

    httpd = HTTPServer(("localhost", args.port), HTTPRequestHandler)
    (host, port, *_) = httpd.server_address
    print(f"Connect to server at http://{str(host)}:{port}/index.html")
    httpd.serve_forever()


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "serve",
        help="serve a Linton web site locally on your computer, for testing",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="port on which to listen [default: random]",
        type=int,
        default=0,
    )
    parser.add_argument(
        "document_root",
        metavar="DIRECTORY",
        help="directory containing source files [default: current working directory]",
        default=os.getcwd(),
        nargs="?",
    )
    parser.set_defaults(func=run)
