# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum
from typing import Self, TypedDict, final, override


class GameStatus(Enum):
	NOTCHECKED = 0
	MISSING = 1
	FAILED = 2
	OK = 3
	SKIPPED = 4


class Checks(TypedDict):
	size: str | None
	crc: str | None
	md5: str | None
	sha1: str | None
	sha256: str | None
	xxh3: str | None
	b3: str | None


class Stats(TypedDict):
	size: GameStatus
	crc: GameStatus
	md5: GameStatus
	sha1: GameStatus
	sha256: GameStatus
	xxh3: GameStatus
	b3: GameStatus


@final
class LookupRom:
	"""Simpler Rom class for ROM name resolution"""

	def __init__(
		self,
		game: str,
		console: str,
		romname: str,
		size: str | None,
		crc: str | None,
		md5: str | None,
		sha1: str | None,
		sha256: str | None,
		xxh3: str | None = None,
		b3: str | None = None,
	) -> None:
		# Name of the file
		self.romname = romname
		# Results of checking the 'checks' fields
		self.checks: Checks = {
			"size": size,
			"crc": crc,
			"md5": md5,
			"sha1": sha1,
			"sha256": sha256,
			"xxh3": xxh3,
			"b3": b3,
		}
		# names of parent game/console
		self.game = game
		self.console = console

	@override
	def __repr__(self) -> str:  # pragma: no cover
		return f"LookupRom({self.game!r}, {self.console!r}, {self.romname!r}, **{self.checks!r})"

	@override
	def __str__(self) -> str:  # pragma: no cover
		return (
			f"Rom name: {self.romname!s}\n"
			f"Game name: {self.game!s}\n"
			f"Console name: {self.console!s}\n"
			f"Checks: {self.checks!s}\n"
		)


@final
class Rom:
	def __init__(
		self,
		romname: str,
		size: str | None,
		crc: str | None,
		md5: str | None,
		sha1: str | None,
		sha256: str | None,
		xxh3: str | None = None,
		b3: str | None = None,
	):
		# Name of the file
		self.romname = romname
		# Results of checking the 'checks' fields
		self.stats: Stats = {
			"size": GameStatus.NOTCHECKED,
			"crc": GameStatus.NOTCHECKED,
			"md5": GameStatus.NOTCHECKED,
			"sha1": GameStatus.NOTCHECKED,
			"sha256": GameStatus.NOTCHECKED,
			"xxh3": GameStatus.NOTCHECKED,
			"b3": GameStatus.NOTCHECKED,
		}
		# hash/size values
		self.checks: Checks = {
			"size": size,
			"crc": crc,
			"md5": md5,
			"sha1": sha1,
			"sha256": sha256,
			"xxh3": xxh3,
			"b3": b3,
		}
		# status of the ROM
		self.status = GameStatus.NOTCHECKED

	def result_string(self) -> str:  # pragma: no cover
		return (
			f"Rom name: {self.romname}\n"
			f"Size: {self.stats.get('size')}\n"
			f"CRC: {self.stats.get('crc')}\n"
			f"MD5: {self.stats.get('md5')}\n"
			f"SHA1: {self.stats.get('sha1')}\n"
			f"SHA2: {self.stats.get('sha256')}\n"
			f"XXH3: {self.stats.get('xxh3')}\n"
			f"BLAKE3: {self.stats.get('b3')}\n"
			f"Status: {self.status}\n"
		)

	@override
	def __repr__(self) -> str:  # pragma: no cover
		return f"Rom({self.romname!r}, **{self.checks!r})"

	@override
	def __str__(self) -> str:  # pragma: no cover
		return (
			f"Rom name: {self.romname!s}\n"
			f"Checks: {self.checks!s}\n"
			f"Stats: {self.stats!s}\n"
			f"Status: {self.status!s}"
		)

	def equals(self, other: Self) -> bool:
		"""Compare with another rom for equality of data (NOT STATUS)"""
		return self.romname == other.romname and self.checks == other.checks


@final
class Game:
	def __init__(self, name: str, console: str, roms: list[Rom]) -> None:
		# Name of the title
		self.name = name
		# Name of the console the game was developed for
		self.console = console
		# Files that form the game
		self.roms = roms
		# Overall status of the game
		self.status = GameStatus.NOTCHECKED

	@override
	def __str__(self) -> str:  # pragma: no cover
		res = f"Game: {self.name!s}\nSystem: {self.console!s}\nRoms: \n"
		for rom in self.roms:
			res = res + f"{rom!s}\n"
		return res.rstrip()

	@override
	def __repr__(self) -> str:  # pragma: no cover
		return f"Game({self.name!r}, {self.console!r}, {self.roms!r})"

	def equals(self, other: Self) -> bool:
		"""Compare with another rom for equality of data (NOT STATUS)"""
		return (
			self.name == other.name
			and self.console == other.console
			and len(self.roms) == len(other.roms)
			and all(roms[0].equals(roms[1]) for roms in zip(self.roms, other.roms, strict=True))
		)
