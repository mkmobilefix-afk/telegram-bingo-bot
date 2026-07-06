import random


def generate_card():
    B = random.sample(range(1, 16), 5)
    I = random.sample(range(16, 31), 5)
    N = random.sample(range(31, 46), 4)
    G = random.sample(range(46, 61), 5)
    O = random.sample(range(61, 76), 5)

    card = []

    for i in range(5):
        row = [
            B[i],
            I[i],
            "FREE" if i == 2 else N[i if i < 2 else i - 1],
            G[i],
            O[i],
        ]
        card.append(row)

    return card
