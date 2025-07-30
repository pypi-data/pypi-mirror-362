#!/usr/bin/env python3
# Output the path from the first argument to the root of the directory

import sys
from pathlib import Path


# Read command-line arguments
page = Path(sys.argv[1])
directory = page.parent

path_to_root = Path(".")
while directory != Path("."):
    directory = directory.parent
    path_to_root /= ".."

print(path_to_root, end="")
