from collections import OrderedDict
import unittest
from validator import Validator


class TestValidator(unittest.TestCase):

    def test_validate_regex(self):
        row = OrderedDict([('Product Number', 'P-10001'), ('__row_number', 1)])
        validations = {'Product Number': [{'method': 'regex', 'kwargs': {'pattern': '\\d+'}}]}
        with self.assertLogs(level='ERROR') as log_output:
            # A failing regex match should log a ValueError on Row 1
            is_valid = Validator(validations=validations).validate_row(row)
            self.assertFalse(is_valid)
            self.assertTrue('ERROR on ROW 1' in log_output.output[0])
            self.assertTrue('ValueError' in log_output.output[0])
            error_logs_count = len(log_output)

            # Test same row value against a valid regex
            validations = {'Product Number': [{'method': 'regex', 'kwargs': {'pattern': '[A-Z]+-\\d+'}}]}
            is_valid = Validator(validations=validations).validate_row(row)
            self.assertTrue(is_valid)

            # No more error logs should have been produced
            self.assertEqual(error_logs_count, len(log_output))


if __name__ == '__main__':
    unittest.main()