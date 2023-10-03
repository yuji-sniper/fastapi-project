def greeting():
    yield 'Good morning'
    yield 'Good afternoon'
    yield 'Good night'

def counter(num:int=10):
    for _ in range(num):
        yield 'run'

for g in greeting():
    print(g)

print('#################')

g = greeting()
c = counter()

print(next(g))
print(next(c))
print(next(c))
print(next(c))
print(next(c))
print(next(c))
print(next(g))
print(next(c))
print(next(c))
print(next(c))
print(next(g))

