# 不考虑顺序，比较两个List是否相等

L1 = [{'rowidObject': 88}, {'rowidObject': 3}, {'rowidObject': 11}, {'rowidObject': 6}]
L2 = [{'rowidObject': 3}, {'rowidObject': 11}, {'rowidObject': 88}, {'rowidObject': 6}]

# 方法一：排序List
def sortA (item):
    return item['rowidObject']

L1.sort(key=sortA)
L2.sort(key=sortA)

print('L1:', L1)
print('L2:', L2)
print('L1 == L2:', L1 == L2)

# 方法二：求差集
ds = [val for val in L2 if val not in L1]  # L2中有而L1中没有的 
print('ds len:', len(ds))
