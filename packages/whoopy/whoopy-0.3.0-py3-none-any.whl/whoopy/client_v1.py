"""Official Whoop API.

Generated against version 1.0 of the API.

Copyright 2022 (C) Felix Geilert
"""

import json
import os
import uuid
import webbrowser
from typing import Any

import requests
from typing_extensions import Self

from .constants import HTTP_OK, MIN_PASSWORD_LENGTH
from .handlers import handler_v1 as handlers

API_VERSION = "1"
API_BASE = "https://api.prod.whoop.com/"
API_AUTH = f"{API_BASE}oauth/oauth2"
SCOPES = [
    "offline",
    "read:recovery",
    "read:cycles",
    "read:sleep",
    "read:workout",
    "read:profile",
    "read:body_measurement",
]


class WhoopClient:
    def __init__(
        self,
        access_token: str,
        expires_in: int,
        scopes: list[str],
        refresh_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ):
        """Creates a new WhoopClient.

        Note that when client_id and client_secret are not provided, the refresh function will not work.

        Args:
            access_token (str): The access token.
            expires_in (int): The time until the token expires (in seconds).
            scopes (list[str]): The scopes that the token has.
            refresh_token (str, optional): The refresh token. Defaults to None.
            client_id (str, optional): The client ID. Defaults to None.
            client_secret (str, optional): The client secret. Defaults to None.
        """
        self.token = access_token
        self.expires_in = expires_in
        self.scopes = scopes
        self.refresh_token = refresh_token
        self._client_id = client_id
        self._client_secret = client_secret

        # create a session
        self.user_agent = "Python/3.X (X11; Linux x86_64)"
        self._update_session()

        # create a bunch of handlers
        self.user = handlers.WhoopUserHandler(self)
        self.cycle = handlers.WhoopCycleHandler(self)
        self.sleep = handlers.WhoopSleepHandler(self)
        self.workout = handlers.WhoopWorkoutHandler(self)
        self.recovery = handlers.WhoopRecoveryHandler(self)

    @property
    def _token(self) -> dict[str, Any]:
        return {
            "access_token": self.token,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "scopes": self.scopes,
        }

    def _update_session(self) -> None:
        """Updates the session with the new token."""
        self._base_path = f"{API_BASE}developer/v1"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "User-Agent": self.user_agent,
            }
        )

    def store_token(self, path: str) -> None:
        """Stores the token to a file.

        Args:
            path (str): The path to the file (e.g. ".tokens/token.json").
        """
        # verify that folder exists
        base_dir = os.path.dirname(path)
        os.makedirs(base_dir, exist_ok=True)

        # store the token
        with open(path, "w") as f:
            json.dump(self._token, f)

    @classmethod
    def from_token(cls, path: str, client_id: str, client_secret: str, overwrite_token: bool = True) -> Self:
        """
        Loads a token from a file and creates a WhoopClient instance.

        Args:
            path (str): The path to the token file (e.g. ".tokens/token.json").
            client_id (str): The OAuth2 client ID.
            client_secret (str): The OAuth2 client secret.
            overwrite_token (bool): Whether to save the refreshed token back to file (default: True).

        Returns:
            WhoopClient: Authenticated client instance with refreshed token.
        """
        with open(path) as f:
            token = json.load(f)
        client = cls(
            token["access_token"],
            token["expires_in"],
            token["scopes"],
            token["refresh_token"],
            client_id,
            client_secret,
        )
        client.refresh()

        # check if token should be updated
        if overwrite_token is True:
            client.store_token(path)

        return client

    # retrieves the authorization url
    @classmethod
    def auth_url(
        cls,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        state: str | None = None,
        scopes: list[str] | None = None,
    ) -> tuple[str, str]:
        """
        Generates authorization URL for the Whoop OAuth2 flow.

        Args:
            client_id (str): The OAuth2 client ID.
            client_secret (str): The OAuth2 client secret.
            redirect_uri (str): The redirect URI registered with Whoop.
            state (str | None): Optional state parameter for CSRF protection (auto-generated if None).
            scopes (list[str] | None): OAuth2 scopes to request (uses all available if None).

        Returns:
            tuple[str, str]: A tuple of (authorization_url, state_parameter).

        Raises:
            ValueError: If state is provided but less than 8 characters.
        """
        # check state
        if not state:
            state = str(uuid.uuid4())

        # retrieve the data
        if len(state) < MIN_PASSWORD_LENGTH:
            raise ValueError("State must be at least 8 characters long")

        # generate the
        scopes = scopes or SCOPES
        scope = " ".join(scopes)
        res = (
            f"{API_AUTH}/auth?"
            f"scope={scope}&"
            f"client_id={client_id}&"
            f"client_secret={client_secret}&"
            f"state={state}&"
            f"redirect_uri={redirect_uri}&"
            "response_type=code"
        )

        return res, state

    @classmethod
    def _parse_token(cls, payload: dict[str, Any], scopes: list[str] | None) -> tuple[dict[str, Any], list[str]]:
        url = f"{API_AUTH}/token"

        # retrieve the codes
        res = requests.post(url, data=payload)
        if res.status_code != HTTP_OK:
            raise RuntimeError(f"Authorization failed with code {res.status_code}")
        codes = res.json()
        token_scopes = codes["scope"].split(" ")

        # validate scopes
        if scopes:
            for scope in scopes:
                if scope not in token_scopes:
                    raise ValueError(f"Scope {scope} not granted")

        return codes, token_scopes

    @classmethod
    def authorize(
        cls,
        code: str,
        client_id: str,
        client_secret: str,
        redirect_url: str = "https://jwt.ms/",
        scopes: list[str] | None = None,
    ) -> Self:
        """
        Authorize the client with the given authorization code.

        Exchanges an authorization code for access and refresh tokens.

        Args:
            code (str): Authorization code from OAuth2 callback.
            client_id (str): The OAuth2 client ID.
            client_secret (str): The OAuth2 client secret.
            redirect_url (str): The redirect URI used in authorization (default: "https://jwt.ms/").
            scopes (list[str] | None): Expected scopes to validate (raises error if not granted).

        Returns:
            WhoopClient: Authenticated client instance.

        Raises:
            RuntimeError: If authorization fails.
            ValueError: If requested scopes were not granted.
        """
        # generate request using the code
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_url,
        }
        codes, token_scopes = cls._parse_token(payload, scopes)

        # generate the client
        return cls(
            codes["access_token"],
            codes["expires_in"],
            token_scopes,
            codes.get("refresh_token", None),
            client_id=client_id,
            client_secret=client_secret,
        )

    @classmethod
    def auth_flow(
        cls,
        client_id: str,
        client_secret: str,
        redirect_url: str = "https://jwt.ms/",
        state: str | None = None,
        scopes: list[str] | None = None,
    ) -> Self:
        """Runs through the entire auth flow.

        Note: This requires to copy the code query attribute from the resulting redirect url.

        Args:
            client_id (str): The client ID.
            client_secret (str): The client secret.
            redirect_url (str, optional): The redirect URL. Defaults to "https://jwt.ms/".
            state (str, optional): The state passed through to the output of request. Defaults to None.
            scopes (list[str], optional): The scopes to request. Defaults to None.
                (In case of None, all scopes are requested.)

        Returns:
            The client object.
        """
        # retrieve url
        url, state = cls.auth_url(client_id, client_secret, redirect_url, state, scopes)

        # send user to auth and wait for code
        webbrowser.open(url)
        code = input("Copy Code Attribute from URL: ")

        # authorize
        return cls.authorize(code, client_id, client_secret, redirect_url, scopes)

        # complete

    def refresh(self) -> None:
        """
        Refreshes the access token using the refresh token.

        Updates the client's token information with new access token and expiry.

        Raises:
            ValueError: If no refresh token or client credentials are available.
            RuntimeError: If token refresh fails.
        """
        # verify client is setup correctly
        if self.refresh_token is None:
            raise ValueError("No refresh token provided")
        if self._client_id is None or self._client_secret is None:
            raise ValueError("No client id or secret provided")

        # generate request using the code
        payload = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        # retrieve the codes
        codes, _ = self._parse_token(payload, self.scopes)

        # update data
        self.token = codes["access_token"]
        self.expires_in = codes["expires_in"]
        self.refresh_token = codes.get("refresh_token", None)

        # update sess
        self._update_session()

    @classmethod
    def from_token_or_flow(cls, secret_json: str, token_path: str, scopes: list[str] | None = None) -> Self:
        """
        Creates a new WhoopClient from a token or by using the authorization flow.

        If a valid token exists at token_path, loads and refreshes it. Otherwise,
        initiates the OAuth2 authorization flow.

        Args:
            secret_json (str): Path to JSON file containing client_id, client_secret, and redirect_uri.
            token_path (str): Path to save/load the token file.
            scopes (list[str] | None): OAuth2 scopes to request (uses all available if None).

        Returns:
            WhoopClient: Authenticated client instance.
        """
        # load the secret
        with open(secret_json) as f:
            secret = json.load(f)

        # check if token exists
        if os.path.exists(token_path):
            return cls.from_token(
                token_path,
                secret["client_id"],
                secret["client_secret"],
                overwrite_token=True,
            )

        # create a new client
        client = cls.auth_flow(
            secret["client_id"],
            secret["client_secret"],
            secret["redirect_uri"],
            scopes=scopes,
        )
        client.store_token(token_path)

        return client
