from typing import Optional
from pydantic import BaseModel
import json
import os
import requests
import pathlib

from .config import (
    DEVICE_CODE_LOGIN_URL,
    DEVICE_CODE_TOKEN_CHECK_URL,
    GH_AUTH_TOKEN_URL,
    GH_COPILOT_INTERNAL_AUTH_URL,
    CLIENT_ID,
    BASE_HEADERS,
    CONFIG_DIR,
)


class GithubUserData(BaseModel):
    avatar_url: str
    bio: Optional[str]
    blog: str
    company: Optional[str]
    created_at: str
    email: Optional[str]
    events_url: str
    followers: int
    followers_url: str
    following: int
    following_url: str
    gists_url: str
    gravatar_id: str
    hireable: Optional[bool]
    html_url: str
    id: int
    location: Optional[str]
    login: str
    name: str
    node_id: str
    notification_email: Optional[str]
    organizations_url: str
    public_gists: int
    public_repos: int
    received_events_url: str
    repos_url: str
    site_admin: bool
    starred_url: str
    subscriptions_url: str
    twitter_username: Optional[str]
    updated_at: str
    url: str
    user_view_type: str


class GithubCopilotEndpoints(BaseModel):
    api: str
    proxy: str
    telemetry: str


class GithubCopilotAuth(BaseModel):
    annotations_enabled: bool
    chat_enabled: bool
    chat_jetbrains_enabled: bool
    code_quote_enabled: bool
    code_review_enabled: bool
    codesearch: bool
    copilotignore_enabled: bool
    endpoints: GithubCopilotEndpoints
    expires_at: int
    individual: bool
    limited_user_quotas: Optional[int]
    limited_user_reset_date: Optional[int]
    # nes_enabled: bool
    prompt_8k: bool
    public_suggestions: str
    refresh_in: int
    sku: str
    snippy_load_test_enabled: bool
    telemetry: str
    token: str
    tracking_id: str
    trigger_completion_after_accept: Optional[bool] = False
    vsc_electron_fetcher_v2: bool
    xcode: bool
    xcode_chat: bool


class GitHubDeviceTokenResponse(BaseModel):
    access_token: str
    token_type: str
    scope: str


class GitHubDeviceLoginResponse(BaseModel):
    interval: int
    user_code: str
    expires_in: int
    verification_uri: str
    device_code: str


class GithubAuth(BaseModel):
    user: GithubUserData
    token: str
    copilot_auth: GithubCopilotAuth


class Authentication:
    def request_github_auth(self) -> GitHubDeviceLoginResponse:
        """Request GitHub device login."""
        response = requests.post(
            DEVICE_CODE_LOGIN_URL,
            json={"client_id": CLIENT_ID, "scope": "read:user"},
            headers=BASE_HEADERS,
        )
        response.raise_for_status()
        return GitHubDeviceLoginResponse(**response.json())

    def check_github_auth(self, device_code: str) -> GitHubDeviceTokenResponse:
        """Check GitHub device token status."""
        response = requests.post(
            DEVICE_CODE_TOKEN_CHECK_URL,
            json={
                "client_id": CLIENT_ID,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
            headers=BASE_HEADERS,
        )
        response.raise_for_status()

        if "authorization_pending" in response.text:
            raise Exception("Authorization pending")

        return GitHubDeviceTokenResponse(**response.json())

    def gh_get_user(self, token: str) -> GithubUserData:
        """Fetch GitHub user data."""
        headers = BASE_HEADERS | {
            "authorization": f"token {token}",
        }
        response = requests.get(GH_AUTH_TOKEN_URL, headers=headers)
        response.raise_for_status()
        return GithubUserData(**response.json())

    def gh_copilot_authenticate(self, token: str) -> GithubCopilotAuth:
        """Authenticate with GitHub Copilot."""
        headers = BASE_HEADERS | {"authorization": f"token {token}"}
        response = requests.get(GH_COPILOT_INTERNAL_AUTH_URL, headers=headers)
        response.raise_for_status()
        return GithubCopilotAuth(**response.json())

    def get_token(self) -> str:
        """Retrieve token from environment or local storage."""
        token = os.getenv("COPILOT_TOKEN")
        if token:
            return token

        token_path = CONFIG_DIR / "token.json"

        if not token_path.exists():
            raise FileNotFoundError("Token file not found")

        with open(token_path, "r") as f:
            data = json.load(f)
            return data["token"]

    def save_token(self, token: str) -> pathlib.Path:
        """Save token to local storage."""

        token_path = CONFIG_DIR / "token.json"

        with open(token_path, "w") as f:
            json.dump({"token": token}, f)

        return token_path

    def auth(self) -> GithubAuth:
        """Perform GitHub authentication."""
        response = self.request_github_auth()
        print(
            f"Please visit {response.verification_uri} and enter the code {response.user_code}"
        )

        while True:
            try:
                auth = self.check_github_auth(response.device_code)
                token_path = self.save_token(auth.access_token)
                print(f"Token saved successfully to '{token_path}'")
                user = self.gh_get_user(auth.access_token)
                copilot_auth = self.gh_copilot_authenticate(auth.access_token)

                return GithubAuth(
                    user=user, token=auth.access_token, copilot_auth=copilot_auth
                )
            except Exception:
                import time

                time.sleep(response.interval)

    def cache_auth(self) -> GithubAuth:
        """Retrieve cached authentication."""
        token = self.get_token()
        user = self.gh_get_user(token)
        copilot_auth = self.gh_copilot_authenticate(token)

        return GithubAuth(user=user, token=token, copilot_auth=copilot_auth)

    def try_auth(self) -> GithubAuth:
        """Retrieve cached authentication or re-authenticate."""
        try:
            token = self.get_token()
        except FileNotFoundError:
            auth = self.auth()
            token = auth.token

        user = self.gh_get_user(token)
        copilot_auth = self.gh_copilot_authenticate(token)

        return GithubAuth(user=user, token=token, copilot_auth=copilot_auth)


if __name__ == "__main__":
    authentication = Authentication()
    result = authentication.try_auth()
    print("Dheepak" in result.user.name)
