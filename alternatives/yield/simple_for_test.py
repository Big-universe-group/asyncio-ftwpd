""" for循环 """


def start_generator():
    print('Study yield')
    # 注意, 5, 8, 16在调用next, send的时候返回(生成器的迭代返回值)
    m_1 = yield 5
    print(f'First yield return value:{m_1}')
    m_2 = yield 8
    print(f'Second yield return value:{m_2}')
    _ = yield 16
    print('End generator')


# for自动帮忙处理了StopIteration异常
for index, gt in enumerate(start_generator()):
    print(f'>>>>generator item: {gt}')
