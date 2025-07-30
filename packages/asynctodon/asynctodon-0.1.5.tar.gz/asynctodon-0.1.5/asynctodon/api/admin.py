from collections.abc import AsyncIterable, Sequence
from typing import Literal

from .base import ClientBase, object_to_id, parse_data

from ..enums import AccountStatus, AdminAccountAction, BlockSeverity
from ..objects import (
	AdminAccount,
	AdminDomainAllow,
	AdminDomainBlock,
	AdminEmailBlock,
	AdminReport,
	ListDeserializer,
	ObjectBase,
	Role
)


ORIGIN_VALUES = Literal["local", "remote"]


# remove when implemented
class AdminWarningPreset(ObjectBase):
	pass


class AdminBase(ClientBase):
	async def admin_account(self, id: str) -> AdminAccount:
		return await self.send("GET", f"/api/v1/admin/accounts/{id}", AdminAccount)


	async def admin_account_action(self,
								id: AdminAccount | str,
								type: AdminAccountAction | str,
								report: AdminReport | str | None = None,
								warning_preset: AdminWarningPreset | str | None = None,
								text: str | None = None,
								send_email_notification: bool = True) -> None:

		id = object_to_id(id)
		data = parse_data(
			type = AdminAccountAction.parse(type),
			report_id = object_to_id(report),
			warning_preset_id = object_to_id(warning_preset),
			text = text,
			send_email_notification = send_email_notification
		)

		await self.send("POST", f"/api/v1/admin/accounts/{id}/action", None, data)


	async def admin_account_action_revert(self,
										id: AdminAccount | str,
										type: AdminAccountAction | str) -> AdminAccount:

		id = object_to_id(id)

		match AdminAccountAction.parse(type):
			case AdminAccountAction.DISABLE:
				action = "enable"

			case AdminAccountAction.SENSITIVE:
				action = "unsensitive"

			case AdminAccountAction.SUSPEND:
				action = "unsuspend"

			case AdminAccountAction.SILENCE:
				action = "unsilence"

			case _:
				raise ValueError("Invalid account action")

		return await self.send("POST", f"/api/v1/admin/accounts/{id}/{action}", AdminAccount)


	async def admin_account_delete(self, id: AdminAccount | str) -> AdminAccount:
		id = object_to_id(id)
		return await self.send("DELETE", f"/api/v1/admin/accounts/{id}", AdminAccount)


	async def admin_account_response(self, id: AdminAccount | str, approve: bool) -> AdminAccount:
		id = object_to_id(id)
		response = "approve" if approve else "reject"
		return await self.send("POST", f"/api/v1/admin/accounts/{id}/{response}", AdminAccount)


	async def admin_accounts(self,
							origin: ORIGIN_VALUES | None = None,
							status: AccountStatus | str | None = None,
							permissions: str | None = None,
							roles: Sequence[Role | str] | None = None,
							invited_by: AdminAccount | str | None = None,
							username: str | None = None,
							display_name: str | None = None,
							domain: str | None = None,
							email: str | None = None,
							ip: str | None = None,
							max_id: str | None = None,
							min_id: str | None = None,
							since_id: str | None = None,
							limit: int = 100) -> list[AdminAccount]:

		data = parse_data(
			origin = origin,
			status = AccountStatus.parse(status) if status else None,
			permissions = permissions,
			role_ids = [object_to_id(v) for v in roles] if roles is not None else None,
			invited_by = object_to_id(invited_by),
			username = username,
			display_name = display_name,
			by_domain = domain,
			email = email,
			ip = ip,
			max_id = max_id,
			min_id = min_id,
			since_id = since_id,
			limit = limit
		)

		return await self.send(
			"GET", "/api/v2/admin/accounts", ListDeserializer(AdminAccount), data
		)


	# async def admin_dimensions() -> AdminDimension


	async def admin_block_domain(self,
						domain: str,
						severity: BlockSeverity | str = BlockSeverity.SILENCE,
						reject_media: bool = False,
						reject_reports: bool = False,
						private_comment: str | None = None,
						public_comment: str | None = None,
						obfuscate: bool = False) -> AdminDomainBlock:

		data = parse_data(
			domain = domain,
			severity = BlockSeverity.parse(severity),
			reject_media = reject_media,
			reject_reports = reject_reports,
			private_comment = private_comment,
			public_comment = public_comment,
			obfuscate = obfuscate
		)

		return await self.send("POST", "/api/v1/admin/domain_blocks", AdminDomainBlock, data)


	async def admin_allow_domain(self, domain: str) -> AdminDomainAllow:
		params = {"domain": domain}
		return await self.send("POST", "/api/v1/admin/domain_allows", AdminDomainAllow, params)


	async def admin_domain_allow(self, allow_id: int | str) -> AdminDomainAllow:
		return await self.send("GET", f"/api/v1/admin/domain_allows/{allow_id}", AdminDomainAllow)


	async def admin_domain_allows(self,
						min_id: int | None = None,
						max_id: int | None = None,
						since_id: int | None = None,
						limit: int = 100) -> list[AdminDomainAllow]:

		assert 0 <= limit <= 200, "Limit range must be 0 - 200"

		query = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send(
			"GET", "/api/v1/admin/domain_allows", ListDeserializer(AdminDomainAllow), query = query
		)


	async def admin_domain_block(self, block_id: int | str) -> AdminDomainBlock:
		return await self.send("GET", f"/api/v1/admin/domain_blocks/{block_id}", AdminDomainBlock)


	async def admin_domain_unblock(self, block_id: int | str) -> AdminDomainBlock:
		return await self.send(
			"DELETE", f"/api/v1/admin/domain_blocks/{block_id}", AdminDomainBlock
		)


	async def admin_domain_blocks(self,
						min_id: int | None = None,
						max_id: int | None = None,
						since_id: int | None = None,
						limit: int = 100) -> list[AdminDomainBlock]:

		assert 0 <= limit <= 200, "Limit range must be 0 - 200"

		query = parse_data(
			limit = limit,
			min_id = min_id,
			max_id = max_id,
			since_id = since_id
		)

		return await self.send(
			"GET", "/api/v1/admin/domain_blocks", ListDeserializer(AdminDomainBlock), query = query
		)


	async def admin_email_block(self, id: str) -> AdminEmailBlock:
		return await self.send("GET", f"/api/v1/admin/canonical_email_blocks/{id}", AdminEmailBlock)


	async def admin_email_block_add(self,
									email: str | None = None,
									hashdata: str | None = None) -> AdminEmailBlock:

		if not email and not hashdata:
			raise ValueError("Must provide email or hashdata")

		data = parse_data(
			email = email,
			canonical_email_hash = hashdata
		)

		return await self.send(
			"POST", "/api/v1/admin/canonical_email_blocks", AdminEmailBlock, data
		)


	async def admin_email_block_delete(self, id: AdminEmailBlock | str) -> None:
		id = object_to_id(id)
		return await self.send("DELETE", f"/api/v1/admin/canonical_email_blocks/{id}", None)


	async def admin_email_block_test(self, email: str) -> list[AdminEmailBlock]:
		return await self.send(
			"POST", "/api/v1/admin/canonical_email_blocks/test",
			ListDeserializer(AdminEmailBlock),
			{"email": email}
		)


	async def admin_email_blocks(self,
								max_id: str | None = None,
								min_id: str | None = None,
								limit: str | None = None,
								since_id: str | None = None) -> list[AdminEmailBlock]:

		return await self.send(
			"GET", "/api/v1/admin/canonical_email_blocks", ListDeserializer(AdminEmailBlock)
		)


	async def admin_update_domain(self,
						block: AdminDomainBlock | int | str,
						severity: BlockSeverity | str | None = None,
						reject_media: bool | None = None,
						reject_reports: bool | None = None,
						private_comment: str | None = None,
						public_comment: str | None = None,
						obfuscate: bool | None = None) -> AdminDomainBlock:

		block_id = object_to_id(block)
		data = parse_data(
			severity = BlockSeverity.parse(severity) if severity else None,
			reject_media = reject_media,
			reject_reports = reject_reports,
			private_comment = private_comment,
			public_comment = public_comment,
			obfuscate = obfuscate
		)

		return await self.send(
			"PUT", f"/api/v1/admin/domain_blocks/{block_id}", AdminDomainBlock, data
		)


	async def admin_unallow_domain(self, allow: AdminDomainAllow | int | str) -> AdminDomainAllow:
		return await self.send(
			"DELETE", f"/api/v1/admin/domain_allows/{object_to_id(allow)}", AdminDomainAllow
		)


	async def admin_unblock_domain(self, block: AdminDomainBlock | int | str) -> AdminDomainBlock:
		return await self.send(
			"DELETE", f"/api/v1/admin/domain_blocks/{object_to_id(block)}", AdminDomainBlock
		)


	# todo: create function based on this to work on any paginated endpoint
	async def all_admin_domain_blocks(self, chunk_size: int = 100) -> AsyncIterable[AdminDomainBlock]:
		max_id: int = 0

		while True:
			new_items = await self.admin_domain_blocks(max_id = max_id or None, limit = chunk_size)

			if not len(new_items):
				break

			max_id = int(new_items[-1].id)

			for item in new_items:
				yield item

			if len(new_items) < chunk_size:
				break
