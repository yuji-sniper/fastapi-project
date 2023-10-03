# リスト内包表記
t = (1, 2, 3, 4, 5)
t2 = (5, 6, 7, 8, 9, 10)

r = []
for i in t:
    r.append(i)

print(r)

r = [i for i in t if (i % 2 == 0)]

print(r)

r = []
for i in t:
    for j in t2:
        r.append(i * j)

print(r)

# わかりにくいから2階層以上の場合は非推奨
r = [(i * j) for i in t for j in t2]

print(r)



# 辞書内包表記
w = ['mon', 'tue', 'wed']
f = ['coffee', 'milk', 'water']

d = {}
for k, v in zip(w, f):
    d[k] = v

print(d)

d = {k: v for k, v in zip(w, f)}
print(d)



# 集合内包表記
s = set()

for i in range(10):
    s.add(i)

print(s)

s = {i for i in range(10) if i % 2 == 0}
print(s)
