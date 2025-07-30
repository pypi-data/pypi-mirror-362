import asyncio
import json

from blib import File, GenericError, JsonBase, Query, Url, get_object_name
from collections.abc import AsyncIterator, Mapping, Sequence
from httpx import AsyncClient, Response, URL
from typing import Any, IO, Self, TypeVar, Union, cast, overload

from . import api
from .base import CODE_REDIRECT
from .enums import StreamEventType
from .errors import ClientError, ServerError
from .objects import Application, ListDeserializer, ObjectBase


C = TypeVar("C", bound = Union[JsonBase[Any], ObjectBase])
T = TypeVar("T")


class Client(api.AccountBase, api.AppBase, api.AdminBase, api.FilterBase, api.InstanceBase,
			api.MiscBase, api.NotificationBase, api.StatusBase, api.StreamBase, api.TagBase,
			api.TimelineBase):
	"Client for the Mastodon API."

	def __init__(self,
				host: str,
				token: str | None = None,
				name: str | None = None,
				website: Url | str | None = None,
				redirect_uri: Url | str | None = None,
				client_id: str | None = None,
				client_secret: str | None = None,
				scopes: Sequence[str] | None = None,
				timeout: int | float = 5,
				stream_timeout: int | float = 600,
				https: bool = True) -> None:
		"""
			Create a new ``Client`` object

			:param host: Hostname to connect to
			:param token: Client token to pass to authenticated endpoints
			:param name: Name to be used in the ``User-Agent`` header and when registering the
				application
			:param website: Website of the application
			:param redirect_uri: Location to redirect to when authenticating a user
			:param client_id: Client identifier from a previous application registration
			:param client_secret: Client secret from a previous application registration
			:param scopes: API scopes the application will use
			:param timeout: Number of seconds to wait for requests before giving up
			:param stream_timeout: Number of seconds to wait for a message or heartbeat on
				streaming endpoints
			:param https: Use ``https`` instead of ``http``
		"""

		self._client = AsyncClient(
			http2 = True,
			timeout = timeout,
			max_redirects = 5,
			headers = {
				"User-Agent": name or "Asynctodon"
			}
		)

		self.https: bool = https
		self.host = host
		self.token: str | None = token
		self.name: str | None = name
		self.website: Url | None = website if website is None else Url.parse(website)
		self.redirect_uri: str = redirect_uri or CODE_REDIRECT
		self.client_id: str | None = client_id
		self.client_secret: str | None = client_secret
		self.scopes: list[str] = ["read"] if scopes is None else list(scopes)
		self.stream_timeout: int | float = stream_timeout


	def __repr__(self) -> str:
		return f"Client({repr(self.host)}, name={repr(self.name)})"


	async def __aenter__(self) -> Self:
		return self


	async def __aexit__(self, *_: Any) -> None:
		await self.close()


	@classmethod
	def new_from_app(cls: type[Self],
					app: Application,
					host: str,
					token: str | None = None) -> Self:
		"""
			Create a new ``Client`` from an ``Application``

			:param app: Application info to use
			:param host: Instance to connect to
			:param token: Access token to use
		"""

		client = cls(host, token)
		client.set_details_from_app(app)
		return client


	@property
	def host(self) -> str:
		"Instance the client will send requests to"

		return self._client._base_url.host


	@host.setter
	def host(self, value: str) -> None:
		if "/" in value:
			raise ValueError("Host must not contain path segments")

		self._client._base_url = URL(f"{'https' if self.https else 'http'}://{value}/")


	async def close(self) -> None:
		"Close all open connections"

		if self._client.is_closed:
			return

		await self._client.aclose()
		await asyncio.sleep(0)


	def set_details_from_app(self, app: Application) -> None:
		"""
			Set application details from an ``Application`` object

			:param app: Application to set details from
		"""

		self.name = app.name
		self.website = app.website
		self.redirect_url = app.redirect_uri or CODE_REDIRECT
		self.client_id = app.client_id
		self.client_secret = app.client_secret
		self.scopes = app.scope or ["read"]


	@overload
	async def send(self,
				method: str,
				path: str,
				cls: type[C],
				data: Mapping[str, Any] | Sequence[Any] | None = None,
				query: Query | Mapping[str, str] | None = None,
				form: Mapping[str, Any] | None = None,
				token: bool = True) -> C:
		...


	@overload
	async def send(self,
				method: str,
				path: str,
				cls: ListDeserializer[C],
				data: Mapping[str, Any] | Sequence[Any] | None = None,
				query: Query | Mapping[str, str] | None = None,
				form: Mapping[str, Any] | None = None,
				token: bool = True) -> list[C]:
		...


	@overload
	async def send(self,
				method: str,
				path: str,
				cls: None,
				data: Mapping[str, Any] | Sequence[Any] | None = None,
				query: Query | Mapping[str, str] | None = None,
				form: Mapping[str, Any] | None = None,
				token: bool = True) -> None:
		...


	async def send(self,
				method: str,
				path: str,
				cls: type[C] | ListDeserializer[C] | None,
				data: Mapping[str, Any] | Sequence[Any] | None = None,
				query: Query | Mapping[str, str] | None = None,
				form: Mapping[str, Any] | None = None,
				token: bool = True) -> C | list[C] | None:
		"""
			Send a request to the instance

			:param method: HTTP method of the endpoint
			:param path: Path of the endpoint
			:param cls: Class to use when parsing returned data. Use ``None`` if not expecting a
				response.
			:param data: JSON data to send with the request. Do not use with ``form``.
			:param query: Query parameters to append to the url
			:param form: HTML form data to send with the request. Do not use with ``data``.
			:param token: Ensure a token is set before sending the request
		"""

		open_files: list[IO[bytes]] = []
		headers: dict[str, str] = {
			"Accept": "application/json"
		}

		if self.token is None:
			if token:
				raise ClientError(f"Token required for endpoint: {method} {path}")

		else:
			headers["Authorization"] = f"Bearer {self.token}"

		body: dict[str, Any] | Sequence[Any] = {}
		files: dict[str, tuple[str, IO[bytes]]] = {}
		resp: Response | None = None

		try:
			# todo: create a TypedDict to sort out this mess
			if form is not None:
				for key, value in form.items():
					if isinstance(value, File):
						value = value.resolve()
						open_files.append(value.open("rb"))
						files[key] = (value.name, open_files[-1])

					else:
						body[key] = value # type: ignore[index]

				resp = await self._client.request(
					method = method,
					url = path,
					params = query, # type: ignore[arg-type]
					files = files or None,
					data = cast(dict[str, str], body) or None,
					headers = headers
				)

			elif data is not None:
				headers["Content-Type"] = "application/json"

				resp = await self._client.request(
					method = method,
					url = path,
					params = query, # type: ignore[arg-type]
					content = data.to_json() if isinstance(data, JsonBase) else json.dumps(data),
					headers = headers
				)

			else:
				resp = await self._client.request(
					method = method,
					url = path,
					params = query, # type: ignore[arg-type]
					files = files or None,
					headers = headers
				)

			resp_data = (await resp.aread()).decode(resp.charset_encoding or "utf-8")

			if resp.status_code >= 400:
				if resp.headers.get("Content-Type") == "application/json":
					msg: JsonBase[str] = JsonBase.parse(resp_data)
					raise ServerError(resp.status_code, msg.get("error_description", msg["error"]))

				# this should never get called, but keeping here just in case
				if resp.headers.get("Content-Type") == "text/html":
					raise ServerError(resp.status_code, resp.reason_phrase)

				raise ServerError(resp.status_code, resp_data)

			if cls is not None:
				if type(cls) is ListDeserializer:
					return cls(json.loads(resp_data))

				if type(cls) is type and issubclass(cls, JsonBase):
					return cls.parse(resp_data) # type: ignore[return-value]

				raise ValueError(f"Invalid parser class: {get_object_name(cls)}")

		finally:
			if resp is not None:
				await resp.aclose()

			for file in open_files:
				file.close()

		return None


	async def stream(self,
				path: str,
				query: Query | Mapping[str, str] | None = None,
				parser: api.StreamParser[T] = str) -> AsyncIterator[api.StreamEvent[T]]: # type: ignore[assignment]
		"""
			Connect to a streaming endpoint and return an iterator of events

			:param path: Path to the streaming endpoint
			:param query: Query parameters to append to the url
		"""

		if self.token is None:
			raise ClientError("Missing client token")

		headers: dict[str, str] = {
			"Accept": "application/json",
			"Authorization": f"Bearer {self.token}"
		}

		if query is None:
			query = {}

		pre_resp = self._client.stream(
			"GET", path,
			params = query, # type: ignore[arg-type]
			headers = headers,
			timeout = self.stream_timeout
		)

		event_name: str | None = None

		async with pre_resp as resp:
			async for line in resp.aiter_lines():
				if line.startswith("{\"error\""):
					data: JsonBase[str] = JsonBase.parse(line)
					raise ServerError(400, data["error"])

				if line.startswith("event:"):
					event_name = line[6:].strip()

				elif line.startswith("data:") and event_name is not None:
					messageData = line[5:].strip()

					try:
						parsedData = parser(messageData)

					except GenericError as e:
						# the url field of a message is sometimes empty and causes a parse error
						print(f"[WARN] error when parsing message: {e}")
						print(f"[WARN] type: {event_name}")
						print(f"[WARN] data: {messageData}")
						continue

					yield api.StreamEvent(StreamEventType.parse(event_name), parsedData)

					# if event_name in {"delete", "announcement.delete"}:
					# 	yield api.StreamEvent(event_type, JsonBase({"id": line_data}))

					# elif event_name == "filters_changed":
					# 	# not sure what the data for this event looks like, so ignore for now
					# 	yield api.StreamEvent(event_type, JsonBase({"id": "0"}))

					# else:
					# 	yield api.StreamEvent(event_type, JsonBase.parse(line_data))

					event_name = None
