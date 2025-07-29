from typing import Any
from fastapi.testclient import TestClient
from ascender.core import Provider
from ascender.core.applications.application import Application

from httpx._client import CookieTypes


def provideTestClient(
        raise_server_exceptions: bool = True,
        root_path: str = "",
        backend: str = "asyncio",
        backend_options: dict[str, Any] | None = None,
        cookies: CookieTypes = None,
        headers: dict[str, str] = None,
) -> Provider:
    return {
        "provide": TestClient,
        "use_factory": lambda application: TestClient(
            app=application.app, 
            raise_server_exceptions=raise_server_exceptions,
            root_path=root_path,
            backend=backend,
            backend_options=backend_options,
            cookies=cookies,
            headers=headers
        ),
        "deps": [Application]
    }