from tornado import gen
from tornado import ioloop


@gen.coroutine
def foo():
    print('Running in foo')
    yield gen.sleep(0)
    print('Explicit context switch to foo again')


@gen.coroutine
def bar():
    print('Explicit context to bar')
    yield gen.sleep(0)
    print('Implicit context switch back to bar')


# 老版本: 使用gen.coroutine装饰器和yield来达到协程效果
# tornado6: 直接使用async和await修饰符
@gen.coroutine
def main():
    yield [foo(), bar()]


# 1. iollop
# ioloop主事件循环: 用于非阻塞套接字的I/O事件循环
# 注意, 从tornado6开始, ioloop是一个包装 asyncio 事件循环
ioloop = ioloop.IOLoop.current()
# 2. 运行
ioloop.run_sync(main)
