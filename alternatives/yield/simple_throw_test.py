""" 测试throw  """


def simple_throw_generator():
    try:
        yield 'first'
        yield 'second'
        yield 'third'
        yield 'fouth'
    except ValueError:
        print('ValueError异常')
    except TypeError:
        print('TypeError异常')


def while_throw_generator():
    for _ in range(3):
        try:
            yield 'first'
            yield 'second'
            yield 'third'
        except ValueError:
            print('ValueError异常')
        except TypeError:
            print('TypeError异常')



# 1. 测试主动抛出异常的情况, 注意, 最后抛出异常之后还会自动执行一次next, 从而导致抛出StopIteration, 很重要
gt = simple_throw_generator()
print('------------------begin---------------')
try:
    print(next(gt))
    print(gt.throw(ValueError))
except StopIteration as msg:
    print(f'>>> StopIteration: {msg}')
print('--------------------------------------')
print()


# 2. 测试上面的知识点: throw之后会再次执行一次next, 这里并未抛出StopIteration异常
# 而是进入下一个循环重新返回first
gt = while_throw_generator()
print('------------------begin---------------')
try:
    print(next(gt))
    print(gt.throw(ValueError))
except StopIteration as msg:
    print(f'>>> StopIteration: {msg}')
print(next(gt))
print('--------------------------------------')
print()
