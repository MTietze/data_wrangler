from decimal import Decimal
import logging
import re


class Transformer(object):

    casing_options = ('upper', 'lower', 'title')
    type_options = {'int': int,
                    'decimal': Decimal}

    def __init__(self, transformations, output_fieldmap):
        self.transformations = transformations
        self.output_fieldmap = output_fieldmap

    def transform_row(self, row):
        output_row = {}
        for output_field, input_field in self.output_fieldmap.items():
            value = row.get(input_field)
            for transformation in self.transformations.get(output_field, []):
                sources = {}
                if 'source_columns' in transformation:
                    sources = {k: v for k, v in row.items() if k in transformation['source_columns']}
                try:
                    value = self._apply_transformation(sources=sources,
                                                       value=value,
                                                       method=transformation['method'],
                                                       **transformation.get('kwargs', {}))
                except Exception:
                    logging.exception(f"Unable to apply transformation: {transformation} to row {row}")
            output_row[output_field] = value
        return output_row

    def _apply_transformation(self, method, value, sources, **kwargs):
        return getattr(self, method)(value=value, sources=sources, **kwargs)

    @staticmethod
    def format_string(value, sources, template='', **kwargs):
        sources = sources or {}
        if sources:
            # If formatting multiple sources, expects a keyword format string
            return template.format(**sources)
        # If formatting the current column value, expects a positional format string
        return template.format(value)

    def modify_casing(self, value, casing, **kwargs):
        # applies builtin case modifier string methods to value
        assert(casing in self.casing_options)
        return getattr(value, casing)()

    def modify_type(self, value, target_type, **kwargs):
        # Cleans value for formatting into a number, then applies a type coercion method to value
        value = re.sub(r'[^-\.0-9]*', '', value)
        assert(target_type in self.type_options)
        return self.type_options[target_type](value)
