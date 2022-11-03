"""
test: 测试aiohttp异步获取资源
注意: 相比1d, 这里使用asyncio.as_completed对coroutine队列列表进行封装, 返回generator
"""
import time
import random
import asyncio
import aiohttp

URL = 'https://api.github.com/events'
MAX_CLIENTS = 3


async def aiohttp_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response


async def fetch_async(pid):
    start = time.time()
    sleepy_time = random.randint(2, 5)
    print('Fetch async process {} started, sleeping for {} seconds'.format(
        pid, sleepy_time))

    await asyncio.sleep(sleepy_time)

    response = await aiohttp_get(URL)
    dt = response.headers.get('Date')

    response.close()
    return 'Process {}: {}, took: {:.2f} seconds'.format(
        pid, dt, time.time() - start)


async def fetch_sleep_async(pid):
    """ 确保每次sleep时间相同来验证协程是否提升了效率 """
    print('Fetch sleep async process {} started'.format(pid))
    start = time.time()
    dt = time.ctime()
    await asyncio.sleep(2 + pid)
    print('Sleep Process {}: {}, took: {:.2f} seconds'.format(
        pid, dt, time.time() - start))
    return dt


# 1. 所有async修饰的函数都是coro协程对象
# 2. as_completed接收tasks列表并返回一个可迭代的coro生成器
# 3. 注意, 从输出(多执行几次)来看, await阻塞之后异步调用顺序不固定
async def asynchronous():
    start = time.time()
    futures = [fetch_async(i) for i in range(1, MAX_CLIENTS + 1)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        print('<<' * (i + 1) + f' Process {i + 1}')
        result = await future
        print('{} {}'.format(">>" * (i + 1), result))

    print("Process took: {:.2f} seconds".format(time.time() - start))


async def bambooasync():
    """ 一个函数中包含多个IO操作, 其中一个IO操作为同步 """
    print('\n\n')
    start = time.time()
    _start, _dt = 0, 0
    futures = [fetch_sleep_async(i) for i in range(1, MAX_CLIENTS + 2)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        print('<<' * (i + 1) + f' Process {i + 1}')
        await future
        if not _start:
            _start = time.time()
        print('{} {}'.format(">>" * (i + 1), time.ctime()))
        time.sleep(2)
        print('{} block sleep: {:.2f}'.format(">>" * (i + 1), time.time() - _start))

    print("Bamboo took: {:.2f} seconds".format(time.time() - start))


# 1. 在整个async的调用过程中, 所有的对象都是异步对象, 特别是涉及IO的操作, 任何涉及异步IO的函数都需要使用async注释
# 否则异步就如同虚设
#   a. run_until_complete调用: 一个coro(coroutine)协程对象CO-1
#   b. CO1中包含对tasks列表的迭代和异步等待
#   c. 每一个Task中包含两个coro中断
#
# 2. 最后关于async修饰的函数中若存在某个同步阻塞, 则效率可能仍然还是不高, 见上面的bamobooasync函数
#   另外, 一个async中多个await, 并不能保证所有task都是先执行完第一个await再执行第二await的(重要)
ioloop = asyncio.get_event_loop()
rb = asynchronous()
ioloop.run_until_complete(rb)

bamboorb = bambooasync()
ioloop.run_until_complete(bamboorb)
ioloop.close()
