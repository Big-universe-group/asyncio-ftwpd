""" 一些特殊的asyncio实例 """

import time
import asyncio


async def coro_but_not_io(pid):
    print(f'async封装的里层无中IO中断的函数>>: {pid}')


async def coro_but_exist_yield(pid):
    print(f'async封装的里层有yield但未返回Future或者Task的函数>>: {pid}')
    yield 'bifeng'  # 返回字符串但是实际需要返回Task, Future等


async def coro(pid):
    print(f'aysnc正常的协程函数: {pid}, start')
    await asyncio.sleep(1)
    print(f'aysnc正常的协程函数: {pid}, end')



ioloop = asyncio.get_event_loop()
_tasks = [asyncio.ensure_future(coro_but_not_io(i)) for i in range(1, 3)]
ioloop.run_until_complete(asyncio.wait(_tasks))
ioloop.close()

try:
    asyncio.set_event_loop(asyncio.new_event_loop())  # 创建新的loop(3.5版本问题)
    ioloop = asyncio.get_event_loop()
    _tasks = [asyncio.ensure_future(coro_but_exist_yield(i)) for i in range(1, 3)]
    #  ioloop.run_until_complete(asyncio.wait(_tasks))
    ioloop.run_until_complete(_tasks)
    ioloop.close()
except Exception:
    pass


# 测试以普通调用方式调用协程函数
result = coro(1)
print(f'正常方式调用协程函数(返回coro对象):{result}')
