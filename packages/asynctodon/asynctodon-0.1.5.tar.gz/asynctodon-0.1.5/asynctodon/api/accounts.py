from blib import JsonBase, Url
from collections.abc import Sequence
from typing import Any

from .base import ClientBase, object_to_id, object_to_ids, parse_data

from ..enums import AccountAction, ReportCategory, VisibilityLevel
from ..objects import (
	Account,
	List,
	ListDeserializer,
	Relationship,
	Report,
	Rule,
	Status,
	Suggestion
)


class AccountBase(ClientBase):
	async def account(self, acct_id: int | str) -> Account:
		return await self.send("GET", f"/api/v1/accounts/{acct_id}", Account)


	# added in 4.3.0
	async def accounts(self, *acct_ids: str) -> Account:
		data = {"id": acct_ids}
		return await self.send("GET", "/api/v1/accounts", Account, data)


	async def account_action(self,
							acct: Account | int | str,
							action: AccountAction | str,
							**kwargs: Any) -> Relationship:

		acct = object_to_id(acct)
		action = AccountAction.parse(action)
		return await self.send("POST", f"/api/v1/accounts/{acct}/{action}", Relationship, kwargs)


	async def account_lookup(self, handle: str) -> Account | None:
		query = {"acct": handle}
		return await self.send("GET", "/api/v1/accounts/lookup", Account, query = query)


	async def block_domain(self, domain: str) -> None:
		await self.send("POST", "/api/v1/domain_blocks", None, {"domain": domain})


	async def blocked_accounts(self,
						min_id: int | None = None,
						max_id: int | None = None,
						since_id: int | None = None,
						limit: int = 20) -> list[Account]:

		query = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send("GET", "/api/v1/blocks", ListDeserializer(Account), query = query)


	async def blocked_domains(self,
						min_id: int | None = None,
						max_id: int | None = None,
						since_id: int | None = None,
						limit: int = 20) -> list[str]:

		query = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send("GET", "/api/v1/domain_blocks", ListDeserializer(None), query = query)


	async def create_account(self,
							username: str,
							email: str,
							password: str,
							agree: bool,
							locale: str = "en",
							reason: str | None = None) -> None:

		data = parse_data(
			username = username,
			email = email,
			password = password,
			agreement = agree,
			locale = locale,
			reason = reason
		)

		await self.send("POST", "/api/v1/accounts", None, data)


	async def delete_avatar(self) -> Account:
		return await self.send("DELETE", "/api/v1/profile/header", Account)


	async def familiar_followers(self, *accts: Account | str | int) -> list[Relationship]:
		data = {
			"id": [str(acct.id if isinstance(acct, Account) else acct) for acct in accts],
		}

		return await self.send(
			"GET", "/api/v1/accounts/familiar_followers", ListDeserializer(Relationship), data
		)


	async def feature(self, acct: Account | int | str) -> Relationship:
		return await self.account_action(acct, AccountAction.FEATURE)


	async def featured_accounts(self,
						limit: int = 40,
						max_id: int | None = None,
						since_id: int | None = None) -> list[Account]:

		data = parse_data(
			limit = limit,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send("GET", "/api/v1/endorsements", ListDeserializer(Account), data)


	async def follow(self,
					acct: Account | int | str,
					reblogs: bool = True,
					notify: bool = False,
					languages: Sequence[str] | None = None) -> Relationship:

		data = parse_data(
			reblogs = reblogs,
			notify = notify,
			languages = list(languages) if languages is not None else None
		) or {}

		return await self.account_action(acct, AccountAction.FOLLOW, **data)


	async def follow_requests(self,
							limit: int = 40,
							min_id: int | None = None,
							max_id: int | None = None) -> list[Account]:

		data = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id
		)

		return await self.send("GET", "/api/v1/follow_requests", ListDeserializer(Account), data)


	async def followers(self,
									acct: Account | int | str,
									min_id: int | None = None,
									max_id: int | None = None,
									since_id: int | None = None,
									limit: int = 40) -> list[Account]: # max 80

		acct = object_to_id(acct)
		data = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send(
			"GET", f"/api/v1/accounts/{acct}/followers", ListDeserializer(Account), data
		)


	async def following(self,
					acct: Account | int | str,
					min_id: int | None = None,
					max_id: int | None = None,
					since_id: int | None = None,
					limit: int = 40) -> list[Account]: # max 80

		acct = object_to_id(acct)
		data = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send(
			"GET", f"/api/v1/accounts/{acct}/following", ListDeserializer(Account), data
		)


	async def lists_containing_account(self, acct: Account | int | str) -> list[List]:
		acct = object_to_id(acct)
		return await self.send("GET", f"/api/v1/accounts/{acct}/lists", ListDeserializer(List))


	async def me(self) -> Account:
		return await self.send("GET", "/api/v1/accounts/verify_credentials", Account)


	async def mute_account(self, acct: Account | int | str) -> Relationship:
		return await self.account_action(acct, AccountAction.MUTE)


	async def muted_accounts(self,
						min_id: int | None = None,
						max_id: int | None = None,
						since_id: int | None = None,
						limit: int = 20) -> list[Account]:

		query = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send("GET", "/api/v1/mutes", ListDeserializer(Account), query = query)


	async def preferences(self) -> JsonBase[Any]:
		return await self.send("GET", "/api/v1/preferences", JsonBase)


	async def relationships(self,
						*accts: Account | str | int,
						with_suspended: bool = False) -> list[Relationship]:

		data = {
			"id": [str(acct.id if isinstance(acct, Account) else acct) for acct in accts],
			"with_suspended": with_suspended
		}

		return await self.send(
			"GET", "/api/v1/accounts/relationships", ListDeserializer(Relationship), data
		)


	async def remove_follower(self, acct: Account | int | str) -> Relationship:
		acct = object_to_id(acct)
		return await self.send(
			"POST", f"/api/v1/accounts/{acct}/remove_from_followers", Relationship
		)


	async def remove_suggested_account(self, acct: Account | int | str) -> None:
		acct = object_to_id(acct)
		await self.send("DELETE", f"/api/v2/suggestions/{acct}", None)


	async def report_user(self,
					acct: Account | int | str,
					statuses: list[Status | int | str] | None = None,
					rules: list[Rule | int | str] | None = None,
					comment: str | None = None,
					forward: bool = False,
					category: ReportCategory = ReportCategory.OTHER) -> Report:

		data = parse_data(
			account_id = object_to_id(acct),
			status_ids = object_to_ids(statuses or []) or None,
			comment = comment,
			forward = forward,
			category = category if not rules else ReportCategory.VIOLATION,
			rule_ids = object_to_ids(rules or []) or None
		)

		return await self.send("POST", "/api/v1/reports", Report, data)


	async def response_to_request(self, acct: Account | int | str, accept: bool) -> Relationship:
		if isinstance(acct, Account):
			acct = acct.id

		action = "authorize" if accept else "reject"
		return await self.send("POST", f"/api/v1/follow_requests/{acct}/{action}", Relationship)


	# resolve parameter does nothing
	async def search_accounts(self,
					query: Url | str,
					limit: int = 40,
					offset: int | None = None,
					following: bool = False) -> list[Account]:

		data = parse_data(
			q = query,
			limit = str(limit),
			offset = offset,
			following = str(following).lower(),
			resolve = str(isinstance(query, Url) or query.startswith(("https://", "http://"))).lower()
		)

		return await self.send(
			"GET", "/api/v1/accounts/search", ListDeserializer(Account), query = data
		)


	async def set_account_note(self, acct: Account | int | str, note: str | None) -> Relationship:
		acct = object_to_id(acct)
		params = {"comment": note or ""}
		return await self.send("POST", f"/api/v1/accounts/{acct}/note", Relationship, params)


	async def suggested_accounts(self, limit: int = 40) -> list[Suggestion]:
		data = {"limit": limit}
		return await self.send("GET", "/api/v2/suggestions", ListDeserializer(Suggestion), data)


	async def unblock_domain(self, domain: str) -> None:
		await self.send("DELETE", "/api/v1/domain_blocks", None, {"domain": domain})


	async def unfeature(self, acct: Account | int | str) -> Relationship:
		return await self.account_action(acct, AccountAction.UNFEATURE)


	async def unfollow(self, acct: Account | int | str) -> Relationship:
		return await self.account_action(acct, AccountAction.UNFOLLOW)


	async def unmute_account(self, acct: Account | int | str) -> Relationship:
		return await self.account_action(acct, AccountAction.UNMUTE)


	async def update_account(self,
							display_name: str | None = None,
							bio: str | None = None,
							avatar: Any = None,
							header: Any = None,
							locked: bool | None = None,
							bot: bool | None = None,
							discoverable: bool | None = None,
							hide_relationships: bool | None = None,
							indexable: bool | None = None,
							default_post_level: VisibilityLevel | str | None = None,
							default_sensitive: bool | None = None,
							default_language: str | None = None,
							fields: dict[str, str] | None = None) -> Account:

		if default_post_level is not None:
			if isinstance(default_post_level, str):
				default_post_level = VisibilityLevel.parse(default_post_level)

			if default_post_level == VisibilityLevel.DIRECT:
				raise ValueError("Default post level cannot be 'direct'")

		data = parse_data(
			display_name = display_name,
			note = bio,
			locked = locked,
			bot = bot,
			hide_collections = hide_relationships,
			indexable = indexable,
			source = parse_data(
				privacy = default_post_level,
				sensitive = default_sensitive
			)
		)

		if fields is not None:
			if data is None:
				data = {}

			data["fields_attributes"] = {}

			for idx, item in enumerate(fields.items()):
				data[str(idx)] = {
					"name": item[0],
					"value": item[1]
				}

		return await self.send("PATCH", "/api/v1/accounts/update_credentials", Account, data)
