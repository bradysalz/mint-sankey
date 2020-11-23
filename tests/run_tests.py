from datetime import datetime
import unittest

import toml

import sankey_gen


class TestRunner(unittest.TestCase):

    def test_main(self):
        sankey_gen.main(config_file='tests/incometest/config.toml')

        with open('tests/incometest/actual.txt', 'r') as f:
            actual = f.readlines()

        with open('tests/incometest/expected.txt', 'r') as f:
            expected = f.readlines()

        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
