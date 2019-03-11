i = [1, 2, 3, 4, 5, 6, 7, 8]


def p():
    for a in i:
        yield a


a = p()
print(a.__next__())
print(a.__next__())
print(a.__next__())
print(a.__next__())
print(a.__next__())
print(a.__next__())
print(a.__next__())
print(a.__next__())
print(a.__next__())

