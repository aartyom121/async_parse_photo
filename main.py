import os
from time import perf_counter
import aiofiles
import asyncio
import aiohttp
import fake_useragent
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random
header = {
    'user-agent': user
}


async def get_response(session, lk):
    async with session.get(lk, headers=header) as resp:
        return await resp.text()


async def get_image(session, img, link_download):
    try:
        img_name = (img.find('div', class_='img_block_inner').find('div', class_='image-meta-data-container')
                    .find('div', class_='like-button no-select').get('data-image-file-name'))
        print(img_name)
        async with session.get(f'{link_download}{img_name}') as img_b:
            img_bytes = await img_b.read()
        async with aiofiles.open(f'photo/{img_name}', 'wb') as file:
            await file.write(img_bytes)
    except AttributeError:
        pass


async def main():
    if not os.path.exists('photo'):
        os.makedirs('photo')
    link_download = f'https://wallpapers-hub.art//wallpaper-images-download/'
    link = 'https://wallpapers-hub.art/group/rick-and-morty'
    async with aiohttp.ClientSession() as session:
        response = await get_response(session, link)
        soup = BeautifulSoup(response, 'lxml')
        block = soup.find('div', class_='content_inner').find('div', class_='gallery_block')
        img_block = block.find_all('div', class_='img_block')
        tasks = [get_image(session, img, link_download) for img in img_block]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start = perf_counter()
    asyncio.run(main())
    print(f"time: {perf_counter() - start:.2f}")
    # time: 3.055884100002004
