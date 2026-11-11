from __future__ import annotations

import asyncio

import aiohttp
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from app.core.clients.proxy import _open_upstream_websocket

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("extension_header", [None, "Sec-WebSocket-Extensions", "sec-websocket-extensions"])
async def test_custom_upgrade_preserves_text_binary_and_buffered_messages(extension_header: str | None) -> None:
    messages: list[str | bytes] = ["héllo 世界", b"\x00\xff\x80"]
    # Small messages also consume queue space. This burst exceeds its high-water
    # mark without requiring a large test payload.
    messages.extend(f"event-{index}" for index in range(2048))
    handshake_extensions: list[str | None] = []
    trace_headers: list[str | None] = []

    async def upstream(request: web.Request) -> web.WebSocketResponse:
        handshake_extensions.append(request.headers.get(aiohttp.hdrs.SEC_WEBSOCKET_EXTENSIONS))
        trace_headers.append(request.headers.get("X-Trace-Test"))
        websocket = web.WebSocketResponse()
        await websocket.prepare(request)
        for message in messages:
            if isinstance(message, str):
                await websocket.send_str(message)
            else:
                await websocket.send_bytes(message)
        await websocket.close()
        return websocket

    app = web.Application()
    app.router.add_get("/responses", upstream)
    headers = {"X-Trace-Test": "frame-regression"}
    if extension_header is not None:
        headers[extension_header] = "permessage-deflate"
    async with asyncio.timeout(5), TestServer(app) as server, aiohttp.ClientSession(trust_env=False) as session:
        websocket_context, websocket = await _open_upstream_websocket(
            session=session,
            url=str(server.make_url("/responses")),
            headers=headers,
            connect_timeout_seconds=2,
            max_msg_size=1024,
        )
        async with websocket_context:
            assert websocket.compress == 0
            for expected in messages:
                message = await websocket.receive()
                expected_type = aiohttp.WSMsgType.TEXT if isinstance(expected, str) else aiohttp.WSMsgType.BINARY
                assert message.type == expected_type
                assert message.data == expected
            assert (await websocket.receive()).type == aiohttp.WSMsgType.CLOSE
            assert websocket.exception() is None

    assert handshake_extensions == [None]
    assert trace_headers == ["frame-regression"]
