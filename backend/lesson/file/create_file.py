s = """\
AAA
BBB
CCC
DDD
"""

with open('test.txt', 'a') as f:
    f.write(s)

with open('test.txt', 'r') as f:
    while True:
        line = f.readline()
        print(line, end='')
        if not line:
            break

with open('test.txt', 'r') as f:
    while True:
        chunk = 2
        line = f.read(chunk)
        print(line)
        if not line:
            break
