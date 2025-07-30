import os
from base64 import b64encode
from typing import cast, override

import mcp.types as mt
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext

from ..devopness_api import DevopnessCredentials, ensure_authenticated
from ..types import MCP_TRANSPORT_PROTOCOL


class AuthMiddleware(Middleware):
    @override
    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, mt.CallToolResult],
    ) -> mt.CallToolResult:
        credentials = get_credentials(context)
        await ensure_authenticated(context.fastmcp_context, credentials)  # type: ignore[arg-type]

        return await call_next(context)


def get_credentials(
    ctx: MiddlewareContext[mt.CallToolRequestParams],
) -> DevopnessCredentials:
    transport = cast(
        MCP_TRANSPORT_PROTOCOL,
        ctx.fastmcp_context.fastmcp.env.DEVOPNESS_MCP_SERVER_TRANSPORT,  # type: ignore[union-attr]
    )

    if transport == "stdio":
        return credentials_stdio()

    if transport == "streamable-http":
        return credentials_http_stream()

    raise ValueError(f"Unknown transport: {transport}")


def credentials_stdio() -> DevopnessCredentials:
    user_email = os.environ.get("DEVOPNESS_USER_EMAIL")
    user_pass = os.environ.get("DEVOPNESS_USER_PASSWORD")

    if user_email and user_pass:
        return credentials_stdio_email_password(user_email, user_pass)

    # TODO: add support for api-key (eg: DEVOPNESS_API_KEY)
    #       and call `credentials_stdio_api_key(api_key)`

    raise RuntimeError(
        "ERROR: Devopness Credentials."
        "\nThe environment variables DEVOPNESS_USER_EMAIL and"
        " DEVOPNESS_USER_PASSWORD must be set."
    )


def credentials_stdio_email_password(
    user_email: str,
    user_pass: str,
) -> DevopnessCredentials:
    return DevopnessCredentials(
        type="email_password",
        data=b64encode(f"{user_email}:{user_pass}".encode()).decode("utf-8"),
    )


def credentials_http_stream() -> DevopnessCredentials:
    request_headers: dict[str, str] = get_http_headers()

    # FastMCP `get_http_headers` returns all headers as lowercase
    oauth_token = request_headers.get("authorization")

    if oauth_token:
        return credentials_http_stream_oauth_token(oauth_token)

    user_email = request_headers.get("devopness-user-email")
    user_pass = request_headers.get("devopness-user-password")

    if user_email and user_pass:
        return credentials_http_stream_email_password(user_email, user_pass)

    # TODO: add support for api-key (eg: Devopness-Api-Key) and
    #       call `credentials_http_stream_api_key(api_key)`

    raise RuntimeError(
        "ERROR: Devopness Credentials."
        "\nThe headers Devopness-User-Email and"
        " Devopness-User-Password must be set."
    )


def credentials_http_stream_oauth_token(oauth_token: str) -> DevopnessCredentials:
    return DevopnessCredentials(
        type="oauth_token",
        data=b64encode(oauth_token.replace("Bearer ", "").encode()).decode("utf-8"),
    )


def credentials_http_stream_email_password(
    user_email: str,
    user_pass: str,
) -> DevopnessCredentials:
    return DevopnessCredentials(
        type="email_password",
        data=b64encode(f"{user_email}:{user_pass}".encode()).decode("utf-8"),
    )
