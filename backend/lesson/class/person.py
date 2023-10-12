class Person:
    """
    人間
    """
    
    name: str # 名前
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def do_something(self) -> None:
        self.say()
        self.run(5)
    
    def say(self) -> None:
        """
        名前を呼んで挨拶する
        """
        print(f'Hello {self.name}!')
    
    def run(self, num: int) -> None:
        """
        走る
        """
        print('run' * num)

person = Person('Mike')
person.do_something()
