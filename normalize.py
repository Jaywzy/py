# 把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。
# 输入：['adam', 'LISA', 'barT']，输出：['Adam', 'Lisa', 'Bart']

# def normalize(name):
#     res = ''
#     for c in name:
#         res = res + c.lower();
#     res = res[0].upper() + res[1:]
#     return res

def normalize(name):
    def lower(s):
        return s.lower()
    res = list(map(lower, name))
    res[0] = res[0].upper()
    return ''.join(res)

# 测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)