from __future__ import annotations

__version__ = "v0.0.192"
__license__ = "MIT License"

from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmissionError(Exception):
    pass


class StopPropagationError(StopAsyncIteration):
    pass


class ContinuePropagationError(StopAsyncIteration):
    pass


crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")

# ruff: noqa: E402
from . import enums, errors, filters, handlers, raw, types
from .client import Client
from .sync import compose, idle

__all__ = [
    "Client",
    "ContinuePropagationError",
    "StopPropagationError",
    "StopTransmissionError",
    "compose",
    "crypto_executor",
    "enums",
    "errors",
    "filters",
    "handlers",
    "idle",
    "raw",
    "types",
]
