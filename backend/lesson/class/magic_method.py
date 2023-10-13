class Word:
    
    def __init__(self, text: str) -> None:
        self.text = text

    def __str__(self) -> str:
        return 'Word!'

    def __len__(self):
        return len(self.text)
    
    def __add__(self, word: "Word") -> str:
        return self.text.lower() + word.text.lower()

    def __eq__(self, word: "Word") -> bool:
        return self.text.lower() == word.text.lower()

w = Word('test')
w2 = Word('test')
print(w)
print(len(w))
print(w + w2)
print(w == w2)
