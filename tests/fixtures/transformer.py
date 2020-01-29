from transformer import Transformer


class CustomTransformer(Transformer):
    def __init__(self, transformations, output_fieldmap):
        super().__init__(transformations, output_fieldmap)
        self.type_options['float'] = float

    def format_float_string(self, value, sources, template='{:.1f}', **kwargs):
        # Extends base class by chaining 2 existing transformations and providing a default template for floats.
        value = self.modify_type(value, 'float')
        return super().format_string(value, sources, template, **kwargs)