s = """\
AAA
BBB
CCC
DDD
"""

with open('test.txt', 'w') as f:
    f.write(s)

with open('test.txt', 'r') as f:
    print(f.tell())
    print(f.read(1))
    f.seek(5)
    print(f.tell())
    print(f.read(1))
    f.seek(14)
    print(f.tell())
    print(f.read(1))
    f.seek(2)
    print(f.tell())
    print(f.read(1))
    
