from collections import defaultdict

s = 'askdausdahakerwekasda'

d = defaultdict(int)

for c in s:
    d[c] += 1

print(d)
