# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

from difflib import SequenceMatcher
from pathlib import Path

from rich.progress import MofNCompleteColumn, Progress, SpinnerColumn

from pyrom.args import ResolveArgs
from pyrom.console import console, errconsole
from pyrom.game import LookupRom
from pyrom.hashes import get_hash

matcher = SequenceMatcher(None, "SEQ1", "SEQ2")


def _resolve_candidates(
	unknown: Path, candidates: list[LookupRom], checks: list[str], reportall: bool, lenient: bool
) -> list[LookupRom]:
	"""
	Given a path and a list of candidates, give the closest matching name with the correct hash
	"""
	res: list[LookupRom] = []
	filesize = str(unknown.stat().st_size)

	# Speed up by trying to match most name-similar roms first
	matcher.set_seq2(str(unknown))

	def mykey(seq1: LookupRom):
		matcher.set_seq1(seq1.romname)
		return matcher.ratio()

	candidates = sorted(
		candidates,
		key=mykey,
		reverse=True,
	)

	if lenient:
		if reportall:
			return candidates
		return [candidates[0]]

	for cand in candidates:
		if cand.checks["size"] == filesize:
			correct = True
			for alg in checks:
				if (
					cand.checks[alg] is not None
					and (tmp := get_hash(unknown, alg)) is not None
					and (tmp != cand.checks[alg])
				):
					correct = False
					break
			if correct:
				if reportall:
					res.append(cand)
				else:
					return [cand]
	return res


def resolve_files(
	roms: list[LookupRom], romfiles: list[Path], args: ResolveArgs
) -> list[tuple[Path, list[LookupRom]]]:
	"""
	Given a list of possible roms and romfiles to be resolved,
	return a list of tuples of unknown rom + list of potential candidates
	"""
	res: list[tuple[Path, list[LookupRom]]] = []

	# allows for duplicates
	filemap: dict[str, list[LookupRom]] = {}
	for rom in roms:
		if rom.checks["size"] is not None:
			if rom.checks["size"] not in filemap:
				filemap[rom.checks["size"]] = [rom]
			else:
				filemap[rom.checks["size"]].append(rom)
		else:
			errconsole.print(f"ROM {rom.romname} does not have a size set!")

	if len(filemap.keys()) == 0:
		errconsole.print("No ROMs could be resolved")
		return res

	with Progress(
		SpinnerColumn(),
		*Progress.get_default_columns(),
		MofNCompleteColumn(),
		console=console,
		disable=args.quiet,
	) as progress:
		task = progress.add_task("Resolving ROM file names...", total=len(romfiles))
		for unknown in romfiles:
			filesize = str(unknown.stat().st_size)
			if filesize not in filemap:
				res.append((unknown, []))
				progress.update(task, advance=1)
				continue
			candidates = filemap[filesize]
			if args.lenient and len(candidates) == 1:
				for rom in candidates:
					if rom.checks["size"] == filesize:
						res.append((unknown, [rom]))
						break
				progress.update(task, advance=1)
				continue
			# multiple candidates -> resolve
			# cannot use the console/game name here, we wouldn't be using this otherwise
			res.append(
				(
					unknown,
					_resolve_candidates(
						unknown, candidates, args.checks, args.reportall, args.lenient
					),
				)
			)
			progress.update(task, advance=1)

	return res
