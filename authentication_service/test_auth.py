from authentication_service.main import app as test_app
from authentication_service.dependency import db as test_db
from authentication_service.dependency import init_database
from authentication_service.models import Auth
import unittest
import json

# test_app.config.from_object(TestConfig)
# TODO: modify and update the test cases created in assignment 1


class TestTicket(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = test_db
        self.db.create_all()
        self.db.session.add(Auth(id=1, public_id="abcd1234", email="test1@gmail.com", password=321, admin=True))
        self.db.session.add(Auth(id=2, public_id="4321dcba", email="test2@gmail.com", password=123, admin=False))
        self.db.session.commit()

        self.app = test_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Auth.query.delete()
        self.db.session.commit()

    def test_login(self):
        # send the request and check the response status code
        response = self.app.post("/auth/login", data={"user_email": "test1@gmail.com", "password": 321})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

    def test_login_with_invalid_password(self):
        # send the request and check the response status code
        response = self.app.post("/auth/login", data={"user_email": "test1@gmail.com", "password": 222111})
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "fail"})

    def test_login_with_invalid_user_email(self):
        # send the request and check the response status code
        response = self.app.post("/auth/login", data={"user_email": "badtest@gmail.com", "password": 321})
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "fail"})

    # Testing exist ticket deletion
    def test_delete_user_from_auth(self):

        # send the request and check the response status code
        create_response = self.app.delete("/auth/delete/<user_id>", data={"public_id": "abcd1234"})
        self.assertEqual(create_response.status_code, 200)

        user = Auth.query.filter_by(public_id="abcd1234").first()
        self.assertEqual(user.email, "test1@gmail.com")
        self.assertEqual(user.password, 321)

        # send the request and check the response status code
        delete_response = self.app.put("/auth/delete/<user_id>", data={"public_id": "abcd1234"})
        self.assertEqual(delete_response.status_code, 200)

        user = Auth.query.filter_by(public_id="abcd1234").first()
        self.assertEqual(user, None)

    # Testing non-exist ticket deletion
    def test_delete_user_from_auth_with_invalid_id(self):
        # send the request and check the response status code
        delete_response = self.app.delete("/auth/delete/<user_id>", data={"public_id": "uvwx9876"})
        self.assertEqual(delete_response.status_code, 404)

