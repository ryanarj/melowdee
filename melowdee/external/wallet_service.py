

import aiohttp


async def generate_wallet(password):
    async with aiohttp.ClientSession() as session:
        url = 'http://127.0.0.1:8080/genWallet'
        async with session.post(url=url, data={'password': password}) as resp:
            body = await resp.json()
            return body
