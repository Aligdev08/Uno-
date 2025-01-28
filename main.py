import random

colours = ["blue", "red", "green", "yellow"]


class Card:
    def __init__(self):
        class_name = self.__class__.__name__
        checked_capitals = []
        skip_amount = 0
        for index, character in enumerate(class_name):
            index += skip_amount
            if index != 0:
                if character == character.upper():
                    if index not in checked_capitals:
                        class_name = class_name[:index] + " " + class_name[index:]
                        checked_capitals.append(index + 1)
                        skip_amount += 1
        try:
            colour: str = self.colour
        except AttributeError:  # this Card class has no colour attribute
            colour = None
        try:
            value: int = self._value
        except AttributeError:  # this Card class has no colour attribute
            value = None
        self.name = f"{colour.capitalize()} {value} {class_name}" if colour else class_name

    def __str__(self):
        return self.name


class ColouredCard(Card):
    def __init__(self, colour: str):
        self.colour = colour

        super().__init__()

        if colour not in colours:
            raise ValueError("This is not a valid card colour!")


class StandardCard(ColouredCard):
    def __init__(self, colour: str, value: int):
        if 0 > value <= 9:
            raise ValueError("This is not a valid card value!")
        self._value = value
        super().__init__(colour)


class ReverseCard(ColouredCard):
    def __init__(self, colour: str):
        super().__init__(colour)


class SkipCard(ColouredCard):
    def __init__(self, colour: str):
        super().__init__(colour)


class WildCard(Card):
    pass


class WildCardFour(WildCard):
    pass


class DrawTwoCard(ColouredCard):
    def __init__(self, colour: str):
        super().__init__(colour)


class Piles:
    def __init__(self, deck: list):
        random.shuffle(deck)
        self.deck = deck
        self.discard = []


def generate_piles() -> Piles:
    default_deck = []
    for i in range(1, 20):
        if i < 4:  # only do the following for the first 4 iterations
            default_deck.append(WildCard())
            default_deck.append(WildCardFour())
        for colour in colours:
            if i < 2:  # only do the following for the first 2 iterations
                default_deck.append(DrawTwoCard(colour))
                default_deck.append(ReverseCard(colour))
                default_deck.append(SkipCard(colour))
            default_deck.append(StandardCard(colour, (i/2).__trunc__()))

    return Piles(default_deck)


def request_player_count() -> int:
    response = input("How many people are playing? ")
    try:
        player_count_ = int(response.strip())
    except ValueError:
        print("Please input an integer.")
        return request_player_count()

    if player_count_ > 10 or player_count_ < 2:
        print("Please input a number from 2-10.")
        return request_player_count()
    return player_count_


player_count = request_player_count()
piles = generate_piles()
for deck in piles.deck:
    print(deck)
print(len(piles.deck))