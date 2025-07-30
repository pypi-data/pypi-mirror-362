from .base import ClientBase, object_to_id, parse_data

from ..objects import List, ListDeserializer, Status, Tag


class TimelineBase(ClientBase):
	async def hashtag_timeline(self,
							tag: Tag | str,
							any_tags: list[str] | None = None,
							all_tags: list[str] | None = None,
							no_tags: list[str] | None = None,
							only_local: bool = False,
							only_remote: bool = False,
							only_media: bool = False,
							min_id: int | None = None,
							max_id: int | None = None,
							since_id: int | None = None,
							limit: int = 20) -> list[Status]:

		tag = object_to_id(tag, "name")
		data = parse_data(
			any = any_tags,
			all = all_tags,
			none = no_tags,
			local = only_local,
			remote = only_remote,
			only_media = only_media,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id,
			limit = limit
		)

		return await self.send(
			"GET", f"/api/v1/timelines/tag/{tag}", ListDeserializer(Status), data
		)


	async def home_timeline(self,
							min_id: int | None = None,
							max_id: int | None = None,
							since_id: int | None = None,
							limit: int = 20) -> list[Status]:

		data = parse_data(
			min_id = min_id,
			max_id = max_id,
			since_id = since_id,
			limit = limit
		)

		return await self.send("GET", "/api/v1/timelines/home", ListDeserializer(Status), data)


	async def list_timeline(self,
							list_id: List | int | str,
							min_id: int | None = None,
							max_id: int | None = None,
							since_id: int | None = None,
							limit: int = 20) -> list[Status]:

		list_id = object_to_id(list_id)
		data = parse_data(
			min_id = min_id,
			max_id = max_id,
			since_id = since_id,
			limit = limit
		)

		return await self.send(
			"GET", f"/api/v1/timelines/list/{list_id}", ListDeserializer(Status), data
		)


	async def public_timeline(self,
							only_local: bool = False,
							only_remote: bool = False,
							only_media: bool = False,
							min_id: int | None = None,
							max_id: int | None = None,
							since_id: int | None = None,
							limit: int = 20) -> list[Status]:

		if only_local and only_remote:
			raise ValueError("only_local and only_remote are mutually exclusive")

		data = parse_data(
			local = only_local,
			remote = only_remote,
			only_media = only_media,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id,
			limit = limit
		)

		return await self.send("GET", "/api/v1/timelines/public", ListDeserializer(Status), data)
