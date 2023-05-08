# 小结
# 当函数的参数个数太多，需要简化时，使用functools.partial可以创建一个新的函数，这个新函数可以固定住原函数的部分参数，从而在调用时更简单。

import functools

int2 = functools.partial(int, base = 2)
print(int2('1000000'))

# 创建偏函数时，实际上可以接收函数对象、*args和**kw这3个参数
int8 = functools.partial(int, '1000000', base = 8)
print(int8())