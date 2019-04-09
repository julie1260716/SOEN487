from user_profile.app_profile import app as test_app
from user_profile.app_profile import db as test_db
from user_profile.database_profile import Profile, Profile
import unittest
import json

# test_app.config.from_object(TestConfig)

class TestProfile(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = test_db
        self.db.create_all()
        self.db.session.add(Profile(profile_id=1, profile_name="A star is born", profile_number=50))
        self.db.session.add(Profile(profile_id=2, profile_name="Escape Room", profile_number=30))
        self.db.session.commit()

        self.app = test_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Profile.query.delete()
        self.db.session.commit()

    def test_get_all_profiles(self):
        # send the request and check the response status code
        response = self.app.get("/profile")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        profile_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(profile_list), list)
        self.assertDictEqual(profile_list[0], {"profile_id": "1", "profile_name": "A star is born", "profile_number": "50"})
        self.assertDictEqual(profile_list[1], {"profile_id": "2", "profile_name": "Escape Room", "profile_number": "30"})

    def test_get_profile_with_valid_name(self):
        # send the request and check the response status code
        response = self.app.get("/profile/Escape Room")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        person = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(person, {"profile_id": "2", "profile_name": "Escape Room", "profile_number": "30"})

    def test_get_profile_with_invalid_name(self):
        # send the request and check the response status code
        response = self.app.get("/profile/Silent Hill")
        self.assertEqual(response.status_code, 404)

    def test_get_profile_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/profile/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        profile = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(profile, {"profile_id": "1", "profile_name": "A star is born", "profile_number": "50"})

    def test_get_profile_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/profile/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this profile id."})

    # Testing new profile insertion
    def test_create_profile_with_new_id(self):

        # send the request and check the response status code
        response = self.app.put("/profile", data={"profile_id": 3, "profile_name": "The Upside", "profile_number": 65})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        profile = Profile.query.filter_by(profile_id=3).first()
        self.assertEqual(profile.profile_name, "The Upside")
        self.assertEqual(profile.profile_number, 65)

    # Testing exist profile update by id
    def test_update_profile_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.put("/profile/update", data={"profile_id": 1,
                                                        "profile_name": "A star is born",
                                                        "profile_number": 10})

        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        profile = Profile.query.filter_by(profile_id=1).first()
        self.assertEqual(profile.profile_number, 10)

    # Testing exist profile update by id
    def test_update_profile_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.put("/profile/update", data={"profile_id": 1000000,
                                                        "profile_name": "Invalid Profile ID",
                                                        "profile_number": 555})

        self.assertEqual(response.status_code, 404)

    # Testing exist profile update by profile name
    def test_update_profile_without_id(self):
        # send the request and check the response status code
        response = self.app.put("/profile/update", data={"profile_name": "A star is born", "profile_number": 10})

        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        profile = Profile.query.filter_by(profile_id=1).first()
        self.assertEqual(profile.profile_number, 10)

    # Testing exist profile deletion
    def test_delete_profile_with_valid_id(self):

        # send the request and check the response status code
        create_response = self.app.put("/profile", data={"profile_id": 3, "profile_name": "The Upside", "profile_number": 65})
        self.assertEqual(create_response.status_code, 200)

        profile = Profile.query.filter_by(profile_id=3).first()
        self.assertEqual(profile.profile_name, "The Upside")
        self.assertEqual(profile.profile_number, 65)

        # send the request and check the response status code
        delete_response = self.app.put("/profile/delete", data={"profile_id": 3})
        self.assertEqual(delete_response.status_code, 200)

        profile = Profile.query.filter_by(profile_id=3).first()
        self.assertEqual(profile, None)

    # Testing non-exist profile deletion
    def test_delete_profile_with_invalid_id(self):
        # send the request and check the response status code
        delete_response = self.app.put("/profile/delete", data={"profile_id": 1000000})
        self.assertEqual(delete_response.status_code, 404)

