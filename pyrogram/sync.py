from __future__ import annotations

import asyncio
import functools
import inspect
import threading

from pyrogram import types
from pyrogram.methods import Methods
from pyrogram.methods.utilities import compose as compose_module
from pyrogram.methods.utilities import idle as idle_module


def async_to_sync(obj, name) -> None:
    function = getattr(obj, name)
    main_loop = asyncio.get_event_loop()

    def async_to_sync_gen(agen, loop, is_main_thread):
        async def anext(agen):
            try:
                return await agen.__anext__(), False
            except StopAsyncIteration:
                return None, True

        while True:
            if is_main_thread:
                item, done = loop.run_until_complete(anext(agen))
            else:
                item, done = asyncio.run_coroutine_threadsafe(
                    anext(agen),
                    loop,
                ).result()

            if done:
                break

            yield item

    @functools.wraps(function)
    def async_to_sync_wrap(*args, **kwargs):
        coroutine = function(*args, **kwargs)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if (
            threading.current_thread() is threading.main_thread()
            or not main_loop.is_running()
        ):
            if loop.is_running():
                return coroutine
            if inspect.iscoroutine(coroutine):
                return loop.run_until_complete(coroutine)

            if inspect.isasyncgen(coroutine):
                return async_to_sync_gen(coroutine, loop, True)
            return None
        if inspect.iscoroutine(coroutine):
            if loop.is_running():

                async def coro_wrapper():
                    return await asyncio.wrap_future(
                        asyncio.run_coroutine_threadsafe(coroutine, main_loop),
                    )

                return coro_wrapper()
            return asyncio.run_coroutine_threadsafe(coroutine, main_loop).result()

        if inspect.isasyncgen(coroutine):
            if loop.is_running():
                return coroutine
            return async_to_sync_gen(coroutine, main_loop, False)
        return None

    setattr(obj, name, async_to_sync_wrap)


def wrap(source) -> None:
    for name in dir(source):
        method = getattr(source, name)

        if not name.startswith("_") and (
            inspect.iscoroutinefunction(method) or inspect.isasyncgenfunction(method)
        ):
            async_to_sync(source, name)


# Wrap all Client's relevant methods
wrap(Methods)

# Wrap types' bound methods
for class_name in dir(types):
    cls = getattr(types, class_name)

    if inspect.isclass(cls):
        wrap(cls)

# Special case for idle and compose, because they are not inside Methods
async_to_sync(idle_module, "idle")
idle = idle_module.idle

async_to_sync(compose_module, "compose")
compose = compose_module.compose
