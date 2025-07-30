from blib import JsonBase, Query, Url
from collections.abc import AsyncIterator, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar, Union, overload

from ..enums import StreamEventType
from ..objects import Application, ListDeserializer, ObjectBase


T = TypeVar("T")
C = TypeVar("C", bound = Union[JsonBase[Any], ObjectBase])
O = TypeVar("O", bound = ObjectBase) # noqa: E741
J = TypeVar("J", covariant = True)


@overload
def object_to_id(obj: None, prop: str | None = None) -> None:
	...


@overload
def object_to_id(obj: O | int | str, prop: str | None = None) -> str:
	...


def object_to_id(obj: O | int | str | None, prop: str | None = None) -> str | None:
	"""
		Attempts to return the specified property (`id` by default) of an object. If the object is a
		string, just return it
	"""

	if obj is None:
		return None

	if isinstance(obj, ObjectBase):
		return str(getattr(obj, prop or "id"))

	return str(obj)


def object_to_ids(obj_list: list[O | int | str], prop: str | None = None) -> list[str]:
	"Same as `object_to_id` except for a list of items"

	return [object_to_id(item, prop) for item in obj_list]


def parse_data(**kwargs: Any) -> dict[str, Any] | None:
	"Go though some key/value pairs and remove any pairs that have a value of `None`"

	return {key: value for key, value in kwargs.items() if value is not None} or None


def version(introduced: str, deprecated: str | None, removed: str | None) -> None:
	pass


class StreamParser(Protocol[J]):
	"Callable for parsing messages from the streaming API"

	def __call__(self, data: str) -> J:
		"""
			:param data: Raw streaming message
			:return: The newly parsed streaming message
		"""


@dataclass(slots = True)
class StreamEvent(Generic[T]):
	"Represents an event from a streaming API endpoint. `data` will always have an `id` key."

	type: StreamEventType
	"Type of event"

	data: T
	"Data associated with the event"


class ClientBase:
	host: str
	https: bool
	token: str | None
	name: str | None
	website: Url | None
	redirect_uri: str
	client_id: str | None
	client_secret: str | None
	scopes: list[str]


	def set_details_from_app(self, app: Application) -> None:
		...


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

		raise NotImplementedError


	def stream(self,
				path: str,
				query: Mapping[str, str] | None = None,
				parser: StreamParser[T] = str) -> AsyncIterator[StreamEvent[T]]: # type: ignore[assignment]

		raise NotImplementedError
