# kindly

This repo is created to solve interview assignment- Chatbot

## File Structure
* ratestask_server.py:- This is the starting point of application. Run this file to start the server and the apis. Run this as ```python3 ratestask_server.py```
* ratestask_helper.py:- This file consists of helper functions to server api requests
* logger.py:- This file defined logger for logging messages
* db_connection_pool.py:- This file is used to create DB connection pool and to execute DB queries
* config.py:- This is used to have config for the application
* constants.py:- This file contains all the constants value
* ratestack_config.json:- This json file can be used to alter default values specified in constants.py file
* ratestask_integration_tests.py:- This file consists of some integration tests. Wrote some testcases to show my ability to write test cases. Run this as `python3 ratestask_integration_tests.py`
* ratestask_integration_tests.json:- This file serves as input to integration tests file
* ratestask_unit_tests.py:- This file consists of unit test. Run this as `python3 ratestask_unit_tests.py`
* requirements.txt: This file specifies all the packages to run above application. Run this as `pip3 install -r requirements.txt`