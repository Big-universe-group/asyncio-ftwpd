""" 简单测试yield的基本语法

@生成器问题:
    1. python 的 generator 只保留栈帧上下文, 不保留调用栈, 而且 generator 函数不允许 return.
    2. 仅有调用next()函数的时候才会执行函数语句, 在for循环中会自动调用next()方法.

@yield:
    1. 函数执行过程中遇到一个yield会中断一次, 返回一个迭代值, 函数保存自己的变量和状态.
    2. 下次迭代时从yield下一条语句继续执行, 函数恢复之前状态, 直到遇到下一个yield返回迭代值, 这样循环.
    3. send()和next()都有返回值: yield后面表达式的值
    4. 一旦一个函数中包含yield, 则该函数被调用的时候就会返回一个generator
        type(yield_func)    === function
        type(yield_func())  === generator 

@corotine对象: 协程的讨论对象就是CPU, 在处理IO事件的时候是不涉及到CPU处理的, 见计算机组成原理:
    1. IO所需要的CPU资源非常少, 大部分工作由 DMA完成
    2. 在CPU和磁盘之间有一个中间人, 其就是DMA(Direct Memory Access), 相当于一个小CPU
    3. 整个IO事件流程:
        a. CPU计算文件地址, 发起DMA请求: 操作类型, 设备地址, 内存地址, 操作数据等
        b. DMA接管总线: 进行IO读写, 非协程环境下CPU在当前进程阻塞挂起, 切换进程上下文到其他进程中.
        c. DMA操作完成: 通知CPU并释放总线资源

        参考: https://blog.csdn.net/weixin_37989267/article/details/111041650

@生成器:
    关于生成器, python可以通过__iter__, next方法来实现一个生成器类, 见下方的Generator

@opcode: 操作码, 将python源代码编译之后的最终数据, 例如dis命令输出的LOAD_CONST, STORE_FAST等值 

@yield 底层C实现: (https://zhuanlan.zhihu.com/p/358035238)
    1. 编译时
        a. 若发现函数有yield表达式, 则标识ste_generator=1
        b. 执行OPCode时若发现ste_generator为1则函数整体会被打上标识CO_GENERATOR
    2. 执行时
        a. 函数被执行的时候, 若存在CO_GENERATOR, 则不会执行函数, 而是返回generator类型对象, 并且
            存储函数的stack point信息以便后续迭代
        b. 迭代运行时, 一旦碰到YIELD_VALUE的OPCode指令时, 则保存stack point并返回结果(await应该没这么简单)
        c. 其中生成器的迭代依赖栈顶f_stacktop和偏移f_lasti的移动
    
@生成器宏跳转介绍(https://sund.site/posts/py-yield/)
    1. YIELD_VALUE流程:
        a. 栈顶元素赋值给retval
        b. 记录栈顶指针: f->f_stacktop = stack_pointer;
        c. 跳转到fast_yield, 进行一些状态判断在返回retval
        d. 注意retval就是python代码中yield返回的当前迭代器数据(栈顶)
    
    2. 生成器如何记录上次返回location/index
        a. PyFrameObject对象中变量f_lasti保存代码当前执行到了字节码的哪个位置
        b. next再次调用的时候, 生成器传递上次保存再f_lasti中的字节码位置, 直接JUMPTO(f->f_lasti)到上次位置
        c. 重复上面的步骤
"""


class Generator:
    """ 一个简单的的生成器类实现: 斐波那契数列 """
    def __init__(self, max_value):
        self.max = max_value
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def next(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration()


def start_generator():
    print('Study yield')
    # 注意, 5, 8, 16在调用next, send的时候返回(生成器的迭代返回值)
    m_1 = yield 5
    print(f'First yield return value:{m_1}')
    m_2 = yield 8
    print(f'Second yield return value:{m_2}')
    _ = yield 16
    print('End generator')


# **注意**, gt.send(None)等价于next(gt), 在一定意义上两者作用类似, 但是next()只能传递None, send可以传递值
try:
    gt = start_generator()

    _n = gt.send(None)
    print(f'--generate value-{_n}\n')

    _n = next(gt)
    print(f'--generate value-{_n}\n')

    _n = gt.send('Fighting-->send')
    print(f'--generate value-{_n}\n')

    _n = next(gt)
    print(f'--generate value-{_n}\n')

except StopIteration as msg:
    print(f'Exception:{msg}')
