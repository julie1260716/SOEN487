from user_service.app_user import app as test_app
from user_service.app_user import db as test_db
from user_service.database_user import User
import unittest
import json


"""Test works when remove all auth check"""
class TestUser(unittest.TestCase):
    def setUp(self):
        self.db = test_db
        self.db.create_all()
        self.db.session.add(User(public_id="123a"),
                        fname="Jennifer",
                        lname="Williams",
                        birthday="1988-05-19",
                        email="JenniferTWilliams@rhyta.com",
                        phone="209-752-1056",
                        address="1613 Freed Drive"))
        self.db.session.add(User(public_id="abc111",
                        fname="Carlos",
                        lname="Bartlett",
                        birthday="1978-03-29",
                        email="CarlosABartlett@jourrapide.com",
                        phone="321-328-4916",
                        address="2754 Terry Lane"))
        self.db.session.commit()

        self.app = test_app.test_client()

    def tearDown(self):
        User.query.delete()
        self.db.session.commit()

    # Testing create user
    def test_create_user(self):

        # send the post request with the payload and check the response status code
        response = self.app.put("/user", data={"public_id":"jdidk123","first_name":"yang",
                                               "last_name":"an",
                                               "date_of_birth":"1988-05-19",
                                               "email":"JenniferTWilliams@rhyta.com",
                                               "phone_number":"209-752-1056",
                                               "address": "1613 Freed Drive"})
        self.assertEqual(response.status_code, 200)
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        user = User.query.filter_by(public_id="jdidk123").first()
        self.assertEqual(user.fname, "yang")
    # Testing create user without first_name
    def test_create_user_missing_info(self):
        # send the post request with the payload and check the response status code
        response = self.app.put("/user", data={"public_id":"jdidk123","first_name":"",
                                               "last_name":"an",
                                               "date_of_birth":"1988-05-19",
                                               "email":"JenniferTWilliams@rhyta.com",
                                               "phone_number":"209-752-1056",
                                               "address": "1613 Freed Drive"})
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Cannot create new user profile. Missing mandatory fields"})


    # Testing get user success
    def test_get_user_valid(self):
        # send the request and check the response status code
        response = self.app.get("/user/123a")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        user = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(user, {"public_id":"123a","first_name":"Jennifer",
                                               "last_name":"Williams",
                                               "date_of_birth":"1988-05-19",
                                               "email":"JenniferTWilliams@rhyta.com",
                                               "phone_number":"209-752-1056",
                                               "address": "1613 Freed Drive"})
    # Testing get user with invalid user id
    def test_get_user_with_invalid_id(self):
        response = self.app.get("/user/123")
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find user profile with this user_id."})


    # Testing update user
    def test_update_user(self):
        response =  self.app.put("/user/123a", data={"first_name":"yang",
                                               "last_name":"an"})
        self.assertEqual(response.status_code, 200)
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        user = User.query.filter_by(public_id="123a").first()
        self.assertEqual(user.fname, "yang")
        self.assertEqual(user.lname, "an")

    # Testing update user with invalid user id
    def test_update_user_invalid_id(self):
        response = self.app.put("/user/123", data={"first_name": "yang",
                                                    "last_name": "an"})
        self.assertEqual(response.status_code, 404)
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot update, user not found."})

    # Testing update user with empty content
    def test_update_user_invalid_id(self):
        response = self.app.put("/user/123", data={})
        self.assertEqual(response.status_code, 404)
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Nothing to update."})


