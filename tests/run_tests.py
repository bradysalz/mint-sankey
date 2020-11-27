from datetime import datetime
import unittest

import toml

import sankey_gen


class TestRunner(unittest.TestCase):

    def test_main(self):
        for test_type in ["category", "date", "income"]:
            path_root = f'tests/{test_type}test/'
            sankey_gen.main(config_file=f'{path_root}config.toml')

            with open(f'{path_root}actual.txt', 'r') as f:
                actual = f.readlines()

            with open(f'{path_root}expected.txt', 'r') as f:
                expected = f.readlines()

            self.assertListEqual(expected, actual, f'Failed test type {test_type}')


if __name__ == '__main__':
    unittest.main()
