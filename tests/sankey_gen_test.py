from datetime import datetime
import unittest

import toml

import sankey_gen


class TestSankeyGen(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        config_file = open('tests/config-test.toml', 'r')
        self.config = toml.load(config_file)
        config_file.close()

        self.output_fname = 'output-test.txt'

    def test_parse_csv(self):
        results = sankey_gen.parse_csv('data/test-data.csv')
        self.assertEqual(len(results), 11)

    def test_add_paystub(self):
        out_f = open(self.output_fname, 'w')
        take_home = sankey_gen.add_paystub(
            out_f,
            self.config['paycheck']['net_earnings'],
            self.config['paycheck']['pretax'],
            scale=1)

        out_f.close()
        self.assertEqual(take_home, 870)

        with open(self.output_fname, 'r') as f:
            func_results = f.readlines()

        test_results = [
            "Wages [100] Federal Income Tax\n", "Wages [30] Social Security\n",
            "Wages [870] Take Home\n"
        ]

        self.assertListEqual(func_results, test_results)

    def test_filter_by_date(self):
        trans = sankey_gen.parse_csv('data/test-data.csv')

        start_date = datetime.strptime('06/01/2018', '%m/%d/%Y')
        end_date = datetime.strptime('07/01/2018', '%m/%d/%Y')

        results = sankey_gen.filter_transactions(
            transactions=trans,
            start_date=start_date,
            end_date=end_date,
            vendors=[],
            categories=[],
            use_labels=False)

        self.assertEqual(len(results), 4)

    def test_filter_by_vendor(self):
        trans = sankey_gen.parse_csv('data/test-data.csv')

        start_date = datetime.strptime('05/01/2018', '%m/%d/%Y')
        end_date = datetime.strptime('08/01/2018', '%m/%d/%Y')

        results = sankey_gen.filter_transactions(
            transactions=trans,
            start_date=start_date,
            end_date=end_date,
            vendors=self.config['transactions']['ignore_vendors'],
            categories=[],
            use_labels=False)

        self.assertEqual(len(results), 10)

    def test_filter_by_category(self):
        trans = sankey_gen.parse_csv('data/test-data.csv')

        start_date = datetime.strptime('05/01/2018', '%m/%d/%Y')
        end_date = datetime.strptime('08/01/2018', '%m/%d/%Y')

        results = sankey_gen.filter_transactions(
            transactions=trans,
            start_date=start_date,
            end_date=end_date,
            vendors=[],
            categories=self.config['transactions']['ignore_categories'],
            use_labels=False)

        self.assertEqual(len(results), 10)

    def test_filter_by_label(self):
        trans = sankey_gen.parse_csv('data/test-data.csv')

        start_date = datetime.strptime('05/01/2018', '%m/%d/%Y')
        end_date = datetime.strptime('08/01/2018', '%m/%d/%Y')

        results = sankey_gen.filter_transactions(
            transactions=trans,
            start_date=start_date,
            end_date=end_date,
            vendors=[],
            categories=self.config['transactions']['ignore_categories'],
            use_labels=True)

        self.assertEqual(len(results), 9)

    def test_summarize_transactions(self):
        trans = sankey_gen.parse_csv('data/test-data.csv')

        results = sankey_gen.summarize_transactions(
            transactions=trans, use_labels=False, threshold=0)

        expected = {
            'Restaurants': 74,
            'Hotel': 105,
            'Gas & Fuel': 24,
            'Groceries': 24,
            'Income': 35,
            'Bad Category': 52
        }
        self.assertDictEqual(results, expected)

    def test_summarize_transactions_with_label(self):
        trans = sankey_gen.parse_csv('data/test-data.csv')

        results = sankey_gen.summarize_transactions(
            transactions=trans, use_labels=True, threshold=0)

        expected = {
            'Bad Category': 82,
            'Restaurants': 44,
            'Hotel': 105,
            'Gas & Fuel': 24,
            'Groceries': 24,
            'Income': 35
        }
        self.assertDictEqual(results, expected)

    def test_summarize_transactions_with_threshold(self):
        trans = sankey_gen.parse_csv('data/test-data.csv')

        results = sankey_gen.summarize_transactions(
            transactions=trans, use_labels=False, threshold=50)

        expected = {
            'Restaurants': 74,
            'Hotel': 105,
            'Bad Category': 52,
            'Misc': 83
        }
        self.assertDictEqual(results, expected)

    def test_add_transactions(self):
        trans = sankey_gen.parse_csv('data/test-data.csv')

        f = open(self.output_fname, 'w')
        sankey_gen.add_transactions(f, trans, 1000, self.config)
        f.close()

        with open(self.output_fname, 'r') as f:
            results = f.readlines()

        expected = [
            'Take Home [78] Hotel\n', 'Take Home [12] Misc\n',
            'Take Home [910] Savings\n'
        ]
        self.assertListEqual(results, expected)

    def test_main(self):
        sankey_gen.main(config_file='tests/config-test.toml')

        with open(self.output_fname, 'r') as f:
            results = f.readlines()

        expected = [
            'Wages [221] Federal Income Tax\n',
            'Wages [66] Social Security\n',
            'Wages [1926] Take Home\n',
            'Take Home [78] Hotel\n',
            'Take Home [12] Misc\n',
            'Take Home [1836] Savings\n',
        ]

        self.assertListEqual(results, expected)


if __name__ == '__main__':
    unittest.main()
