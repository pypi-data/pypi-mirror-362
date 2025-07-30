# SPDX-FileCopyrightText: © 2025 Corn
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import final

from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme


@final
class ResultHighlighter(RegexHighlighter):
	"""Marks the OK/MISSING/FAIL strings"""

	base_style = "result."
	highlights = [  # noqa
		"(?P<ok>OK)",
		"(?P<miss>M[Ii][Ss]{2}[Ii][Nn][Gg])",
		"(?P<fail>F[Aa][Ii][Ll]([Ee][Dd])?)",
		r"(?P<not>N[Oo][Tt] ?[Cc][Hh][Ee][Cc][Kk][Ee][Dd])",
		r"(?P<skip>S[Kk][Ii][Pp]{2}[Ee][Dd])",
	]


theme = Theme(
	{
		"result.ok": "green",
		"result.miss": "yellow",
		"result.fail": "red",
		"result.not": "bright_blue",
		"result.skip": "bright_yellow",
	}
)
console = Console(highlighter=ResultHighlighter(), theme=theme)
if not console.is_terminal:
	console.soft_wrap = True
errconsole = Console(stderr=True)
if not errconsole.is_terminal:
	errconsole.soft_wrap = True
