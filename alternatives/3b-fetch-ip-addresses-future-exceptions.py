"""
test: 测试async异步异常情况, 异常会在调用result时触发
Concurrency和Parallelism: 并发和并行
协程和线程: 协程由开发者来决定如何进行任务的切换, 数据共享也比较容易, 至少不会出现并行
"""

from collections import namedtuple
import time
import asyncio
import traceback
import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'this-is-not-an-attr'),
    Service('borken', 'http://no-way-this-is-going-to-work.com/json', 'ip')
)

async def aiohttp_get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_ip(service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    try:
        json_response = await aiohttp_get_json(service.url)
    except:
        return '{} is unresponsive'.format(service.name)

    ip = json_response[service.ip_attr]
    return '{} finished with result: {}, took: {:.2f} seconds'.format(
        service.name, ip, time.time() - start)


async def asynchronous():
    futures = [fetch_ip(service) for service in SERVICES]
    done, _ = await asyncio.wait(futures)

    print('======' * 5)
    # 注意, 在进行future.result()打印的时候会把coroutine中的异常打印出来
    for future in done:
        try:
            print(future.result())
        except:
            print("Unexpected error: {}".format(traceback.format_exc()))


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
