# Mint Sankey

![Version](https://img.shields.io/badge/python-3.6-brightgreen.svg)
[![Build Status](https://travis-ci.org/bradysalz/mint-sankey.svg?branch=master)](https://travis-ci.org/bradysalz/mint-sankey)

`mint-sankey` is a tool that will take your [Mint](https://www.mint.com) transactions, combine it with your paycheck info, and dump text data out so that [SankeyMatic](http://sankeymatic.com) can read it.

You can see an example input file in [`data/test-data.csv`](data/test-data.csv), which will generate output like so:

```
Wages [221] Federal Income Tax
Wages [66] Social Security
Wages [926] Take Home
Take Home [78] Hotel
Take Home [12] Misc
Take Home [836] Savings
```

You can then copy-paste this away into SankeyMatic and get the following plot:

![SankeyMatic sample data](img/sankeymatic_sample_output.png)

## Getting Started

### Prerequisites

Using the tool requires Python 3.6 or higher.

Go to [Mint](https://www.mint.com) and download your transaction history to the `data/` folder. The default name used is `transactions.csv`.

### Installing

Clone the repo and install the requirements:

```
pip install -r requirements.txt
```
Copy `config-sample.toml` to `config.toml` and edit away.

### Running

Run the tool with `python sankey_gen.py`. The default output file is `output.txt`. Copy the contents of that file into [SankeyMatic](http://sankeymatic.com) and enjoy!

## TODOs

High level features I'd like to add:

* Add percentage output as opposed to just absolute values

## Style & Formatting

I use:

* `yapf` for formatting
* `flake8` for linting
* `pyre` for type checking

In general, I try to be `yapf` and `flake8` issue free, and minimize as many errors as possible from `pyre`. Once the errors start showing up as a result of other (`pip`-installed) modules, I punt on them. To use these, run:

```
pip install -r requirements-dev.txt
pyre init
```

## License

Do what you want, see `LICENSE.md`

## Acknowledgements

* [nowthis](https://github.com/nowthis) for creating [SankeyMatic tool](https://github.com/nowthis/sankeymatic)
