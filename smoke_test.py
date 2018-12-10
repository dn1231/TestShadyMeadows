import json
import pytest

from shadymeadows import ShadyMeadows


URL = pytest.config.getoption('--url')


def test_end_to_end():
    sm = ShadyMeadows(URL)
    ############
    # Log in
    ############
    status_code, body = sm.login('admin', 'password')
    assert status_code == 200
    body_dict = json.loads(body)
    assert 'token' in body_dict
    # Save the token from the login for future operations
    token = body_dict['token']
    ############
    # View the rooms
    ############
    status_code, body = sm.get_rooms(token)
    assert status_code == 200
    body_dict = json.loads(body)
    assert 'rooms' in body_dict
    ############
    # Create a new room
    ############
    room_num = 201
    type = 'Suite'
    beds = 1
    accessible = True
    details = 'Wifi, TV, Mini-bar, Nice view'
    status_code, body = sm.create_room(token, room_num, type, beds, accessible, details)
    assert status_code == 200
    body_dict = json.loads(body)
    assert 'roomid' in body_dict
    assert body_dict['roomNumber'] == room_num
    assert body_dict['type'] == type
    assert body_dict['beds'] == beds
    assert body_dict['accessible'] == accessible
    assert body_dict['details'] == details
    # Save the new room data for further operation
    new_room = body_dict
    ############
    # View the rooms after adding a new room
    ############
    status_code, body = sm.get_rooms(token)
    assert status_code == 200
    body_dict = json.loads(body)
    # Verify a new room has been added
    assert new_room in body_dict['rooms']
    ############
    # View single room
    ############
    status_code, body = sm.get_room(token, new_room['roomid'])
    assert status_code == 200
    body_dict = json.loads(body)
    assert body_dict['roomid'] == new_room['roomid']
    assert body_dict['roomNumber'] == room_num
    assert body_dict['type'] == type
    assert body_dict['beds'] == beds
    assert body_dict['accessible'] == accessible
    assert body_dict['details'] == details
    assert body_dict['bookings'] == []
    ############
    # Create a booking
    ############
    first_name = 'John'
    last_name = 'Smith'
    price = 200
    deposit_paid = True
    check_in = '2018-12-09'
    check_out = '2018-12-11'
    status_code, body = sm.create_booking(token, new_room['roomid'], first_name, last_name, price, deposit_paid, check_in, check_out)
    assert status_code == 200
    body_dict = json.loads(body)
    assert 'bookingid' in body_dict
    assert body_dict['booking']['roomid'] == new_room['roomid']
    assert body_dict['booking']['firstname'] == first_name
    assert body_dict['booking']['lastname'] == last_name
    assert body_dict['booking']['totalprice'] == price
    assert body_dict['booking']['depositpaid'] == deposit_paid
    assert body_dict['booking']['bookingdates']['checkin'] == check_in
    assert body_dict['booking']['bookingdates']['checkout'] == check_out
    new_booking = body_dict['booking']
    ############
    # View single room after a booking has been added
    ############
    status_code, body = sm.get_room(token, new_room['roomid'])
    assert status_code == 200
    body_dict = json.loads(body)
    assert new_booking in body_dict['bookings']
    ############
    # Get report
    ############
    status_code, body = sm.get_report(token)
    assert status_code == 200
    body_dict = json.loads(body)
    for report in body_dict['report']:
        if report['room'] == str(room_num):
            assert report['values'] == [{'date': '2018-12-09'}, {'date': '2018-12-10'}, {'date': '2018-12-11'}]
            break
    else:
        raise Exception('Room was not found in report')
    ############
    # Search
    ############
    status_code, body = sm.search(token, first_name)
    assert status_code == 200
    body_dict = json.loads(body)
    assert len(body_dict['bookings']) == 1
    assert body_dict['bookings'][0]['roomid'] == new_room['roomid']
    assert body_dict['bookings'][0]['firstname'] == first_name
    assert body_dict['bookings'][0]['lastname'] == last_name
    assert body_dict['bookings'][0]['totalprice'] == price
    assert body_dict['bookings'][0]['depositpaid'] == deposit_paid
    assert body_dict['bookings'][0]['bookingdates']['checkin'] == check_in
    assert body_dict['bookings'][0]['bookingdates']['checkout'] == check_out
    ############
    # Delete a booking
    ############
    status_code, body = sm.delete_booking(token, new_booking['bookingid'])
    assert status_code == 202
    assert body == ''
    ############
    # View single room after a booking has been deleted
    ############
    status_code, body = sm.get_room(token, new_room['roomid'])
    assert status_code == 200
    body_dict = json.loads(body)
    assert body_dict['bookings'] == []
    ############
    # Get report
    ############
    status_code, body = sm.get_report(token)
    assert status_code == 200
    body_dict = json.loads(body)
    for report in body_dict['report']:
        if report['room'] == str(room_num):
            assert report['values'] == []
            break
    else:
        raise Exception('Room was not found in report')
    ############
    # Search after a booking has been deleted
    ############
    status_code, body = sm.search(token, first_name)
    assert status_code == 200
    body_dict = json.loads(body)
    assert body_dict['bookings'] == []
    ############
    # Delete a room
    ############
    status_code, body = sm.delete_room(token, new_room['roomid'])
    assert status_code == 202
    assert body == ''
