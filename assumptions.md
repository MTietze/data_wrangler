###Assumptions and Simplifications
* The input CSV file spec is intended as a guide for what the file will look like, not an actual specification file that we'll be parsing.
* This code will be run on a machine which has enough space to hold both the input and output files.
* We aren't too concerned about auditing yet.
* "Invalid rows" should be detectable by configuring validations.
* The intended users are Python programmers, who will configure and run or extend this library. The DSL feels too technical for the average business user.
If the plan was to port this into other languages, we might want to rely less on the Python string formatting syntax, or accept different syntax more intuitive to each language in question.
* chunk_size was built in with the assumption that it will be important later. Chances are, this library will want to support functionality such as writing/reading from staging tables, and parallel processing of rows, both of which can make use of operating on the file in chunks.
* Multiple transformations can be applied to each column, but they don't operate as a proper pipeline where one feeds the next. The assumption is that this will be fixed and built out later. 