#!/usr/bin/env python3

from aiohttp import web
import asyncio
import hashlib
import logging
import requests
import time
import urllib.request

NUM = 0
USE_REQUESTS = True
logging.basicConfig(format='%(levelname)s | %(message)s', level=logging.INFO)


async def handle_download(request):
    global NUM
    NUM += 1

    post_data = await request.post()
    if 'url' not in post_data:
        raise web.HTTPBadRequest()

    url = post_data['url']
    logging.info(f'request #{NUM}: {url}')
    start = time.time()

    if USE_REQUESTS:
        response = requests.get(post_data['url'])
        data = response.content
        headers = response.headers
        status_code = response.status_code
    else:
        response = urllib.request.urlopen(post_data['url'])
        data = response.read()
        headers = {k: v for k, v in response.headers.items()}
        status_code = response.status

    stop = time.time()
    hsh = hashlib.md5(data).hexdigest()

    with open(f'/tmp/{hsh}.bin', 'wb') as f:
        f.write(data)

    logging.info(f'request #{NUM}: downloaded {len(data)/1024/1024}MB in {(stop - start):.2f}s. code: {status_code}, hsh: {hsh}')
    return web.Response()


async def init(loop):
    app = web.Application()
    app.router.add_route('POST', '/dl', handle_download)
    return await loop.create_server(app.make_handler(), '0.0.0.0', 8000)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
