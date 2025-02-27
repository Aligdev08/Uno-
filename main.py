import random
from helper import make_ordinal
from abc import abstractmethod

colours = ["blue", "red", "green", "yellow"]


class Player:
    def __init__(self, name: str, hand: list["Card"]):
        self.name = name
        self.hand = hand


class Piles:
    def __init__(self, deck: list["Card"]):
        random.shuffle(deck)
        self.deck = deck
        self.discard = []
        self.forwards = True


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

        colour: str = getattr(self, "colour", None)
        value: int = getattr(self, "_value", None)

        self.name = (
            f"{colour.capitalize()}{f' {value} ' if value else ' '}{class_name}"
            if colour
            else class_name
        )

    @abstractmethod
    def play(self, piles: Piles, player: Player, hand_index: int):
        pass

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

    def play(self, piles: Piles, player: Player, hand_index: int):
        piles.discard.append(self)
        player.hand.pop(hand_index)
        print(f"{player.name} played {self}!")


class ReverseCard(ColouredCard):
    def __init__(self, colour: str):
        super().__init__(colour)

    def play(self, piles: Piles, player: Player, hand_index: int):
        piles.forwards = not piles.forwards
        piles.discard.append(self)
        player.hand.pop(hand_index)
        print(f"{player.name} played {self}!")


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
            default_deck.append(
                StandardCard(colour, (i / 2).__trunc__())
            )  # add the right values using i
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
    response = input(f"What is the {make_ordinal(index + 1)} player's name?")
    try:
        player_name_ = str(response)
    except ValueError:
        print("Please input a valid string.")
        return request_player_name(index)

    return player_name_


def request_card_number(max_num: int) -> int:
    response = input(f"Input the hand number of the card that you would like to play? ")
    try:
        card_number_ = int(response)
    except ValueError:
        print("Please input a valid number.")
        return request_card_number()
    if card_number_ > max_num or card_number_ < 1:
        print("Please input a number that's in your hand.")
        return request_card_number(max_num)

    return card_number_


def generate_hand(deck: list[Card]):
    hand = []
    for _ in range(1, 7):
        removed_card = deck.pop()
        hand.append(removed_card)

    return hand


def print_hand(player: Player):
    print(
        f"-------------------------- Hand of '{player.name}' --------------------------"
    )
    for index, card in enumerate(player.hand, start=1):
        print(f"{index}. {card}")
    print("\n")


def print_hands(players: list[Player]):
    for player in players:
        print_hand(player)


player_count = request_player_count()

piles = generate_piles()

players: list[Player] = []
for i in range(0, player_count):
    player_name = request_player_name(i)
    player = Player(player_name, generate_hand(piles.deck))

    players.append(player)

done = False
print_hands(players)
active_player = 0

while not done:
    player = players[active_player]
    print(
        f"\n--------------------------------------- {player.name}'s turn. ---------------------------------------"
    )
    print_hand(player)
    card_number = request_card_number(len(player.hand))
    player.hand[card_number - 1].play(piles, player, card_number - 1)

    if piles.forwards:
        active_player += 1
    else:
        active_player -= 1
        if active_player < 0 < len(players):
            active_player = len(players) - 1
