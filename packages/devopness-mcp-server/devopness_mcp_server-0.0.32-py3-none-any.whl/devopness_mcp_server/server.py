from typing import cast

from fastmcp.server.server import logger

from devopness_mcp_server.lib.devopness_api import get_devopness_client
from devopness_mcp_server.lib.environment import EnvironmentVariables
from devopness_mcp_server.lib.middlewares import register_middlewares
from devopness_mcp_server.lib.patch import (
    patch_oauth_middleware_and_routes,
    patch_server_context_injection,
)
from devopness_mcp_server.lib.tools import register_tools
from devopness_mcp_server.lib.types import MCP_TRANSPORT_PROTOCOL, Server


class MCPServer(Server):
    def __init__(self, env: EnvironmentVariables) -> None:
        super().__init__(
            name="Devopness MCP Server",
        )

        logger.info(f"Starting {self.name} setup...")

        self.env = env
        self.devopness = get_devopness_client(env)
        self.logger = logger

        register_middlewares(self)
        register_tools(self)

        if (self.env.DEVOPNESS_MCP_SERVER_TRANSPORT) == "streamable-http":
            patch_oauth_middleware_and_routes(self)

        patch_server_context_injection(self)

        logger.info(f"Finished {self.name} setup.")

    def start(self) -> None:
        transport = cast(
            MCP_TRANSPORT_PROTOCOL,
            self.env.DEVOPNESS_MCP_SERVER_TRANSPORT,
        )

        match transport:
            case "stdio":
                super().run(transport, show_banner=False)

            case "streamable-http":
                super().run(
                    transport,
                    show_banner=False,
                    host=self.env.DEVOPNESS_MCP_SERVER_HOST,
                    port=self.env.DEVOPNESS_MCP_SERVER_PORT,
                )
