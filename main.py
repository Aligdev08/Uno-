colours = ["blue", "red", "green", "yellow"]


class Card:

    def __str__(self):
        class_name = self.__class__.__name__
        capitals = []
        for index, character in enumerate(class_name):
            if index != 0:
                if character == character.upper():
                    capitals.append(character)


class ColouredCard(Card):
    def __init__(self, colour: str):
        if colour not in colours:
            raise ValueError
        self._colour = colour


class StandardCard(ColouredCard):
    def __init__(self, colour: str, value: int):
        super().__init__(colour)
        self._value = value


class ReverseCard(ColouredCard):
    def __init__(self, colour: str):
        super().__init__(colour)


class SkipCard(ColouredCard):
    def __init__(self, colour: str):
        super().__init__(colour)


class WildCard(Card):
    pass


class DrawTwoCard(ColouredCard):
    def __init__(self, colour: str):
        super().__init__(colour)


class Piles:
    def __init__(self):
        deck = []
        discard = []


def generate_piles() -> Piles:
    pass


def request_player_count() -> int:
    response = input("How many people are playing?")
    try:
        player_count_ = int(response)
    except ValueError:
        print("Please input an integer.")
        return request_player_count()

    if player_count_ > 10 or player_count_ < 2:
        print("Please input a number from 2-10.")
        return request_player_count()
    return player_count_


player_count = request_player_count()
piles = generate_piles()
