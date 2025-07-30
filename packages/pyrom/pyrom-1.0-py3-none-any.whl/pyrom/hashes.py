# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

from hashlib import file_digest
from pathlib import Path
from typing import BinaryIO
from zlib import crc32

default_checks = ("size", "crc", "md5", "sha1", "sha256")
available_checks = default_checks
supported_checks = ("size", "crc", "md5", "sha1", "sha256", "xxh3", "b3")

try:
	from xxhash import xxh3_128_hexdigest

	available_checks = (*available_checks, "xxh3")
except ModuleNotFoundError:
	xxh3_128_hexdigest = None

try:
	from blake3 import blake3

	available_checks = (*available_checks, "b3")
except ModuleNotFoundError:
	blake3 = None


def _crc32(file: BinaryIO) -> str:
	"""Takes a file object and returns the CRC32 checksum (lowercase) of the file."""
	_ = file.seek(0)  # reset to start, just in case
	result = 0
	while data := file.read(1024**2):
		result = crc32(data, result)
	return f"{result:08X}".lower()


def get_hash(file: Path, alg: str) -> str | None:
	"""
	Hash a file with the given algorithm (or return the file size)
	paramater alg must be from available_checks
	"""
	match alg:
		case "size":
			realdig = str(file.stat().st_size)
		case "crc":
			with open(file, "rb") as f:
				realdig = _crc32(f)
		case "md5" | "sha1" | "sha256":
			with open(file, "rb") as f:
				realdig = file_digest(f, alg).hexdigest()
		case "xxh3":
			if xxh3_128_hexdigest is None:
				realdig = None
			else:
				with open(file, "rb") as f:
					realdig = xxh3_128_hexdigest(f.read())
		case "b3":
			if blake3 is None:
				realdig = None
			else:
				with open(file, "rb") as f:
					realdig = blake3(f.read()).hexdigest()
		case _:
			raise RuntimeError("Internal error: invalid hashing algorithm specified")
	return realdig
