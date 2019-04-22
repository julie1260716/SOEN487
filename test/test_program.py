from ticket_booking_service.app_ticket_booking import db as ticket_service_db
from authentication_service.main import db as auth_service_db
from user_service.app_user import db as user_service_db
import unittest
import requests
import json

LOGIN_URL = 'http://127.0.0.1:5000/auth/login'
SIGNUP_URL = 'http://127.0.0.1:5000/auth/sign-up'
TOKEN_VER_URL = 'http://127.0.0.1:5000/auth/check'
GET_USER_URL = 'http://127.0.0.1:5001/user/'
BOOK_TICKET_URL = 'http://127.0.0.1:5005/ticket-booking'
BOOKING_HTML_URL = 'http://127.0.0.1:5005/booking.html'


class TestProgram(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        self.db = auth_service_db
        self.db.drop_all()
        self.db.session.commit()

        self.db = user_service_db
        self.db.drop_all()
        self.db.session.commit()

        # ticket_service_db.drop_all()

        self.db = auth_service_db
        self.db.create_all()
        self.db.session.commit()

        self.db = user_service_db
        self.db.create_all()
        self.db.session.commit()

        # ticket_service_db.create_all()

    def test_signup_success(self):
        """
        Test: sign_up, create_user, get_user

        """
        # Step 1: Prepare the data need to be tested
        signup_data = {'firstName': 'Carlos',
                       'lastName': 'Bartlett',
                       'email': 'CarlosABartlett@jourrapide.com',
                       'dateOfBirth': '1978-03-29',
                       'phoneNumber': '321-328-4916',
                       'address': '2754 Terry Lane',
                       'password': '123456'}

        signup_resp = requests.post(SIGNUP_URL, data=signup_data)
        self.assertEqual(signup_resp.status_code, 200)

        # Step 2: Check if the data have been inserted into auth table
        login_data = {'user_email': 'CarlosABartlett@jourrapide.com', 'password': '123456'}
        login_resp = requests.post(LOGIN_URL, data=login_data)
        self.assertEqual(login_resp.status_code, 200)

        # Step 3: Test if the data have been inserted into user table
        token = login_resp.json()['token']
        headers = {'content-type': 'application/json', 'x-access-token': token}
        token_verif_resp = requests.get(TOKEN_VER_URL, headers=headers)
        current_user = token_verif_resp.json()["current_user_info"]
        public_id = current_user["public_id"]

        req_url = GET_USER_URL + public_id
        user_info_resp = requests.get(req_url, headers=headers)
        # print(user_info_resp.text)
        self.assertEqual(user_info_resp.status_code, 200)
        user_data = user_info_resp.json()
        assert_data = {
            'fname': 'Carlos',
            'lname': 'Bartlett',
            'email': 'CarlosABartlett@jourrapide.com',
            'birthday': '1978-03-29',
            'phone': '321-328-4916',
            'address': '2754 Terry Lane',
            'id': '1',
            'public_id': public_id
        }

        self.assertDictEqual(user_data, assert_data)

    def test_login_fail_info_missing(self):

        # Step 1: Prepare the data need to be tested
        signup_data = {'firstName': 'Jennifer',
                       'lastName': 'Williams',
                       'email': 'JenniferTWilliams@rhyta.com',
                       'dateOfBirth': '1988-05-19',
                       'phoneNumber': '209-752-1056',
                       'address': '1613 Freed Drive',
                       'password': '123456'}

        signup_resp = requests.post(SIGNUP_URL, data=signup_data)
        self.assertEqual(signup_resp.status_code, 200)

        # Step 2: Test login function with incomplete form input data
        login_data = {'user_email': 'JenniferTWilliams@rhyta.com'}
        resp = requests.post(LOGIN_URL, data=login_data)
        self.assertEqual(resp.status_code, 401)

        login_data = {'password': '123456'}
        resp = requests.post(LOGIN_URL, data=login_data)
        self.assertEqual(resp.status_code, 401)

    def test_login_fail_user_not_exist(self):
        login_data = {'user_email': 'UserNotExist@gmail.com', 'password': '123456'}
        resp = requests.post(LOGIN_URL, data=login_data)
        self.assertEqual(resp.status_code, 401)

    def test_login_fail_wrong_password(self):

        # Step 1: Prepare the data need to be tested
        signup_data = {'firstName': 'Jennifer',
                       'lastName': 'Williams',
                       'email': 'JenniferTWilliams@rhyta.com',
                       'dateOfBirth': '1988-05-19',
                       'phoneNumber': '209-752-1056',
                       'address': '1613 Freed Drive',
                       'password': '123456'}

        signup_resp = requests.post(SIGNUP_URL, data=signup_data)
        self.assertEqual(signup_resp.status_code, 200)

        # Step 2: Test login function with wrong user password
        login_data = {'user_email': 'JenniferTWilliams@rhyta.com', 'password': '555555'}
        resp = requests.post(LOGIN_URL, data=login_data)
        self.assertEqual(resp.status_code, 401)

    def test_login_success(self):

        # Step 1: Prepare the data need to be tested
        signup_data = {'firstName': 'Jennifer',
                       'lastName': 'Williams',
                       'email': 'JenniferTWilliams@rhyta.com',
                       'dateOfBirth': '1988-05-19',
                       'phoneNumber': '209-752-1056',
                       'address': '1613 Freed Drive',
                       'password': '123456'}

        signup_resp = requests.post(SIGNUP_URL, data=signup_data)
        self.assertEqual(signup_resp.status_code, 200)

        # Step 2: Test login function with correct user email and password
        login_data = {'user_email': 'JenniferTWilliams@rhyta.com', 'password': '123456'}
        resp = requests.post(LOGIN_URL, data=login_data)
        self.assertEqual(resp.status_code, 200)

    def test_ticket_booking(self):
        """ Test: book_ticket """
        # Step 1: Create an user account
        signup_data = {'firstName': 'Carlos',
                       'lastName': 'Bartlett',
                       'email': 'CarlosABartlett@jourrapide.com',
                       'dateOfBirth': '1978-03-29',
                       'phoneNumber': '321-328-4916',
                       'address': '2754 Terry Lane',
                       'password': '123456'}

        signup_resp = requests.post(SIGNUP_URL, data=signup_data)
        self.assertEqual(signup_resp.status_code, 200)

        # Step 2: Login in the user just created
        login_data = {'user_email': 'CarlosABartlett@jourrapide.com', 'password': '123456'}
        login_resp = requests.post(LOGIN_URL, data=login_data)
        self.assertEqual(login_resp.status_code, 200)

        # Step 3: Extract the token for sending a http request to ticket booking
        token = login_resp.json()['token']
        headers = {'content-type': 'application/json', 'x-access-token': token}

        ticket_data = {
            'movie_name': "Frozen",
            'theater_loc': "Montreal",
            'show_date': "2019-04-25",
            'show_time': "17:30",
            'ticket_qty': "2"
        }

        ticket_data = json.dumps(ticket_data)
        book_resp = requests.post(BOOK_TICKET_URL, data=ticket_data, headers=headers)
        # print(book_resp.text)
        self.assertEqual(book_resp.status_code, 200)

        ticket_data_2 = {
            'movie_name': "Imitation",
            'theater_loc': "Montreal",
            'show_date': "2019-04-27",
            'show_time': "20:30",
            'ticket_qty': "1"
        }

        ticket_data_2 = json.dumps(ticket_data_2)
        book_resp = requests.post(BOOK_TICKET_URL, data=ticket_data_2, headers=headers)
        self.assertEqual(book_resp.status_code, 200)

