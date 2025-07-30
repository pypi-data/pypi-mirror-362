#!/usr/bin/env python3
"""Setup script for wmcoredb package."""

import os
import glob
from setuptools import setup

# Find all SQL files
sql_files = []
for sql_file in glob.glob("src/sql/**/*.sql", recursive=True):
    # Remove the src/ prefix for the destination path
    dest_path = sql_file.replace("src/", "")
    sql_files.append((f"wmcoredb/{os.path.dirname(dest_path)}", [sql_file]))

setup(
    packages=[],
    include_package_data=False,
    data_files=sql_files,
) 