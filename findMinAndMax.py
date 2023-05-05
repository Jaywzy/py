# 请使用迭代查找一个list中最小和最大值，并返回一个tuple：
def findMinAndMax(L):
    min = None
    max = None
    for num in L:
        if min == None:
            min = num
        if max == None:
            max = num
        if num < min:
            min = num
        if num > max:
            max = num
    return (min, max)

# 测试
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')