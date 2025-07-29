import asyncio
from collections.abc import Coroutine
from typing import Any, TypeVar

T = TypeVar("T")


def run(coroutine: Coroutine[Any, Any, T]) -> T:
    """Run a coroutine and return the result, using uvloop if available."""
    try:
        import uvloop  # type: ignore[import-not-found]  # noqa: PLC0415

        return uvloop.run(coroutine)
    except ImportError:
        return asyncio.run(coroutine)
