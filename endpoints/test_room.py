import json
import pytest

from shadymeadows import ShadyMeadows


# URL will be set from the --url flag when called with pytest.
# If no flag is passed then it will default to the value in conftest.py
URL = pytest.config.getoption('--url')


# The list containing the room types to test in test_valid_room_types()
VALID_ROOM_TYPES = ['Single', 'Twin', 'Family', 'Suite']

@pytest.mark.parametrize('type', VALID_ROOM_TYPES)
def test_valid_room_types(type):
    ''' This test case will be run for each value in VALID_ROOM_TYPES.
    Each room type will be set to the "type" variable.
    '''
    sm = ShadyMeadows(URL)
    # Login first
    status_code, body = sm.login('admin', 'password')
    assert status_code == 200
    # Convert the response body from a json string to a dictionary
    body_dict = json.loads(body)
    token = body_dict['token']
    # Create the room
    room_num = 999
    beds = 1
    accessible = False
    details = 'Wifi, TV, Mini-bar'
    status_code, body = sm.create_room(token, room_num, type, beds, accessible, details)
    # Verify the room was created
    assert status_code == 200
    body_dict = json.loads(body)
    assert 'roomid' in body_dict
    assert body_dict['roomNumber'] == room_num
    assert body_dict['type'] == type
    assert body_dict['beds'] == beds
    assert body_dict['accessible'] == accessible
    assert body_dict['details'] == details
