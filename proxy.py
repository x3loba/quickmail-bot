# language: Python, file: proxy.py
import asyncio, itertools, random

class ProxyPool:
    def __init__(self, path="proxies.txt"):
        try:
            self.proxies = [l.strip() for l in open(path) if l.strip() and not l.startswith("#")]
        except FileNotFoundError:
            self.proxies = []
        random.shuffle(self.proxies)
        self._it = itertools.cycle(self.proxies) if self.proxies else None
        self._lock = asyncio.Lock()

    async def next(self):
        if not self._it:
            return None
        async with self._lock:
            return next(self._it)
