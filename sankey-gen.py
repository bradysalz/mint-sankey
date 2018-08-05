#!/usr/bin/env python3.6
"""Sakey diagram generator for budgeting 'fun'

See the README for more info.
"""
import csv
from datetime import datetime
import typing
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


def add_paystub(f: typing.IO, earnings: float, pretax_vals: Dict, *,
                scale: float) -> int:
    """Create SankeyMatic strings from configuration income+pretax info

    Args:
        f: output file
        earnings: net income
        pretax_vals: dictionary with all pretax items and their value
        scale: scaling factor to apply to all values (based on time period)

        The format is:
            {Source} [{Amount}] {Type}

        Returns:
            total take home income over the plotting period
    """
    take_home = earnings * scale
    sorted_pretax = sorted(pretax_vals.items(), key=lambda kv: kv[1])
    sorted_pretax.reverse()
    for name, value in sorted_pretax:
        f.write(f'Wages [{value * scale}] {name}\n')
        take_home -= value * scale

    f.write(f'Wages [{take_home}] Take Home\n')
    return int(take_home)


def filter_transactions(transactions: List[Transaction], start_date: datetime,
                        end_date: datetime, vendors: List[str],
                        categories: List[str],
                        use_labels: bool) -> List[Transaction]:
    """Filter transactions based on date, vendor, and type

    Args:
        transactions: list of all transactions
        start_date: ignore all transactions before this date
        end_date: ignore all transactions after this date
        vendors: ignore all transactions from these vendors
        categories: ignore all transactions within these categories
        use_labels: check labels in addition to categories

    Returns:
        Filtered list of transactions
    """

    filt_trans = []
    for t in transactions:
        if t.date <= start_date or t.date >= end_date:
            continue

        if t.vendor in vendors:
            continue

        if use_labels and t.label in categories:
            continue

        if t.category in categories:
            continue

        filt_trans.append(t)
    return filt_trans


def summarize_transactions(transactions: List[Transaction], use_labels: bool,
                           threshold: int) -> Dict[str, int]:
    """Bundle transactions up by category and calculate total amount per

    Args:
        transactions: list of all transactions
        use_labels: if True, uses labels instead of categories if they exist
        threshold: minimum amount for a category
            if below the threshold, the categorys thrown into "Misc"

    Returns:
        dict of category name, category value pairs
    """
    category_sums = {}
    for t in transactions:
        if use_labels and t.label != '':
            category = t.label
        else:
            category = t.category

        if category in category_sums:
            category_sums[category] += t.amount
        else:
            category_sums[category] = t.amount

    misc_amt = 0
    for name in category_sums.copy():
        if category_sums[name] < threshold:
            misc_amt += category_sums.pop(name)

    if misc_amt:
        category_sums['Misc'] = misc_amt

    return category_sums


def add_transactions(f: typing.IO, transactions: List[Transaction],
                     take_home: int, config: Dict):
    """Generate SankeyMatic strings from filtered transactions

    Args:
        f: output file
        transactions: list of all transactions
        take_home: total take home pay for the period
        config: config file
    """

    start_date = datetime.strptime(config['time']['start_date'], '%m/%d/%Y')
    end_date = datetime.strptime(config['time']['end_date'], '%m/%d/%Y')

    filt_trans = filter_transactions(
        transactions=transactions,
        start_date=start_date,
        end_date=end_date,
        vendors=config['transactions']['ignore_vendors'],
        categories=config['transactions']['ignore_categories'],
        use_labels=config['transactions']['prefer_labels'])

    summed_categories = summarize_transactions(
        transactions=filt_trans,
        use_labels=config['transactions']['prefer_labels'],
        threshold=config['transactions']['category_threshold'])

    expenditure = 0
    sorted_cat = sorted(summed_categories.items(), key=lambda kv: kv[1])
    sorted_cat.reverse()
    for name, value in sorted_cat:
        f.write(f'Take Home [{value}] {name}\n')
        expenditure += value

    savings = take_home - expenditure
    f.write(f'Take Home [{savings}] Savings\n')


if __name__ == "__main__":
    try:
        config_file = open('config.toml', 'r')
    except IOError:
        config_file = open('config-sample.toml', 'r')

    config = toml.load(config_file)

    if config['paths']['use_custom_input']:
        transactions = parse_csv(config['paths']['input_file'])
    else:
        transactions = parse_csv('data/transactions.csv')

    if config['paths']['use_custom_output']:
        fname = config['paths']['output_path']
    else:
        fname = 'output.txt'

    output_file = open(fname, 'w')

    take_home = add_paystub(
        output_file,
        config['paycheck']['net_earnings'],
        config['paycheck']['pretax'],
        scale=2)

    start_date = datetime.strptime('6/1/2018', '%m/%d/%Y')
    end_date = datetime.strptime('7/1/2018', '%m/%d/%Y')
    add_transactions(output_file, transactions, take_home, config)

    output_file.close()
