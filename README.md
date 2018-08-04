# Mint Sankey

![](https://img.shields.io/badge/python-3.6-brightgreen.svg)

`mint-sankey` is a tool that will take your [Mint](https://www.mint.com) transactions, combine it with your paycheck info, and dump text data out so that [SankeyMatic](http://sankeymatic.com) can read it.

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

Run the tool with `python sankey-gen.py`. The default output file is `output.txt`. Copy the contents of that file into [SankeyMatic](http://sankeymatic.com) and enjoy!

## TODOs

High level features I'd like to add:

* Support for different time periods (right now hard-coded as month for income)
* Add example `transactions.csv` and `output.txt` as a reference
* More tests in `sankey-gen.py`
* Learn some sort of CI tool!

## License

Do what you want, see `LICENSE.md`

## Acknowledgements

* [nowthis](https://github.com/nowthis) for creating [SankeyMatic tool](https://github.com/nowthis/sankeymatic)
