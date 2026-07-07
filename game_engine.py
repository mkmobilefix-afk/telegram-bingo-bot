import random
import json


def generate_bingo_card():
    """
    Generate a standard 5x5 Bingo card.
    Center is FREE.
    """

    B = random.sample(range(1, 16), 5)
    I = random.sample(range(16, 31), 5)
    N = random.sample(range(31, 46), 5)
    G = random.sample(range(46, 61), 5)
    O = random.sample(range(61, 76), 5)

    N[2] = "FREE"

    card = [
        [B[0], I[0], N[0], G[0], O[0]],
        [B[1], I[1], N[1], G[1], O[1]],
        [B[2], I[2], N[2], G[2], O[2]],
        [B[3], I[3], N[3], G[3], O[3]],
        [B[4], I[4], N[4], G[4], O[4]],
    ]

    return card


def card_to_json(card):
    return json.dumps(card)


def json_to_card(data):
    return json.loads(data)


def generate_called_numbers():
    numbers = list(range(1, 76))
    random.shuffle(numbers)
    return numbers


def generate_cards(count=100):
    """
    Generate multiple unique bingo cards.
    """

    cards = []
    seen = set()

    while len(cards) < count:

        card = generate_bingo_card()

        key = json.dumps(card)

        if key not in seen:
            seen.add(key)
            cards.append(card)

    return cards


def get_random_card():
    """
    Return one random bingo card.
    """

    cards = generate_cards()

    return random.choice(cards)
