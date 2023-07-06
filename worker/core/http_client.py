import aiohttp


class Client:
    def __init__(self, session):
        self.session = session

    async def send_request(self, url, proxy):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=f"http://{proxy}") as resp:
                    # you can make requests without a proxy
                    # async with session.get(url) as resp:
                    return await resp.text(encoding="utf-8")
        except aiohttp.ClientError as e:
            print(f"An error occurred: {e}")
            return None


async def get_client_session():
    async with aiohttp.ClientSession() as session:
        return session
