"""Games of probability (Vietnamese: Trò chơi xác suất)

This module provides classes that are used as games of chance and things that based on probability, using the `random` module.

This module could be imported as `gop` or `tcxs`.

Classes: `Coin`, `FiftyTwoCardPack`, `Dice`, `UnoPack`, `Revolver`."""

# Classes are sorted by time created

import random

class Coin:
    """A coin. When used, it flips the coin, and returns either 'heads' or 'tails'. Does not have any parameter"""
    def __str__(self): return random.choice(['heads', 'tails'])

class FiftyTwoCardPack:
    """A Standard 52-card pack.
    
    When used, it shuffles the 52-card pack a number of times based on the `shuffle_times` parameter,
    and returns a card based on the `drawn_card` parameter. Parameters:
    - `shuffle_times` — the number of times the pack will be shuffled
    - `drawn_card` — the card which will be returned, it will also be removed from the pack;
    `drawn_card = 0` will return the top card, `drawn_card = -1` will return the bottom card

    You can use the constructor function `list()` to make it return the entire pack instead of a single card."""
    def __init__(self, shuffle_times, drawn_card):
        self.shuffle_times = int(shuffle_times)
        if shuffle_times < 0: raise ValueError("'shuffle_times' parameter must not have a negative value")
        self.drawn_card = int(drawn_card)
        self.pack = ['A♠','2♠','3♠','4♠','5♠','6♠','7♠','8♠','9♠','10♠','J♠','Q♠','K♠',
                     'A♣','2♣','3♣','4♣','5♣','6♣','7♣','8♣','9♣','10♣','J♣','Q♣','K♣',
                     'A♦','2♦','3♦','4♦','5♦','6♦','7♦','8♦','9♦','10♦','J♦','Q♦','K♦',
                     'A♥','2♥','3♥','4♥','5♥','6♥','7♥','8♥','9♥','10♥','J♥','Q♥','K♥']
        self.shuffled_times = 0
        while self.shuffled_times < self.shuffle_times:
            random.shuffle(self.pack)
            self.shuffled_times += 1
    def __str__(self): return self.pack.pop(self.drawn_card)
    def __iter__(self):
        for card in self.pack: yield card

class Dice:
    """(A) regular dice.
    
    When used, it rolls the dice, the number of dice is based on the `number_of_dice` parameter,
    and returns the sum of all the results. Parameter:
    - `number_of_dice` — the number of dice that will be used
    
    You can use the constructor function `int()` if you want to make a operation between it and a number,
    or `list()` to make it return the list of all results instead of the sum of them."""
    def __init__(self, number_of_dice):
        if number_of_dice < 0: raise ValueError("'number_of_dice' parameter must not have a negative value")
        self.number_of_dice = int(number_of_dice)
        self.total_result = 0
        self.list_result = []
        self.dice_used = 0
        while self.dice_used < self.number_of_dice:
            self.result = random.choice([1, 2, 3, 4, 5, 6])
            self.total_result += self.result
            self.list_result.append(self.result)
            self.dice_used += 1
    def __str__(self): return f'{self.total_result}'
    def __int__(self): return self.total_result
    def __iter__(self):
        for result in self.list_result: yield result

class UnoPack:
    """An *UNO* pack.
    
    When used, it shuffles the *UNO* pack a number of times based on the `shuffle_times` parameter,
    and returns a card based on the `drawn_card` parameter. Shares similar parameters with `FiftyTwoCardPack` class.

    You can use the constructor function `list()` to make it return the entire pack instead of a single card.

    The order of the cards is based on https://commons.wikimedia.org/wiki/File:UNO_cards_deck.svg."""
    def __init__(self, shuffle_times, drawn_card):
        self.shuffle_times = int(shuffle_times)
        if shuffle_times < 0: raise ValueError("'shuffle_times' parameter must not have a negative value")
        self.drawn_card = int(drawn_card)
        self.pack = ['Red 0','Red 1','Red 2','Red 3','Red 4','Red 5','Red 6','Red 7','Red 8','Red 9','Red Skip','Red Reverse',
                         'Red Draw 2','Wild',
                     'Yellow 0','Yellow 1','Yellow 2','Yellow 3','Yellow 4','Yellow 5','Yellow 6','Yellow 7','Yellow 8','Yellow 9',
                         'Yellow Skip','Yellow Reverse','Yellow Draw 2','Wild',
                     'Green 0','Green 1','Green 2','Green 3','Green 4','Green 5','Green 6','Green 7','Green 8','Green 9','Green Skip',
                         'Green Reverse','Green Draw 2','Wild',
                     'Blue 0','Blue 1','Blue 2','Blue 3','Blue 4','Blue 5','Blue 6','Blue 7','Blue 8','Blue 9','Blue Skip',
                         'Blue Reverse','Blue Draw 2','Wild',
                     'Red 1','Red 2','Red 3','Red 4','Red 5','Red 6','Red 7','Red 8','Red 9','Red Skip','Red Reverse','Red Draw 2',
                         'Wild Draw 4',
                     'Yellow 1','Yellow 2','Yellow 3','Yellow 4','Yellow 5','Yellow 6','Yellow 7','Yellow 8','Yellow 9','Yellow Skip',
                         'Yellow Reverse','Yellow Draw 2','Wild Draw 4',
                     'Green 1','Green 2','Green 3','Green 4','Green 5','Green 6','Green 7','Green 8','Green 9','Green Skip',
                         'Green Reverse','Green Draw 2','Wild Draw 4',
                     'Blue 1','Blue 2','Blue 3','Blue 4','Blue 5','Blue 6','Blue 7','Blue 8','Blue 9','Blue Skip','Blue Reverse',
                         'Blue Draw 2','Wild Draw 4']
        # The order is based on https://commons.wikimedia.org/wiki/File:UNO_cards_deck.svg
        self.shuffled_times = 0
        while self.shuffled_times < self.shuffle_times:
            random.shuffle(self.pack)
            self.shuffled_times += 1
    def __str__(self): return self.pack.pop(self.drawn_card)
    def __iter__(self):
        for card in self.pack: yield card

class Revolver:
    """THESE ARE JUST GAMES OF CHANCE. I DO NOT SUPPORT VIOLENCE.

    A revolver has a cylinder contains 7 chambers.

    When used, it places a single cartridge in the revolver, spins the cylinder,
    rotates it a number of times based on the `rotate_times` parameter, and returns what is inside the current (first) chamber,
    which can be either 'Empty' or 'Cartridge' (just like Russian Roulette). Parameter:
    - `rotate_times` — the number of times the cylinder will be rotated
    
    You can use the constructor function `list()` to make it return the entire cylinder instead of a single chamber."""
    def __init__(self, rotate_times):
        self.rotate_times = int(rotate_times)
        if rotate_times < 0: raise ValueError("'shuffle_times' parameter must not have a negative value")
        self.cylinder = ['Empty', 'Empty', 'Empty', 'Empty', 'Empty', 'Empty', 'Empty']
        self.cylinder[random.choice([0, 1, 2, 3, 4, 5, 6])] = 'Cartridge'
        self.rotated_times = 0
        while self.rotated_times < self.rotate_times:
            self.cylinder.insert(0, self.cylinder.pop())
            self.rotated_times += 1
    def __str__(self): return self.cylinder[0]
    def __iter__(self):
        for chamber in self.cylinder: yield chamber

class UnoFlipPack:
    """An *UNO FLIP!* pack.
    
    When used, it shuffles the *UNO FLIP!* pack a number of times based on the `shuffle_times` parameter,
    and returns a card based on the `drawn_card` parameter. Shares similar parameters with `FiftyTwoCardPack` class.

    You can use the constructor function `list()` to make it return the entire pack instead of a single card.

    The order of the cards is based on https://commons.wikimedia.org/wiki/File:UNO_cards_deck.svg."""
    def __init__(self, shuffle_times, drawn_card):
        self.shuffle_times = int(shuffle_times)
        if shuffle_times < 0: raise ValueError("'shuffle_times' parameter must not have a negative value")
        self.drawn_card = int(drawn_card)
        self.light_pack = [
                     'Red 1','Red 2','Red 3','Red 4','Red 5','Red 6','Red 7','Red 8','Red 9','Red Skip','Red Reverse','Red Draw 1',
                         'Wild', 'Red Flip',
                     'Yellow 1','Yellow 2','Yellow 3','Yellow 4','Yellow 5','Yellow 6','Yellow 7','Yellow 8','Yellow 9',
                         'Yellow Skip','Yellow Reverse','Yellow Draw 1','Wild','Yellow Flip',
                     'Green 1','Green 2','Green 3','Green 4','Green 5','Green 6','Green 7','Green 8','Green 9','Green Skip',
                         'Green Reverse','Green Draw 1','Wild','Green Flip',
                     'Blue 1','Blue 2','Blue 3','Blue 4','Blue 5','Blue 6','Blue 7','Blue 8','Blue 9','Blue Skip','Blue Reverse',
                         'Blue Draw 1','Wild','Blue Flip',
                     'Red 1','Red 2','Red 3','Red 4','Red 5','Red 6','Red 7','Red 8','Red 9','Red Skip','Red Reverse','Red Draw 1',
                         'Wild Draw 2','Red Flip',
                     'Yellow 1','Yellow 2','Yellow 3','Yellow 4','Yellow 5','Yellow 6','Yellow 7','Yellow 8','Yellow 9','Yellow Skip',
                         'Yellow Reverse','Yellow Draw 1','Wild Draw 2','Yellow Flip',
                     'Green 1','Green 2','Green 3','Green 4','Green 5','Green 6','Green 7','Green 8','Green 9','Green Skip',
                         'Green Reverse','Green Draw 1','Wild Draw 2','Green Flip',
                     'Blue 1','Blue 2','Blue 3','Blue 4','Blue 5','Blue 6','Blue 7','Blue 8','Blue 9','Blue Skip','Blue Reverse',
                         'Blue Draw 1','Wild Draw 2','Blue Flip']
        self.dark_pack = [
                     'Teal 1','Teal 2','Teal 3','Teal 4','Teal 5','Teal 6','Teal 7','Teal 8','Teal 9','Teal Skip','Teal Reverse',
                         'Teal Draw 5','Wild','Teal Flip',
                     'Pink 1','Pink 2','Pink 3','Pink 4','Pink 5','Pink 6','Pink 7','Pink 8','Pink 9','Pink Skip','Pink Reverse',
                         'Pink Draw 5','Wild','Pink Flip',
                     'Purple 1','Purple 2','Purple 3','Purple 4','Purple 5','Purple 6','Purple 7','Purple 8','Purple 9','Purple Skip',
                         'Purple Reverse','Purple Draw 5','Wild','Purple Flip',
                     'Orange 1','Orange 2','Orange 3','Orange 4','Orange 5','Orange 6','Orange 7','Orange 8','Orange 9','Orange Skip',
                         'Orange Reverse','Orange Draw 5','Wild','Orange Flip',
                    'Teal 1','Teal 2','Teal 3','Teal 4','Teal 5','Teal 6','Teal 7','Teal 8','Teal 9','Teal Skip','Teal Reverse',
                         'Teal Draw 5', 'Wild Draw Color','Teal Flip',
                     'Pink 1','Pink 2','Pink 3','Pink 4','Pink 5','Pink 6','Pink 7','Pink 8','Pink 9','Pink Skip','Pink Reverse',
                         'Pink Draw 5','Wild Draw Color','Pink Flip',
                     'Purple 1','Purple 2','Purple 3','Purple 4','Purple 5','Purple 6','Purple 7','Purple 8','Purple 9','Purple Skip',
                         'Purple Reverse','Purple Draw 5','Wild Draw Color','Purple Flip',
                     'Orange 1','Orange 2','Orange 3','Orange 4','Orange 5','Orange 6','Orange 7','Orange 8','Orange 9','Orange Skip',
                         'Orange Reverse','Orange Draw 5','Wild Draw Color','Orange Flip']
        random.shuffle(self.dark_pack)
        self.shuffled_times = 0
        self.pack = []
        for card in range(0, 112): self.pack.append(f'{self.light_pack[card]} | {self.dark_pack[card]}')
        while self.shuffled_times < self.shuffle_times:
            random.shuffle(self.pack)
            self.shuffled_times += 1
    def __str__(self): return f'{self.pack.pop(self.drawn_card)}'
    def __iter__(self):
        for card in self.pack: yield card

# SPECIAL SECTION — ANYTHING ELSE THAT RELATES TO THE MODULE
memorial = ['flip_the_coin()', 'shuffle_pack()', 'shuffle_reveal_pack()', 'roll_the_dice()', 'roll_the_dice()', 'shuffle_uno_pack()',
'shuffle_reveal_uno_pack()', 'russian_roulette()', 'russian_roulette_reveal()']
"""In memory of all functions that only existed in the very first version and were removed on the next version
(They are sorted by time created)"""