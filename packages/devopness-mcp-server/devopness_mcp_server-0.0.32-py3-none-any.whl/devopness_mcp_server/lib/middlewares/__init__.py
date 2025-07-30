from ..types import Server
from .auth_middleware import AuthMiddleware


def register_middlewares(server: Server) -> None:
    middlewares = [
        AuthMiddleware,
    ]

    for middleware in middlewares:
        server.logger.info(f"Registering {middleware.__name__}")
        server.add_middleware(middleware())
