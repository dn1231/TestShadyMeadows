import requests


class ShadyMeadows():
    LOGIN_ENDPOINT = '/auth/login/'
    ROOM_ENDPOINT = '/room/'
    BOOKING_ENDPOINT = '/booking/'
    REPORT_ENDPOINT = '/report/'
    SEARCH_ENDPOINT = '/search/'
    DEFAULT_HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self, address):
        self._address = address
        
    def login(self, username, password):
        url = self._address + self.LOGIN_ENDPOINT
        data = {
            'username': username,
            'password': password
        }
        res = requests.post(url, headers=self.DEFAULT_HEADERS, json=data)
        return res.status_code, res.text

    def get_rooms(self, token):
        url = self._address + self.ROOM_ENDPOINT
        cookies = {
            'token': token
        }
        res = requests.get(url, cookies=cookies)
        return res.status_code, res.text

    def create_room(self, token, number, type, beds, accessible, details):
        url = self._address + self.ROOM_ENDPOINT
        cookies = {
            'token': token
        }
        data = {
            'roomNumber': number,
            'type': type,
            'beds': beds,
            'accessible': accessible,
            'details': details
        }
        res = requests.post(url, cookies=cookies, headers=self.DEFAULT_HEADERS, json=data)
        return res.status_code, res.text

    def get_room(self, token, room_id):
        url = self._address + self.ROOM_ENDPOINT + str(room_id)
        cookies = {
            'token': token
        }
        res = requests.get(url, cookies=cookies)
        return res.status_code, res.text

    def delete_room(self, token, room_id):
        url = self._address + self.ROOM_ENDPOINT + str(room_id)
        cookies = {
            'token': token
        }
        res = requests.delete(url, cookies=cookies, headers=self.DEFAULT_HEADERS)
        return res.status_code, res.text

    def create_booking(self, token, room_id, first_name, last_name, price, deposit_paid, check_in, check_out):
        url = self._address + self.BOOKING_ENDPOINT
        cookies = {
            'token': token
        }
        booking_dates = {
            'checkin': check_in,
            'checkout': check_out
        }
        data = {
            'roomid': room_id,
            'firstname': first_name,
            'lastname': last_name,
            'totalprice': price,
            'depositpaid': deposit_paid,
            'bookingdates': booking_dates
        }
        res = requests.post(url, cookies=cookies, headers=self.DEFAULT_HEADERS, json=data)
        return res.status_code, res.text

    def delete_booking(self, token, booking_id):
        url = self._address + self.BOOKING_ENDPOINT + str(booking_id)
        cookies = {
            'token': token
        }
        res = requests.delete(url, cookies=cookies, headers=self.DEFAULT_HEADERS)
        return res.status_code, res.text

    def get_report(self, token):
        url = self._address + self.REPORT_ENDPOINT
        cookies = {
            'token': token
        }
        res = requests.get(url, cookies=cookies, headers=self.DEFAULT_HEADERS)
        return res.status_code, res.text

    def search(self, token, keyword):
        url = self._address + self.SEARCH_ENDPOINT
        cookies = {
            'token': token
        }
        params = {
            'keyword': keyword
        }
        res = requests.get(url, cookies=cookies, headers=self.DEFAULT_HEADERS, params=params)
        return res.status_code, res.text
