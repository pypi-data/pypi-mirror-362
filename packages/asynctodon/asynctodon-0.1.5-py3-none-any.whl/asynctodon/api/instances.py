from blib import JsonBase

from .base import ClientBase

from ..objects import Activity, DomainBlock, ExtendedDescription, Instance, ListDeserializer, Rule


class InstanceBase(ClientBase):
	async def domain_blocks(self) -> list[DomainBlock]:
		return await self.send(
			"GET", "/api/v1/instance/domain_blocks", ListDeserializer(DomainBlock)
		)


	async def extended_description(self) -> ExtendedDescription:
		return await self.send(
			"GET", "/api/v1/instance/extended_description", ExtendedDescription, token = False
		)


	async def instance_activity(self) -> list[Activity]:
		return await self.send(
			"GET", "/api/v1/instance/activity", ListDeserializer(Activity), token = False
		)


	async def instance_info(self, version: int = 2) -> Instance:
		# todo: check instance version to get correct endpoint
		return await self.send("GET", f"/api/v{version}/instance", Instance, token = False)


	async def instance_peers(self) -> list[str]:
		return await self.send(
			"GET", "/api/v1/instance/peers", ListDeserializer(None), token = False
		)


	async def rules(self) -> list[Rule]:
		return await self.send(
			"GET", "/api/v1/instance/rules", ListDeserializer(Rule), token = False
		)


	async def translation_languages(self) -> dict[str, list[str]]:
		return await self.send(
			"GET", "/api/v1/instance/translation_languages", JsonBase, token = False
		)
