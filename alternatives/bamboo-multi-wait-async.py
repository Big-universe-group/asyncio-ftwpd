""" 测试一个函数出现多个await的情况
参考: https://stackoverflow.com/questions/34377319/combine-awaitables-like-promise-all
"""
import time
import asyncio


async def say_after_time(delay, what):
    await asyncio.sleep(delay)
    print(f'Say: {what}, delay: {delay}')


async def save_multi_after_time(what):
    for i in range(3):
        await say_after_time(i + 1, what)


async def multi_wait():
    """ 关于一个coroutine对象中多个await, 参考2a-XXX.py中的as_completed用法 """
    # 1. await一个函数, 该函数里面串行await多个coroutine对象
    print(f'----> 多个await1: {round(time.time(), 4)}')
    await save_multi_after_time('hello')

    # 2. 使用gather返回await对象(包含多个并发执行tasks)
    #  这里也可以使用: asyncio.wait([asyncio.ensure_future(..) for i in range(3)])替换下面的gather
    print(f'----> 多个await2: {round(time.time(), 4)}')
    await asyncio.gather(*[say_after_time(i+1, 'gather') for i in range(3)])

    # 3. 返回一个coroutine函数
    print(f'----> 多个await3: {round(time.time(), 4)}')
    await say_after_time(3, 'world')

    print(f'----> 多个await end: {round(time.time(), 4)}')


async def multi_wait_other():
    print(f'----> 多个await first: {round(time.time(), 4)}')
    await say_after_time(2, 'hello')
    print(f'----> 多个await first end: {round(time.time(), 4)}')


async def multi_wait_second():
    print(f'----> 多个await second: {round(time.time(), 4)}')
    await say_after_time(3, 'world')
    print(f'----> 多个await second end: {round(time.time(), 4)}')


loop = asyncio.get_event_loop()
loop.run_until_complete(multi_wait())
loop.close()
