# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from rich.progress import (
	MofNCompleteColumn,
	Progress,
	SpinnerColumn,
)

from pyrom.args import MorphArgs
from pyrom.console import console
from pyrom.game import Game, GameStatus
from pyrom.hashes import get_hash, supported_checks

progress = Progress(
	SpinnerColumn(), *Progress.get_default_columns(), MofNCompleteColumn(), console=console
)


def morph_games(games: list[Game], args: MorphArgs) -> list[Game]:
	progress.disable = args.quiet
	if args.trim:
		games = [
			game for game in games if game.status not in {GameStatus.MISSING, GameStatus.FAILED}
		]
	with progress:
		checking = progress.add_task("Checking files...", total=len(games))
		with ThreadPoolExecutor(max_workers=args.loaders) as pool:
			futures = [pool.submit(_morph_game, game, args) for game in games]
			for _ in concurrent.futures.as_completed(futures):
				progress.update(checking, advance=1)
	return games


def _morph_game(game: Game, args: MorphArgs) -> None:
	for rom in game.roms:
		for alg in supported_checks:
			if alg in args.checks:
				if rom.checks[alg] is None:
					file = Path(rom.romname)
					if file.exists():
						rom.checks[alg] = get_hash(file, alg)
					elif args.trim:
						game.status = GameStatus.MISSING
						return
			else:
				rom.checks[alg] = None
