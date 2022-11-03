"""
test: 测试sync和async下两个for循环的时间和输出
"""

import random
import time
import asyncio


def task(pid):
    """Synchronous non-deterministic task.

    """
    time.sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


async def task_coro(pid):
    """Coroutine non-deterministic task

    """
    await asyncio.sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


def synchronous():
    for i in range(1, 10):
        task(i)


# 1. 相比asyncio.create_task, ensure_future参数除了coro协程之外, 还可以是Future, awaitable对象
#   协程: 底层调用loop.create_task, 返回Task对象
#   Future对象: 直接返回, 注意Future对象是Task的父类
#   awaitable对象: await该对象__await__方法, 再次执行ensure_future并返回Task/Future
#
# 2. asyncio.gather: 搜集协程执行的结果并且按照传入的顺序返回结果
# 3. asyncio.wait: 等待协程执行完毕, 可以通过传入return_when以决定返回的时机, 其返回值:
#   done, pending = asyncio.wait(tasks)
#       @done: 已完成任务列表
#       @pending: 等待(Future)完成的任务列表
#   大多数请下gather就够用, 但是wait提供了更灵活的功能, 并且其返回封装好的 tasks
#
# 4. 注意, 一般来说await装饰的语句都涉及IO操作
#
# 5. 注意不适用asyncio.wait和使用的不同用法
#   不使用: for循环中每一个task都需要加await
#   使用: 对整个tasks进行asyncio.await
#
# 6. 注意, Future类似javascript的promise, 可以从JS这方面了解python的future
#
# 7. asyncio.wait在3.8之后不支持直接传入coro对象, 需要通过create_task将coro对象转为
#   task对象才可以使用wait函数
async def asynchronous():
    tasks = [asyncio.ensure_future(task_coro(i)) for i in range(1, 10)]
    await asyncio.wait(tasks)

start = time.time()
print('Synchronous:')
synchronous()
print(f'-----------> total time: {time.time() - start}')

start = time.time()
ioloop = asyncio.get_event_loop()
print('Asynchronous:')
ioloop.run_until_complete(asynchronous())
print(f'-----------> total time: {time.time() - start}')

ioloop.close()
