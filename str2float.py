from functools import reduce

def str2float(s):
    l = s.split('.')
    l = list(map(lambda n: reduce(lambda x, y: int(x) * 10 + int(y), n), l))
    return l[0] + (l[-1] / (10 ** len(str(l[-1]))))

print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('测试成功!')
else:
    print('测试失败!')