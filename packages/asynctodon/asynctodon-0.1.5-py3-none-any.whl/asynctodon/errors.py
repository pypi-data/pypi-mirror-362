from typing import Any


class ClientError(Exception):
	"Generic exception for client-side errors"


class InvalidFieldError(KeyError):
	"Error that gets raised when the specified key cannot be found on a JSON object"

	def __init__(self, obj: Any, key: str) -> None:
		Exception.__init__(self, f"'{type(obj).__name__}' does not have a '{key}' field")

		self.object_name: str = type(obj).__name__
		"Name of the associated object"

		self.key: str = key
		"Name of the missing key"


class ServerError(Exception):
	"Generic exception for server-side errors"

	def __init__(self, status: int, message: str) -> None:
		Exception.__init__(self, f"[{status}] {message}")

		self.status: int = status
		"HTTP status code returned from the server"

		self.message: str = message
		"Message returned from the server"
