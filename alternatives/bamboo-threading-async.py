""" 搭配threading和协程, 适配某些特定场景 """

import asyncio
import time
import threading


# 需要执行的函数异步任务
async def func(num):
    print(f'准备调用func,大约耗时{num}')
    await asyncio.sleep(num)
    print(threading.currentThread())
    print(f'耗时{num}之后,func函数运行结束')
 

# 定义一个专门创建事件循环的loop函数，在另一个线程中启动它
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
  
 
# 定义一个main函数
def main():
    coroutine1 = func(3)
    coroutine2 = func(2)
    coroutine3 = func(1)
    # 在当前线程下创建事件循环(未启动), 在start_loop里面启动
    new_loop = asyncio.new_event_loop()
    # 通过当前线程开启新的线程去启动事件循环
    t = threading.Thread(target=start_loop, args=(new_loop,))
    t.start()

    print(threading.currentThread())
    # 这几条语句是关键，代表在新线程中事件循环不断"游走"执行
    asyncio.run_coroutine_threadsafe(coroutine1, new_loop)
    asyncio.run_coroutine_threadsafe(coroutine2, new_loop)
    asyncio.run_coroutine_threadsafe(coroutine3, new_loop)

    # 在main定义个循环用于检测main和协程是否同时执行
    print('----注意, 此时会先执行该代码, 不像其他例子run_until_complete一直阻塞----')
 

if __name__ == '__main__':
    main()
