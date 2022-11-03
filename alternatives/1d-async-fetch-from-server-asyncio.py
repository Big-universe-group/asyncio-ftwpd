"""
test: 测试urllib同步获取和aiohttp异步获取同一个资源的区别
注意: 这里使用asyncio.ensure_future封装coroutine对象
"""
import time
import urllib.request
import asyncio
import aiohttp

URL = 'https://api.github.com/events'
MAX_CLIENTS = 3


def fetch_sync(pid):
    print('Fetch sync process {} started'.format(pid))
    start = time.time()
    with urllib.request.urlopen(URL) as response:
        datetime = response.getheader('Date')

    print('Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start))

    return datetime


async def aiohttp_get(url, pid):
    """Nothing to see here, carry on ..."""
    print(f'Aiohttp start: {pid}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f'aiohttp get complete:{pid}')
            return response


async def fetch_async(pid):
    """ 基于aiohttp来异步请求资源 """
    print('Fetch async process {} started'.format(pid))
    start = time.time()
    # 所有 await装饰的语句都是IO操作逻辑
    response = await aiohttp_get(URL, pid)
    datetime = response.headers.get('Date')

    print('Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start))

    response.close()
    return datetime


def synchronous():
    start = time.time()
    # 注意fetch_sync是一个同步IO函数, 所以这里肯定是阻塞一个个执行
    for i in range(1, MAX_CLIENTS + 1):
        fetch_sync(i)
    print("Process took: {:.2f} seconds".format(time.time() - start))


async def asynchronous():
    start = time.time()
    # 注意, 这里是fetch_async而非fetch_sync
    tasks = [asyncio.ensure_future(
        fetch_async(i)) for i in range(1, MAX_CLIENTS + 1)]
    # 关于asyncio.wait见1c中说明
    print('>>>wait')
    await asyncio.wait(tasks)
    print("Process took: {:.2f} seconds".format(time.time() - start))


print('Synchronous:')
synchronous()
print('--------------------->end\n\n')

print('Asynchronous:')
ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
print('--------------------->end')
