class UpperCaseError(Exception):
    pass

def check():
    words = ['apple', 'BANANA', 'orange']
    for word in words:
        if word.isupper():
            raise UpperCaseError(word)

try:
    check()
except UpperCaseError as e:
    print(f'大文字エラーだよ! {e}')
