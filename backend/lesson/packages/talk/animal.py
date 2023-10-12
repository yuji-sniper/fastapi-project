from packages.tools import utils

def sing():
    return('クワックワ！')

def cry():
    return(utils.say_twice('えん'))

if __name__ == '__main__':
    print(sing())
    print('animal:', __name__)
