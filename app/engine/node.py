from typing import Callable, Awaitable

class Node:
    def __init__(self, name: str, func: Callable[..., Awaitable[dict]]):
        self.name = name
        self.func = func

    async def run(self, state: dict):
        return await self.func(state)
