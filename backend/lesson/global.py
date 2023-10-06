animal = 'cat'

def f():
    global animal
    animal = 'dog'
    
    fruit = 'apple'
    print('local:', locals())

f()

print(animal)
print('globals:', globals())
