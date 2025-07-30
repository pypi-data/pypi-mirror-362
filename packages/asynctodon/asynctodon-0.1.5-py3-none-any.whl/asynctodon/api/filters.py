from typing import Literal

from .base import ClientBase, object_to_id, parse_data

from ..enums import MuteContext
from ..objects import Filter, FilterKeyword, FilterStatus, ListDeserializer, Status


class FilterBase(ClientBase):
	async def add_filter_keyword(self,
								filter: Filter | int | str,
								keyword: str,
								whole_word: bool = False) -> FilterKeyword:

		filter = object_to_id(filter)
		data = {
			"keyword": keyword,
			"whole_word": whole_word
		}

		return await self.send("POST", f"/api/v2/filters/{filter}/keywords", FilterKeyword, data)


	async def add_status_to_filter(self,
								filter: Filter | str | int,
								status: Status | str | int) -> FilterStatus:

		filter = object_to_id(filter)
		data = {
			"status_id": object_to_id(status)
		}

		return await self.send("POST", f"/api/v2/filters/{filter}/statuses", FilterStatus, data)


	async def delete_filter(self, filter: Filter | int | str) -> None:
		filter = object_to_id(filter)
		await self.send("DELETE", f"/api/v2/filters/{filter}", None)


	async def filter(self, id: int | str) -> Filter:
		return await self.send("GET", f"/api/v2/filters/{id}", Filter)


	async def filters(self) -> list[Filter]:
		return await self.send("GET", "/api/v2/filters", ListDeserializer(Filter))


	async def filter_keyword(self, id: int | str) -> FilterKeyword:
		return await self.send("GET", f"/api/v2/filters/keywords/{id}", FilterKeyword)


	async def filter_keywords(self, id: int | str) -> list[FilterKeyword]:
		return await self.send(
			"GET", "/api/v2/filters/{id}/keywords", ListDeserializer(FilterKeyword)
		)


	async def filtered_status(self, id: int | str) -> FilterStatus:
		return await self.send("GET", f"/api/v2/filters/statuses/{id}", FilterStatus)


	async def filtered_statuses(self, filter: Filter | int | str) -> list[FilterStatus]:
		filter = filter = object_to_id(filter)
		return await self.send(
			"GET", f"/api/v2/filters/{filter}/statuses", ListDeserializer(FilterStatus)
		)


	async def new_filter(self,
						title: str,
						keywords: dict[str, bool],
						context: list[MuteContext | str],
						action: Literal["warn", "hide"] = "warn",
						expires_in: int | None = None) -> Filter:

		# keywords: word, match whole world

		keyword_data = []

		for keyword, whole_word in keywords.items():
			keyword_data.append({
				"keyword": keyword,
				"whole_word": whole_word
			})

		data = parse_data(
			title = title,
			keywords = keywords,
			filter_action = action,
			expires_in = expires_in,
			keywords_attributes = keyword_data
		)

		return await self.send("POST", "/api/v2/filters", Filter, data)


	async def remove_filter_keyword(self, keyword: FilterKeyword | int | str) -> None:
		keyword = object_to_id(keyword)
		await self.send("DELETE", f"/api/v2/filters/keywords/{keyword}", None)


	async def remove_status_from_filter(self, status: FilterStatus | str | int) -> None:
		status = object_to_id(status)
		await self.send("DELETE", f"/api/v2/filters/statuses/{status}", None)


	# todo: handle updating/deleting existing keywords
	async def update_filter(self,
						filter: Filter | int | str,
						title: str | None = None,
						keywords: dict[str, bool] | None = None,
						context: list[MuteContext | str] | None = None,
						action: Literal["warn", "hide"] | None = None,
						expires_in: int | None = None) -> Filter:

		if keywords is not None:
			keyword_data = []

			for keyword, whole_word in keywords.items():
				keyword_data.append({
					"keyword": keyword,
					"whole_word": whole_word
				})

		else:
			keyword_data = None

		filter = object_to_id(filter)
		data = parse_data(
			title = title,
			keywords = keywords,
			filter_action = action,
			expires_in = expires_in,
			keywords_attributes = keyword_data
		)

		return await self.send("PUT", f"/api/v2/filters/{filter}", Filter, data)


	async def update_filter_keyword(self,
									filter_keyword: FilterKeyword | int | str,
									keyword: str,
									whole_word: bool = False) -> FilterKeyword:

		filter_keyword = object_to_id(keyword)
		data = {
			"keyword": keyword,
			"whole_word": whole_word
		}

		return await self.send(
			"PUT", f"/api/v2/filters/keywords/{filter_keyword}", FilterKeyword, data
		)
