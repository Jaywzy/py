# 利用切片操作，实现一个trim()函数，去除字符串首尾的空格，注意不要调用str的strip()方法：

# def trim(s):
#     if len(s) == 0:
#         return ''
#     if s[0] != ' ' and s[-1] != ' ':
#         return s
#     if s[0] == ' ':
#         s = s[1:]
#     if s[-1] == ' ':
#         s = s[:-1]
#     return trim(s)

def trim(s):
    if s[:1] == ' ':
        s = trim(s[1:])
    elif s[-1:] == ' ':
        s = trim(s[:-1])
    return s

# 测试:
if trim('hello  ') != 'hello':
    print('测试失败 -- 1')
elif trim('  hello') != 'hello':
    print('测试失败 -- 2')
elif trim('  hello  ') != 'hello':
    print('测试失败 -- 3')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败 -- 4')
elif trim('') != '':
    print('测试失败 -- 5')
elif trim('    ') != '':
    print('测试失败 -- 6')
else:
    print('测试成功!')