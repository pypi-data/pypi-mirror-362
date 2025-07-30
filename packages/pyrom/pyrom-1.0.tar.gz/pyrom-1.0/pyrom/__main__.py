# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Global program settings
from argparse import Action, ArgumentError, ArgumentParser, Namespace
from collections.abc import Sequence
from os import cpu_count
from pathlib import Path
from typing import TYPE_CHECKING, override

from pyrom import __version__
from pyrom.check import check_games, find_games
from pyrom.console import console, errconsole
from pyrom.game import Game, LookupRom
from pyrom.hashes import available_checks
from pyrom.morph import morph_games
from pyrom.parsing import parse_files
from pyrom.resolve import resolve_files
from pyrom.stats import (
	print_custom_textfile,
	print_datfile,
	print_pairs,
	print_pairs_machine,
	print_stats,
)

if TYPE_CHECKING:  # pragma: no cover
	from pyrom.args import MorphArgs, MyArgs, ResolveArgs


class CheckAction(Action):
	def __init__(self, option_strings, dest, nargs=None, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
		if nargs is not None:
			raise ValueError("nargs not allowed")
		super().__init__(option_strings, dest, **kwargs)  # pyright: ignore[reportUnknownArgumentType]

	@override
	def __call__(
		self,
		parser: ArgumentParser,
		namespace: Namespace,
		values: str | Sequence[str] | None,
		option_string: str | None = None,
	):
		if not isinstance(values, str):
			raise TypeError("argument must be a single string")
		res = values.split(",")
		for alg in res:
			if alg not in available_checks:
				raise ArgumentError(self, "unknown hash algorithm")
		setattr(namespace, self.dest, res)


def main() -> None:
	parser = ArgumentParser(prog="pyrom")
	_ = parser.add_argument("-v", "--version", action="version", version=__version__)
	_ = parser.add_argument(
		"-f",
		"--show-failed",
		action="store_true",
		help="Show a list of corrupted ROMs after checks are finished",
		dest="failed",
	)
	_ = parser.add_argument(
		"-S",
		"--show-summary",
		action="store_true",
		help="After checks are finished, display how many files are ok/missing/corrupt etc.",
		dest="summary",
	)
	_ = parser.add_argument(
		"-s",
		"--show-skipped",
		action="store_true",
		help="Show a list of duplicate titles skipped",
		dest="skipped",
	)
	_ = parser.add_argument(
		"-m",
		"--show-missing",
		action="store_true",
		help="Show a list of missing titles after checks are finished",
		dest="missing",
	)
	_ = parser.add_argument(
		"-j",
		"--threads",
		help="How many threads to use for reading files from disk (default = nproc/4)",
		default=int(max((cpu_count() or 4) / 4, 1)),
		type=int,
	)
	_ = parser.add_argument(
		"-l",
		"--hashers",
		help="How many hash checks to run in parallel (default = nproc/4)",
		default=int(max((cpu_count() or 4) / 4, 1)),
		type=int,
	)
	_ = parser.add_argument(
		"--strict",
		action="store_true",
		help="Match ROMs only if the directory they are in matches the console name",
	)
	_ = parser.add_argument(
		"-u",
		"--print-unresolved",
		action="store_true",
		help="Print all files that could not be matched to a game.\
		Note that unresolved files are not considered the result\
		and will always be printed to stdout. May increase the runtime since\
		ALL files in the target directory will be checked.",
		dest="prun",
	)
	_ = parser.add_argument(
		"-d",
		"--dir",
		default=".",
		help="Root directory in which ROMs are stored (default is the current directory).",
	)
	# TODO: different formats (JSON/XML...)
	_ = parser.add_argument(
		"-r",
		"--machine-readable",
		action="store_true",
		help="Display results in a machine-readable format",
		dest="machine",
	)
	_ = parser.add_argument(
		"-C",
		"--disable-checks",
		action=CheckAction,
		help=f"Comma-separated list of checks to disable {available_checks}",
		dest="checks",
		default="",
	)
	_ = parser.add_argument(
		"-o",
		"--output-file",
		type=Path,
		default=None,
		dest="output",
		help="Name of a file file to write results to.\
			Without this option results are written to stdout.\
			(You will likely want to use this with the --machine option)",
	)
	_ = parser.add_argument(
		"-q",
		"--quiet",
		action="store_true",
		help="Silence progress bars",
		default=not console.is_terminal,
	)
	_ = parser.add_argument("files", nargs="+", help="DATfiles to get checksums from", type=Path)
	args: MyArgs = parser.parse_args()  # pyright: ignore[reportAssignmentType]
	# surely, the user wouldn't want NO output at all
	if (
		not args.summary
		and not args.skipped
		and not args.failed
		and not args.missing
		and not args.prun
	):
		args.failed = True
		args.summary = True

	for file in args.files:
		if not file.exists():
			errconsole.print(f"File '{file}' does not exist.")
			return
	if args.output is not None:
		try:
			args.output.touch()
		except PermissionError as e:
			errconsole.print(f"Cannot open output file:{e}")
			return

	games: list[Game] = parse_files(args.files, args.quiet)
	check_games(games, args)
	print_stats(games, args)


def resolve() -> None:
	parser = ArgumentParser(prog="pyrom-resolve")
	_ = parser.add_argument("-v", "--version", action="version", version=__version__)
	_ = parser.add_argument(
		"-d",
		"--datfiles",
		nargs="+",
		required=True,
		help="DAT files acting as a source of names",
		type=Path,
	)
	_ = parser.add_argument(
		"-f",
		"--romfiles",
		nargs="+",
		required=True,
		help="The roms for which correct names should be determined",
		type=Path,
	)
	_ = parser.add_argument(
		"-l",
		"--lenient",
		action="store_true",
		help="Do not use hash to check every candidate of matching size,\
				but possibly report false positives instead of no match",
	)
	_ = parser.add_argument(
		"-r",
		"--report-all",
		action="store_true",
		help="Check for all possible matches (can be EXTREMELY slow!)",
		dest="reportall",
	)
	_ = parser.add_argument(
		"-c",
		"--checks",
		help=f"Comma-separated list of checks to use {available_checks} (size always used)",
		default="",
		action=CheckAction,
	)
	_ = parser.add_argument(
		"-m",
		"--machine-readable",
		action="store_true",
		help="Display results in a machine-readable format",
		dest="machine",
	)
	_ = parser.add_argument(
		"-o",
		"--output-file",
		type=Path,
		default=None,
		dest="output",
		help="Name of a file file to write results to.\
			Without this option results are written to stdout.\
			(You will likely want to use this with the --machine option)",
	)
	_ = parser.add_argument(
		"-q", "--quiet", help="Less output", default=not console.is_terminal, action="store_true"
	)
	args: ResolveArgs = parser.parse_args()  # pyright: ignore[reportAssignmentType]
	for dfile in args.datfiles:
		if not dfile.exists():
			errconsole.print(f"File '{dfile}' does not exist.")
			return
	for rfile in args.romfiles:
		if not rfile.exists():
			errconsole.print(f"File '{rfile}' does not exist.")
			return
	if args.output is not None:
		try:
			args.output.touch()
		except PermissionError as e:
			errconsole.print(f"Cannot open output file:{e}")
			return

	games = parse_files(args.datfiles, args.quiet)
	lookuproms: list[LookupRom] = []
	for game in games:
		lookuproms.extend(
			LookupRom(game.name, game.console, rom.romname, **rom.checks) for rom in game.roms
		)

	pairs = resolve_files(lookuproms, args.romfiles, args)
	if args.machine:
		print_pairs_machine(pairs, args.output)
	else:
		print_pairs(pairs, args.output)


def morph() -> None:
	parser = ArgumentParser(prog="pyrom-morph")
	_ = parser.add_argument("-v", "--version", action="version", version=__version__)
	_ = parser.add_argument(
		"datfiles", help="Dat files to get initial data from", nargs="+", type=Path
	)
	_ = parser.add_argument(
		"-d", "--dir", default=".", help="Root directory in which ROMs are stored"
	)
	_ = parser.add_argument(
		"-c",
		"--select-checks",
		action=CheckAction,
		help=f"Comma-separated list of checks to enable {available_checks}",
		dest="checks",
		default=available_checks,
	)
	_ = parser.add_argument(
		"-q",
		"--quiet",
		action="store_true",
		help="Do not show progress bars or spinners",
		dest="quiet",
		default=not console.is_terminal,
	)
	_ = parser.add_argument(
		"-t",
		"--trim",
		action="store_true",
		help="Do not include files that were not found in the result",
		dest="trim",
	)
	_ = parser.add_argument(
		"-f",
		"--output-format",
		choices=["xml", "custom"],
		help="The format to use for output. Default is xml (normal DATfile).",
		dest="format",
		default="xml",
	)
	_ = parser.add_argument(
		"-n",
		"--no-resolve",
		dest="noresolve",
		help="Do not resolve games or fill in missing hashes",
		action="store_true",
	)
	_ = parser.add_argument(
		"-j",
		"--loaders",
		help="How many threads to use for reading files from disk (default = nproc/4)",
		default=int(max((cpu_count() or 4) / 4, 1)),
		type=int,
	)
	_ = parser.add_argument(
		"-l",
		"--hashers",
		help="How many hash checks to run in parallel (default = nproc/4)",
		default=int(max((cpu_count() or 4) / 4, 1)),
		type=int,
	)
	_ = parser.add_argument("-o", "--output-file", type=Path, default=None, dest="output")
	args: MorphArgs = parser.parse_args()  # pyright: ignore[reportAssignmentType]
	for dfile in args.datfiles:
		if not dfile.exists():
			errconsole.print(f"File '{dfile}' does not exist.")
			return
	if args.output is not None:
		try:
			args.output.touch()
		except PermissionError as e:
			errconsole.print(f"Cannot open output file:{e}")
			return

	games = parse_files(args.datfiles, args.quiet)
	if not args.noresolve:
		find_games(games, args)
		games = morph_games(games, args)
	if args.format == "xml":
		print_datfile(games, args)
	else:
		print_custom_textfile(games, args)


if __name__ == "__main__":
	main()
