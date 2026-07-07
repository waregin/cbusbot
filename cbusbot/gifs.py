"""GIF search via the Klipy API (Tenor drop-in replacement; Tenor shut down 2026-06-30).

Klipy documents migration as swapping tenor.googleapis.com for api.klipy.com.
Sources disagree on the exact response shape, so extraction handles the
Tenor-v2 shape (results[].media_formats.gif.url), the Tenor-v1 shape
(results[].url), and Klipy's native shape (data[].file.<size>.gif.url).

Quick manual test once KLIPY_KEY is in .env:
    python -m cbusbot.gifs twerking
"""

import logging
import os
import random

import aiohttp

from cbusbot.config import ROOT

log = logging.getLogger(__name__)

SEARCH_URL = "https://api.klipy.com/v2/search"


class GifSearchError(RuntimeError):
    pass


def _extract_urls(payload: dict) -> list[str]:
    urls: list[str] = []
    results = payload.get("results")
    if isinstance(results, list):  # Tenor v2 / v1 compatible
        for r in results:
            media = r.get("media_formats") or {}
            url = (media.get("gif") or {}).get("url") or r.get("url")
            if url:
                urls.append(url)
        return urls
    data = payload.get("data")  # Klipy native
    items = data.get("data") if isinstance(data, dict) else data
    for r in items or []:
        files = r.get("file") or {}
        for size in ("hd", "md", "sm"):
            url = ((files.get(size) or {}).get("gif") or {}).get("url")
            if url:
                urls.append(url)
                break
    return urls


async def search_gif(query: str, *, limit: int = 25) -> str:
    """Return the URL of a random GIF matching `query`."""
    key = os.environ.get("KLIPY_KEY")
    if not key:
        raise GifSearchError("KLIPY_KEY is not set in the environment/.env")
    params = {"q": query, "key": key, "limit": str(limit)}
    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(SEARCH_URL, params=params) as resp:
            resp.raise_for_status()
            payload = await resp.json()
    urls = _extract_urls(payload)
    if not urls:
        raise GifSearchError(f"no gif results for {query!r} (payload keys: {list(payload)})")
    return random.choice(urls)


if __name__ == "__main__":
    import asyncio
    import sys

    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    print(asyncio.run(search_gif(sys.argv[1] if len(sys.argv) > 1 else "twerking")))
