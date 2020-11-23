from datetime import datetime
from enum import Enum
from typing import List


class Transaction:
    """Transactions are single entries in my credit/debit account

    Not all fields are currently used. However, it's easier to add that info
    now and future proof for later, so here we go.

    Fields:
        date: datestamp of transaction
        vendor: what vendor issued the transaction
        amount: transaction amount
        debit: True if debit else False [credit]
        category: transaction category [usually Mint generated]
        label: transaction label [usually Mint generated]
        source: where did this expenditure come from in my budget
    """

    def __init__(self,
                 date: datetime = None,
                 amount: float = None,
                 debit: bool = None,
                 vendor: str = None,
                 category: str = None,
                 label: str = None,
                 source: 'Transaction' = None):
        self.date = date
        self.vendor = vendor
        self.amount = amount
        self.debit = debit
        self.category = category
        self.label = label
        self.source = source

    def __str__(self):
        return f"<Transaction {self.vendor} {self.amount}>"

    def load_from_csv(self, data: List):
        """Store a csv-row of data in the object

        Args:
            data: list form of a transaction csv row
        """
        self.date = datetime.strptime(data[0], "%m/%d/%Y")
        self.vendor = data[1]
        self.amount = int(float(data[3]))
        self.debit = True if data[4] == 'debit' else False
        self.category = data[5]
        self.label = data[7]

    def make_sakey_string(self) -> str:
        """Create a string with the relevant SakeyMatic formatting

        The format is:
            {Source} [{Amount}] {Type}
        """
        if self.source:
            return f"{self.source.category} [{self.amount}] {self.category}"
        else:
            return f"NULL [{self.amount}] {self.category}"

