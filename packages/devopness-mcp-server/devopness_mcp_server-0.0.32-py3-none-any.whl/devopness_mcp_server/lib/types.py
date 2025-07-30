"""
This module defines types and constants used to manage data visibility
when interacting with Large Language Models (LLMs) in the MCP Server.
"""

from logging import Logger
from typing import Annotated, Any, List, Literal, Optional, cast

from fastmcp import Context, FastMCP
from pydantic import Field

from devopness import DevopnessClientAsync
from devopness.base.base_model import DevopnessBaseModel

from .environment import EnvironmentVariables

MCP_TRANSPORT_PROTOCOL = Literal[
    "stdio",
    "streamable-http",
]


MAX_RESOURCES_PER_PAGE = 5
"""
The Large Language Models (LLMs) can start hallucinating during resource listing
if the volume of data is 'large', which is easily achieved when listing an
environment resource such as an application or server.

To avoid the hallucinations that can lead to errors and harm to the user of the
MCP Server, we set the maximum number of resources per page for listing.

If the resource that the user is looking for is not on the first page,
the LLM is able to list the <page + 1> until it finds the user's resource.
"""

type ResourceType = Literal[
    "application",
    "credential",
    "daemon",
    "environment",
    "project",
    "server",
    "service",
    "ssh-key",
    "ssl-certificate",
    "virtual-host",
]

type TypeListServerID = Annotated[
    List[int],
    Field(
        min_length=1,
        description="List of Server IDs to which the action will be targeted.",
    ),
]


class ExtraData(DevopnessBaseModel):
    url_web_permalink: Optional[str] = None
    application_hide_config_file_content: bool = False
    server_instance_type: Optional[str] = None


type TypeExtraData = Optional[ExtraData]


class Server(FastMCP[Any]):
    """
    Custom Devopness MCP Server model extending the base FastMCP.

    This class adds additional fields required by Devopness-specific tools,
    such as access to environment variables via the `env` property.
    """

    env: EnvironmentVariables
    devopness: DevopnessClientAsync
    logger: Logger


class ServerContext(Context):
    """
    Custom context wrapper for FastMCP, injecting the custom `Server` class.

    This overrides the default `fastmcp` attribute from the base `Context` class,
    casting it to the custom `Server` model to allow tool access to extended fields
    (e.g., `fastmcp.env`).
    """

    server: Server
    devopness: DevopnessClientAsync

    def __init__(self, ctx: Context) -> None:
        # Inject the custom `Server` and `Devopness`
        self.server = cast(Server, ctx.fastmcp)
        self.devopness = self.server.devopness

        # Mirror the base `Context` attributes
        self.fastmcp = ctx.fastmcp
        self._tokens = ctx._tokens
        self._notification_queue = ctx._notification_queue
