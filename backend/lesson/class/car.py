class Car:
    model: str|None
    
    def __init__(self, model:str=None) -> None:
        self.model = model
    
    def run(self) -> None:
        print('run!')


class ToyotaCar(Car):
    def run(self) -> None:
        print('fast')


class TeslaCar(Car):
    __can_auto_run: bool
    passwd: str
    
    def __init__(
            self,
            model: str = None,
            can_auto_run=False,
            passwd='123'
        ) -> None:
        super().__init__(model)
        self.__can_auto_run = can_auto_run
        self.passwd = passwd
    
    @property
    def can_auto_run(self) -> bool:
        return self.__can_auto_run
    
    @can_auto_run.setter
    def can_auto_run(self, is_enable: bool):
        if self.passwd == '456':
            self.__can_auto_run = is_enable
        else:
            raise ValueError
    
    def run(self) -> None:
        print(self.__can_auto_run)
        print('super fast')
    
    def auto_run(self) -> None:
        print('auto run!')


# toyota_car = ToyotaCar('Lexas')
# print(toyota_car.model)
# toyota_car.run()

tesla_car = TeslaCar(model='Model S', passwd='456')

try:
    tesla_car.can_auto_run = True
    print(tesla_car.can_auto_run)
except ValueError:
    print('パスワードが違います')
