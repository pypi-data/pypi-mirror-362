# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable


def only_one_of[T](values: list[T], expr: Callable[[T], bool]) -> T | None:
	one = None
	for val in values:
		if expr(val):
			if one is None:
				one = val
			else:
				return None
	return one


def all_of[T](real: list[T], exp: set[T]) -> bool:
	res = True
	for st in real:
		if st not in exp:
			res = False
			break
	return res
