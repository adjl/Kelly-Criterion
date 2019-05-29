#!/usr/bin/env python3

import math


bankroll: int = int(input('Bankroll: '))
win_chance: int = int(input('Chance of winning: '))
turns: int = 4
for i in range(turns):
    print('-' * 33)
    optimal_bet: int = math.ceil(bankroll * (win_chance / 50 - 1))
    print('Optimal bet: {}'.format(optimal_bet))
    if i < turns - 1:
        result: str = input('[W]in or [L]oss: ').upper()
        bankroll += optimal_bet if result == 'W' else -optimal_bet
        win_chance = win_chance + 1 if result == 'W' else 70
