"""
test: 测试sync和async下两个for循环的时间和输出
"""

import random
import time
import asyncio


def task(pid):
    """Synchronous non-deterministic task. """
    t = random.randint(0, 10) * 0.001
    time.sleep(t)
    print(f'Task {pid} done: {round(t, 4)}')


async def block_task(pid):
    """ 从结果可知, 即使task使用async封装, 若不适用await进行yield处理则总的处理时间还是各个任务的相加
    @参考(简述python异步i/o库 —— asyncio): https://juejin.cn/post/6844903507552632840
    @其他说明见1-sync-XXX.py中的docs中介绍
    """
    t = random.randint(0, 10) * 0.001
    time.sleep(t)

    # asyncio.sleep本身就返回一个coroutine, 碰到该语句时不会等待而是直接中断, 但若是未搭配await来
    # 处理中断则asyncio.sleep就像不存在一样.
    # 注意: asyncio.sleep实际上是asyncio库提供的一个有sleep的模拟中断
    #  print(f'Task {pid} ready: {round(t, 4)}, time:{round(time.time(), 4)}')
    #  asyncio.sleep(t)

    print(f'Task {pid} done: {round(t, 4)}, time:{round(time.time(), 4)}')


async def task_coro(pid):
    """Coroutine non-deterministic task

    """
    t = random.randint(0, 10) * 0.001
    await asyncio.sleep(t)
    print(f'Task {pid} done: {round(t, 4)}, time:{round(time.time(), 4)}')


def task_coro_yield(pid):
    """ async/await就是为了替代老式的yield from """
    t = random.randint(0, 10) * 0.001
    yield from asyncio.sleep(t)
    print(f'Task {pid} done: {round(t, 4)}, time:{round(time.time(), 4)}')


def synchronous():
    for i in range(1, 5):
        task(i)


def get_asynchronous_block_tasks():
    return [asyncio.ensure_future(block_task(i)) for i in range(1, 5)]


# 1. 相比asyncio.create_task, ensure_future参数除了coro协程之外, 还可以是Future, awaitable对象
#   coroutine对象: 底层调用loop.create_task, 返回Task对象
#       -> 一个协程对象就是一个原生可以挂起的函数, Task就是对协程的进一步封装, 包含协程的各种状态
#       -> task创建: ensure_future或者 create_task, 参数为coroutine对象
#   Task对象: 任务, 对coroutine函数的封装, 记录协程的各种状态, 这样才能更好的控制
#   Future对象: 直接返回, 一个操作的最终结果但不会立即得到, 观察者模式(?), 注意Future对象是Task的父类
#   awaitable对象: await该对象__await__方法, 再次执行ensure_future并返回Task/Future
#
# 2. asyncio.gather: 搜集协程执行的结果并且按照传入的顺序返回结果
#       await asyncio.gather(*tasks)
# 3. asyncio.wait: 等待协程执行完毕, 可以通过传入return_when以决定返回的时机, 其返回值:
#       done, pending = asyncio.wait(tasks)
#           @done: 已完成任务列表
#           @pending: 等待(Future)完成的任务列表
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
    tasks = [asyncio.ensure_future(task_coro(i)) for i in range(1, 5)]
    await asyncio.wait(tasks)


start = time.time()
print('Synchronous:')
synchronous()
print(f'-----------> total time: {time.time() - start}')


start = time.time()
print('Asynchronous block:')
ioloop = asyncio.get_event_loop()
_tasks = get_asynchronous_block_tasks()
ioloop.run_until_complete(asyncio.wait(_tasks))
ioloop.close()
print(f'-----------> total time: {time.time() - start}')

# 参考: https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
start = time.time()
asyncio.set_event_loop(asyncio.new_event_loop())  # 创建新的loop(3.5版本问题)
ioloop = asyncio.get_event_loop()
print('Asynchronous:')
ioloop.run_until_complete(asynchronous())
print(f'-----------> total time: {time.time() - start}\n\n')

ioloop.close()


is_coro = asyncio.iscoroutine(block_task(999))
is_coro_func = asyncio.iscoroutinefunction(block_task)
print(f'=====> 判断一个函数或者实例是否为协程: 是否coro对象: {is_coro}, 是否coro函数:{is_coro_func}')
