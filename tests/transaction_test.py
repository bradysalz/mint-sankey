from datetime import datetime
import unittest

import transaction


class TestTransaction(unittest.TestCase):
    def test_sakey_gen(self):
        now = datetime.now()
        t1 = transaction.Transaction(
            date=now,
            vendor='McDonalds',
            amount=6.66,
            debit=True,
            category='Restaurants')

        t2 = transaction.Transaction(
            date=now,
            vendor='Burger King',
            amount=7.77,
            debit=True,
            category='Movies',
            source=t1)

        self.assertEqual(t1.make_sakey_string(), "NULL [6.66] Restaurants")
        self.assertEqual(t2.make_sakey_string(), "Restaurants [7.77] Movies")


if __name__ == "__main__":
    unittest.main()
