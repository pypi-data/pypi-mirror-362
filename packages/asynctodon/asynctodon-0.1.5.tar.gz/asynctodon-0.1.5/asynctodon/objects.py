from __future__ import annotations

import difflib

from blib import JsonBase, Url, get_object_name
from collections.abc import Callable, Sequence
from copy import deepcopy
from typing import Any, Generic, Self, TypeVar, overload

from .base import ApiDate, StatusDiff
from .errors import InvalidFieldError

from .enums import (
	AdminReportCategory,
	BlockSeverity,
	FilterAction,
	ListReplyPolicy,
	MediaType,
	NotificationType,
	PermissionFlag,
	PreviewCardType,
	ReportCategory,
	SeveredRelationshipType,
	SuggestionType,
	VisibilityLevel
)


T = TypeVar("T")
A = TypeVar("A")


def join_scope(value: Sequence[str] | str) -> str:
	if isinstance(value, str):
		return value

	return " ".join(value)


def split_scope(value: str | Sequence[str]) -> list[str]:
	if not isinstance(value, str):
		return list(value)

	return value.split(" ")


def url_parse(data: Any) -> Url:
	if not data:
		raise ValueError(f"Invalid url string: {data}")

	return Url.parse(data)


class ObjectBase(JsonBase[Any]):
	"Base class for all API objects"

	FIELDS: dict[str, Field[Any]]
	"All of the fields associated with the class"


	def __init__(self, data: dict[str, Any] | None = None, **kwargs: Any) -> None:
		"""
			Create a new object (usually from an API response).

			.. note:: ``ObjectBase`` can not be initiated by itself. Use a sub-object.

			:param kwargs: Key/value pairs to be assigned to the object
		"""

		if type(self) is ObjectBase:
			raise NotImplementedError()

		self._extra: dict[str, Any] = {}

		kwargs.update(data or {})

		for key, value in kwargs.items():
			if key not in type(self).FIELDS:
				self._extra[key] = value

			else:
				setattr(self, key, value)


	def __getitem__(self, key: str) -> Any:
		if key not in type(self).FIELDS:
			raise KeyError(key)

		return dict.get(self, key, None)


	def __setitem__(self, key: str, value: Any) -> None:
		if key not in type(self).FIELDS:
			raise InvalidFieldError(self, key) from None

		if value is None:
			self.pop(key, None)
			return

		dict.__setitem__(self, key, value)


	def __repr__(self) -> str:
		props = []

		for key in type(self).FIELDS:
			try:
				props.append(f"{key}={repr(self[key])}")

			except KeyError:
				continue

		return f"{type(self).__name__}({', '.join(props)})"


	def clear(self) -> None:
		dict.clear(self) # type: ignore[arg-type]
		self._extra.clear()


	def setdefault(self, key: str, value: Any = None) -> Any:
		try:
			return self[key]

		except KeyError:
			pass

		self[key] = value
		return value


	def to_dict(self) -> JsonBase[Any]:
		"Return the object as a JSON-safe ``dict`` object"

		data: JsonBase[Any] = JsonBase()

		for key, value in self.items():
			if value is None:
				data[key] = None
				continue

			if (field := type(self).FIELDS[key]).serializer is not None:
				data[key] = field.serializer(value)

			else:
				data[key] = value

		return data


	def to_json(self, indent: int | str | None = None, **kwargs: Any) -> str:
		"Return the object as a JSON string"

		return self.to_dict().to_json(indent, **kwargs)


	def unassigned_values(self) -> dict[str, Any]:
		"Values not associated with a field"

		return deepcopy(self._extra)


	def update(self, data: dict[str, Any] | None, **kwargs: Any) -> None: # type: ignore[override]
		kwargs.update(data or {})

		for key, value in kwargs.items():
			self[key] = value


class Field(Generic[T]):
	def __init__(self,
				deserializer: type[ObjectBase] | Callable[[Any], T] | None = None,
				serializer: type[ObjectBase] | Callable[[T], Any] | None = None,
				key: str | None = None) -> None:
		"""
			Creates a new ``Field`` descriptor and adds itself to :attr:`ObjectBase.FIELDS`

			:param deserializer: Method to call when setting a value
			:param serializer: Method to call in :meth:`ObjectBase.to_dict` or
				:meth:`ObjectBase.to_json`
			:param key: Name of the key to use when getting or setting a value. This will be the
				name of the property by default.
		"""

		if type(deserializer) is type and issubclass(deserializer, (ObjectBase, ListDeserializer)):
			if serializer is None:
				serializer = deserializer.to_dict # type: ignore[assignment,union-attr]

			deserializer = deserializer.parse # type: ignore[assignment]

		if type(serializer) is type and issubclass(serializer, (ObjectBase, ListSerializer)):
			serializer = serializer.to_dict # type: ignore[assignment,union-attr]

		self.key: str = key or ""
		self.deserializer: Callable[[Any], T] | None = deserializer # type: ignore[assignment]
		self.serializer: Callable[[T], Any] | None = serializer


	def __set_name__(self, cls: type[ObjectBase], key: str) -> None:
		if not self.key:
			self.key = key

		if not hasattr(cls, "FIELDS"):
			cls.FIELDS = {}

		cls.FIELDS[key] = self


	@overload
	def __get__(self, obj: ObjectBase, cls: Any) -> T:
		...


	@overload
	def __get__(self, obj: None, cls: Any) -> Self:
		...


	def __get__(self, obj: ObjectBase | None, cls: Any) -> Self | T:
		if obj is None:
			raise RuntimeError("Field is not a static property")

		try:
			return obj[self.key] # type: ignore[no-any-return]

		except KeyError:
			raise AttributeError(
				f"'{get_object_name(obj)}' does not have attribute '{self.key}'") from None


	def __set__(self, obj: ObjectBase, value: T | None) -> None:
		if value is None:
			try:
				self.__delete__(obj)

			except KeyError:
				pass

			return

		if self.deserializer is not None:
			value = self.deserializer(value)

		obj[self.key] = value


	def __delete__(self, obj: ObjectBase) -> None:
		del obj[self.key]


	@classmethod
	def list(cls: type[Self],
			deserializer: type[ObjectBase] | Callable[[Any], A] | type[A] | None,
			serializer: type[ObjectBase] | Callable[[A], Any] | type[A] | None = None,
			key: str | None = None) -> Self:
		"""
			Create a new list-based ``Field`` object

			:param deserializer: Method to call when setting a value
			:param serializer: Method to call in :meth:`ObjectBase.to_dict` or
				:meth:`ObjectBase.to_json`
			:param key: Name of the key to use when getting or setting a value. This will be the
				name of the property by default.
		"""

		if isinstance(deserializer, type) and issubclass(deserializer, ObjectBase):
			if serializer is None:
				serializer == ListSerializer(deserializer)

			deserializer = ListDeserializer(deserializer) # type: ignore[assignment]

		if isinstance(serializer, type) and issubclass(serializer, ObjectBase):
			serializer = ListSerializer(serializer) # type: ignore[assignment]

		return cls(deserializer, serializer, key) # type: ignore[arg-type]


class ListDeserializer(Generic[T]):
	def __init__(self, parser: type[ObjectBase] | Callable[[Any], T] | type[T] | None) -> None:
		if type(parser) is type and issubclass(parser, ObjectBase):
			parser = parser.parse # type: ignore[assignment]

		self.parser: Callable[[Any], T] | type[T] | None = parser # type: ignore[assignment]


	def __call__(self, data: list[Any]) -> list[T]:
		if self.parser is None:
			return data

		return [self.parser(item) for item in data] # type: ignore[call-arg]


	def parse(self, data: list[Any]) -> list[T]:
		return self(data)


class ListSerializer(Generic[T]):
	def __init__(self, dumper: type[ObjectBase] | Callable[[T], Any] | type[T] | None) -> None:
		if type(dumper) is type and issubclass(dumper, ObjectBase):
			dumper = dumper.to_dict # type: ignore[assignment]

		self.dumper: Callable[[T], Any] | type[T] | None = dumper


	def __call__(self, data: list[T]) -> list[Any]:
		if self.dumper is None:
			return data

		return [self.dumper(item) for item in data] # type: ignore[call-arg]


## sub objects ##
class AccountField(ObjectBase):
	"`Account Field <https://docs.joinmastodon.org/entities/Account/#Field>`_"

	name: Field[str] = Field()
	value: Field[str] = Field()
	verified_at: Field[ApiDate | None] = Field(ApiDate.parse, str)


class AdminEmailBlockHistory(ObjectBase):
	day: Field[ApiDate] = Field(lambda data: ApiDate.parse(int(data)), lambda data: data.timestamp())
	accounts: Field[int] = Field(int, str)
	users: Field[int] = Field(int, str)


class AdminIP(ObjectBase):
	"`Admin IP <https://docs.joinmastodon.org/entities/Admin_Ip/>`_"

	ip: Field[str] = Field()
	used_at: Field[ApiDate] = Field(ApiDate.parse, str)


class AnnouncementAccount(ObjectBase):
	"`Announcement Account <https://docs.joinmastodon.org/entities/Announcement/#Account>`_"

	id: Field[str] = Field()
	username: Field[str] = Field()
	url: Field[Url] = Field(Url.parse)
	acct: Field[str] = Field()


class AnnouncementStatus(ObjectBase):
	"`Announcement Status <https://docs.joinmastodon.org/entities/Announcement/#Status>`_"

	id: Field[str] = Field()
	url: Field[Url] = Field(Url.parse)


class PreviewCard(ObjectBase):
	url: Field[Url] = Field(Url.parse)
	title: Field[str] = Field()
	description: Field[str] = Field()
	type: Field[PreviewCardType] = Field(PreviewCardType)
	author_name: Field[str] = Field()
	authro_url: Field[Url] = Field(Url.parse)
	provider_name: Field[str] = Field()
	provider_url: Field[Url] = Field(Url.parse)
	html: Field[str] = Field()
	width: Field[int] = Field()
	height: Field[int] = Field()
	image: Field[Url] = Field(Url.parse)
	embed_url: Field[Url] = Field(Url.parse)
	blurhash: Field[str] = Field()


class CredentialSource(ObjectBase):
	note: Field[str] = Field()
	privacy: Field[str] = Field()
	sensitive: Field[bool] = Field()
	language: Field[str] = Field()
	follow_requests_count: Field[int] = Field()
	hide_collections: Field[bool] = Field()
	discoverable: Field[bool] = Field()
	indexable: Field[bool] = Field()

	fields: Field[list[AccountField]] = Field.list(AccountField)


class Emoji(ObjectBase):
	shortcode: Field[str] = Field()
	url: Field[Url] = Field(Url.parse)
	static_url: Field[Url] = Field(Url.parse)
	visible_in_picker: Field[bool] = Field()
	category: Field[str] = Field()


class FilterKeyword(ObjectBase):
	id: Field[str] = Field()
	keyword: Field[str] = Field()
	whole_word: Field[bool] = Field()


class FilterStatus(ObjectBase):
	id: Field[str] = Field()
	status_id: Field[str] = Field()


class Filter(ObjectBase):
	id: Field[str] = Field()
	title: Field[str] = Field()
	context: Field[list[str]] = Field()
	expires_at: Field[ApiDate] = Field(ApiDate.parse, str)
	filter_action: Field[FilterAction] = Field(FilterAction)
	keywords: Field[list[FilterKeyword]] = Field.list(FilterKeyword)
	statuses: Field[list[FilterStatus]] = Field.list(FilterStatus)


class FilterResult(ObjectBase):
	filter: Field[Filter] = Field(Filter, Filter)
	keyword_matches: Field[list[str]] = Field()
	status_matches: Field[list[str]] = Field()


class InstanceConfigAccounts(ObjectBase):
	max_featured_tags: Field[int] = Field()


class InstanceConfigMedia(ObjectBase):
	supported_mime_types: Field[list[str]] = Field()
	image_size_limit: Field[int] = Field()
	image_matrix_limit: Field[int] = Field()
	video_size_limit: Field[int] = Field()
	video_frame_rate_limit: Field[int] = Field()
	video_matrix_limit: Field[int] = Field()


class InstanceConfigPoll(ObjectBase):
	max_options: Field[int] = Field()
	max_characters_per_option: Field[int] = Field()
	min_expiration: Field[int] = Field()
	max_expiration: Field[int] = Field()


class InstanceConfigStatus(ObjectBase):
	max_characters: Field[int] = Field()
	characters_reserved_per_url: Field[int] = Field()
	supported_mime_types: Field[list[str]] = Field()


class InstanceConfigTranslation(ObjectBase):
	enabled: Field[bool] = Field()


class InstanceConfigUrls(ObjectBase):
	streaming: Field[Url] = Field(Url.parse)
	status: Field[str] = Field()


class InstanceConfigVapid(ObjectBase):
	public_key: Field[str] = Field()


class InstanceConfig(ObjectBase):
	urls: Field[InstanceConfigUrls] = Field(InstanceConfigUrls)
	vapid: Field[InstanceConfigVapid] = Field(InstanceConfigVapid)
	accounts: Field[InstanceConfigAccounts] = Field(InstanceConfigAccounts)
	statuses: Field[InstanceConfigStatus] = Field(InstanceConfigStatus)
	media_attachments: Field[InstanceConfigMedia] = Field(InstanceConfigMedia)
	polls: Field[InstanceConfigPoll] = Field(InstanceConfigPoll)
	translation: Field[InstanceConfigTranslation] = Field(InstanceConfigTranslation)


class InstanceContact(ObjectBase):
	email: Field[str] = Field()
	account: Field[Account] = Field(lambda data: Account.parse(data), lambda data: data.to_dict())


class InstanceRegistration(ObjectBase):
	enabled: Field[bool] = Field()
	approval_required: Field[bool] = Field()
	message: Field[str] = Field()
	url: Field[Url] = Field(Url.parse)


class InstanceThumbnail(ObjectBase):
	url: Field[Url] = Field(Url.parse)


class InstanceUsageUsers(ObjectBase):
	active_month: Field[int] = Field()


class InstanceUsage(ObjectBase):
	users: Field[InstanceUsageUsers] = Field(InstanceUsageUsers)


class Marker(ObjectBase):
	last_read_id: Field[str] = Field()
	version: Field[int] = Field()
	updated_at: Field[ApiDate] = Field(ApiDate.parse)


class Media(ObjectBase):
	id: Field[str] = Field()
	type: Field[MediaType] = Field(MediaType)
	url: Field[Url] = Field(Url.parse)
	preview_url: Field[Url] = Field(Url.parse)
	remote_url: Field[Url] = Field(Url.parse)
	meta: Field[dict[str, Any]] = Field() # todo: figure out what keys this has
	description: Field[str] = Field()
	blurhash: Field[str] = Field()


class Mention(ObjectBase):
	id: Field[str] = Field()
	username: Field[str] = Field()
	url: Field[Url] = Field(Url.parse)
	acct: Field[str] = Field()


class NotificationGroup(ObjectBase):
	group_key: Field[str] = Field()
	notifications_count: Field[int] = Field()
	type: Field[NotificationType] = Field(NotificationType.parse)
	most_recent_notification_id: Field[str] = Field()
	page_min_id: Field[str] = Field()
	page_max_id: Field[str] = Field()
	latest_page_notification_at: Field[ApiDate] = Field(ApiDate.parse, ApiDate.to_string)
	sample_account_ids: Field[list[str]] = Field()
	status_id: Field[str] = Field()
	report: Field[AdminReport] = Field(lambda data: AdminReport.parse(data))
	event: Field[RelationshipSeveranceEvent] = Field(
		lambda data: RelationshipSeveranceEvent.parse(data))
	moderation_warning: Field[dict[str, Any]] = Field() # create AccountWarning class


class NotificationPolicySummary(ObjectBase):
	pending_requests_count: Field[int] = Field()
	pending_notifications_count: Field[int] = Field()


class PartialAccount(ObjectBase):
	id: Field[str] = Field()
	acct: Field[str] = Field()
	url: Field[Url] = Field(Url.parse)
	avatar: Field[Url] = Field(Url.parse)
	avatar_static: Field[Url] = Field(Url.parse)
	locked: Field[bool] = Field()
	bot: Field[bool] = Field()


	@property
	def handle(self) -> str:
		if "@" in self.acct:
			return self.acct
		return f"{self.acct}@{self.url.domain}"


class PollOption(ObjectBase):
	title: Field[str] = Field()
	votes_count: Field[int] = Field()


class Poll(ObjectBase):
	id: Field[str] = Field()
	expires_at: Field[ApiDate] = Field(ApiDate.parse, str)
	expired: Field[bool] = Field()
	multiple: Field[bool] = Field()
	votes_count: Field[int] = Field()
	voters_count: Field[int] = Field()
	voted: Field[bool] = Field()
	own_votes: Field[list[int]] = Field()
	emojis: Field[list[Emoji]] = Field.list(Emoji,)
	options: Field[list[PollOption]] = Field.list(PollOption,)


class Reaction(ObjectBase):
	name: Field[str] = Field()
	count: Field[int] = Field()
	me: Field[bool] = Field()
	url: Field[Url] = Field(url_parse)
	static_url: Field[Url] = Field(url_parse)


class RelationshipSeveranceEvent(ObjectBase):
	id: Field[str] = Field()
	type: Field[SeveredRelationshipType] = Field(SeveredRelationshipType)
	purged: Field[bool] = Field()
	target_name: Field[str] = Field()
	relationship_count: Field[int] = Field()
	created_at: Field[ApiDate] = Field(ApiDate.parse)


class Role(ObjectBase):
	"`Role <https://docs.joinmastodon.org/entities/Role/>`_"

	id: Field[str] = Field()
	name: Field[str] = Field()
	color: Field[str] = Field()
	permissions: Field[PermissionFlag] = Field(PermissionFlag.parse)
	highlighted: Field[bool] = Field()


class StatusApplication(ObjectBase):
	name: Field[str] = Field()
	website: Field[str] = Field()


class StatusTag(ObjectBase):
	name: Field[str] = Field()
	url: Field[Url] = Field(Url.parse)


class TagHistory(ObjectBase):
	day: Field[ApiDate] = Field(ApiDate.parse, ApiDate.timestamp)
	users: Field[int] = Field(int, str)
	accounts: Field[int] = Field(int, str)


class Tag(ObjectBase):
	name: Field[str] = Field()
	url: Field[str] = Field()
	following: Field[bool] = Field()
	history: Field[TagHistory]


class TranslationMedia(ObjectBase):
	id: Field[str] = Field()
	description: Field[str] = Field()


class TranslationPoll(ObjectBase):
	id: Field[str] = Field()
	options: Field[list[str]] = Field.list(lambda obj: obj["title"], lambda obj: {"title": obj})


## main objects ##
class AccessToken(ObjectBase):
	token_type: Field[str] = Field()
	access_token: Field[str] = Field()
	scope: Field[list[str]] = Field(split_scope, join_scope)
	created_at: Field[ApiDate] = Field(ApiDate.parse, str)


class Account(ObjectBase):
	id: Field[str] = Field()
	username: Field[str] = Field()
	acct: Field[str] = Field()
	display_name: Field[str] = Field()
	uri: Field[Url] = Field(Url.parse)
	url: Field[Url] = Field(Url.parse)
	note: Field[str] = Field()
	avatar: Field[Url] = Field(Url.parse)
	avatar_static: Field[Url] = Field(Url.parse)
	header: Field[Url] = Field(Url.parse)
	header_static: Field[Url] = Field(Url.parse)
	locked: Field[bool] = Field()
	bot: Field[bool] = Field()
	group: Field[bool] = Field()
	noindex: Field[bool] = Field()
	suspended: Field[bool] = Field()
	limited: Field[bool] = Field()
	discoverable: Field[bool] = Field()
	indexable: Field[bool] = Field()
	hide_collections: Field[bool] = Field()
	statuses_count: Field[int] = Field()
	followers_count: Field[int] = Field()
	following_count: Field[int] = Field()
	moved: Field[Account] = Field(lambda data: Account.parse(data), lambda data: data.to_dict())
	last_status_at: Field[ApiDate] = Field(ApiDate.parse, str)
	created_at: Field[ApiDate] = Field(ApiDate.parse, str)
	fields: Field[list[AccountField]] = Field.list(AccountField)
	roles: Field[list[Role]] = Field.list(Role)
	emojis: Field[list[Emoji]] = Field.list(Emoji)

	# credential account only
	role: Field[Role] = Field(Role)
	source: Field[CredentialSource] = Field(CredentialSource)


	@property
	def handle(self) -> str:
		return f"{self.username}@{self.url.domain}"


class Activity(ObjectBase):
	week: Field[int] = Field(int, str)
	statuses: Field[int] = Field(int, str)
	logins: Field[int] = Field(int, str)
	registrations: Field[int] = Field(int, str)


class AdminAccount(ObjectBase):
	id: Field[str] = Field()
	username: Field[str] = Field()
	domain: Field[str] = Field()
	created_at: Field[ApiDate] = Field(ApiDate.parse, str)
	email: Field[str] = Field()
	ip: Field[AdminIP] = Field(AdminIP)
	role: Field[Role] = Field(Role)
	confirmed: Field[bool] = Field()
	suspended: Field[bool] = Field()
	silenced: Field[bool] = Field()
	disabled: Field[bool] = Field()
	approved: Field[bool] = Field()
	locale: Field[str] = Field()
	invite_request: Field[str] = Field()
	ips: Field[AdminIP] = Field(AdminIP)
	account: Field[Account] = Field(Account)
	created_by_application_id: Field[str] = Field()
	invited_by_account_id: Field[str] = Field()


class AdminDomainAllow(ObjectBase):
	id: Field[str] = Field()
	domain: Field[str] = Field()
	created_at: Field[ApiDate] = Field()


class AdminDomainBlock(ObjectBase):
	id: Field[str] = Field()
	domain: Field[str] = Field()
	digest: Field[str] = Field()
	created_at: Field[ApiDate] = Field()
	severity: Field[BlockSeverity] = Field(BlockSeverity.parse)
	reject_media: Field[bool] = Field()
	reject_reports: Field[bool] = Field()
	private_comment: Field[str] = Field()
	public_comment: Field[str] = Field()
	obfuscate: Field[bool] = Field()


class AdminEmailBlock(ObjectBase):
	id: Field[str] = Field()
	domain: Field[str] = Field()
	created_at: Field[ApiDate] = Field()
	history: Field[list[AdminEmailBlockHistory]] = Field.list(AdminEmailBlockHistory)


class AdminReport(ObjectBase):
	id: Field[str] = Field()
	action_taken: Field[bool] = Field()
	action_taken_at: Field[ApiDate] = Field(ApiDate.parse, str)
	category: Field[str] = Field(AdminReportCategory.parse, str)
	comment: Field[str] = Field()
	forwarded: Field[bool] = Field()
	created_at: Field[ApiDate] = Field(ApiDate.parse, str)
	updated_at: Field[ApiDate] = Field(ApiDate.parse, str)
	target_account: Field[AdminAccount] = Field(AdminAccount)
	assigned_account: Field[AdminAccount] = Field(AdminAccount)
	action_taken_by_account: Field[AdminAccount] = Field(AdminAccount)
	statuses: Field[list[Status]] = Field.list(
		lambda data: Status.parse(data), lambda data: data.to_dict())
	rules: Field[list[Rule]] = Field.list(lambda data: Rule.parse(data), lambda data: data.to_dict())


class Announcement(ObjectBase):
	id: Field[str] = Field()
	content: Field[str] = Field()
	starts_at: Field[ApiDate] = Field(ApiDate.parse)
	ends_at: Field[ApiDate] = Field(ApiDate.parse)
	published: Field[bool] = Field()
	all_day: Field[bool] = Field()
	published_at: Field[ApiDate] = Field(ApiDate.parse)
	updated_at: Field[ApiDate] = Field(ApiDate.parse)
	read: Field[bool] = Field()
	emojis: Field[list[Emoji]] = Field.list(Emoji)
	reactions: Field[list[Reaction]] = Field.list(Reaction)
	tags: Field[list[StatusTag]] = Field.list(StatusTag)
	statuses: Field[list[AnnouncementStatus]] = Field.list(AnnouncementStatus)
	mentions: Field[list[AnnouncementAccount]] = Field.list(AnnouncementAccount)


class Application(ObjectBase):
	id: Field[str] = Field()
	name: Field[str] = Field()
	website: Field[Url] = Field(Url.parse)
	redirect_uri: Field[str] = Field()
	client_id: Field[str] = Field()
	client_secret: Field[str] = Field()
	scope: Field[list[str]] = Field(split_scope, join_scope)
	vapid_key: Field[str] = Field() # deprecated


class DomainBlock(ObjectBase):
	domain: Field[str] = Field()
	digest: Field[str] = Field()
	severity: Field[BlockSeverity] = Field(BlockSeverity.parse)
	comment: Field[str] = Field()


class ExtendedDescription(ObjectBase):
	content: Field[str] = Field()
	updated_at: Field[ApiDate] = Field(ApiDate.parse)


class FeaturedTag(ObjectBase):
	id: Field[str] = Field()
	name: Field[str] = Field()
	url: Field[Url] = Field(Url.parse)
	statuses_count: Field[int] = Field()
	last_status_at: Field[ApiDate] = Field(ApiDate.parse)


class Rule(ObjectBase):
	id: Field[str] = Field()
	text: Field[str] = Field()
	hint: Field[str] = Field()


class GroupedNotificationsResults(ObjectBase):
	accounts: Field[list[Account]] = Field.list(Account)
	partial_accounts: Field[list[PartialAccount]] = Field.list(PartialAccount)
	statuses: Field[list[Status]] = Field.list(lambda data: Status.parse(data))
	notification_groups: Field[list[NotificationGroup]] = Field.list(NotificationGroup)


class Instance(ObjectBase):
	domain: Field[str] = Field()
	title: Field[str] = Field()
	version: Field[str] = Field()
	source_url: Field[Url] = Field(Url.parse)
	description: Field[str] = Field()
	languages: Field[list[str]] = Field()
	usage: Field[InstanceUsage] = Field(InstanceUsage)
	thumbnail: Field[InstanceThumbnail] = Field(InstanceThumbnail)
	configuration: Field[InstanceConfig] = Field(InstanceConfig)
	contact: Field[InstanceContact] = Field(InstanceContact)
	rules: Field[list[Rule]] = Field.list(Rule)
	registrations: Field[InstanceRegistration] = Field(InstanceRegistration)


class LinkTrendHistory(ObjectBase):
	day: Field[ApiDate] = Field(lambda data: ApiDate.parse(int(data)))
	accounts: Field[int] = Field(int, str)
	users: Field[int] = Field(int, str)


class LinkTrend(ObjectBase):
	url: Field[Url] = Field(url_parse)
	title: Field[str] = Field()
	description: Field[str] = Field()
	type: Field[str] = Field()
	author_name: Field[str] = Field()
	author_url: Field[Url] = Field(url_parse)
	provider_name: Field[str] = Field()
	provider_url: Field[Url] = Field(url_parse)
	html: Field[Url] = Field()
	width: Field[int] = Field()
	height: Field[int] = Field()
	image: Field[Url] = Field(url_parse)
	embed_url: Field[Url] = Field(url_parse)
	blurhash: Field[Url] = Field()
	history: Field[list[LinkTrendHistory]] = Field.list(LinkTrendHistory)


class List(ObjectBase):
	id: Field[str] = Field()
	title: Field[str] = Field()
	replies_policy: Field[ListReplyPolicy] = Field(ListReplyPolicy)


class Markers(ObjectBase):
	home: Field[Marker] = Field(Marker, Marker)
	notifications: Field[Marker] = Field(Marker)


class NotificationPolicy(ObjectBase):
	filter_not_following: Field[bool] = Field()
	filter_not_followers: Field[bool] = Field()
	filter_new_accounts: Field[bool] = Field()
	fitler_private_mentions: Field[bool] = Field()

	summary: Field[NotificationPolicySummary] = Field(NotificationPolicySummary)


class OEmbed(ObjectBase):
	type: Field[str] = Field()
	version: Field[str] = Field()
	title: Field[str] = Field()
	author_name: Field[str] = Field()
	author_url: Field[Url] = Field(url_parse)
	provider_name: Field[str] = Field()
	provider_url: Field[Url] = Field(url_parse)
	cache_age: Field[str] = Field()
	html: Field[Url] = Field()
	width: Field[int] = Field()
	height: Field[int] = Field()


class Relationship(ObjectBase):
	id: Field[str] = Field()
	following: Field[bool] = Field()
	showing_reblogs: Field[bool] = Field()
	notifying: Field[bool] = Field()
	languages: Field[list[str]] = Field()
	followed_by: Field[bool] = Field()
	blocking: Field[bool] = Field()
	blocked_by: Field[bool] = Field()
	muting: Field[bool] = Field()
	muting_notifications: Field[bool] = Field()
	requested: Field[bool] = Field()
	requested_by: Field[bool] = Field()
	domain_blocking: Field[bool] = Field()
	endorsed: Field[bool] = Field()
	note: Field[str] = Field()


class Report(ObjectBase):
	id: Field[str] = Field()
	action_taken: Field[bool] = Field()
	action_taken_at: Field[ApiDate] = Field(ApiDate.parse)
	category: Field[ReportCategory] = Field(ReportCategory)
	comment: Field[str] = Field()
	forwarded: Field[bool] = Field()
	created_at: Field[ApiDate] = Field(ApiDate.parse)
	status_ids: Field[list[str]] = Field()
	rule_ids: Field[list[str]] = Field()
	target_account: Field[str] = Field()


class ScheduledStatusParamsPoll(ObjectBase):
	options: Field[list[str]] = Field()
	expires_in: Field[int] = Field(int, str)
	multiple: Field[bool] = Field()
	hide_totals: Field[bool] = Field()


class ScheduledStatusParams(ObjectBase):
	text: Field[str] = Field()
	spoiler_text: Field[str] = Field()
	in_reply_to_id: Field[str] = Field()
	sensitive: Field[bool] = Field()
	language: Field[str] = Field()
	application_id: Field[int] = Field()
	media_ids: Field[list[str]] = Field()
	scheduled_at: Field[ApiDate] = Field(ApiDate.parse, str)
	idempotency: Field[str] = Field()
	with_rate_limit: Field[bool] = Field()

	poll: Field[ScheduledStatusParamsPoll] = Field(
		ScheduledStatusParamsPoll, ScheduledStatusParamsPoll
	)


class ScheduledStatus(ObjectBase):
	id: Field[str] = Field()
	scheduled_at: Field[ApiDate] = Field(ApiDate.parse, str)
	media_attachments: Field[list[Media]] = Field.list(Media)
	params: Field[ScheduledStatusParams] = Field(ScheduledStatusParams)


class Status(ObjectBase):
	id: Field[str] = Field()
	uri: Field[Url] = Field(Url.parse)
	url: Field[Url] = Field(Url.parse)
	created_at: Field[ApiDate] = Field(ApiDate.parse, str)
	account: Field[Account] = Field(Account)
	content: Field[str] = Field()
	visibility: Field[VisibilityLevel] = Field(VisibilityLevel.parse)
	sensitive: Field[bool] = Field()
	spoiler_text: Field[str] = Field()
	application: Field[StatusApplication] = Field(StatusApplication)
	reblogs_count: Field[int] = Field()
	favourites_count: Field[int] = Field()
	replies_count: Field[int] = Field()
	in_reply_to_id: Field[str] = Field()
	in_reply_to_account_id: Field[str] = Field()
	language: Field[str] = Field()
	edited_at: Field[ApiDate] = Field(ApiDate.parse, str)
	favourited: Field[bool] = Field()
	reblogged: Field[bool] = Field()
	muted: Field[bool] = Field()
	bookmarked: Field[bool] = Field()
	pinned: Field[bool] = Field()
	local_only: Field[bool] = Field()
	reblog: Field[Status] = Field(lambda data: Status.parse(data), lambda data: data.to_dict())
	card: Field[PreviewCard] = Field(PreviewCard)
	poll: Field[Poll] = Field(Poll, Poll)
	media_attachments: Field[list[Media]] = Field.list(Media)
	mentions: Field[list[Mention]] = Field.list(Mention)
	tags: Field[list[Tag]] = Field.list(Tag)
	emojis: Field[list[Emoji]] = Field.list(Emoji)
	filtered: Field[list[FilterResult]] = Field.list(FilterResult)


class Search(ObjectBase):
	accounts: Field[list[Account]] = Field.list(Account)
	hashtags: Field[list[Tag]] = Field.list(Tag)
	statuses: Field[list[Status]] = Field.list(Status)


class StatusContext(ObjectBase):
	ancestors: Field[list[Status]] = Field.list(Status)
	descendants: Field[list[Status]] = Field.list(Status)


class StatusSource(ObjectBase):
	id: Field[str] = Field()
	text: Field[str] = Field()
	spoiler_text: Field[str] = Field()


class StatusEdit(ObjectBase):
	content: Field[str] = Field()
	spoiler_text: Field[str] = Field()
	sensitive: Field[bool] = Field()
	created_at: Field[ApiDate] = Field(ApiDate.parse)
	account: Field[Account] = Field(Account)
	poll: Field[Poll] = Field(Poll, Poll)
	emojis: Field[list[Emoji]] = Field.list(Emoji)
	media_attachments: Field[list[Media]] = Field.list(Media)


	def diff(self, status: Status) -> StatusDiff:
		return StatusDiff(
			"\n".join(difflib.ndiff(
				self.content.splitlines(),
				status.content.splitlines()
			)),
			"\n".join(difflib.ndiff(
				self.spoiler_text.splitlines(),
				status.spoiler_text.splitlines()
			))
		)


class Conversation(ObjectBase):
	id: Field[str] = Field()
	unread: Field[bool] = Field()
	last_status: Field[Status] = Field(Status)
	accounts: Field[list[Account]] = Field.list(Account)


class Suggestion(ObjectBase):
	source: Field[SuggestionType] = Field(SuggestionType.parse)
	account: Field[Account] = Field(Account)


class Translation(ObjectBase):
	content: Field[str] = Field()
	spoiler_text: Field[str] = Field()
	poll: Field[TranslationPoll] = Field(TranslationPoll)
	detected_source_language: Field[str] = Field()
	provider: Field[str] = Field()
	media_attachments: Field[list[TranslationMedia]] = Field.list(TranslationMedia)


class WebPushSubscriptionAlerts(ObjectBase):
	follow: Field[bool] = Field()
	favourite: Field[bool] = Field()
	reblog: Field[bool] = Field()
	mention: Field[bool] = Field()
	poll: Field[bool] = Field()


class WebPushSubscription(ObjectBase):
	id: Field[str] = Field()
	endpoint: Field[Url] = Field()
	server_key: Field[str] = Field()
	alerts: Field[WebPushSubscriptionAlerts] = Field.list(WebPushSubscriptionAlerts)


class Notification(ObjectBase):
	id: Field[str] = Field()
	type: Field[NotificationType] = Field(NotificationType)
	created_at: Field[ApiDate] = Field(ApiDate.parse)
	account: Field[Account] = Field(Account)
	status: Field[Status] = Field(Status)
	report: Field[Report] = Field(Report)
	relationship_severance_event: Field[RelationshipSeveranceEvent] = Field(
		RelationshipSeveranceEvent
	)


class NotificationRequest(ObjectBase):
	id: Field[str] = Field()
	created_at: Field[ApiDate] = Field(ApiDate.parse)
	updated_at: Field[ApiDate] = Field(ApiDate.parse)
	from_account: Field[Account] = Field(Account)
	notifications_count: Field[int] = Field()
	last_status: Field[Status] = Field(Status)
