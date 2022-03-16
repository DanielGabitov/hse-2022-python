import os
import sys
import time
import random
import aiohttp
import asyncio
import aiofiles

URL = 'https://picsum.photos/200'


async def routine(*, n: int, path: str):
    async with aiohttp.ClientSession() as session:
        for i in range(n):
            async with session.get(URL) as response:
                img_path = os.path.join(path, f'img_{i}.jpg')
                async with aiofiles.open(f'{img_path}', 'bw') as file:
                    await file.write((await response.read()))
                time.sleep(random.random())


if __name__ == "__main__":
    img_number: int = int(sys.argv[1])
    folder_path: str = sys.argv[2]
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    asyncio.run(routine(n=img_number, path=folder_path))
