#!/usr/bin/env python3.6
"""Sakey diagram generator for budgeting 'fun'

See the README for more info.
"""
import csv
from typing import Dict, List

import toml

from transaction import Transaction


def parse_csv(fname: str) -> List[Transaction]:
    """Parse a CSV file into a list of transactions

    Args:
        fname: filename
        use_labels: if a label is not None, use that as the category instead

    Returns:
        Each row as a Transaction stored in a list
    """
    transactions = []

    with open(fname, 'r', encoding='ISO-8859-1') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # skip header row

        for row in csv_reader:
            t = Transaction()
            t.load_from_csv(row)
            transactions.append(t)

    return transactions


def calc_income_values(fname: str, earnings: float, pretax_vals: Dict) -> int:
    """Create SankeyMatic strings from configuration income+pretax info

    Args:
        fname: output file name
        earnings: total earnings over the plotting period
        pretax_vals: dictionary with all pretax items and their value

        The format is:
            {Source} [{Amount}] {Type}

        Returns:
            total take home income over the plotting period
    """
    with open(fname, 'w') as f:
        take_home = earnings
        for name, value in pretax_vals.items():
            f.write(f'Wages [{value}] {name} \n')
            take_home -= value

        f.write(f'Wages [{take_home}] Take Home')
    return take_home


if __name__ == "__main__":
    try:
        config_file = open('config.toml', 'r')
    except IOError:
        config_file = open('config-sample.toml', 'r')

    config = toml.load(config_file)
    print(config)
    if config['paths']['use_custom_input']:
        transactions = parse_csv(config['paths']['input_file'])
    else:
        transactions = parse_csv('data/transactions.csv')

    # generate input strings

    if config['paths']['use_custom_output']:
        fname = config['paths']['output_path']
    else:
        fname = 'output.txt'

    take_home = calc_income_values(fname, config['paycheck']['net_earnings'],
                                   config['paycheck']['pretax'])
    # generate pretax strings
    # generate transaction string
