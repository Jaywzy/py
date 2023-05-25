# input可以暂停程序
def testInput():
    for i in list(range(10)):
        if (i > 2):
            input('输入任意值继续')
        print(i)

testInput()