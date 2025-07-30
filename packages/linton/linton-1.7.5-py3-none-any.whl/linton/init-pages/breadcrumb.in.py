#!/usr/bin/env python3

import sys
import urllib.parse
from pathlib import Path


# Get command-line arguments
page = Path(sys.argv[1])

# Extract page name and normalize path
path = page.parent

# Generate and print breadcrumb
tree = ""
classes = "breadcrumb-item breadcrumb-active"
while str(path) not in (".", "/"):
    quoted_parents = urllib.parse.quote(str(path))
    tree = (
        f'<li class="{classes}">'
        + f'<a href="$run(path-to-root.in.py,$path)/{quoted_parents}/index.html">{path.name}</a>'
        + f"</li>{tree}"
    )
    classes = "breadcrumb-item"
    path = path.parent
print(
    '<li class="breadcrumb-item">'
    + '<a href="$run(path-to-root.in.py,$path)/index.html">$include(Title.in.txt)</a>'
    + f"</li>{tree}"
)
