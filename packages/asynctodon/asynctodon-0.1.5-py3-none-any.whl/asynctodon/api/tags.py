from .base import ClientBase, object_to_id, parse_data

from ..objects import Account, FeaturedTag, ListDeserializer, Tag


class TagBase(ClientBase):
	async def featured_account_tags(self, acct: Account | int | str) -> list[FeaturedTag]:
		acct = object_to_id(acct)
		return await self.send(
			"GET",
			f"/api/v1/accounts/{acct}/featured_tags",
			ListDeserializer[FeaturedTag](FeaturedTag)
		)


	async def featured_tags(self) -> list[FeaturedTag]:
		return await self.send("GET", "/api/v1/featured_tags", ListDeserializer(FeaturedTag))


	async def feature_tag(self, name: str) -> FeaturedTag:
		if name.startswith("#"):
			name = name[1:]

		return await self.send("POST", "/api/v1/featured_tags", FeaturedTag, {"name": name})


	async def follow_tag(self, tag: Tag | int | str) -> Tag:
		tag = object_to_id(tag, "name")
		return await self.send("POST", f"/api/v1/tags/{tag}/follow", Tag)


	async def followed_tags(self,
							limit: int = 100,
							min_id: int | None = None,
							max_id: int | None = None,
							since_id: int | None = None) -> list[Tag]:

		data = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send("GET", "/api/v1/followed_tags", ListDeserializer(Tag), data)


	async def suggested_tags(self) -> list[FeaturedTag]:
		return await self.send(
			"GET", "/api/v1/featured_tags/suggestions", ListDeserializer(FeaturedTag)
		)


	async def tag(self, id: str) -> Tag:
		return await self.send("GET", f"/api/v1/tags/{id}", Tag)


	async def unfeature_tag(self, tag: FeaturedTag | int | str) -> None:
		tag = object_to_id(tag)
		await self.send("DELETE", f"/api/v1/feature_tags/{tag}", None)


	async def unfollow_tag(self, tag: Tag | int | str) -> Tag:
		tag = object_to_id(tag, "name")
		return await self.send("POST", f"/api/v1/tags/{tag}/unfollow", Tag)
