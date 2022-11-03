""" 测试close函数, 不同于throw, 一旦调用close就立刻退出 """


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


gt = while_throw_generator()
print('------------------begin---------------')
try:
    print(next(gt))
    gt.close()
    # 再次调用就会发生异常
    print(next(gt))
except StopIteration as msg:
    print(f'>>> StopIteration: {msg}')
print('--------------------------------------')
print()
