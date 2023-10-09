scores = {
    'A': 100,
    'B': 85,
    'C': 95,
}

ranking = sorted(scores, key=scores.get, reverse=True)

print(ranking)
