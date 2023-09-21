# Description
The framework is based on the pytest + playwright

# Installation
1. [download](https://www.python.org/downloads/release/python-3113/) and install Python 3.11.3
2. clone the framework
3. open a terminal window and navigate to the framework's root directory
4. create a virtual environment: 
    ```commandline 
    python -m venv <path to the framework root directory>/venv
    ```
5. activate the virtual environment:
   * POSIX:
     ```commandline 
     source venv/bin/activate
     ```
   * Windows:
     ```commandline 
     venv\Scripts\activate.bat
     ```
6. install dependencies: ``
     ```commandline 
     pip install -r requirements.txt
     ```

# Running tests:
In order to run test, you have to navigate to the framework's root directory

## CLI options
* all the pytest's options - [see documentation](https://docs.pytest.org/en/6.2.x/usage.html)
* all the playwright's options - [see documentation](https://playwright.dev/docs/test-cli#reference)

* `--env`  
  base url to the test environment  
  default value: https://twitter.com
* `--screen_width`  
   default value: 1920
* `--screen_height`  
   default value: 1080
* `--TWITTER_USER_NAME`
* `--TWITTER_PASSWORD`




For example, to run all the tests in headed mode, you can use this command:
```commandline
pytest --TWITTER_USER_NAME="..." --TWITTER_PASSWORD="..."  --headed
```

# Authentication
For all the tests that request fixture "home_page", authentication is done automatically once per session

# Reports
A junit report will be written to [reports/junit_report.xml](./reports/junit_report.xml)