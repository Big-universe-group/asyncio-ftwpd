""" 测试在async嵌套函数中调用多个其他async函数, 但是最终调用外层函数时未使用ensure_future导致的阻塞问题 """
import asyncio 
import time
import threading


async def hello1():
    print(f"Hello world 01 begin,my thread is:{threading.currentThread()}")
    await asyncio.sleep(3)
    print("Hello again 01 end")
  

async def hello2():
    print(f"Hello world 02 begin,my thread is:{threading.currentThread()}")
    await asyncio.sleep(2)
    print("Hello again 02 end")
  

async def hello3():
    print(f"Hello world 03 begin,my thread is:{threading.currentThread()}")
    await hello2()
    await hello1()
    print("Hello again 03 end")
  

async def hello4Async():
    """ 不同于hello3, 这里将依赖关系删除, 但最终可能不是实际需求 """
    print(f"Hello world 04 begin,my thread is:{threading.currentThread()}")
    task1 = asyncio.ensure_future(hello2())
    task2 = asyncio.ensure_future(hello1())
    await asyncio.gather(*[task1, task2])
    print("Hello again 03 end")
  

# 1. 直接同步调用async函数实际上相当于同步调用: 异步编程难点--确保处处是异步
#   每次调用hello3, 在内部就必须串行执行多个await, 这是没办法的.
#
# --> 这也是异步协程的难点, 合理的配置, 减少函数之间的依赖
# 
#   当然, 为了解决此需求则要引入多线程搭配协程使用, asyncio本身就实现了多线程实现逻辑,
#   见bamboo-threading-async.py
print('---------------------------------------')
_start = time.time()
loop = asyncio.get_event_loop()
tasks = [hello3()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
_end = time.time()
print(f'>>>end: {_end - _start}\n\n')


print('---------------------------------------')
_start = time.time()
asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.get_event_loop()
tasks = [hello4Async()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
_end = time.time()
print(f'>>>end: {_end - _start}\n\n')
