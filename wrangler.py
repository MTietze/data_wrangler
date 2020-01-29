import csv
import logging
import sys
import yaml
from transformer import Transformer
from validator import Validator


class Wrangler(object):

    def __init__(self, config_path=None, config=None, validator_class=Validator, transformer_class=Transformer):
        # Expects to receive either a path to a config file or a python dict of config
        if config_path is not None:
            with open(config_path) as file:
                self.config = yaml.load(file, Loader=yaml.FullLoader)
        else:
            self.config = config
        self.chunk_size = self.config.get('chunk_size', 100)
        self.output_path = self.config['output_path']
        self.input_path = self.config['input_path']

        columns = self.config['columns']
        transformations = {column['output_key']: column.get('transformations', []) for column in columns}
        validations = {column['input_key']: column.get('validations', []) for column in columns if
                       'input_key' in column}
        self.output_map = {column['output_key']: column.get('input_key') for column in columns}

        self.transformer = transformer_class(transformations, self.output_map)
        self.validator = validator_class(validations)

    def wrangle(self):
        with open(self.input_path) as input_file:
            with open(self.output_path, "w+") as output_file:
                self.output_writer = csv.DictWriter(output_file, fieldnames=list(self.output_map.keys()))
                self.output_writer.writeheader()
                reader = csv.DictReader(input_file)
                chunk_list = []
                for idx, row in enumerate(reader):
                    row['__row_number'] = idx + 1
                    chunk_list.append(row)
                    if idx % self.chunk_size == 0:
                        self.write_rows(chunk_list)
                        chunk_list = []
                self.write_rows(chunk_list)
        logging.info("{} rows processed".format(idx + 1))

    def write_rows(self, rows):
        for idx, row in enumerate(rows):
            is_valid = self.validator.validate_row(row)
            if is_valid:
                row = self.transformer.transform_row(row)
                self.write_row(row)

    def write_row(self, row):
        if row is None:
            return row
        self.output_writer.writerow(row)


if __name__ == '__main__':
    config_path = sys.argv[1]
    wrangler = Wrangler(config_path=config_path)
    wrangler.wrangle()
