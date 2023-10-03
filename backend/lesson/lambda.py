from typing import Callable

l = ['Mon', 'tue', 'Wed', 'Thu', 'fri', 'sat', 'Sun']


def change(words: [], func: Callable):
    for word in words:
        print(func(word))

capital: Callable[[str], str] = lambda word: word.capitalize()

change(l, capital)
