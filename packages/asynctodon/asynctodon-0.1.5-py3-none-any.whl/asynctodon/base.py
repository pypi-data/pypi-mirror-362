from blib import Date
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Self


CODE_REDIRECT: str = "urn:ietf:wg:oauth:2.0:oob"


class ApiDate(Date):
	"""
		``Date`` class for API objects
	"""

	FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
	ALT_FORMATS: Sequence[str] = (
		"%Y-%m-%dT%H:%M:%S.%zZ",
		"%Y-%m-%d"
	)


	@classmethod
	def parse(cls: type[Self], date: datetime | str | int | float, try_iso: bool = True) -> Self:
		if isinstance(date, str):
			date = date.split(".", 1)[0]

		return super().parse(date)


# todo: create diffs for poll values and media descriptions
@dataclass
class StatusDiff:
	content: str
	spoiler_text: str
