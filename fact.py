# 递归实现阶乘函数

def fact1(n):
    next = n - 1
    if next > 0:
        return n * fact1(next)
    else:
        return 1

print(fact1(4))  # 24
print(fact1(5))  # 120

#尾递归，防止栈溢出
def fact2(n):
    return fact_mul(n, 1)

def fact_mul(num, product):
    if num == 1:
        return product
    else:
        return fact_mul(num - 1, num * product)

print(fact2(4))
print(fact2(5))
print(fact2(10))