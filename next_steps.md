###Next Steps
* Establish what "a very large number of rows" might be and load/performance test this
* Evaluate if I should scrap this project and use an existing ETL tool
* Package and version this and host in on a repo so that other projects can pull it in as a dependency
* Document transformation and validation methods. 
* Define interfaces and add type hinting to maintain order as new methods are written. 
* Refactor shared functionality. 
* Fix transformation pipeline so that you can configure chains of operations.
* Improve logging and auditing of data 
#### Depending on needs:
* allow persisting/retrieving data from a database or cloud storage such as S3
* support parallel processing of chunks, maybe a task queue or multithreading
