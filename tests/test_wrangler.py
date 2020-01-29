import os
import unittest
import yaml
from wrangler import Wrangler


class TestWrangler(unittest.TestCase):

    def test_wrangle_success(self):
        with open('./tests/fixtures/test_config.yaml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        Wrangler(config=config).wrangle()
        with open('./tests/fixtures/test_output.csv', 'r') as output:
            with open('./tests/fixtures/wrangler_success_output.csv', 'r') as fixture:
                # Assert output file matches expected
                diff = set(output).difference(fixture)
                self.assertEqual(len(diff), 0)
        os.remove('./tests/fixtures/test_output.csv')


if __name__ == '__main__':
    unittest.main()