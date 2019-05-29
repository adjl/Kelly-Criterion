#!/usr/bin/env python3

import math
import sys


def kelly_criterion(win_chance: int) -> float:
    return win_chance / 50.0 - 1.0


def calc_bet_size(bankroll: int, fraction: float) -> int:
    return math.ceil(bankroll * fraction)


def calc_max_bankroll(bankroll: int, win_chance: int, turns: int) -> int:
    for i in range(turns):
        bankroll += calc_bet_size(bankroll, kelly_criterion(win_chance + i))
    return bankroll


def input_option(msg: str) -> str:
    option: str
    while True:
        try:
            option = input(msg).upper()
            break
        except (KeyboardInterrupt, EOFError):
            print(end='\n')
    return option


def main() -> None:
    turns: int = 4

    bankroll: int = int(input('Bankroll: '))
    win_chance: int = int(input('Chance of winning: '))

    min_bankroll: int = calc_bet_size(bankroll, math.pow(0.6, turns))
    max_bankroll: int = calc_max_bankroll(bankroll, win_chance, turns)

    max_loss: int = bankroll - min_bankroll
    max_profit: int = max_bankroll - bankroll

    max_loss_percent: float = max_loss / bankroll * 100.0
    max_profit_percent: float = max_profit / bankroll * 100.0

    print(f'Min bankroll forecast: {min_bankroll:,}', end=' ')
    print(f'(max loss of -{max_loss:,}, -{max_loss_percent:.2f}%)')
    print(f'Max bankroll forecast: {max_bankroll:,}', end=' ')
    print(f'(max profit of +{max_profit:,}, +{max_profit_percent:.2f}%)')

    for i in range(turns):
        optimal_bet: int = calc_bet_size(bankroll, kelly_criterion(win_chance))
        print(f'{"-" * 70}\nOptimal bet: ({optimal_bet:,}) {optimal_bet}')

        if i < turns - 1:
            option: str = input_option('[W]in, [L]oss or [Q]uit: ')
            if option == 'Q':
                break
            bankroll += optimal_bet if option == 'W' else -optimal_bet
            win_chance = win_chance + 1 if option == 'W' else 70


try:
    main()
except (KeyboardInterrupt, EOFError):
    sys.exit()
