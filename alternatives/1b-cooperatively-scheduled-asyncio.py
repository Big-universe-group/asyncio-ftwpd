"""
test: 流程同1-sync中一直, 只不过增加了执行打印的相对时间从而直观的感受task的启动时间
filename: cooperatively(合作的) scheduled
参考:
    https://www.dongwm.com/post/understand-asyncio-2/
"""
import time
import asyncio

start = time.time()


def tic():
    return 'at %1.1f seconds' % (time.time() - start)


async def gr1():
    # Busy waits for a second, but we don't want to stick around...
    print('gr1 started work: {}'.format(tic()))
    await asyncio.sleep(2)
    print('gr1 ended work: {}'.format(tic()))


async def gr2():
    # Busy waits for a second, but we don't want to stick around...
    print('gr2 started work: {}'.format(tic()))
    await asyncio.sleep(2)
    print('gr2 Ended work: {}'.format(tic()))


async def gr3():
    print("Lets do some stuff while the coroutines are blocked, {}".format(tic()))
    await asyncio.sleep(1)
    print("Done!")


ioloop = asyncio.get_event_loop()
# 1. create_task: 将coro协程封装为一个Task以便调度
# 2. 从python3.7+开始统一使用asyncio.create_task来代替loop.create_task和asyncio.ensure_future
tasks = [
    ioloop.create_task(gr1()),
    ioloop.create_task(gr2()),
    ioloop.create_task(gr3())
]
# asyncio.wait
wb = asyncio.wait(tasks)
print('====' * 5)
print(wb, type(wb))
print('====' * 5)
ioloop.run_until_complete(wb)
ioloop.close()
