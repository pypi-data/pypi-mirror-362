import base64
import json
from functools import wraps
from typing import Any, Awaitable, Callable, List

import fastmcp.server.dependencies
import fastmcp.server.http
import fastmcp.tools.tool
import httpx
from mcp.server.auth.middleware.auth_context import AuthContextMiddleware
from mcp.server.auth.middleware.bearer_auth import BearerAuthBackend
from mcp.server.auth.provider import TokenVerifier
from mcp.server.auth.routes import cors_middleware
from starlette.middleware import Middleware as StarletteMiddleware
from starlette.middleware.authentication import (
    AuthenticationMiddleware as StarletteAuthenticationMiddleware,
)
from starlette.requests import Request
from starlette.responses import (
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
)
from starlette.routing import Route

from .token_verifier import create_introspection_verifier
from .types import Server, ServerContext

__all__ = [
    "patch_oauth_middleware_and_routes",
    "patch_server_context_injection",
]


def patch_server_context_injection(server: Server) -> None:
    """
    Patch FastMCP's context injection to use custom ServerContext.

    This replaces the default FastMCP context with our custom ServerContext
    that provides access to the custom server instance.
    """
    original_get_context = fastmcp.tools.tool.get_context  # type: ignore[attr-defined]

    @wraps(original_get_context)
    def enhanced_get_context() -> ServerContext:
        """
        Enhanced context provider that returns custom ServerContext.

        Returns:
            ServerContext: Custom context with OAuth-enabled server instance
        """
        original_context = original_get_context()
        return ServerContext(original_context)

    # Apply patches to both modules that use get_context
    fastmcp.tools.tool.get_context = enhanced_get_context  # type: ignore[attr-defined]
    fastmcp.server.dependencies.get_context = enhanced_get_context

    server.logger.info("Custom ServerContext injection patch applied")


def patch_oauth_middleware_and_routes(server: Server) -> None:
    """
    Patch FastMCP's authentication setup with OAuth support.

    This replaces FastMCP's OAuth implementation with a full-featured
    OAuth 2.0 setup that includes:
    - Bearer token authentication middleware
    - OAuth discovery endpoints per RFC 8414
    - Resource metadata endpoints per RFC 9728
    - Complete authorization flow endpoints
    """
    server.logger.info("Applying OAuth middleware and routes patch...")

    # Initialize OAuth token verifier with introspection
    token_verifier: Any = create_introspection_verifier(
        server.env.DEVOPNESS_MCP_AUTH_SERVER_INTROSPECTION_URL,
        server.env.DEVOPNESS_MCP_SERVER_URL,
    )

    server.auth = token_verifier

    @wraps(fastmcp.server.http.setup_auth_middleware_and_routes)
    def setup_oauth_middleware_and_routes(
        auth: TokenVerifier,
    ) -> tuple[List[Any], List[Any], List[str]]:
        """
        Enhanced authentication setup with OAuth support.

        Replaces FastMCP's default authentication setup to provide:
        - Full OAuth 2.0 Authorization Code flow with PKCE
        - RFC-compliant discovery endpoints
        - Proper bearer token authentication
        - Resource indicator support per RFC 8707

        Args:
            auth: Token verifier for authentication

        Returns:
            Tuple of (middleware, routes, required_scopes)

        Note:
            This addresses limitations in FastMCP's OAuth implementation:
            - Missing OAuth metadata discovery (RFC 8414)
            - No resource indicators support (RFC 8707)
            - Incomplete protected resource metadata (RFC 9728)

            See: https://github.com/jlowin/fastmcp/issues/914
                 https://github.com/jlowin/fastmcp/issues/972
        """
        # Authentication middleware stack
        middleware = [
            StarletteMiddleware(
                StarletteAuthenticationMiddleware,
                backend=BearerAuthBackend(auth),
            ),
            StarletteMiddleware(AuthContextMiddleware),
        ]

        # OAuth discovery and flow endpoints
        oauth_routes = [
            # OAuth Discovery Endpoints (RFC 8414, RFC 9728)
            Route(
                path="/.well-known/oauth-protected-resource",
                endpoint=cors_middleware(
                    create_route_handler(handle_protected_resource_metadata, server),
                    ["GET", "OPTIONS"],
                ),
                methods=["GET", "OPTIONS"],
            ),
            Route(
                path="/.well-known/oauth-authorization-server",
                endpoint=cors_middleware(
                    create_route_handler(handle_authorization_server_metadata, server),
                    ["GET", "OPTIONS"],
                ),
                methods=["GET", "OPTIONS"],
            ),
            # OAuth Flow Endpoints
            Route(
                path="/register",
                endpoint=cors_middleware(
                    create_route_handler(handle_client_registration, server),
                    ["POST", "OPTIONS"],
                ),
                methods=["POST", "OPTIONS"],
            ),
            Route(
                path="/authorize",
                endpoint=create_route_handler(handle_authorization_request, server),
                methods=["GET"],
            ),
            Route(
                path="/token",
                endpoint=cors_middleware(
                    create_route_handler(handle_token_request, server),
                    ["POST"],
                ),
                methods=["POST"],
            ),
        ]

        return middleware, oauth_routes, []

    # Apply the patch
    fastmcp.server.http.setup_auth_middleware_and_routes = (
        setup_oauth_middleware_and_routes
    )

    server.logger.info("OAuth middleware and routes patch applied successfully")


def create_route_handler(
    handler: Callable[[Server, Request], Awaitable[Response]],
    server: Server,
) -> Callable[[Request], Awaitable[Response]]:
    """
    Create a route handler with server context injection.

    Args:
        handler: The actual route handler function
        server: Server instance to inject into handler

    Returns:
        Wrapped handler function that accepts only Request
    """

    async def route_wrapper(request: Request) -> Response:
        return await handler(server, request)

    return route_wrapper


async def handle_protected_resource_metadata(  # noqa: RUF029
    server: Server,
    request: Request,
) -> JSONResponse | PlainTextResponse:
    """
    Handle OAuth protected resource metadata discovery (RFC 9728).

    This endpoint provides metadata about the protected resource to help
    clients understand authorization requirements and server capabilities.

    Args:
        server: Server instance with configuration
        request: HTTP request object

    Returns:
        JSON response with protected resource metadata or CORS preflight response
    """
    if request.method == "OPTIONS":
        return create_cors_preflight_response(["GET", "OPTIONS"])

    metadata = {
        "resource": server.env.DEVOPNESS_MCP_SERVER_URL,
        "authorization_servers": [server.env.DEVOPNESS_MCP_SERVER_URL],
    }

    return JSONResponse(metadata)


async def handle_authorization_server_metadata(  # noqa: RUF029
    server: Server,
    request: Request,
) -> JSONResponse | PlainTextResponse:
    """
    Handle OAuth authorization server metadata discovery (RFC 8414).

    This endpoint provides OAuth server configuration and capabilities
    to enable automatic client configuration and flow discovery.

    Args:
        server: Server instance with OAuth configuration
        request: HTTP request object

    Returns:
        JSON response with authorization server metadata or CORS preflight response
    """
    if request.method == "OPTIONS":
        return create_cors_preflight_response(["GET", "OPTIONS"])

    metadata = {
        "issuer": server.env.DEVOPNESS_MCP_SERVER_URL,
        "registration_endpoint": server.env.DEVOPNESS_MCP_SERVER_REGISTER_URL,
        "authorization_endpoint": server.env.DEVOPNESS_MCP_SERVER_AUTHORIZE_URL,
        "token_endpoint": server.env.DEVOPNESS_MCP_SERVER_TOKEN_URL,
        "response_types_supported": ["code"],
        "code_challenge_methods_supported": ["S256"],
        "grant_types_supported": ["authorization_code"],
        "token_endpoint_auth_methods_supported": [
            "client_secret_basic",
            "client_secret_post",
        ],
    }

    return JSONResponse(metadata)


async def handle_client_registration(
    server: Server,
    request: Request,
) -> JSONResponse | PlainTextResponse:
    """
    Handle OAuth client registration requests (RFC 7591).

    Proxies client registration requests to the external OAuth server
    and returns the registered client information.

    Args:
        server: Server instance with OAuth configuration
        request: HTTP request with client registration data

    Returns:
        JSON response with registered client data or CORS preflight response

    Raises:
        HTTPException: If registration fails at the OAuth server
    """
    if request.method == "OPTIONS":
        return create_cors_preflight_response(["POST", "OPTIONS"])

    try:
        registration_data = await request.json()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                server.env.DEVOPNESS_MCP_AUTH_SERVER_REGISTER_URL,
                json=registration_data,
            )
            response.raise_for_status()

        client_data = response.json()
        return JSONResponse(client_data)

    except httpx.HTTPStatusError as e:
        server.logger.error(
            f"OAuth registration failed: {e.response.status_code} - {e.response.text}"
        )
        raise
    except httpx.RequestError as e:
        server.logger.error(f"OAuth registration request failed: {e}")
        raise
    except json.JSONDecodeError as e:
        server.logger.error(f"Invalid JSON in registration request: {e}")
        raise


async def handle_authorization_request(  # noqa: RUF029
    server: Server,
    request: Request,
) -> RedirectResponse:
    """
    Handle OAuth authorization requests (RFC 6749 Section 4.1.1).

    Redirects authorization requests to the external OAuth server with
    proper parameter encoding and state management.

    Args:
        server: Server instance with OAuth configuration
        request: HTTP request with authorization parameters

    Returns:
        Redirect response to OAuth authorization server
    """
    query_params = dict(request.query_params)

    # Encode query parameters for safe transmission
    encoded_params = base64.b64encode(json.dumps(query_params).encode("utf-8")).decode(
        "utf-8"
    )

    authorization_url = (
        f"{server.env.DEVOPNESS_MCP_AUTH_SERVER_AUTHORIZE_URL}?next={encoded_params}"
    )

    return RedirectResponse(url=authorization_url)


async def handle_token_request(
    server: Server,
    request: Request,
) -> Response:
    """
    Handle OAuth token requests (RFC 6749 Section 4.1.3).

    Proxies token exchange requests to the external OAuth server
    and returns the access token response.

    Args:
        server: Server instance with OAuth configuration
        request: HTTP request with token exchange data

    Returns:
        Token response from OAuth server

    Raises:
        HTTPException: If token exchange fails at the OAuth server
    """
    try:
        form_data = await request.form()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                server.env.DEVOPNESS_MCP_AUTH_SERVER_TOKEN_URL,
                json=dict(form_data),
            )
            response.raise_for_status()

        return Response(
            content=response.content,
            media_type=response.headers.get("content-type", "application/json"),
        )

    except httpx.HTTPStatusError as e:
        server.logger.error(
            f"OAuth token exchange failed: {e.response.status_code} - {e.response.text}"
        )
        raise
    except httpx.RequestError as e:
        server.logger.error(f"OAuth token request failed: {e}")
        raise


def create_cors_preflight_response(allowed_methods: List[str]) -> PlainTextResponse:
    """
    Create a CORS preflight response for OAuth endpoints.

    Args:
        allowed_methods: List of HTTP methods allowed for the endpoint

    Returns:
        CORS preflight response with appropriate headers
    """
    return PlainTextResponse(
        "",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": ", ".join(allowed_methods),
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
            "Access-Control-Max-Age": "86400",  # 24 hours
        },
    )
