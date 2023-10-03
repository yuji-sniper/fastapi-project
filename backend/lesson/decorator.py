def print_info(func: callable):
    def wrapper(*args, **kwargs):
        print('start')
        result = func(*args, **kwargs)
        print('end')
        return result
    return wrapper

def print_more(func: callable):
    def wrapper(*args, **kwargs):
        print('func:', func.__name__)
        print('args:', args)
        print('kwargs:', kwargs)
        result = func(*args, **kwargs)
        print('result:', result)
        return result
    return wrapper

@print_info
@print_more
def add_num(a, b):
    return a + b

@print_info
def sub_num(a, b):
    return a - b

r1 = add_num(1, 2)
print(r1)

r2 = sub_num(3, 1)
print(r2)
