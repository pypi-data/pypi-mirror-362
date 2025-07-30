from blib import Query
from datetime import datetime, timedelta

from .base import ClientBase, object_to_id, object_to_ids, parse_data

from ..base import ApiDate
from ..enums import StatusAction, VisibilityLevel
from ..objects import (
	Account,
	ListDeserializer,
	Media,
	ScheduledStatus,
	Status,
	StatusContext,
	StatusEdit,
	StatusSource,
	Translation
)


class StatusBase(ClientBase):
	async def account_statuses(self,
								acct: Account | int | str,
								min_id: int | None = None,
								max_id: int | None = None,
								since_id: int | None = None,
								limit: int = 20, # max 40
								only_media: bool = False,
								exclude_replies: bool = False,
								exclude_reblogs: bool = False,
								pinned: bool = False,
								tag: str | None = None) -> list[Status]:

		acct = object_to_id(acct)
		data = parse_data(
			limit = limit,
			only_media = only_media,
			exclude_replies = exclude_replies,
			exclude_reblogs = exclude_reblogs,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id,
			tagged = tag
		)

		return await self.send(
			"GET", f"/api/v1/accounts/{acct}/statuses", ListDeserializer(Status), data
		)


	async def bookmark(self, status: Status | int | str) -> Status:
		return await self.status_action(status, StatusAction.BOOKMARK)


	async def bookmarks(self,
					min_id: int | None = None,
					max_id: int | None = None,
					since_id: int | None = None,
					limit: int = 20) -> list[Status]:

		query = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send("GET", "/api/v1/bookmarks", ListDeserializer(Status), query = query)


	async def boost(self, status: Status | int | str) -> Status:
		return await self.status_action(status, StatusAction.BOOST)


	async def boosted_by(self, status: Status | int | str) -> list[Account]:
		status = object_to_id(status)
		return await self.send(
			"GET", f"/api/v1/statuses/{status}/reblogged_by", ListDeserializer(Account)
		)


	async def cancel_scheduled_status(self, status: Status | int | str) -> None:
		status = object_to_id(status)
		return await self.send("DELETE", f"/api/v1/scheduled_statuses/{status}", None)


	async def delete_status(self, status: Status | int | str) -> None:
		status = object_to_id(status)
		return await self.send("DELETE", f"/api/v1/statuses/{status}", None)


	async def favorite(self, status: Status | int | str) -> Status:
		return await self.status_action(status, StatusAction.FAVORITE)


	async def favorited_by(self, status: Status | int | str) -> list[Account]:
		status = object_to_id(status)
		return await self.send(
			"GET", f"/api/v1/statuses/{status}/favourited_by", ListDeserializer(Account)
		)


	async def favorites(self,
						min_id: int | None = None,
						max_id: int | None = None,
						since_id: int | None = None,
						limit: int = 20) -> list[Status]:

		query = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send("GET", "/api/v1/favourites", ListDeserializer(Status), query = query)


	async def mute(self, status: Status | int | str) -> Status:
		return await self.status_action(status, StatusAction.MUTE)


	async def new_scheduled_status(self,
					text: str,
					summary: str | None = None,
					reply_to: Status | int | str | None = None,
					media: list[Media | int | str] | None = None,
					sensitive: bool = False,
					poll_options: list[str] | None = None,
					poll_expires: timedelta | int | None = None,
					poll_multiple: bool = False,
					poll_hide_totals: bool = False,
					level: VisibilityLevel | None = None,
					language: str | None = None,
					scheduled_at: datetime | None = None,
					idempotency_key: str | None = None) -> Status:
		return Status()


	async def new_status(self,
					text: str,
					summary: str | None = None,
					reply_to: Status | int | str | None = None,
					media: list[Media | int | str] | None = None,
					sensitive: bool = False,
					poll_options: list[str] | None = None,
					poll_expires: timedelta | int | None = None,
					poll_multiple: bool = False,
					poll_hide_totals: bool = False,
					level: VisibilityLevel | None = None,
					language: str | None = None,
					scheduled_at: datetime | None = None,
					idempotency_key: str | None = None) -> Status:

		poll = None

		if poll_options:
			if isinstance(poll_expires, timedelta):
				poll_expires = poll_expires.seconds

			poll = parse_data(
				options = poll_options,
				expires_in = poll_expires,
				multiple = poll_multiple,
				hide_totals = poll_hide_totals
			)

		if reply_to is not None:
			reply_to = object_to_ids([reply_to])[0]

		data = parse_data(
			status = text,
			media_ids = object_to_ids(media or []) or None,
			poll = poll,
			in_reply_to_id = reply_to,
			sensitive = sensitive,
			spoiler_text = summary,
			language = language,
			visibility = VisibilityLevel.parse(level) if level is not None else level,
			scheduled_at = scheduled_at.isoformat() if scheduled_at is not None else scheduled_at
		)

		return await self.send("POST", "/api/v1/statuses", Status, data)


	async def pin(self, status: Status | int | str) -> Status:
		return await self.status_action(status, StatusAction.PIN)


	async def scheduled_status(self, id: int | str) -> ScheduledStatus:
		return await self.send("GET", f"/api/v1/scheduled_statuses/{id}", ScheduledStatus)


	async def scheduled_statuses(self,
								min_id: int | None = None,
								max_id: int | None = None,
								since_id: int | None = None,
								limit: int = 20) -> list[ScheduledStatus]:

		data = parse_data(
			min_id = min_id,
			max_id = max_id,
			since_id = since_id,
			limit = limit
		)

		return await self.send(
			"GET", "/api/v1/scheduled_statuses", ListDeserializer(ScheduledStatus), data
		)


	async def status(self, status_id: int | str) -> Status:
		return await self.send("GET", f"/api/v1/statuses/{status_id}", Status)


	async def status_action(self, status: Status | int | str, action: StatusAction | str) -> Status:
		status = object_to_id(status)
		action = StatusAction.parse(action)
		return await self.send("POST", f"/api/v1/statuses/{status}/{action}", Status)


	async def status_context(self, status: Status | int | str) -> StatusContext:
		status = object_to_id(status)
		return await self.send("GET", f"/api/v1/statuses/{status}/context", StatusContext)


	async def status_history(self, status: Status | int | str) -> list[StatusEdit]:
		status = object_to_id(status)
		return await self.send(
			"GET", f"/api/v1/statuses/{status}/history", ListDeserializer(StatusEdit)
		)


	async def status_source(self, status: Status | int | str) -> StatusSource:
		status = object_to_id(status)
		return await self.send("GET", f"/api/v1/statuses/{status}/source", StatusSource)


	async def statuses(self, *ids: int | str) -> list[Status]:
		data = Query()

		for item in ids:
			data.append("id[]", str(item))

		return await self.send("GET", "/api/v1/statuses", ListDeserializer(Status), query = data)


	async def translate_status(self,
							status: Status | int | str,
							lang: str | None = None) -> Translation:

		status = object_to_id(status)
		data = parse_data(lang = lang)
		return await self.send("POST", f"/api/v1/statuses/{status}/translate", Translation, data)


	async def unbookmark(self, status: Status | int | str) -> Status:
		return await self.status_action(status, StatusAction.UNBOOKMARK)


	async def unboost(self, status: Status | int | str) -> Status:
		return await self.status_action(status, StatusAction.UNBOOST)


	async def unfavorite(self, status: Status | int | str) -> Status:
		return await self.status_action(status, StatusAction.UNFAVORITE)


	async def unmute(self, status: Status | int | str) -> Status:
		return await self.status_action(status, StatusAction.UNMUTE)


	async def unpin(self, status: Status | int | str) -> Status:
		return await self.status_action(status, StatusAction.UNPIN)


	async def update_scheduled_status_date(self,
										status: Status | int | str,
										date: ApiDate | str) -> ScheduledStatus:

		status = object_to_id(status)
		data = {"scheduled_at": ApiDate.parse(date).to_string()}
		return await self.send("PUT", f"/api/v1/scheduled_statuses/{status}", ScheduledStatus, data)


	async def update_status(self,
					status: Status | int | str,
					text: str | None = None,
					summary: str | None = None,
					reply_to: Status | int | str | None = None,
					media: list[Media | int | str] | None = None,
					sensitive: bool = False,
					poll_options: list[str] | None = None,
					poll_expires: timedelta | int | None = None,
					poll_multiple: bool = False,
					poll_hide_totals: bool = False,
					level: VisibilityLevel | None = None,
					language: str | None = None,
					scheduled_at: datetime | None = None,
					idempotency_key: str | None = None) -> Status:

		status = object_to_id(status)
		poll = None

		if poll_options:
			if isinstance(poll_expires, timedelta):
				poll_expires = poll_expires.seconds

			poll = parse_data(
				options = poll_options,
				expires_in = poll_expires,
				multiple = poll_multiple,
				hide_totals = poll_hide_totals
			)

		if reply_to is not None:
			reply_to = object_to_ids([reply_to])[0]

		data = parse_data(
			status = text,
			media_ids = object_to_ids(media or []) or None,
			poll = poll,
			in_reply_to_id = reply_to,
			sensitive = sensitive,
			spoiler_text = summary,
			language = language,
			visibility = VisibilityLevel.parse(level) if level is not None else level,
			scheduled_at = scheduled_at.isoformat() if scheduled_at is not None else scheduled_at
		)

		return await self.send("PUT", f"/api/v1/statuses/{status}", Status, data)


	async def merp(self, text: str, summary: str | None = None) -> Status:
		"""
			Quickly blast your nonsense to the fediverse

			:param text: A random thought to bother the fediverse with
		"""

		data = parse_data(
			status = text,
			spoiler_text = summary
		)

		return await self.send("POST", "/api/v1/statuses", Status, data)
