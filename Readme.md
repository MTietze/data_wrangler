## Environment Setup

This library has been tested on python 3.7 and 3.8. The test suite runs on 3.8 by default.

Please download and install Python here: https://www.python.org/downloads/release/python-381/

Install tox globally:

`pip install tox`


### Running the tests

Tox handles setting up a virtual environment, installing dependencies, and running tests.

From within the data_wrangler directory, run
 
`tox`

If tox complains about missing py38, you may need to run it as `tox -e /path/to/python38`.

### Running Data Wrangler as a Standalone
Create a YAML file at data_wrangler/local_config.yaml. For a quick test, copy over the contents from tests/fixtures/test_config.yaml.

Activate the virtualenv that tox created:

`source .tox/py38/bin/activate`

run `python ./wrangler.py local_config.yaml`

You should now see the generated CSV located at the output_path specified in your local_config.yaml.

### YAML Configuration
 All keys are required unless marked (O)
 
 See tests/fixtures/test_config.yaml for an example.
 
 The YAML file accepts the following top level keys:
 
 * input_path: absolute_or_relative/path/to/input.csv   
 * output_path: absolute_or_relative/path/to/output.csv (must have write permission)   
 * columns: list of columns
 
 #### Columns
 Each column config represents a column in the generated CSV file. They will appear in the same order as in the columns list.
 ##### CAUTION: "__row_number" is a protected column name, and should not be used as an input or output key.
* output_key: Output column header
* input_key (O): Input column header. Provides initial output value if specified.
* validations: list of validations
* transformations: list of transformations

#### Validations

* method: method name to be invoked from Validator class
* kwargs (O): dict of keyword arguments to be passed to method
 
#### Transformations

* method: method name to be invoked from Transformer class
* kwargs (O): dict of keyword arguments to be passed to method
* source_columns (O): List of column.input_keys which will be passed to the transformation method as a dict of {column_name: value}

### Architecuture:
data_wrangler is designed to be a configurable and extensible Python ETL library. It has minimal external dependencies, 
and relies heavily on standard library solutions for manipulation and coercion of data.
The configuration DSL is lightweight, and the most complicated parts are offloaded to [str.format](https://docs.python.org/2/library/string.html#format-string-syntax) and
[regex](https://docs.python.org/3/library/re.html)

Out of the box, data_wrangler can be configured to handle most basic CSV transformations. However, 
its core classes are designed to be inherited from and extended to support the needs of your application.

