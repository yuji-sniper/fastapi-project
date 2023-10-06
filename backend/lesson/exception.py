l = [1, 2, 3]
i = 5

try:
    # () + l
    # x[i]
    l[i]
except IndexError as e:
    print(f'エラーだよ。{e}')
except NameError as e:
    print(f'エラーだぜ。{e}')
except Exception as e:
    print(f'エラーですわよ。{e}')
else:
    print('DONE!!!')
finally:
    print('ファイナル')

print('last')
