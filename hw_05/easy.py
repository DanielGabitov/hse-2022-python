import os
import sys
import aiohttp
import asyncio
import aiofiles


URL = 'https://picsum.photos/200'


async def routine(*, session: aiohttp.ClientSession, path: str, img_name: str):
    async with session.get(URL) as response:
        content = await response.read()
        img_path = os.path.join(path, img_name)
        async with aiofiles.open(img_path, mode='bw') as file:
            await file.write(content)
            await file.close()


async def main_routine(*, n: int, path: str):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *((routine(session=session, path=path, img_name=f"img_{i}.jpg"))
              for i in range(n))
        )


if __name__ == "__main__":
    img_number: int = int(sys.argv[1])
    folder_path: str = sys.argv[2]
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    asyncio.run(main_routine(n=img_number, path=folder_path))
