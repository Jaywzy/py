from collections.abc import Iterator

print(isinstance(iter([]), Iterator))  # True

g = iter([1, 2, 3])
print(next(g))
print(next(g))
print(next(g))

g = iter([5, 6, 7])
for n in g:
    print(n)