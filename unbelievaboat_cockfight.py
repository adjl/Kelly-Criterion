#!/usr/bin/env python3

import math
import sys

from typing import List
from typing import Tuple


base_chance: int = 70


def print_separator() -> None:
    print(f'{"-" * 70}')


def int_input(msg: str) -> int:
    return int(input(msg).replace(',', ''))


def input_option(msg: str, options: str) -> str:
    while True:
        try:
            option: str = input(msg).upper()
            if option in options:
                break
        except (KeyboardInterrupt, EOFError):
            print(end='\n')
    return option


def round_to_inc(bankroll: int, increment: int) -> int:
    return bankroll // increment * increment


def calc_bet_size(bankroll: int, win_chance: int) -> int:
    return math.ceil(bankroll * (win_chance / 50.0 - 1.0))


def calc_all_outcomes(
        outcomes: List[int], bankroll: int, win_chance: int, turn: int) -> List[int]:
    if turn == 0:
        outcomes.append(bankroll)
    else:
        bet_size: int = calc_bet_size(bankroll, win_chance)
        calc_all_outcomes(outcomes, bankroll + bet_size, win_chance + 1, turn - 1)
        calc_all_outcomes(outcomes, bankroll - bet_size, base_chance, turn - 1)
    return outcomes


def calc_stats(
        bankroll: int, win_chance: int, turns: int) -> Tuple[List[int], List[int]]:
    outcomes: List[int] = []
    outcomes = calc_all_outcomes(outcomes, bankroll, win_chance, turns)
    win_outcomes: List[int] = list(filter(
        lambda outcome: outcome > bankroll, outcomes))  # type: ignore
    loss_outcomes: List[int] = list(filter(
        lambda outcome: outcome < bankroll, outcomes))  # type: ignore
    return win_outcomes, loss_outcomes


def calc_value_pct(bankroll: int, outcome: int) -> Tuple[int, float]:
    value: int = outcome - bankroll
    pct: float = value / bankroll * 100.0
    return value, pct


def calc_bankroll(stats: Tuple[int, int, int], increment: int, turns: int) -> int:
    total_bankroll, min_bankroll, win_chance = stats
    total_bankroll_rnd: int = round_to_inc(total_bankroll, increment)
    bankroll: int = total_bankroll_rnd // 2

    while bankroll < total_bankroll_rnd:
        max_loss, _ = calc_value_pct(
            bankroll, min(calc_stats(bankroll, win_chance, turns)[1]))
        if math.ceil(math.fabs(max_loss)) >= total_bankroll - min_bankroll:
            bankroll -= increment
            break
        bankroll += increment
    return bankroll


def calc_profit_chance(win_chance: int) -> Tuple[float, float]:
    w: float = win_chance / 100.0
    b: float = base_chance / 100.0
    max_profit_chance: float = w * (w + 0.01) * (w + 0.02) * (w + 0.03)
    profit_chance: float = max_profit_chance
    profit_chance += w * (w + 0.01) * (w + 0.02) * (0.97 - w)
    profit_chance += w * (w + 0.01) * (0.98 - w) * b
    profit_chance += w * (0.99 - w) * b * (b + 0.01)
    profit_chance += (1.0 - w) * b * (b + 0.01) * (b + 0.02)
    return max_profit_chance * 100.0, profit_chance * 100.0


def print_profit_stats(bankroll: int, win_outcomes: List[int]) -> None:
    max_profit, max_profit_pct = calc_value_pct(bankroll, max(win_outcomes))
    print(f'Max profit forecast: {max(win_outcomes):,}', end=' ')
    print(f'({max_profit:+,}, {max_profit_pct:+.2f}%)')

    avg_profit_bankroll: int = math.ceil(sum(win_outcomes) / len(win_outcomes))
    avg_profit, avg_profit_pct = calc_value_pct(bankroll, avg_profit_bankroll)
    print(f'Avg profit forecast: {avg_profit_bankroll:,}', end=' ')
    print(f'({avg_profit:+,}, {avg_profit_pct:+.2f}%)')

    min_profit, min_profit_pct = calc_value_pct(bankroll, min(win_outcomes))
    print(f'Min profit forecast: {min(win_outcomes):,}', end=' ')
    print(f'({min_profit:+,}, {min_profit_pct:+.2f}%)')


def print_loss_stats(bankroll: int, loss_outcomes: List[int]) -> None:
    min_loss, min_loss_pct = calc_value_pct(bankroll, max(loss_outcomes))
    print(f'Min loss forecast: {max(loss_outcomes):,}', end=' ')
    print(f'({min_loss:+,}, {min_loss_pct:+.2f}%)')

    avg_loss_bankroll: int = math.ceil(sum(loss_outcomes) / len(loss_outcomes))
    avg_loss, avg_loss_pct = calc_value_pct(bankroll, avg_loss_bankroll)
    print(f'Avg loss forecast: {avg_loss_bankroll:,}', end=' ')
    print(f'({avg_loss:+,}, {avg_loss_pct:+.2f}%)')

    max_loss, max_loss_pct = calc_value_pct(bankroll, min(loss_outcomes))
    print(f'Max loss forecast: {min(loss_outcomes):,}', end=' ')
    print(f'({max_loss:+,}, {max_loss_pct:+.2f}%)')


def print_profit_chance(win_chance: int) -> None:
    max_profit_chance, profit_chance = calc_profit_chance(win_chance)
    print(f'Chance of max profit: {max_profit_chance:.2f}%')
    print(f'Chance of profit: {profit_chance:.2f}%')


def main() -> None:
    total_bankroll: int = int_input('Total bankroll: ')
    win_chance: int = int(input('Chance of winning: '))
    option: str = input_option('[C]onservative or [A]ggressive: ', 'CA')
    min_bankroll: int = int_input(
        'Minimum outcome: ') if option == 'A' else total_bankroll

    bankroll: int = 0
    turns: int = 4

    increment: int = 1000000000
    if total_bankroll > min_bankroll:
        bankroll = calc_bankroll(
            (total_bankroll, min_bankroll, win_chance), increment, turns)
    if bankroll == 0 or bankroll >= total_bankroll:
        bankroll = round_to_inc(total_bankroll, increment) // 2

    init_bankroll: int = bankroll
    init_win_chance: int = win_chance

    print_separator()
    print(f'Optimal bankroll: ({bankroll:,}) {bankroll}')

    win_outcomes, loss_outcomes = calc_stats(bankroll, win_chance, turns)
    print_separator()
    print_profit_stats(bankroll, win_outcomes)
    print_loss_stats(bankroll, loss_outcomes)

    print_separator()
    print_profit_chance(win_chance)

    for _ in range(turns):
        optimal_bet: int = calc_bet_size(bankroll, win_chance)
        print_separator()
        print(f'Optimal bet: ({optimal_bet:,}) {optimal_bet}')

        option = input_option('[W]in, [L]oss or [Q]uit: ', 'WLQ')
        if option == 'Q':
            break
        bankroll += optimal_bet if option == 'W' else -optimal_bet
        win_chance = win_chance + 1 if option == 'W' else base_chance

    bankroll_value, bankroll_pct = calc_value_pct(init_bankroll, bankroll)
    print_separator()
    print(f'Current bankroll: {bankroll:,}', end=' ')
    print(f'({bankroll_value:+,}, {bankroll_pct:+.2f}%)')
    print(f'Current win chance: {win_chance} ({win_chance - init_win_chance:+})')


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        sys.exit()
