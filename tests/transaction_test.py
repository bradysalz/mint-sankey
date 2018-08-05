from datetime import datetime
import unittest

import transaction


class TestTransaction(unittest.TestCase):
    def test_load_from_csv(self):
        t = transaction.Transaction()
        t.load_from_csv([
            '01/01/2018', 'Wendys', 'More info on the Baconator', '12.1',
            'debit', 'Entertainment', 'Some Account', '', ''
        ])

        self.assertEqual(t.date, datetime.strptime('01/01/2018', '%m/%d/%Y'))
        self.assertEqual(t.vendor, 'Wendys')
        self.assertEqual(t.amount, 12)
        self.assertEqual(t.debit, True)
        self.assertEqual(t.category, 'Entertainment')

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
