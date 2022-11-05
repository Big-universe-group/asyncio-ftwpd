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
    print("Let's do some stuff while the coroutines are blocked, {}".format(tic()))
    await asyncio.sleep(1)
    print("Done!")


# 注意一点: 协程不是并行, 其是由程序控制的并发, 所以tasks的载入是由顺序的(直到碰到IO才退出)
# 我们举个例子: 若所有的tasks中都没有IO事件(asyncio.sleep(0)), 则其执行顺序和同步一致, 见alternatives/1-xx
async def main():
    tasks = [gr1(), gr2(), gr3()]
    await asyncio.gather(*tasks)


asyncio.run(main())
