"""
Initializes an asynchronous Devopness Client and ensures authentication.
"""

from base64 import b64decode
from dataclasses import dataclass
from typing import Literal

from devopness import DevopnessClientAsync, DevopnessClientConfig
from devopness.base import DevopnessBaseService, DevopnessBaseServiceAsync
from devopness.client_config import get_user_agent
from devopness.models import (
    UserLogin,
)
from devopness_mcp_server.lib.environment import EnvironmentVariables
from devopness_mcp_server.lib.types import ServerContext


def get_devopness_client(env: EnvironmentVariables) -> DevopnessClientAsync:
    config = DevopnessClientConfig(
        auto_refresh_token=False,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": get_user_agent(
                product_name="devopness-mcp-server",
                product_package_name="devopness-mcp-server",
            ),
        },
    )

    config.base_url = env.DEVOPNESS_API_URL or config.base_url

    return DevopnessClientAsync(config)


@dataclass
class DevopnessCredentials:
    type: Literal[
        "email_password",
        "oauth_token",
    ]

    data: str


async def ensure_authenticated(
    ctx: ServerContext,
    credentials: DevopnessCredentials,
) -> None:
    match credentials.type:
        case "email_password":
            decoded_credentials = b64decode(credentials.data).decode("utf-8")
            user_email, user_pass = decoded_credentials.split(":", 1)

            # TODO: only invoke login if not yet authenticated
            user_data = UserLogin(email=user_email, password=user_pass)
            await ctx.devopness.users.login_user(user_data)

        case "oauth_token":
            decoded_token = b64decode(credentials.data).decode("utf-8")

            DevopnessBaseService._access_token = decoded_token
            DevopnessBaseServiceAsync._access_token = decoded_token

        case _:
            raise ValueError(f"Unsupported credentials type: {credentials.type}")
