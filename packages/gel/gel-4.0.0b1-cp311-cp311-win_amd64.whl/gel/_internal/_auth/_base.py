# SPDX-PackageName: gel-python
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright Gel Data Inc. and the contributors.

from __future__ import annotations
from typing import Any, Generic, TYPE_CHECKING, TypeVar

import dataclasses
import logging

import httpx

if TYPE_CHECKING:
    import gel
    from . import _pkce as pkce_mod


logger = logging.getLogger("gel.auth")


@dataclasses.dataclass
class BaseServerFailedResponse:
    status_code: int
    message: str


C = TypeVar("C", bound=httpx.Client | httpx.AsyncClient)


class BaseClient(Generic[C]):
    def __init__(
        self, *, connection_info: gel.ConnectionInfo, **kwargs: Any
    ) -> None:
        if "base_url" not in kwargs:
            params = connection_info.params
            scheme = "http" if params.tls_security == "insecure" else "https"
            base_url = httpx.URL(
                scheme=scheme,
                host=connection_info.host,
                port=connection_info.port,
            )
            kwargs["base_url"] = base_url.join(
                f"branch/{params.branch}/ext/auth"
            )
        if "verify" not in kwargs:
            kwargs["verify"] = connection_info.params.make_ssl_ctx()
        self._client = self._init_http_client(**kwargs)

    def _init_http_client(self, **kwargs: Any) -> C:
        raise NotImplementedError()

    def _generate_pkce(self) -> pkce_mod.BasePKCE[C]:
        raise NotImplementedError()

    def _pkce_from_verifier(self, verifier: str) -> pkce_mod.BasePKCE[C]:
        raise NotImplementedError()

    async def _send_http_request(
        self, request: httpx.Request
    ) -> httpx.Response:
        raise NotImplementedError()

    async def _http_request(self, *args: Any, **kwargs: Any) -> httpx.Response:
        request = self._client.build_request(*args, **kwargs)
        try:
            logger.debug(
                "sending HTTP %s to %r: %r",
                request.method,
                request.url,
                request.content,
            )
        except httpx.RequestNotRead:
            logger.debug("sending HTTP %s to %r", request.method, request.url)
        response = await self._send_http_request(request)
        logger.debug(
            "%r returned response: [%d] %s",
            request.url,
            response.status_code,
            response.text,
        )
        return response
