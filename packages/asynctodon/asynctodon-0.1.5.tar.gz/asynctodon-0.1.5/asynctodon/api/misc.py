from base64 import b64encode
from blib import File, Url
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

from .base import ClientBase, object_to_id, parse_data

from ..enums import SearchType, WebPushPolicy
from ..objects import (
	Account,
	Announcement,
	Conversation,
	Emoji,
	LinkTrend,
	ListDeserializer,
	Markers,
	Media,
	OEmbed,
	Poll,
	Search,
	Status,
	Tag,
	WebPushSubscription
)


@dataclass(slots = True)
class SearchQuery:
	text: str | None = None
	has_type: Literal["media", "poll", "embed"] | None = None
	is_type: Literal["reply", "sensitive"] | None = None
	in_type: Literal["library", "public"] | None = None
	language: str | None = None
	from_acct: Account | int | str | None = None
	before: datetime | None = None
	during: datetime | None = None
	after: datetime | None = None


	def to_str(self) -> str:
		items: list[str] = []

		data = parse_data(
			has_type = self.has_type,
			is_type = self.is_type,
			in_type = self.in_type,
			language = self.language,
			from_acct = self.from_acct,
			before = self.before,
			during = self.during,
			after = self.after,
			text = self.text
		)

		if not data:
			raise ValueError("Must specify at least one search option")

		for key, value in data.items():
			key = key.split("_", 1)[0]

			if isinstance(value, datetime):
				value = value.strftime("%Y-%m-%d")

			elif isinstance(value, Account):
				value = value.acct

			items.append(value if key == "text" else f"{key}:{value}")

		return " ".join(items)


class MiscBase(ClientBase):
	async def announcement_reaction(self,
									item: Announcement | int | str,
									emoji: Emoji | str) -> None:

		data = parse_data(
			item = object_to_id(item),
			emoji = object_to_id(emoji, "name")
		)

		await self.send("PUT", f"/api/v1/announcements/{item}/reactions/{emoji}", None, data)


	async def announcements(self) -> list[Announcement]:
		return await self.send("GET", "/api/v1/announcements", ListDeserializer(Announcement))


	async def conversations(self,
							min_id: int | None = None,
							max_id: int | None = None,
							since_id: int | None = None,
							limit: int = 20) -> list[Conversation]:

		data = parse_data(
			min_id = min_id,
			max_id = max_id,
			since_id = since_id,
			limit = limit
		)

		return await self.send(
			"GET", "/api/v1/conversations", ListDeserializer(Conversation), data
		)


	async def directory(self,
						limit: int = 40,
						offset: int | None = 0,
						order: Literal["active", "new"] = "active",
						local: bool = False) -> list[Account]:

		data = parse_data(
			limit = limit,
			offset = offset,
			order = order,
			local = local
		)

		return await self.send("GET", "/api/v1/directory", ListDeserializer(Account), data)


	async def dismiss_announcement(self, item: Announcement | int | str) -> None:
		item = object_to_id(item)
		return await self.send("POST", f"/api/v1/announcements/{item}/dissmiss", None)


	async def emojis(self) -> list[Emoji]:
		return await self.send(
			"GET", "/api/v1/custom_emojis", ListDeserializer(Emoji), token = False
		)


	async def mark_conversation_read(self, id: Conversation | int | str) -> Conversation:
		id = object_to_id(id)
		return await self.send("POST", f"/api/v1/conversations/{id}/read", Conversation)


	async def markers(self, home: bool = True, notifications: bool = True) -> Markers:
		if not home and not notifications:
			raise ValueError("Must specify at least one timeline")

		data = []

		if home:
			data.append("home")

		if notifications:
			data.append("notifications")

		return await self.send("GET", "/api/v1/markers", Markers, data)


	async def media(self, id: str | int) -> Media:
		return await self.send("GET", f"/api/v1/media/{id}", Media)


	async def oembed(self,
					url: Status | str,
					width: int | None = None,
					height: int | None = None) -> OEmbed:

		data = parse_data(
			url = object_to_id(url, "url"),
			width = width,
			height = height
		)

		return await self.send("GET", "/api/oembed", OEmbed, data, token = False)


	async def poll(self, id: str | int) -> Poll:
		return await self.send("GET", f"/api/v1/polls/{id}", Poll)


	async def push_subscribe(self,
							endpoint: str,
							pubkey: str,
							auth_secret: str,
							mention: bool = False,
							status: bool = False,
							boost: bool = False,
							follow: bool = False,
							follow_request: bool = False,
							favorite: bool = False,
							poll: bool = False,
							update: bool = False,
							sign_up: bool = False,
							report: bool = False,
							policy: WebPushPolicy | str = WebPushPolicy.ALL) -> WebPushSubscription:

		data = {
			"policy": policy,
			"subscription": {
				"endpoint": endpoint,
				"keys": {
					"p256dh": b64encode(pubkey.encode("utf8")).decode("utf-8"),
					"auth": auth_secret
				}
			},
			"data": {
				"mention": mention,
				"status": status,
				"reblog": boost,
				"follow": follow,
				"follow_request": follow_request,
				"favourite": favorite,
				"poll": poll,
				"update": update,
				"admin.sign_up": sign_up,
				"admin.report": report
			}
		}

		return await self.send("POST", "/api/v1/push/subscription", WebPushSubscription, data)


	async def push_subscription(self) -> WebPushSubscription:
		return await self.send("GET", "/api/v1/push/subscription", WebPushSubscription)


	async def remove_announcement_reaction(self,
									item: Announcement | int | str,
									emoji: Emoji | str) -> None:

		data = parse_data(
			item = object_to_id(item),
			emoji = object_to_id(emoji, "name")
		)

		await self.send("DELETE", f"/api/v1/announcements/{item}/reactions/{emoji}", None, data)


	async def remove_conversation(self, id: Conversation | int | str) -> None:
		id = object_to_id(id)
		await self.send("DELETE", f"/api/v1/conversations/{id}", None)


	async def remove_push_subscription(self) -> None:
		await self.send("DELETE", "/api/v1/push/subscription", None)


	async def search(self,
					query: SearchQuery | Url | str,
					type: SearchType | str | None = None,
					following: bool = False,
					acct: Account | int | str | None = None,
					exclude_unreviewed: bool = False,
					min_id: int | str | None = None,
					max_id: int | str | None = None,
					limit: int = 20,
					offset: int | None = None) -> Search | list[Account] | list[Tag] | list[Status]:

		type = SearchType.parse(type) if type is not None else type
		data = parse_data(
			q = query.to_str() if isinstance(query, SearchQuery) else query,
			type = type,
			following = following,
			account_id = object_to_id(acct),
			exclude_unreviewed = exclude_unreviewed,
			min_id = min_id,
			max_id = max_id,
			limit = limit,
			offset = offset,
			resolve = isinstance(query, str) and query.startswith(("https://", "http://"))
		)

		resp = await self.send("GET", "/api/v2/search", Search, data)

		if type == SearchType.ACCOUNTS:
			return resp.accounts

		if type == SearchType.HASHTAGS:
			return resp.hashtags

		if type == SearchType.STATUSES:
			return resp.statuses

		return resp


	async def set_marker(self,
						home: Status | int | str | None = None,
						notifications: Status | int | str | None = None) -> Markers:

		if home is None and notifications is None:
			raise ValueError("At least one timeline must be specified")

		data = {}

		if home is not None:
			data["home"] = {"last_read_id": object_to_id(home)}

		if notifications is not None:
			data["notifications"] = {"last_read_id": object_to_id(notifications)}

		return await self.send("POST", "/api/v1/markers", Markers, data)


	async def trending_links(self, limit: int = 10, offset: int = 0) -> list[LinkTrend]:
		data = {
			"limit": limit,
			"offset": offset
		}

		return await self.send("GET", "/api/v1/trends/links", ListDeserializer(LinkTrend), data)


	async def trending_statuses(self, limit: int = 10, offset: int = 0) -> list[Status]:
		data = {
			"limit": limit,
			"offset": offset
		}

		return await self.send("GET", "/api/v1/trends/statuses", ListDeserializer(Status), data)


	async def trending_tags(self, limit: int = 10, offset: int = 0) -> list[Tag]:
		data = {
			"limit": limit,
			"offset": offset
		}

		return await self.send("GET", "/api/v1/trends/tags", ListDeserializer(Tag), data)


	async def update_media(self,
						media: Media | int | str,
						thumbnail: File | Path | str | None = None,
						description: str | None = None,
						focus: tuple[float, float] | None = None) -> Media:

		media = object_to_id(media)

		if isinstance(thumbnail, (Path, str)):
			thumbnail = Path(thumbnail)

		data = parse_data(
			thumbnail = thumbnail.resolve() if thumbnail is not None else None,
			description = description,
			focus = ",".join(str(item) for item in focus) if focus is not None else None
		)

		return await self.send("PUT", f"/api/v2/media/{media}", Media, form = data)


	async def update_push_subscription(self,
							mention: bool = False,
							status: bool = False,
							boost: bool = False,
							follow: bool = False,
							follow_request: bool = False,
							favorite: bool = False,
							poll: bool = False,
							update: bool = False,
							sign_up: bool = False,
							report: bool = False,
							policy: WebPushPolicy | str = WebPushPolicy.ALL) -> WebPushSubscription:

		data = {
			"policy": policy,
			"data": {
				"mention": mention,
				"status": status,
				"reblog": boost,
				"follow": follow,
				"follow_request": follow_request,
				"favourite": favorite,
				"poll": poll,
				"update": update,
				"admin.sign_up": sign_up,
				"admin.report": report
			}
		}

		return await self.send("PUT", "/api/v1/push/subscription", WebPushSubscription, data)


	async def upload_media(self,
						path: File | Path | str,
						thumbnail: File | Path | str | None = None,
						description: str | None = None,
						focus: tuple[float, float] | None = None) -> Media:

		data = parse_data(
			file = File(str(path)).resolve(),
			thumbnail = File(str(thumbnail)).resolve() if thumbnail is not None else None,
			description = description,
			focus = ",".join(str(item) for item in focus) if focus is not None else None
		)

		return await self.send("POST", "/api/v2/media", Media, form = data)


	# todo: make sure this is how the endpoint actually works
	async def vote(self, poll: Poll | int | str, *choices: int) -> Poll:
		poll = object_to_id(poll)
		return await self.send("POST", f"/api/v1/polls/{poll}/votes", Poll, list(choices))
