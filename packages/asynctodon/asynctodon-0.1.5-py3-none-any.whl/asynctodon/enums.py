from blib import IntFlagEnum, StrEnum
from typing import Self


class AccountAction(StrEnum):
	BLOCK = "block"
	UNBLOCK = "unblock"
	FOLLOW = "follow"
	UNFOLLOW = "unfollow"
	MUTE = "mute"
	UNMUTE = "unmute"
	FEATURE = "pin"
	UNFEATURE = "unpin"


class AccountStatus(StrEnum):
	ACTIVE = "active"
	PENDING = "pending"
	DISABLED = "disabled"
	SILENCED = "silenced"
	SUSPENDED = "suspended"


class AdminAccountAction(StrEnum):
	NONE = "none"
	SENSITIVE = "sensitive"
	DISABLE = "disable"
	SILENCE = "silence"
	SUSPEND = "suspend"


class AdminReportCategory(StrEnum):
	SPAM = "spam"
	VIOLATION = "violation"
	OTHER = "other"


class BlockSeverity(StrEnum):
	NONE = "noop"
	SILENCE = "silence"
	SUSPEND = "suspend"


class FilterAction(StrEnum):
	WARN = "warn"
	HIDE = "hide"


class GrantType(StrEnum):
	CLIENT = "client_credentials"
	CODE = "authorization_code"


class ListReplyPolicy(StrEnum):
	FOLLOW = "followed"
	LIST = "list"
	NONTE = "none"


class MediaType(StrEnum):
	UNKNOWN = "unknown"
	IMAGE = "image"
	GIFV = "gifv"
	VIDEO = "video"
	AUDIO = "audio"


class MuteContext(StrEnum):
	HOME = "home"
	NOTIFICATIONS = "notifications"
	PUBLIC = "public"
	THREAD = "thread"
	ACCOUNT = "account"


class NotificationType(StrEnum):
	MENTION = "mention"
	STATUS = "status"
	BOOST = "reblog"
	FOLLOW = "follow"
	REQUEST = "follow_request"
	FAVORITE = "favourite"
	POLL = "poll"
	UPDATE = "update"
	SIGNUP = "admin.sign_up"
	REACTION = "reaction"
	REPORT = "admin.report"
	SEVERED_RELATIONSHIP = "severed_relationships"
	WARNING = "moderation_warning"


class PermissionFlag(IntFlagEnum):
	ADMINISTRATOR = 0x1
	DEVOPS = 0x2
	AUDIT_LOG = 0x4
	DASHBOARD = 0x8
	REPORTS = 0x10
	FEDERATION = 0x20
	SETTINGS = 0x40
	BLOCKS = 0x80
	TAXONOMIES = 0x100
	APPEALS = 0x200
	USERS = 0x400
	INVITES = 0x800
	RULES = 0x1000
	ANNOUNCEMENTS = 0x2000
	EMOJIS = 0x4000
	WEBHOOKS = 0x8000
	INVITE = 0x10000
	ROLES = 0x20000
	USER_ACCESS = 0x40000
	DELETE = 0x80000


	@classmethod
	def parse(cls: type[Self], data: int | str) -> Self:
		if isinstance(data, str):
			data = int(data)

		if (value := cls(data)).value != data:
			raise ValueError(f"Cannot convert integer to flags: {data}")

		return value


class PreviewCardType(StrEnum):
	LINK = "link"
	PHOTO = "photo"
	VIDEO = "video"
	RICH = "rich"


class ReportCategory(StrEnum):
	SPAM = "spam"
	LEGAL = "legal"
	VIOLATION = "violation"
	OTHER = "other"


class SearchType(StrEnum):
	ACCOUNTS = "accounts"
	HASHTAGS = "hashtags"
	STATUSES = "statuses"


class SeveredRelationshipType(StrEnum):
	DOMAIN_BLOCK = "domain_block"
	USER_DOMAIN_BLOCK = "user_domain_block"
	SUSPENSION = "account_suspension"


class StatusAction(StrEnum):
	FAVORITE = "favourite"
	BOOST = "boost"
	BOOKMARK = "bookmark"
	MUTE = "mute"
	PIN = "pin"
	UNFAVORITE = "unfavourite"
	UNBOOST = "unboost"
	UNBOOKMARK = "unbookmark"
	UNMUTE = "unmute"
	UNPIN = "unpin"


class StreamEventType(StrEnum):
	ANNOUNCEMENT = "announcement"
	ANNOUNCEMENT_DELETE = "announcement.delete"
	ANNOUNCEMENT_REACT = "announcement.reaction"
	CONVERSATION = "conversation"
	DELETE = "delete"
	ENCRYPTED_MESSAGE = "encrypted_message"
	FILTERs = "filters_changed"
	NOTIFICATION = "notification"
	UPDATE = "update"
	STATUS_UPDATE = "status.update"


class SuggestionType(StrEnum):
	STAFF = "staff"
	INTERACTION = "past_interactions"
	GLOBAL = "global"


class VisibilityLevel(StrEnum):
	PUBLIC = "public"
	UNLISTED = "unlisted"
	PRIVATE = "private"
	DIRECT = "direct"


class WebPushPolicy(StrEnum):
	ALL = "all"
	NONE = "none"
	FOLLOWED = "followed"
	FOLLOWER = "follower"
