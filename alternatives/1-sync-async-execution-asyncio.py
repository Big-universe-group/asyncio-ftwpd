"""
注意, python3.5和python3.7中的asyncio有使用区别, 后者明显更方便, 见3.7目录中的asyncio语法使用.
"""
import threading
import asyncio
import requests


async def get_baidu():
    tid = threading.current_thread().ident
    url = 'https://www.baidu.com'
    print(f'---------> ({tid})准备获取百度地址: {url}')
    try:
        resp = requests.get(url, timeout=3)
    except Exception as msg:
        return f'获取信息异常:{msg}'
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
ioloop = asyncio.get_event_loop()

# 2. 创建协程任务并等待处理完成, 注意虽然列表中的任务导入顺序和最终执行输出(列表顺序决定函数首次被调用时间)
# 注意, asyncio.sleep(0)表示无IO, 其执行顺序同同步保持一致
ftask = ioloop.create_task(foo())
btask = ioloop.create_task(bar())
ctask = ioloop.create_task(car())
tasks = [ftask, btask, ctask]
wait_tasks = asyncio.wait(tasks)
# 追, 这里run_until_complete接收的是generator对象
ioloop.run_until_complete(wait_tasks)

# 3. 关闭
ioloop.close()
