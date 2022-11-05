"""
注意, python3.5和python3.7+中的asyncio有使用区别, 后者明显更方便, 见3.9目录中的asyncio语法使用.

**异步编程原则**: 一旦决定使用异步, 则系统的每一层都必须是异步, "开弓没有回头箭", 这就是异步编程

asyncio event_loop事件循环:
    1. 模型结构
        a. select 监听是否存在event, 一旦触发就将task将入execute queue中
        b. 单线程中不断的进行执行task, 执行完成之后重新register task的操作
        c. 重复上面的2个流程直到所有任务处理完成并返回, 这就是event_loop模型
    2. 事件循环
        a. 事件循环是asyncio的核心, 异步执行, 任务回调, 网络IO, 多进程都是基于事件循环实现

asyncio selector模块工作流程:
    1. 底层由epoll实现, timeout用于控制阻塞时间
    2. 若task list非空, 此时epoll(timeout=0)
        a. 调用返回可用的task并append到task list中
        b. 执行task list中的所有task
    3. 若task list为空, 此时epoll(timeout=timeout)
        a. 阻塞等待最新的IO事件

async/await:
    1. 异步函数需要用async修饰
    2. await仅在async函数中生效

那么问题来了: 单线程串行执行task怎么实现并发?
    -> 每一个task就是generator(一个可中断的函数, yield), 这是asyncio的基本要求.
    -> 执行task一旦碰到IO就准备相关上下文和回调, 告知selector并中断函数执行(IO事件)
    -> 通过搭配selector和yield中断, 实现了并发效果, 但是一旦发生IO事件时是阻塞等待, 那上面的所有效果都无从谈起
        比如1c-determinism-XX.py中的block_task函数

参考:
    https://juejin.cn/post/6844903507552632840
    
关于协程函数和事件循环: 
    协程函数不能像普通函数那样调用, 否则只返回coroutine object, 其必须添加到事件循环中.

获取事件循环对象的方法:
    1. asyncio.get_running_loop, 在事件循环的事件运行期间才可以调用(3.7版本), 比如在async函数中调用获取loop,
        这个有点类似flask上下文current_app.
    2. asyncio.get_event_loop
    3. asyncio.new_event_loop, 创建新的事件循环, asyncio.set_event_loop(asyncio.new_event_loop())

获取当前task的方法:
    1. asyncio.current_task(loop=None)  # 3.7+, 只能在running loop中获取
    2. asyncio.all_tasks()  # 3.7+, 返回所有没结束的任务

通过loop运行协程函数的方法:
    1. loop.run_until_complete(tasks)
    2. loop.run() (3.7版本), 注意一个线程不允许同时存在多个时间循环, 而run函数自动

asyncio API层级说明:
    1. 高层API: coroutine, tasks, Queues等
        a. 运行异步协程(3.7): asyncio.run(coro)
        b. 创建task(3.7): asyncio.create_task(coro)
        c. asyncio.sleep()
        d. 设置timeout: asyncio.wait_for(aw, timeout), 等待任务执行的最长时间

        e. 并发运行多个任务(重要): 
            -> await asyncio.gather(*coros_or_futures)
            -> await asyncio.wait(aws), 其中包含一些参数类似javascript promise的几个函数:
                FIRST_COMPLETED: 任何一个task完成或取消则返回
                FIRST_EXCEPTION: 任何一个task异常则返回
                ALL_COMPLETED: 所有task完成或取消则返回
        f. 封装并返回可迭代对象: asyncio.as_completed(aws)

    2. 低层API: Event Loop, Future, Transports and Protocols等

Asyncio使用步骤:
    1. < 3.7版本
        a. 构建loop(EventLoop)
            loop = asyncio.get_event_loop()
            loop = asyncio.get_running_loop()
            loop = asyncio.new_event_loop()
            loop = asyncio.set_event_loop(newloop)

        b. 封装task
            asyncio.create_task(coro)
            asyncio.ensure_future(coro)

            # 底层API
            loop.create_future(coro)
            loop.create_task(coro)

        c. 循环
            loop.run_until_complete(asyncio.wait(tasks))
            loop.run_until_complete(asyncio.gather(*tasks))
            loop.run_until_complete(task_1)
            loop.time()  # 事件循环自身维护的时钟值

        d. close
            loop.close()        # 关闭事件循环
            loop.stop()         # 停止事件循环
            loop.is_running()
            loop.is_closed()

        e. 计划回调
            loop.call_later(delay, callback, *args)         # delay时间之后调用callback
            loop.call_at(when, callback, *args)             # when时间调用callback
            loop.call_soon(callback, *args)                 # 在下一个循环中立刻调用

    2. 3.7版本
        a. 其他不变
        b. 运行: asyncio.run(coro)
    
"""
import time
import threading
import asyncio
import requests


async def no_wait():
    print('no wait')


async def get_baidu():
    _start = time.time()
    tid = threading.current_thread().ident
    url = 'https://www.baidu.com'
    print(f'---------> ({tid})准备获取百度地址: {url}')
    try:
        resp = requests.get(url, timeout=3)
    except Exception as msg:
        return f'获取信息异常:{msg}'
    finally:
        _end = time.time()
        print(f'---------> ({tid}) 耗时: {round(_end - start, 4)}')
    return resp


async def foo():
    """ 注意, 被async修饰的函数就是一个协程对象, 此函数对象不能用普通方式调用 """
    print('Running in foo')
    # 进行网络IO操作, 类似sleep中断
    resp = await get_baidu()
    print(f'Explicit(清晰, 明确) context switch to foo again: {resp}')


async def bar():
    print('Explicit context to bar')
    await asyncio.sleep(0)
    print('Implicit context switch back to bar')


async def car():
    print('进入上下文环境car')
    await asyncio.sleep(0)
    print('退出上下文环境car')


# 1. 类似gevent事件句柄的初始化
start = time.time()
ioloop = asyncio.get_event_loop()

# 2. 创建协程任务并等待处理完成, 注意虽然列表中的任务导入顺序和最终执行输出(列表顺序决定函数首次被调用时间)
# 注意, asyncio.sleep(0)表示无IO, 其执行顺序同同步保持一致
ftask = ioloop.create_task(foo())
btask = ioloop.create_task(bar())
ctask = ioloop.create_task(car())
ntask = ioloop.create_task(no_wait())
tasks = [ftask, btask, ctask, ntask]
for i in range(10):
    tasks.append(ioloop.create_task(foo()))
wait_tasks = asyncio.wait(tasks)
# 注意, 这里run_until_complete接收的是generator对象
ioloop.run_until_complete(wait_tasks)

# 3. 关闭
ioloop.close()
end = time.time()
print(f'\n\n>>>>>>>>>执行总耗时:{round(end - start, 4)}')
