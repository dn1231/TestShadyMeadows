import json
import pytest

from shadymeadows import ShadyMeadows


# URL will be set from the --url flag when called with pytest.
# If no flag is passed then it will default to the value in conftest.py
URL = pytest.config.getoption('--url')


def test_valid_password():
    ''' This is the positive test for logging into the system'''
    username = 'admin'
    password = 'password'
    sm = ShadyMeadows(URL)
    status_code, body = sm.login(username, password)
    assert status_code == 200
    # Verify that there is a token since the log in was successful.
    body_dict = json.loads(body)
    assert 'token' in body_dict


def test_invalid_password():
    ''' This is the negative test for logging into the system'''
    username = 'admin'
    password = 'badpassword'
    sm = ShadyMeadows(URL)
    status_code, body = sm.login(username, password)
    # Check for a for the correct failure stauts status code.
    assert status_code == 403
    # The log in failed therefore there is no response body
    assert body == ''

