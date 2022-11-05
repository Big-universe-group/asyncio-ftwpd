""" 在coroutine函数中获取相关状态 """
import asyncio
import random


async def show_async_status(pid):
    t = random.randint(0, 10) * 0.001
    result = await asyncio.sleep(t)
    task = asyncio.current_task(loop=None)  # 3.7版本
    print(f'当前Task: {task}')
    print(f'所有Task: {asyncio.all_tasks()}')
    print(f'Task {pid} done: {round(t, 4)}')


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(show_async_status(1))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
