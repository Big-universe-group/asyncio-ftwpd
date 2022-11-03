""" yield后面表达式是一个函数
    1. 函数本身是同步的: 无任何问题
    2. 函数本身是异步(yield修饰), 即一个嵌套yield结构, 则返回的实际上是一个generator, 需要2次调用

这个缺陷也是yield from被提出的原因之一
"""


def sync_func():
    print('----this is a sync func----')
    return 'syncFunc'


def async_func():
    print('----this is a sync func----')
    yield 'async func'


def call_sync_func_generator():
    yield sync_func()


def call_async_func_generator():
    yield async_func()


gt = call_sync_func_generator()
print('------------------begin---------------')
try:
    print(next(gt))
except StopIteration as msg:
    print(f'>>> StopIteration: {msg}')
print('--------------------------------------\n')


gt = call_async_func_generator()
print('------------------begin---------------')
try:
    sub_gt = next(gt)
    print(sub_gt)
    next(sub_gt)
except StopIteration as msg:
    print(f'>>> StopIteration: {msg}')
print('--------------------------------------\n')
