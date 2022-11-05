import asyncio


async def foo():
    print('Running in foo')
    await asyncio.sleep(0)
    print('Explicit context switch to foo again')


async def bar():
    print('Explicit context to bar')
    await asyncio.sleep(0)
    print('Implicit context switch back to bar')


# 注意, 这里的用法类似alternatives/1c-xx中的用法, 使用函数封装tasks列表, 不同的是:
#   1. asyncio.wait(tasks)
#   2. asyncio.gather(*tasks)
# 两者的参数是不同的
async def main():
    tasks = [foo(), bar()]
    await asyncio.gather(*tasks)

# 这里注意, 不是loop.run_until_complete(main()), 不用基于get_event_loop来处理
asyncio.run(main())
