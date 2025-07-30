# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
from pathlib import Path


# pyright: reportUninitializedInstanceVariable=false
class MyArgs(argparse.Namespace):
	summary: bool
	missing: bool
	skipped: bool
	files: list[Path]
	failed: bool
	dir: str
	threads: int
	hashers: int
	checks: list[str]
	machine: bool = False  # false -> print human-friendly
	strict: bool
	prun: bool
	output: Path | None
	quiet: bool


# pyright: reportUninitializedInstanceVariable=false
class MorphArgs(argparse.Namespace):
	datfiles: list[Path]
	dir: str
	quiet: bool = False
	checks: list[str]
	trim: bool
	format: str
	noresolve: bool
	output: Path | None
	loaders: int
	hashers: int


# pyright: reportUninitializedInstanceVariable=false
class ResolveArgs(argparse.Namespace):
	datfiles: list[Path]
	romfiles: list[Path]
	checks: list[str]
	lenient: bool
	quiet: bool
	reportall: bool
	machine: bool
	output: Path | None
