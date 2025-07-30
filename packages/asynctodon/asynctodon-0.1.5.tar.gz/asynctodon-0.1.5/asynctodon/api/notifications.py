from collections.abc import Sequence

from .base import ClientBase, object_to_id, parse_data

from ..enums import NotificationType
from ..objects import (
	Account,
	ListDeserializer,
	Notification,
	NotificationPolicy,
	NotificationRequest
)


class NotificationBase(ClientBase):
	# missing api endpoint in docs, so this is just an educated guess
	async def accept_notification_request(self, notif: Notification | int | str) -> None:
		notif = object_to_id(notif)
		return await self.send("POST", f"/api/v1/notifications/requests/:{notif}/accept", None)


	async def deny_notification_request(self, notif: Notification | int | str) -> None:
		notif = object_to_id(notif)
		return await self.send("POST", f"/api/v1/notifications/requests/:{notif}/dismiss", None)


	async def notification(self, id: int | str) -> Notification:
		return await self.send("GET", f"/api/v1/notifications/{id}", Notification)


	async def notification_policy(self) -> NotificationPolicy:
		return await self.send("GET", "/api/v1/notification/policy", NotificationPolicy)


	async def notification_request(self, id: int | str) -> NotificationRequest:
		return await self.send("GET", f"/api/v1/notifications/requests/{id}", NotificationRequest)


	async def notification_requests(self,
									min_id: int | None = None,
									max_id: int | None = None,
									since_id: int | None = None,
									limit: int = 40,
									dismissed: bool = False) -> list[NotificationRequest]:

		data = parse_data(
			min_id = min_id,
			max_id = max_id,
			since_id = since_id,
			limit = limit,
			dismissed = dismissed
		)

		return await self.send(
			"GET", "/api/v1/notifications/requests", ListDeserializer(NotificationRequest), data
		)


	async def notifications(self,
					min_id: int | None = None,
					max_id: int | None = None,
					since_id: int | None = None,
					limit: int = 40,
					acct: Account | int | str | None = None,
					types: Sequence[NotificationType | str] | None = None,
					exclude: Sequence[NotificationType | str] | None = None) -> list[Notification]:

		data = parse_data(
			min_id = min_id,
			max_id = max_id,
			since_id = since_id,
			limit = limit,
			account_id = object_to_id(acct),
			types = [NotificationType.parse(item) for item in types] if types else None,
			exclude_types = [NotificationType.parse(item) for item in exclude] if exclude else None
		)

		return await self.send("GET", "/api/v1/notifications", ListDeserializer(Notification), data)


	async def remove_all_notifications(self) -> None:
		await self.send("POST", "/api/v1/notifications/clear", None)


	async def remove_notification(self, notif: Notification | int | str) -> None:
		notif = object_to_id(notif)
		await self.send("POST", f"/api/v1/notifications/{notif}/dismiss", None)


	async def update_notification_policy(self,
										not_following: bool | None = None,
										not_followers: bool | None = None,
										new_accounts: bool | None = None,
										private_mentions: bool | None = None) -> NotificationPolicy:

		data = parse_data(
			filter_not_following = not_following,
			filter_not_followers = not_followers,
			filter_new_accounts = new_accounts,
			filter_private_mentions = private_mentions
		)

		return await self.send("PUT", "/api/v1/notifications/policy", NotificationPolicy, data)
