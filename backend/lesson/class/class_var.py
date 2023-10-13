class Person:
    
    kind = 'human'
    name: str
    words: list[str]
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.words = []
    
    def who_are_you(self):
        print(self.name, self.kind)
    
    def add_word(self, word: str):
        self.words.append(word)


a = Person('A')
a.who_are_you()
a.add_word('hoge')
a.add_word('fuga')
print(a.words)

b = Person('B')
b.who_are_you()
b.add_word('ほげ')
b.add_word('ふが')
print(b.words)
