import argparse

from devopness_mcp_server.lib.environment import load_environment_variables
from devopness_mcp_server.server import MCPServer


def get_command_line_params() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Devopness MCP Server")

    parser.add_argument(
        "--transport",
        required=False,
        choices=["stdio", "streamable-http"],
        help="Communication transport protocol for the MCP Server. "
        "Can also be set via DEVOPNESS_MCP_SERVER_TRANSPORT. "
        "Defaults to streamable-http.",
    )

    parser.add_argument(
        "--host",
        required=False,
        type=str,
        help="Network interface address for the server to bind to and listen for"
        " incoming connections. "
        "Can also be set via DEVOPNESS_MCP_SERVER_HOST. "
        "Defaults to 127.0.0.1.",
    )

    parser.add_argument(
        "--port",
        required=False,
        type=int,
        help="Network port number for the server to listen on for"
        " incoming connections. "
        "Can also be set via DEVOPNESS_MCP_SERVER_PORT. "
        "Defaults to 8000.",
    )

    return parser.parse_args()


def run() -> None:
    params = get_command_line_params()
    environment = load_environment_variables(params)

    server = MCPServer(environment)
    server.start()


if __name__ == "__main__":
    run()
