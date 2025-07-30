# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from pyrom.hashes import supported_checks

if TYPE_CHECKING:  # pragma: no cover
	import xml.etree.ElementTree as ET
else:
	try:
		import lxml.etree as ET
	except ModuleNotFoundError:
		import xml.etree.ElementTree as ET

from pathlib import Path

from rich.progress import MofNCompleteColumn, Progress, SpinnerColumn

from pyrom.console import console, errconsole
from pyrom.game import Game, Rom


# TODO: multithreading
def parse_files(files: list[Path], quiet: bool = True) -> list[Game]:
	games: list[Game] = []
	with Progress(
		SpinnerColumn(),
		*Progress.get_default_columns(),
		MofNCompleteColumn(),
		console=console,
		disable=quiet,
	) as progress:
		task = progress.add_task("Parsing XML files", total=len(files))
		for file in files:
			match file.suffix:
				case ".xml" | ".dat":
					games.extend(parse_xml(file))
				case ".pyrom":
					games.extend(parse_custom_text(file))
				case _:
					errconsole.print(f"Unknown extension for file: {file}")
			progress.update(task, advance=1)
	return games


def parse_xml(file: Path) -> list[Game]:
	"""Parses a single DATfile into a list of Game entries"""
	games: list[Game] = []
	consolename: str | None = None
	roms: list[Rom] = []
	try:
		for _, el in ET.iterparse(file):
			match el.tag:
				case "name":
					consolename = el.text
				case "rom":
					at = el.attrib
					try:
						roms.append(
							Rom(
								at["name"],
								at.get("size"),
								at.get("crc"),
								at.get("md5"),
								at.get("sha1"),
								at.get("sha256"),
								at.get("xxh3"),
								at.get("b3"),
							)
						)
					except KeyError:  # Skip ROMS without a name - no way to check them anyway
						continue
					if not any(roms[-1].checks.values()):
						errconsole.print(
							f"Error in file '{file}': No hashes for rom '{at['name']}'"
						)
				case "game":
					at = el.attrib
					if len(roms) == 0:
						errconsole.print(
							f"Error in file '{file}': No roms for game {games[-1].name}"
						)
						continue

					games.append(
						Game(
							at.get("name") or "Unknown title",
							consolename or "Unknown",
							roms,
						)
					)
					roms = []
				case _:
					continue
	except ET.ParseError:
		return games

	return games


def parse_custom_text(file: Path) -> list[Game]:
	"""Parses a single PyRom file into a list of Game entries"""
	games: list[Game] = []
	roms: list[Rom] = []
	check_len = len(supported_checks)

	def nonel(string: str) -> str | None:
		return None if string == "None" else string

	lines: list[str]
	with open(file) as f:
		lines = f.readlines()
	i = 0
	while i < len(lines):
		match lines[i][0]:
			case "G":  # Game
				try:
					games.append(Game(lines[i + 1].rstrip(), lines[i + 2].rstrip(), roms))
					roms = []
					i += 3
				except TypeError:
					break
			case "R":  # Rom
				try:
					roms.append(
						Rom(
							lines[i + 1].rstrip(),
							*(nonel(line.rstrip()) for line in lines[i + 2 : i + 2 + check_len]),
						)
					)
					i += check_len + 2
				except TypeError:  # less lines than expected - return what we can
					break
			case _:  # Error
				errconsole.print(f"Error on line {i}")
				raise RuntimeError

	return games
