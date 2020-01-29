from collections import OrderedDict
import unittest
from transformer import Transformer
from tests.fixtures.transformer import CustomTransformer


class TestTransformer(unittest.TestCase):

    def setUp(self):
        self.row = OrderedDict(
            [('Order Number', '1000'), ('Year', '2018'), ('Month', '1'), ('Day', '1'), ('Product Number', 'P-10001'),
             ('Product Name', 'Arugola'), ('Count', '5,250.50'), ('Extra Col1', 'Lorem'), ('Extra Col2', 'Ipsum'),
             ('Empty Column', ''), ('__row_number', 1)])

    def test_concat_and_truncate_string(self):
        transformations = {'New Row': [{'method': 'format_string',
                                       'kwargs': {'template': '{Day}:{Count:.5}'},
                                       'source_columns': ['Day', 'Count']
                                       }]}
        output_fieldmap = {'New Row': ''}
        row = Transformer(transformations=transformations, output_fieldmap=output_fieldmap).transform_row(row=self.row)
        self.assertEqual(row['New Row'], '1:5,250')

    def test_custom_transform(self):
        # custom transform converts field to float truncated to 1 decimal place
        transformations = {'New Row': [{'method': 'format_float_string'}]}
        output_fieldmap = {'New Row': 'Count'}
        row = CustomTransformer(transformations=transformations, output_fieldmap=output_fieldmap).transform_row(row=self.row)
        self.assertEqual(row['New Row'], '5250.5')


if __name__ == '__main__':
    unittest.main()