# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from xml.etree import ElementTree as ET

from rich.console import Console

from pyrom.args import MorphArgs, MyArgs
from pyrom.console import console
from pyrom.game import Game, GameStatus, LookupRom
from pyrom.hashes import supported_checks


def print_stats(games: list[Game], args: MyArgs) -> None:
	counts = [0, 0, 0, 0, 0]
	fails: list[Game] = []
	missing: list[Game] = []
	skipped: list[Game] = []
	for game in games:
		counts[game.status.value] += 1
		match game.status:
			case GameStatus.FAILED:
				fails.append(game)
			case GameStatus.MISSING:
				missing.append(game)
			case GameStatus.SKIPPED | GameStatus.NOTCHECKED:
				skipped.append(game)
			case GameStatus.OK:
				pass

	if args.machine:
		print_machine_stats(counts, fails, missing, skipped, args)
	else:
		print_human_stats(counts, fails, missing, skipped, args)


def print_machine_stats(
	counts: list[int], fails: list[Game], missing: list[Game], skipped: list[Game], args: MyArgs
) -> None:
	console = Console(color_system=None)

	root = ET.Element("pyrom")
	for arg, games, name in zip(
		[args.missing, args.skipped, args.failed],
		[missing, skipped, fails],
		["missing", "skipped", "failed"],
		strict=True,
	):
		if arg:
			el = ET.SubElement(root, name)
			for game in games:
				gameel = ET.SubElement(el, "game", {"name": f"{game.name}"})
				for rom in game.roms:
					_ = ET.SubElement(gameel, "rom", {"name": f"{rom.romname}"})

	if args.summary:
		total = ET.SubElement(root, "summary")
		for name, count in zip(
			["notch", "skipped", "missing", "failed", "ok"],
			[
				counts[GameStatus.NOTCHECKED.value],
				counts[GameStatus.SKIPPED.value],
				counts[GameStatus.MISSING.value],
				counts[GameStatus.FAILED.value],
				counts[GameStatus.OK.value],
			],
			strict=True,
		):
			_ = ET.SubElement(total, name, attrib={"count": f"{count}"})

	if args.output is None:
		console.print(ET.tostring(root, encoding="unicode"))
	else:
		with open(args.output, "w") as f:
			_ = f.write(ET.tostring(root, encoding="unicode"))


def print_human_stats(
	counts: list[int], fails: list[Game], missing: list[Game], skipped: list[Game], args: MyArgs
) -> None:
	for arg, games, name in zip(
		[args.missing, args.skipped, args.failed],
		[missing, skipped, fails],
		["Missing", "Skipped", "Failed"],
		strict=True,
	):
		if arg:
			console.rule(f"{name} games")
			for game in games:
				console.print(f"{game.console}:{game.name}")
				for rom in game.roms:
					console.print(rom.result_string())

	if args.summary:
		console.rule("Total stats")
		console.print(
			f"Not checked: {counts[GameStatus.NOTCHECKED.value]}\n",
			f"Skipped: {counts[GameStatus.SKIPPED.value]}\n",
			f"Missing: {counts[GameStatus.MISSING.value]}\n",
			f"Failed: {counts[GameStatus.FAILED.value]}\n",
			f"OK: {counts[GameStatus.OK.value]}",
			highlight=None,
			style=None,
		)
	console.rule()


def print_pairs(pairs: list[tuple[Path, list[LookupRom]]], output: Path | None = None) -> None:
	for filename, roms in pairs:
		if output is None:
			if len(roms) == 0:
				console.print(f"{filename}: No rom entry found")
			elif len(roms) == 1:
				rom = roms[0]
				console.print(f"'{filename}' -> '{rom.console}' | '{rom.romname}'")
			else:
				console.print(f"'{filename}' -> ", end="")
				for rom in roms:
					console.print(f"'{rom.console}' | '{rom.romname}'; ", end="")
				console.print()
		else:
			with open(output, "w") as f:
				if len(roms) == 0:
					_ = f.write(f"{filename}: No rom entry found\n")
				elif len(roms) == 1:
					rom = roms[0]
					_ = f.write(f"'{filename}' -> '{rom.console}' | '{rom.romname}'\n")
				else:
					_ = f.write(f"'{filename}' -> ")
					for rom in roms:
						_ = f.write(f"'{rom.console}' | '{rom.romname}'; ")
					_ = f.write("\n")


def print_pairs_machine(
	pairs: list[tuple[Path, list[LookupRom]]], output: Path | None = None
) -> None:
	root = ET.Element("pyrom-resolve")
	for file, cands in pairs:
		el = ET.SubElement(root, "ROM")
		el.text = str(file)
		for cand in cands:
			sel = ET.SubElement(el, "Candidate")
			sel.text = cand.romname
			sel.attrib["console"] = cand.console
	if output is None:
		print(ET.tostring(root, encoding="unicode"))
	else:
		with open(output, "w") as f:
			_ = f.write(ET.tostring(root, encoding="unicode"))
			_ = f.write("\n")


def print_datfile(games: list[Game], args: MorphArgs) -> None:
	root = ET.Element("datafile")
	header = ET.SubElement(root, "header")
	idh = ET.SubElement(header, "id")
	idh.text = "1"
	nameh = ET.SubElement(header, "name")
	nameh.text = "Mix of systems"
	_ = ET.SubElement(header, "description")
	_ = ET.SubElement(header, "version")
	auth = ET.SubElement(header, "author")
	auth.text = "PyRom"

	for game in games:
		gameel = ET.SubElement(root, "game", attrib={"name": game.name})
		descel = ET.SubElement(gameel, "description")
		descel.text = game.name
		for rom in game.roms:
			romel = ET.SubElement(gameel, "rom", attrib={"name": Path(rom.romname).name})
			for alg in args.checks:
				if rom.checks[alg] is None:
					continue
				romel.attrib[alg] = rom.checks[alg]
	if args.output is None:
		console.print(ET.tostring(root, encoding="unicode"))
	else:
		with open(args.output, "w") as f:
			_ = f.write(ET.tostring(root, encoding="unicode"))


def print_custom_textfile(games: list[Game], args: MorphArgs) -> None:
	if args.output is None:
		for game in games:
			for rom in game.roms:
				print("Rom")
				print(rom.romname)
				for v in supported_checks:
					print(rom.checks[v])
			print("Game")
			print(game.name)
			print(game.console)
	else:
		with open(args.output, "w") as f:
			for game in games:
				for rom in game.roms:
					_ = f.write("Rom\n")
					_ = f.write(rom.romname + "\n")
					for v in supported_checks:
						_ = f.write(str(rom.checks[v]) + "\n")
				_ = f.write("Game\n")
				_ = f.write(game.name + "\n")
				_ = f.write(game.console + "\n")
