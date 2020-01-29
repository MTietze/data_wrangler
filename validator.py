import logging
import re


class Validator(object):
    def __init__(self, validations):
        self.validations = validations

    def validate_row(self, row):
        is_valid = True
        for key, value in row.items():
            for validation in self.validations.get(key, []):
                try:
                    if 'source_columns' in validation:
                        sources = {k : v for k, v in row.items() if k in row.items()}
                    else:
                        sources = {key: value}
                    error_msg = self._apply_validation(sources, validation)
                    if error_msg:
                        raise ValueError(error_msg)
                except Exception:
                    is_valid = False
                    logging.exception(f"Validation ERROR on ROW {row['__row_number']} Values {sources}, "
                                      f"Method: {validation}")
        return is_valid

    def _apply_validation(self, sources, validation):
        validation_method = validation['method']
        return getattr(self, validation_method)(sources, **validation.get('kwargs', {}))

    @staticmethod
    def regex(sources, pattern=None, **kwargs):
        if not all([re.match(pattern, value) for value in sources.values()]):
            return f"{sources} does not match pattern {pattern}"
