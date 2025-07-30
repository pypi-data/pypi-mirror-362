import webbrowser

from blib import Query, Url

from .base import ClientBase, parse_data

from ..objects import AccessToken, Application


class AppBase(ClientBase):
	def authorization_url(self,
							client_id: str | None = None,
							redirect_uri: str | None = None,
							scopes: list[str] | None = None,
							force_login: bool = False,
							lang: str = "EN") -> Url:

		if client_id is None:
			client_id = self.client_id

		assert client_id is not None, "'client_id' must be set"

		query = Query({
			"response_type": "code",
			"client_id": client_id,
			"redirect_uri": redirect_uri or self.redirect_uri,
			"scope": " ".join(scopes or self.scopes),
			"force_login": "true" if force_login else "false",
			"lang": lang
		})

		return Url(
			domain = self.host,
			path = "/oauth/authorize",
			proto = "https" if self.https else "http",
			query = query
		)


	async def create_app(self,
						name: str | None = None,
						redirect_uri: str | None = None,
						scopes: list[str] | None = None,
						website: str | None = None,
						set_app_details: bool = False) -> Application:

		data = {
			"client_name": name or self.name,
			"redirect_uris": redirect_uri or self.redirect_uri,
			"scopes": " ".join(scopes if scopes else self.scopes),
			"website": website or self.website
		}

		assert data["client_name"] is not None, "'client_name' must be set"

		app = await self.send("POST", "/api/v1/apps", Application, data, token = False)
		app.scope = data["scopes"] # type: ignore[assignment]

		if set_app_details:
			self.set_details_from_app(app)

		return app


	async def obtain_token(self,
						client_id: str | None = None,
						client_secret: str | None = None,
						redirect_uri: str | None = None,
						scopes: list[str] | None = None,
						code: str | None = None,
						set_token: bool = False) -> AccessToken:

		data = parse_data(
			grant_type = "authorization_code" if code is not None else "client_credentials",
			client_id = client_id or self.client_id,
			client_secret = client_secret or self.client_secret,
			redirect_uri = redirect_uri or self.redirect_uri,
			scope = " ".join(scopes or self.scopes),
			code = code
		)

		assert data is not None, "Must set 'client_id' and 'client_secret'"
		assert None not in [data.get("client_id"), data.get("client_secret")], \
			"Must set 'client_id' and 'client_secret'"

		token = await self.send("POST", "/oauth/token", AccessToken, data, token = False)

		if set_token:
			self.token = token.access_token

		return token


	def open_authorization_url(self,
							client_id: str | None = None,
							redirect_uri: str | None = None,
							scopes: list[str] | None = None,
							force_login: bool = False,
							lang: str = "EN") -> None:

		url = self.authorization_url(client_id, redirect_uri, scopes, force_login, lang)
		webbrowser.open(url)


	async def resend_confirmation(self, email: str) -> None:
		await self.send("POST", "/api/v1/emails/confirmations", None, {"email": email})


	async def revoke_token(self, id: str, secret: str, token: str) -> None:
		data = parse_data(
			client_id = id,
			client_secret = secret,
			token = token
		)

		await self.send("POST", "/oauth/revoke", None, data)


	async def verify_token(self) -> Application:
		return await self.send("GET", "/api/v1/apps/verify_credentials", Application)
