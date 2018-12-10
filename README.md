# "Shady Meadows Booking Management" Test Suite

Initial test suite for testing the "Shady Meadows Booking Management" API found at https://automationintesting.online

## Getting Started

These instructions will tell you how to get the test suite configured on your local machine.

### Prerequisites

* Python2 or Python3 (these instructions will assume Python is installed)
* Pytest
* Requests library

### Installing

If you would like to install the dependencies with your package manager then they are usually named `python-pytest` and `python-requests`. These instructions will guide you through the install with `pip`.

Run the following to install the required python libraries for the current user.

**Note:** If you would like to install the libraries for all users then run the command with root privileges without the `--user` flag.

```
$ pip install -r requirements.txt --user
```

## Running the smoke test

The smoke test currently does the following:
* Logs in
* Gets a list of the rooms
* Creates a new room
* Gets a list of the rooms and verifies the new room is in the list
* Gets the data about the new room and verifies there are no bookings
* Creates a booking
* Gets the data about the new room and verifies the new booking is added
* Gets a report and verifies the booking for the new room exists
* Searches for the booking for the new room
* Deletes the booking
* Gets the data about the new room and verifies the booking no longer exists
* Gets a report and verifies the booking no longer exists
* Searches for the booking that no longer exists
* Deletes the room

The smoke test can be run with the following command:

```
$ py.test smoke_test.py
```

The output should look something like this:

```
========================== test session starts ===========================
platform linux -- Python 3.7.1, pytest-4.0.1, py-1.7.0, pluggy-0.8.0
rootdir: /tera/dev/TestShadyMeadows, inifile:
collected 1 item                                                         

smoke_test.py .                                                    [100%]

======================== 1 passed in 3.73 seconds ========================
```

## Running the full test suite

Pytest can detect and run tests in the current directory and all sub directories. Any filename that starts or ends with *test* (excluding the `.py` extension) will be checked for test functions within the file. Test functions have function names that start with *test*.

Therefore, the full test suite can be run with the following command:
```
$ py.test
```

## Extending the test suite

### Project layout

The main level of the project has three important files relating to testing. First is `shadymeadows.py`. This is a basic implementation of the "Shady Meadows Booking Management" API. Second is `conftest.py`. This is explained in the **Extra** section down below. Third is `smoke_test.py`. This is a basic end to end smoke test. Normally I would start the filename with `test_` but `test_smoke.py` is a little unclear as to what it's testing.

There is a directory at the top level named `endpoints/`. This is where the test files for the endpoints should be created. For example, if you wanted to test the *booking* endpoint commands then you would create a `endpoints/test_booking.py` file and add your testcases to that file.

### Pytest test functions

The main thing to know is that `assert` failures and uncaught exceptions will cause pytest to mark a test function as a failure. See https://docs.pytest.org for all your pytest needs.

### Creating more tests

Adding a new test case to a current test file is as easy as adding a new function that starts with *test*. For this project I use the pattern `test_`.  Any new function names that starts this way will be automatically picked up by pytest.

A test file can be added anywhere as long as the file begins or ends with *test* (excluding the `.py` extension). I like to start my test filenames with with `test_`.

### Example tests cases

The `endpoints/` directory currently has two example test files. `test_auth.py` has a positive and negative test case to test the auth endpoint. `test_room.py` has an example of a test case that takes advantage of pytest's ability to parameterize test cases.

## Shady Meadows API

There is a basic implementation of the API that can be found in `shadymeadows.py`. The following methods are implemented:
```
login(username, password)
get_rooms(token)
create_room(token, number, type, beds, accessible, details)
get_room(token, room_id)
delete_room(token, room_id)
create_booking(token, room_id, first_name, last_name, price, deposit_paid, check_in, check_out)
delete_booking(token, booking_id)
get_report(token)
search(token, keyword)
```

Each of these methods returns the status code and the response body of the HTTP call. On thing to note is `login()` will return the token in the response body. The token should be saved and then used for all the other calls.

Here's an example usage of the API that logs in and then prints the room information:

```python
import json
from shadymeadows import ShadyMeadows

url = 'https://automationintesting.online'
sm = ShadyMeadows(url)
status_code, body = sm.login('admin', 'password')
body_dict = json.loads(body)
token = body_dict['token']
status_code, body = sm.get_rooms(token)
print(body)
```

## Extra

### contest.py

`contest.py` contains a configuration to add an optional `--url` flag for when pytest is run. If the flag is not used, the test will default to running against `https://automationintesting.online`. If you wanted to run the tests against another server then you could run the following:

```
$ py.test --url https://localhost:8080
```

### Verbose Flag

I like running pytest with the `-v` flag. This will print all the test cases it runs with a pass/fail message, instead of using symbols. It will also provide more detail with failure messages.

### JUnit XML Flag

Jenkins understands JUnit XML and is the easiest way to have CI process the results from the tests. Use the `--junit-xml` flag to generate an XML file. The flag takes an argument for the file name. Here is an example that creates a `results.xml` JUnit XML file.

```
py.test --junit-xml=results.xml

```