import random

from aiohttp import ClientSession

GITHUB_BASE_URL = "https://api.github.com"
BASE_HEADERS = {
    "Accept:": "application/vnd.github.v3+json"
}

RESOURCE_REPO = "lemonsaurus/lemonsaurus"
CONNECTION_IMAGE_PATH = "tyrant"
FALLBACK_IMAGE = "https://api.github.com/repos/lemonsaurus/lemonsaurus/contents/tyrant/18.png?ref=main"


async def get_random_connection_image(session: ClientSession) -> str:
    url = f"{GITHUB_BASE_URL}/repos/{RESOURCE_REPO}/contents/{CONNECTION_IMAGE_PATH}"
    async with session.get(url, headers=BASE_HEADERS) as r:
        if r.status >= 400:
            return FALLBACK_IMAGE
        resp = await r.json()
    image = random.choice(resp)
    return image.get("download_url") or FALLBACK_IMAGE
