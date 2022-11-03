""" 测试yield函数返回值说明:
    1. 返回空值: return, 则立刻抛出StopIteration异常, 异常msg为空
    2. 返回非空: return XX, 则直接该语句的时候也会抛出StopIteration异常, 但是异常msg变为XX

参考: https://blog.csdn.net/qq_27825451/article/details/85226239

@note: 这里引出yield的第一个缺陷(这也是yield from提出的目的之一):
    a. 生成器没办法通过return返回值, return中的值作为StopIteration的异常msg(StopIteration.value)
当然, 仍然可以通过yield返回后面表达式的值.

"""


def return_empty_generator():
    yield 'first'


def return_emptry_and_exception_generator():
    try:
        yield 'first'
        yield 'second'
        yield 'third'
    except ValueError:
        print('ValueError异常')


def return_xx_generator():
    yield 'first'
    return 'xx end'


gt = return_empty_generator()
print('------------------begin---------------')
try:
    print(next(gt))
    print(next(gt))
except StopIteration as msg:
    print(f'>>> StopIteration: {msg}')
print('--------------------------------------')
print()


gt = return_emptry_and_exception_generator()
print('------------------begin---------------')
try:
    print(next(gt))
    print(gt.throw(ValueError))
    print(next(gt))
except StopIteration as msg:
    print(f'>>> StopIteration: {msg}')
print('--------------------------------------')
print()


gt = return_xx_generator()
print('------------------begin---------------')
try:
    print(next(gt))
    print(next(gt))
except StopIteration as msg:
    print(f'>>> StopIteration: {msg}')
print('--------------------------------------')
print()
