# 回数是指从左向右读和从右向左读都是一样的数，例如12321，909。请利用filter()筛选出回数：

# 我写的，判断对称
# def is_palindrome(n):
#     t = len(str(n))
#     i = 0
#     b = True
#     while i < t / 2:
#         if str(n)[i] != str(n)[-1 * (i + 1)]:
#             b = False
#             break
#         i = i + 1
#     return b

# better，利用切片获取反序串
def is_palindrome(n):
    return str(n) == str(n)[::-1]

# 测试:
output = filter(is_palindrome, range(1, 1000))
print('1 ~ 1000内回数:')
print(list(output))

if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191]:
    print('测试成功!')
else:
    print('测试失败!')