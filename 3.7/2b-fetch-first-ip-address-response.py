from collections import namedtuple
import time
import asyncio
from concurrent.futures import FIRST_COMPLETED
import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query')
)


async def aiohttp_get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_ip(service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    json_response = await aiohttp_get_json(service.url)
    ip = json_response[service.ip_attr]

    return '{} finished with result: {}, took: {:.2f} seconds'.format(
        service.name, ip, time.time() - start)


async def main():
    futures = [fetch_ip(service) for service in SERVICES]
    # 3.8之后asyncio.wait不会自动将coro对象变为Task对象, 需要使用create_task, 否则告警
    # https://blog.csdn.net/m0_69082030/article/details/124327891
    futures = [asyncio.create_task(future) for future in futures]
    done, pending = await asyncio.wait(
        futures, return_when=FIRST_COMPLETED)

    print(done.pop().result())


# 3.5方式, 在3.7运行会报错
#  ioloop = asyncio.get_event_loop()
#  ioloop.run_until_complete(main())
#  ioloop.close()
# 3.7方式
asyncio.run(main())
