# 著名的斐波拉契数列（Fibonacci），除第一个和第二个数外，任意一个数都可由前两个数相加得到

# generator
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1

g = fib(10)

print([n for n in g])

# for n in g:
#     print(n)
# 注意：g被遍历一次后就不能再次被遍历，已经next到头了