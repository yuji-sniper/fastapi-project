class Person:
    
    kind = 'human'
    x: int
    
    def __init__(self) -> None:
        self.x = 100
    
    @classmethod
    def what_is_your_kind(cls):
        print(cls.kind)

    @staticmethod
    def about(year):
        print(f'about human {year}')


a = Person()
a.what_is_your_kind()
Person.what_is_your_kind()
Person.about(20)
