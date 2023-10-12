import abc


class Person(metaclass=abc.ABCMeta):
    age: int
    
    def __init__(self, age:int=1) -> None:
        self.age = age
    
    @abc.abstractmethod
    def drive(self):
        pass


class Baby(Person):
    def __init__(self, age: int = 1) -> None:
        if age < 18:
            super().__init__(age)
        else:
            raise ValueError
    
    def drive(self):
        raise Exception('No drive!')


class Adult(Person):
    def __init__(self, age: int = 1) -> None:
        if age >= 18:
            super().__init__(age)
        else:
            raise ValueError
    
    def drive(self):
        print('ok')


try:
    baby = Baby(3)
    baby.drive()
except ValueError:
    print('年齢おかしいよ!')
except Exception:
    print('運転まだダメ!')

try:
    adult = Adult(25)
    adult.drive()
except ValueError:
    print('年齢おかしいよ!')

