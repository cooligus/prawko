import json
import os
import requests
import ids
import asyncio
import aiofiles
import aiohttp

async def download_images(section_id):
    with open('tmp/{}.json'.format(section_id)) as f:
        d = json.load(f)
        async with aiohttp.ClientSession() as session:
            try:
                os.mkdir(os.path.join('tmp', str(section_id)))
            except OSError:
                pass
            for elem in d:
                if elem['Image'] != '':
                    async with session.get(elem['Image']) as resp:
                        if resp.status == 200:
                            f = await aiofiles.open(os.path.join('tmp', str(section_id), ids.get_element_id(elem['Image'])) + '.jpg', mode='wb')
                            await f.write(await resp.read())
                            await f.close()
                if elem['Video'] != '':
                    async with session.get(elem['Video']) as resp:
                        if resp.status == 200:
                            f = await aiofiles.open(os.path.join('tmp', str(section_id), ids.get_element_id(elem['Video'])) + '.mp4', mode='wb')
                            await f.write(await resp.read())
                            await f.close()