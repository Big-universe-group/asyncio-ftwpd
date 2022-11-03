"""
test: asyncio.wait(return_when=FIRST_COMPLETE)  有一个完成即返回
"""
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
    # 注意, 每一个IO动作都需要使用async注释
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


async def asynchronous():
    futures = [fetch_ip(service) for service in SERVICES]
    # wait返回已完成task列表, pending列表, 见1c中说明
    # 参数return_when表示只有有一个任务完成就返回
    done, _ = await asyncio.wait(
        futures, return_when=FIRST_COMPLETED)

    # 注意, 这里没有对pending任务做处理
    print(done.pop().result())
    print('=============================')


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
