import random
from helper import make_ordinal

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
        self.name = f"{colour.capitalize()}{f' {value} ' if value else ' '}{class_name}" if colour else class_name

    def __repr__(self):
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


class Hand:
    def __init__(self, cards: list[Card]):
        self.cards = cards

    def add(self, card: Card):
        self.cards.append(card)

    def use(self, card: Card):
        if card in self.cards:
            pass  # actually use the card
        else:
            raise AttributeError("Player does not have this card!")


class Player:
    def __init__(self, name: str, hand: Hand):
        self.name = name
        self.hand = hand


def generate_piles() -> Piles:
    default_deck = []
    for i in range(1, 20):
        if i <= 4:  # only do the following for the first 4 iterations
            default_deck.append(WildCard())
            default_deck.append(WildCardFour())
        for colour in colours:
            if i <= 2:  # only do the following for the first 2 iterations
                default_deck.append(DrawTwoCard(colour))
                default_deck.append(ReverseCard(colour))
                default_deck.append(SkipCard(colour))
            default_deck.append(StandardCard(colour, (i / 2).__trunc__()))  # add the right values using i
            #  0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9

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


def request_player_name(index: int) -> str:
    response = input(f"What is the {make_ordinal(index)} player's name?")
    try:
        player_name_ = str(response)
    except ValueError:
        print("Please input a valid string.")
        return request_player_name(index)

    return player_name_


player_count = request_player_count()

piles = generate_piles()

players = []
for i in range(1, player_count):
    player_name = request_player_name(i)
    players.append(
        Player(player_name,

               )
    )
