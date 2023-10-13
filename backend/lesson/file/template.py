import string

with open('template.txt', 'r') as f:
    t = string.Template(f.read())

contents = t.substitute(name='Mike', contents='How are you?')
print(contents)
