# skyclient.py  ───────────────────────────────────────────────────────────────
import time
import logging
from typing import Optional, Dict, Any

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError
from cachetools import TTLCache

logger = logging.getLogger("Sky")

__all__ = ("Sky", "APIError")

class APIError(Exception):
    """Sky-server вернул {'error': ...}"""
    pass

class SkyManager:
    """
    Telegram-SDK для SkyManager traffic-bot platform
    """

    # BASE_URL = "https://boxer-merry-abnormally.ngrok-free.app"
    BASE_URL = "https://api.skymanager.top"

    def __init__(
        self,
        key: str,
        *,
        debug: bool = False,
        timeout: float = 5.0,                 # сек. на весь HTTP-запрос
        verify_ssl: bool = True,
        service_shutdown_timeout: int = 60,   # сек. паузы после сбоя
        cache_ttl: int = 60,                  # сек. кеширования «skip»
        **request_kwargs,
    ):
        if not isinstance(key, str):
            raise TypeError("key must be a string")

        self.key = key
        self.debug = debug
        self.timeout = float(timeout)
        self.verify_ssl = verify_ssl

        self.service_shutdown_timeout = int(service_shutdown_timeout)
        self._service_shutdown = 0.0                      # до какого момента «молчим»

        self._cache: TTLCache[int, bool] = TTLCache(maxsize=10_000, ttl=cache_ttl)

        # доп. параметры передаются напрямую в aiohttp (proxy, headers и т. д.)
        self.request_kwargs = request_kwargs

    # ---------------------------------------------------------------- private
    async def _request(self, method: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Все HTTP-запросы идут сюда.
        * Отдельная сессия → отмена по таймауту не «подвешивает» пул сокетов.
        * ClientTimeout гарантирует, что aiohttp завершит корутину вовремя.
        """
        url = f"{self.BASE_URL}/{method}"
        payload = {"key": self.key}
        if params:
            payload.update(params)

        # общий таймаут + (не)проверка SSL
        timeout_cfg = aiohttp.ClientTimeout(total=self.timeout)
        ssl_param = None if self.verify_ssl else False

        async with aiohttp.ClientSession(timeout=timeout_cfg) as session:
            async with session.post(
                url,
                json=payload,
                ssl=ssl_param,
                headers={"Content-Type": "application/json"},
                **self.request_kwargs,
            ) as response:
                try:
                    result = await response.json()
                except ContentTypeError:
                    # сервер вернул не-JSON (502/504 и т. п.)
                    raw = await response.text()
                    logger.warning("[Sky] bad content-type %s: %.200s", response.content_type, raw)
                    result = {}

                if self.debug:
                    logger.debug("[Sky] %s → %s", method, result)

                return result

    def _server_down(self) -> bool:
        """Проверяем, находимся ли мы в режиме «паузы» после неудачи."""
        return time.time() < self._service_shutdown + self.service_shutdown_timeout

    # ---------------------------------------------------------------- helpers
    async def _safe_request(self, method: str, params: Dict[str, Any] | None = None) -> Dict[str, Any] | None:
        """
        Выполнить запрос с обработкой сбоев.
        При ошибке/таймауте ⇒ ставим «паузу» и возвращаем None.
        """
        if self._server_down():
            return None

        try:
            return await self._request(method, params)
        except (ClientConnectorError, aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.warning("[Sky] network err: %s", e)
        except Exception as e:
            logger.exception("[Sky] unexpected err: %s", e)

        self._service_shutdown = time.time()
        return None

    # ---------------------------------------------------------------- public
    async def get_me(self) -> Dict[str, Any]:
        data = await self._safe_request("get_me")
        return data or {}

    async def check(
        self,
        user_id: int,
        *,
        language_code: Optional[str] = None,
        message: Dict[str, str] | None = None,
        **extra,
    ) -> bool:
        """
        True  → пропускаем пользователя
        False → показываем tasks
        """
        # валидация параметров
        if not self.key or not isinstance(user_id, int) or user_id < 0:
            return True

        # сервер «молчит» или юзер уже кеширован
        if self._server_down() or self._cache.get(user_id, False):
            return True

        params: Dict[str, Any] = {"user_id": user_id, **extra}
        if language_code:
            params["language_code"] = language_code
        if message:
            params["message"] = message

        result = await self._safe_request("check", params)
        if result is None:           # ошибка / таймаут
            return True

        if "error" in result and "skip" not in result:
            raise APIError(result["error"])

        skip = bool(result.get("skip", True))
        if skip and "error" not in result:
            self._cache[user_id] = True

        return skip

    async def get_tasks(
        self,
        user_id: int,
        *,
        limit: int = 5,
        language_code: Optional[str] = None,
        message: Dict[str, str] | None = None,
        **extra,
    ) -> Dict[str, Any]:
        if not isinstance(user_id, int) or user_id < 0 or self._server_down():
            return {}

        params: Dict[str, Any] = {"user_id": user_id, "limit": limit, **extra}
        if language_code:
            params["language_code"] = language_code
        if message:
            params["message"] = message

        result = await self._safe_request("get_tasks", params)
        return result or {}

    async def check_tasks(self, user_id: int, bundle_id: str, **extra) -> bool:
        if (not isinstance(user_id, int)) or user_id < 0 or not bundle_id or self._server_down():
            return False

        params = {"user_id": user_id, "bundle_id": bundle_id, **extra}

        result = await self._safe_request("check_tasks", params)
        return bool(result and result.get("done"))