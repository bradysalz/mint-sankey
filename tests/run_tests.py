from datetime import datetime
import unittest

import toml

import sankey_gen


class TestRunner(unittest.TestCase):

    def test_main(self):
        for folder in ["datetest", "incometest"]:
            sankey_gen.main(config_file=f'tests/{folder}/config.toml')

            with open(f'tests/{folder}/actual.txt', 'r') as f:
                actual = f.readlines()

            with open(f'tests/{folder}/expected.txt', 'r') as f:
                expected = f.readlines()

            self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
