# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

import concurrent.futures
import os
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path

from rich.progress import (
	MofNCompleteColumn,
	Progress,
	SpinnerColumn,
	TaskID,
)
from rich.status import Status

from pyrom.args import MorphArgs, MyArgs
from pyrom.console import console
from pyrom.game import Game, GameStatus, Rom
from pyrom.hashes import available_checks, get_hash
from pyrom.helpers import all_of, only_one_of


def compare_games(game1: Game, game2: Game) -> bool:
	"""
	Determines whether games have the same checksums for their roms and one can therefore be skipped
	"""
	return len(game1.roms) == len(game2.roms) and all(
		game1.roms[i].checks == game2.roms[i].checks for i in range(len(game1.roms))
	)


def find_games(
	games: list[Game], args: MyArgs | MorphArgs, strict: bool = False, prun: bool = False
) -> None:
	"""
	Descend into args.dir and check for existence of files
	All found games will have their romname replace with the real relative path
	The rest will be marked as missing
	"""
	spinner = Status("Finding files")
	if not args.quiet:
		spinner.start()
	# Allows for duplicate entries
	filemap: dict[str, list[Game]] = {}
	rom2game = {rom: game for game in games for rom in game.roms}
	for game in games:
		for rom in game.roms:
			if rom.romname not in filemap:
				filemap[rom.romname] = [game]
			else:
				filemap[rom.romname].append(game)

	for dirpath, _, files in os.walk(args.dir):
		for file in files:
			if file in filemap:
				# TODO: merge the branches more
				gamelist = filemap[file]
				# only one possible game exists that could contain this file
				if len(gamelist) == 1:
					game = gamelist[0]
					if (strict and dirpath.find(game.console) != -1) or not strict:
						for rom in game.roms:
							if rom.romname == file:
								rom.romname = os.path.join(dirpath, file)
						del filemap[file]
				else:
					all_same = True
					# check if the games have the same checksums
					for i in range(len(gamelist) - 1):
						if not compare_games(gamelist[i], gamelist[i + 1]):
							all_same = False
							break

					fullfile = os.path.join(dirpath, file)
					if not all_same:
						# >= 1 of the entries is different from the others, resolve it
						# Try resolving according to console/game name first
						spinner.update(f"Resolving conflicts: {fullfile}")
						resolved = False
						for game in gamelist:
							if dirpath.find(game.console) != -1 or (
								not strict and dirpath.find(game.name) != -1
							):
								for rom in game.roms:
									if rom.romname == file:
										rom.romname = fullfile
								filemap[file].remove(game)
								resolved = True
								break

						# use size first as a fallback
						if not resolved and not strict:
							size = str(Path(fullfile).stat().st_size)
							allroms: list[Rom] = []
							for game in gamelist:
								allroms.extend(rom for rom in game.roms if rom.romname == file)
							if (
								res := only_one_of(
									allroms,
									lambda rom, localsize=size, localfile=file: rom.checks["size"]
									== localsize
									and rom.romname == localfile,
								)
							) is not None:
								res.romname = fullfile
								filemap[file].remove(rom2game[res])
								resolved = True
							elif not any((rom.checks["size"] == size) for rom in allroms):
								# no matches
								resolved = True

						# use CRC as a fallback
						if (
							not resolved
							and not strict
							and (crc := get_hash(Path(fullfile), "crc")) is not None
						):
							for game in gamelist:
								for rom in game.roms:
									if rom.checks["crc"] == crc and rom.romname == file:
										rom.romname = fullfile
										filemap[file].remove(game)
										break
						spinner.update("Finding files")
					else:
						# ROMs are identical, no reason to resolve conflicts
						for game in gamelist[1:]:
							for rom in game.roms:
								if rom.romname == file:
									rom.romname = fullfile
									rom.status = GameStatus.SKIPPED
								game.status = GameStatus.SKIPPED
						game = gamelist[0]
						for rom in game.roms:
							if rom.romname == file:
								rom.romname = os.path.join(dirpath, file)
						del filemap[file]
			elif prun:
				console.print(file)
			if not filemap and not prun:
				break
		if not filemap and not prun:
			break

	for game in games:
		all_missing = True
		for rom in game.roms:
			if rom.romname in filemap:
				rom.status = GameStatus.MISSING
				game.status = GameStatus.FAILED
			else:
				all_missing = False
		if all_missing:
			game.status = GameStatus.MISSING

	spinner.stop()


progress = Progress(
	SpinnerColumn(), *Progress.get_default_columns(), MofNCompleteColumn(), console=console
)


def get_hash_report(file: Path, alg: str, taskid: TaskID | None, exdig: str) -> tuple[str, bool]:
	res = get_hash(file, alg)
	if taskid is not None:
		progress.update(taskid, advance=1)
	return (alg, res == exdig)


def check_game(game: Game, task_id: TaskID | None, args: MyArgs) -> TaskID | None:
	"""Sets the check results for a single game, only give NOTCHECKED games!"""
	files = {rom.romname: Path(rom.romname) for rom in game.roms}
	checks = 0
	if task_id is not None:
		for rom in game.roms:
			for check in rom.checks.values():
				if check is not None:
					checks += 1

		progress.update(task_id, total=checks)
		progress.start_task(task_id)

	if len(game.roms) == 0:
		if task_id is not None:
			progress.update(task_id, completed=checks)
		return task_id or TaskID(0)

	for rom in game.roms:
		if rom.status == GameStatus.MISSING:
			game.status = GameStatus.FAILED
			continue
		with ThreadPoolExecutor(max_workers=args.hashers) as pool:
			futures: list[Future[tuple[str, bool]]] = []
			for alg in available_checks:
				if alg not in args.checks and rom.checks.get(alg):
					futures.append(
						pool.submit(
							get_hash_report,
							files[rom.romname],
							alg,
							task_id,
							rom.checks.get(alg),  # pyright: ignore[reportArgumentType]
						)
					)
				elif rom.checks.get(alg):
					rom.stats[alg] = GameStatus.SKIPPED
			for future in concurrent.futures.as_completed(futures):
				alg, ok = future.result()
				if ok:
					rom.stats[alg] = GameStatus.OK
				else:
					rom.stats[alg] = GameStatus.FAILED
					rom.status = GameStatus.FAILED
					game.status = GameStatus.FAILED
					# If the game has failed, try to cancel the other running checks
					# PERF: already running threads cannot be cancelled
					for tocancel in futures:
						_ = tocancel.cancel()
					break

		if rom.status != GameStatus.FAILED:
			if all_of(
				list(rom.stats.values()),
				{GameStatus.NOTCHECKED, GameStatus.SKIPPED},
			):
				rom.status = GameStatus.SKIPPED
			else:
				rom.status = GameStatus.OK

	if game.status != GameStatus.FAILED:
		if all_of(
			[stat.status for stat in game.roms], {GameStatus.NOTCHECKED, GameStatus.SKIPPED}
		) or any(rom.status == GameStatus.SKIPPED for rom in game.roms):
			game.status = GameStatus.SKIPPED
		else:
			game.status = GameStatus.OK

	# we are done checking for one reason or another
	if task_id is not None:
		progress.update(task_id, completed=checks)
	return task_id or None


def check_games(games: list[Game], args: MyArgs) -> None:
	"""
	Goes through the list of games and sets their Game.stats attribute
	Also prints the names and status of checked games if args.current is true
	"""
	progress.disable = args.quiet
	find_games(games, args, args.strict, prun=args.prun)
	tocheck: list[Game] = [
		game for game in games if game.status not in (GameStatus.MISSING, GameStatus.SKIPPED)
	]
	listsize = 100
	tocheck2 = [tocheck[i : i + listsize] for i in range(0, len(tocheck), listsize)]

	def do_prog(checkingid: TaskID, taskid: TaskID | None):
		progress.update(checkingid, advance=1)
		if taskid is not None:
			progress.remove_task(taskid)

	with progress:
		checking = progress.add_task("Checking files...", total=len(tocheck))
		with ThreadPoolExecutor(max_workers=args.threads) as pool:
			for tocheck3 in tocheck2:
				futures: list[Future[TaskID | None]] = []
				for game in tocheck3:
					if (len(game.roms) > 10) or any(
						(int(rom.checks["size"] or 0) > 2**26) for rom in game.roms
					):
						task_id = progress.add_task(f"Checking {game.name}", start=False)
					else:
						task_id = None

					futures.append(pool.submit(check_game, game, task_id, args))
				for future in futures:
					future.add_done_callback(lambda future: do_prog(checking, future.result()))
