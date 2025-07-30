import asyncio
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, cast, override

import httpx
from fastmcp.server.server import logger
from mcp.server.auth.provider import AccessToken, TokenVerifier


@dataclass
class IntrospectionConfig:
    endpoint: str
    server_url: str
    timeout: float = 10.0
    connect_timeout: float = 5.0
    max_connections: int = 10
    max_keepalive_connections: int = 5
    cache_ttl: int = 300  # 5 minutes cache TTL
    max_retries: int = 3
    retry_delay: float = 1.0


@dataclass
class CachedToken:
    access_token: AccessToken
    cached_at: float
    expires_at: Optional[float] = None

    def is_expired(self, cache_ttl: int) -> bool:
        now = time.time()
        if now - self.cached_at > cache_ttl:
            return True

        return bool(self.expires_at and now >= self.expires_at)


class IntrospectionError(Exception):
    """Custom exception for introspection errors."""


class IntrospectionTokenVerifier(TokenVerifier):
    def __init__(self, config: IntrospectionConfig) -> None:
        self.config = config
        self._token_cache: Dict[str, CachedToken] = {}
        self._client: Optional[httpx.AsyncClient] = None
        self._lock = asyncio.Lock()

        self._validate_config()

    def _validate_config(self) -> None:
        if not self.config.endpoint:
            raise ValueError("Introspection endpoint is required")

        if not self.config.server_url:
            raise ValueError("Server URL is required")

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            timeout = httpx.Timeout(
                self.config.timeout, connect=self.config.connect_timeout
            )
            limits = httpx.Limits(
                max_connections=self.config.max_connections,
                max_keepalive_connections=self.config.max_keepalive_connections,
            )

            self._client = httpx.AsyncClient(
                timeout=timeout,
                limits=limits,
                verify=True,
                follow_redirects=False,  # Prevent redirect attacks
            )

        return self._client

    async def _introspect_token(self, token: str) -> Dict[str, Any]:
        client = await self._get_client()

        data = {"token": token}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        last_exception = None

        for attempt in range(self.config.max_retries):
            try:
                response = await client.post(
                    self.config.endpoint,
                    data=data,
                    headers=headers,
                )

                if response.status_code == 200:
                    return cast(dict[str, Any], response.json())

                if response.status_code == 429:
                    await asyncio.sleep(self.config.retry_delay * (2**attempt))
                    continue

                logger.info(
                    f"Token introspection returned status {response.status_code}"
                )
                return {}

            except httpx.TimeoutException as e:
                last_exception = e
                logger.warning(f"Introspection timeout (attempt {attempt + 1}): {e}")
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay * (2**attempt))

            except httpx.RequestError as e:
                last_exception = e  # type: ignore[assignment]
                logger.warning(
                    f"Introspection request error (attempt {attempt + 1}): {e}"
                )

                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay * (2**attempt))

            except Exception as e:
                last_exception = e  # type: ignore[assignment]
                logger.error(f"Unexpected error during introspection: {e}")
                break

        # All retries failed
        raise IntrospectionError(
            f"Token introspection failed after {self.config.max_retries} attempts"
        ) from last_exception

    def _validate_token_data(self, data: Dict[str, Any]) -> bool:
        token_active: bool = data.get("active", False)

        return token_active

    def _create_access_token(self, token: str, data: Dict[str, Any]) -> AccessToken:
        scopes = []
        if data.get("scope"):
            scopes = data.get("scope", "").split()

        return AccessToken(
            token=token,
            client_id=data.get("client_id", "unknown"),
            scopes=scopes,
            expires_at=data.get("exp"),
            resource=data.get("aud"),
        )

    async def _get_cached_token(self, token: str) -> Optional[AccessToken]:
        cached = self._token_cache.get(token)
        if cached and not cached.is_expired(self.config.cache_ttl):
            return cached.access_token

        # Remove expired token from cache
        if cached:
            del self._token_cache[token]

        return None

    def _cache_token(self, token: str, access_token: AccessToken) -> None:
        cached_token = CachedToken(
            access_token=access_token,
            cached_at=time.time(),
            expires_at=access_token.expires_at,
        )

        self._token_cache[token] = cached_token

        # Simple cache cleanup - remove expired entries
        expired_tokens = [
            t
            for t, cached in self._token_cache.items()
            if cached.is_expired(self.config.cache_ttl)
        ]

        for expired_token in expired_tokens:
            del self._token_cache[expired_token]

    @override
    async def verify_token(self, token: str) -> Optional[AccessToken]:
        if not token:
            return None

        cached_token = await self._get_cached_token(token)
        if cached_token:
            return cached_token

        async with self._lock:
            cached_token = await self._get_cached_token(token)
            if cached_token:
                return cached_token

            try:
                data = await self._introspect_token(token)
                if not self._validate_token_data(data):
                    return None

                access_token = self._create_access_token(token, data)
                self._cache_token(token, access_token)

                return access_token

            except IntrospectionError as e:
                logger.warning(f"Token introspection failed: {e}")
                return None

            except Exception as e:
                logger.error(f"Unexpected error during token verification: {e}")
                return None

    async def close(self) -> None:
        """Close HTTP client and cleanup resources."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

        self._token_cache.clear()


def create_introspection_verifier(
    endpoint: str,
    server_url: str,
) -> IntrospectionTokenVerifier:
    config = IntrospectionConfig(endpoint=endpoint, server_url=server_url)

    return IntrospectionTokenVerifier(config)
