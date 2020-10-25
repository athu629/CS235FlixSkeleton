# CS235FlixSkeleton
Initially the skeleton python project for the 2020 S2 CompSci 235 practical assignment which has now been edited/changed/modified and added to fulfill the assignment 2 sepcs.

## Description

A Web application that uses:
- a domain model developed in assignment one.
- Python's Flask framework and flask blueprints 
- use of Jinja templating library and WTForms
- Use of Repository
- Testing including the initial domain testing, repo testing, services testing and web app testing using the pytest tool. 

## Installation

**Installation via requirements.txt** 

## Execution

**Running the application**

From the *COMPSCI235FlixSkeleton* directory, and running the wsgi.py file.

## Configuration

The *COMPSCI-235/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.


## Testing

Testing requires that file *COMPSCI-235/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. The test data file 'test_movies.csv' can be found in 'CS235FlixSkeleton/datafiles'

E.g. 

`TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'Alyssa', 'Documents', 'UOA', 'Uni 2020',
                        'CS235', 'CS235_A1', 'CS235FlixSkeleton', 'datafiles')`


 