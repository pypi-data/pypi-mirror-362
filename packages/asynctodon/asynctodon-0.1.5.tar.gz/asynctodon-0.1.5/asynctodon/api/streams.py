import asyncio
import inspect

from collections.abc import AsyncIterator, Awaitable, Callable
from typing import ParamSpec, TypeVar

from .base import ClientBase, StreamEvent

from ..errors import ServerError
from ..objects import Notification, Status


T = TypeVar("T")
P = ParamSpec("P")


class StreamBase(ClientBase):
	async def stream_health(self) -> bool:
		try:
			await self.send("GET", "/api/v1/streaming/health", None)
			return True

		except ServerError as error:
			if error.status >= 500:
				return False

			raise


	def stream_hashtag(self, tag: str, only_local: bool = False) -> AsyncIterator[StreamEvent[Status]]:
		params = {"tag": tag}
		path = "/api/v1/streaming/hashtag"

		if only_local:
			path += "/local"

		return self.stream(path, params, parser = Status.parse)


	def stream_home(self) -> AsyncIterator[StreamEvent[Status]]:
		return self.stream("/api/v1/streaming/user", parser = Status.parse)


	def stream_direct(self) -> AsyncIterator[StreamEvent[Status]]:
		return self.stream("/api/v1/streaming/direct", parser = Status.parse)


	def stream_list(self, list_id: str) -> AsyncIterator[StreamEvent[Status]]:
		params = {"list": list_id}
		return self.stream("/api/v1/streaming/list", params, parser = Status.parse)


	def stream_notifications(self) -> AsyncIterator[StreamEvent[Notification]]:
		return self.stream("/api/v1/streaming/user/notification", parser = Notification.parse)


	def stream_public(self,
					only_media: bool = False,
					only_remote: bool = False,
					only_local: bool = False) -> AsyncIterator[StreamEvent[Status]]:

		params = {"only_media": str(only_media).lower()}
		path = "/api/v1/streaming/public"

		if only_remote and only_local:
			raise ValueError("'only_remote' and 'only_local' are mutually exclusive")

		if only_remote:
			path += "/remote"

		elif only_local:
			path += "/local"

		return self.stream(path, params, parser = Status.parse)


	async def stream_with_callback(self,
							iterator: AsyncIterator[StreamEvent[T]],
							callback: Callable[[StreamEvent[T]], None]) -> asyncio.Task[None]:
		"""
			Run a stream iterator in the background and return the associated :class:`asyncio.Task`
			object

			:param iterator: Async iterator from a :meth:`asynctodon.Client.stream` method
			:param callback: Function that gets called for every stream event
		"""

		return asyncio.create_task(self.handle_stream_with_callback(iterator, callback))


	async def handle_stream_with_callback(self,
							iterator: AsyncIterator[StreamEvent[T]],
							callback: Callable[[StreamEvent[T]], Awaitable[None] | None]) -> None:

		try:
			async for event in iterator:
				if inspect.iscoroutinefunction(callback):
					await callback(event)

				else:
					callback(event)

		except asyncio.CancelledError:
			pass
