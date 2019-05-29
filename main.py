#!/usr/bin/env python3

import math


def kelly_criterion(win_chance: int) -> float:
    return win_chance / 50.0 - 1.0


def calc_bet_size(bankroll: int, fraction: float) -> int:
    return math.ceil(bankroll * fraction)


def calc_max_bankroll(bankroll: int, win_chance: int, turns: int) -> int:
    for i in range(turns):
        bankroll += calc_bet_size(bankroll, kelly_criterion(win_chance + i))
    return bankroll


turns: int = 4

bankroll: int = int(input('Bankroll: '))
win_chance: int = int(input('Chance of winning: '))

min_bankroll: int = calc_bet_size(bankroll, math.pow(0.6, turns))
max_bankroll: int = calc_max_bankroll(bankroll, win_chance, turns)

max_loss: int = bankroll - min_bankroll
max_profit: int = max_bankroll - bankroll

max_loss_percent: float = max_loss / bankroll * 100.0
max_profit_percent: float = max_profit / bankroll * 100.0

print(' '.join((f'Min bankroll forecast: {min_bankroll:,}',
                f'(max loss of -{max_loss:,}, -{max_loss_percent:.2f}%)')))
print(' '.join((f'Max bankroll forecast: {max_bankroll:,}',
                f'(max profit of +{max_profit:,}, +{max_profit_percent:.2f}%)')))

for i in range(turns):
    optimal_bet: int = calc_bet_size(bankroll, kelly_criterion(win_chance))
    print(f'{"-" * 70}\nOptimal bet: ({optimal_bet:,}) {optimal_bet}')

    if i < turns - 1:
        result: str = input('[W]in or [L]oss: ').upper()
        bankroll += optimal_bet if result == 'W' else -optimal_bet
        win_chance = win_chance + 1 if result == 'W' else 70
