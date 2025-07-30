from .base import ClientBase, object_to_id, parse_data

from ..enums import ListReplyPolicy
from ..objects import Account, List, ListDeserializer


class ListBase(ClientBase):
	async def create_list(self,
						title: str,
						replies_policy: ListReplyPolicy = ListReplyPolicy.LIST,
						exclusive: bool = False) -> List:

		data = {
			"title": title,
			"replies_policy": replies_policy,
			"exclusive": exclusive
		}

		return await self.send("POST", "/api/v1/lists", List, data = data)


	async def delete_list(self, id: List | int | str) -> None:
		id = object_to_id(id)
		return await self.send("DELETE", f"/api/v1/lists/{id}", None)


	async def get_list(self, id: int | str) -> List:
		return await self.send("GET", f"/api/v1/lists/{id}", List)


	async def list_add_accounts(self, id: List | int | str, *accts: Account | int | str) -> None:
		if not accts:
			raise ValueError("Must specify at least one account")

		id = object_to_id(id)
		data = [object_to_id(acct) for acct in accts]
		return await self.send("POST", f"/api/v1/lists/{id}/accounts", None, data)


	async def list_remove_accounts(self, id: List | int | str, *accts: Account | int | str) -> None:
		if not accts:
			raise ValueError("Must specify at least one account")

		id = object_to_id(id)
		data = [object_to_id(acct) for acct in accts]
		return await self.send("DELETE", f"/api/v1/lists/{id}/accounts", None, data)


	async def list_accounts(self,
							id: List | int | str,
							min_id: int | None = None,
							max_id: int | None = None,
							since_id: int | None = None,
							limit: int = 40) -> list[Account]:

		id = object_to_id(id)
		data = parse_data(
			min_id = min_id,
			max_id = max_id,
			since_id = since_id,
			limit = limit
		)

		return await self.send(
			"PUT", f"/api/v1/lists/{id}/accounts", ListDeserializer(Account), data
		)


	async def lists(self) -> list[List]:
		return await self.send("GET", "/api/v1/lists", ListDeserializer(List))


	async def update_list(self,
						id: List | int | str,
						title: str | None,
						replies_policy: ListReplyPolicy | None = None,
						exclusive: bool | None = None) -> List:

		id = object_to_id(id)
		data = parse_data(
			title = title,
			replies_policy = replies_policy,
			exclusive = exclusive
		)

		if not data:
			raise ValueError("Must specify at least one parameter to change")

		return await self.send("PUT", f"/api/v1/lists/{id}", List, data)
