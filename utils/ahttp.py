import aiohttp, asyncio
from io import BytesIO


class HTTP:
    def __init__(self, timeout=5):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        self.image_types = ["image/png", "image/pjpeg", "image/jpeg", "image/x-icon"]
        self.media_types = self.image_types + ["image/gif"]

    async def is_image(self, url: str):
        try:
            async with self.session.head(url) as resp:
                if resp.status == 200:
                    mime = resp.headers.get("Content-type", "").lower()
                    if any([mime == x for x in self.image_types]):
                        return True
                    else:
                        return False
        except:
            return False

    async def is_safe(self, url: str, max_bytes: int = 4194304):
        try:
            async with self.session.head(url) as resp:
                if resp.status == 200:
                    tBytes = int(resp.headers.get("content-length", str(max_bytes + 1)))
                    return tBytes <= max_bytes
        except:
            return False

    async def is_gif(self, url: str):
        try:
            async with self.session.head(url) as resp:
                if resp.status == 200:
                    mime = resp.headers.get("Content-type", "").lower()
                    if mime == "image/gif":
                        return True
                    else:
                        return False
        except:
            return False

    async def download(self, url: str, path: str):
        try:
            async with self.session.get(url) as resp:
                data = await resp.read()
                with open(path, "wb") as f:
                    f.write(data)
        except:
            return

    async def bytes_download(self, url: str, no_io: bool = False):
        try:
            async with self.session.get(url) as resp:
                data = await resp.read()
                if no_io:
                    return data

                return BytesIO(data)
        except:
            print("asdasd")
            return

    async def get_json(self, url: str):
        try:
            async with self.session.get(url) as resp:
                try:
                    load = await resp.json()
                    return load
                except:
                    return {}
        except:
            return {}

    async def get_text(self, url: str):
        try:
            async with self.session.get(url) as resp:
                try:
                    text = await resp.text()
                    return text
                except:
                    return
        except:
            return

    async def get(self, url: str, **kwargs):
        headers = kwargs.get("headers")
        params = kwargs.get("params")
        return_type = kwargs.get("return_type")
        t = kwargs.get("timeout")
        if t is not None:
            timeout = aiohttp.ClientTimeout(total=t)
        else:
            timeout = self.timeout

        try:
            async with self.session.get(
                url, headers=headers, params=params, timeout=timeout
            ) as resp:
                if return_type == "text":
                    try:
                        text = await resp.text()
                        return text
                    except:
                        return ""
                elif return_type == "json":
                    try:
                        load = await resp.json()
                        return load
                    except:
                        return {}
                elif return_type == "bytes":
                    try:
                        load = await res.read()
                        return BytesIO(load)
                    except:
                        return None
                else:
                    return resp
        except:
            return

    async def post(self, url: str, **kwargs):
        data = kwargs.get("data")
        headers = kwargs.get("headers")
        return_type = kwargs.get("return_type")
        t = kwargs.get("timeout", 5)
        timeout = aiohttp.ClientTimeout(total=t)
        if t is not None:
            timeout = aiohttp.ClientTimeout(total=t)
        else:
            timeout = self.timeout
        try:
            async with self.session.post(
                url, data=data, headers=headers, timeout=timeout
            ) as resp:
                if return_type == "text":
                    try:
                        text = await resp.text()
                        return text
                    except:
                        return ""
                elif return_type == "json":
                    try:
                        load = await resp.json()
                        return load
                    except:
                        return {}
                elif return_type == "bytes":
                    try:
                        load = await resp.read()
                        return BytesIO(load)
                    except:
                        return None
                else:
                    return resp
        except:
            return

    async def close(self):
        await self.session.close()
