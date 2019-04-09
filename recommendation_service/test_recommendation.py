from recommendation_service.app_recommendation import app as test_app
from recommendation_service.app_recommendation import db as test_db
from recommendation_service.database_recommendation import Recommendation, Recommendation
import unittest
import json

# test_app.config.from_object(TestConfig)

class TestRecommendation(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = test_db
        self.db.create_all()
        self.db.session.add(Recommendation(recommendation_id=1, movie_name="A star is born", recommendation_number=50))
        self.db.session.add(Recommendation(recommendation_id=2, movie_name="Escape Room", recommendation_number=30))
        self.db.session.commit()

        self.app = test_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Recommendation.query.delete()
        self.db.session.commit()

    def test_get_all_recommendations(self):
        # send the request and check the response status code
        response = self.app.get("/recommendation")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        recommendation_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(recommendation_list), list)
        self.assertDictEqual(recommendation_list[0], {"recommendation_id": "1", "movie_name": "A star is born", "recommendation_number": "50"})
        self.assertDictEqual(recommendation_list[1], {"recommendation_id": "2", "movie_name": "Escape Room", "recommendation_number": "30"})

    def test_get_recommendation_with_valid_name(self):
        # send the request and check the response status code
        response = self.app.get("/recommendation/Escape Room")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        person = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(person, {"recommendation_id": "2", "movie_name": "Escape Room", "recommendation_number": "30"})

    def test_get_recommendation_with_invalid_name(self):
        # send the request and check the response status code
        response = self.app.get("/recommendation/Silent Hill")
        self.assertEqual(response.status_code, 404)

    def test_get_recommendation_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/recommendation/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        recommendation = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(recommendation, {"recommendation_id": "1", "movie_name": "A star is born", "recommendation_number": "50"})

    def test_get_recommendation_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/recommendation/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this recommendation id."})

    # Testing new recommendation insertion
    def test_create_recommendation_with_new_id(self):

        # send the request and check the response status code
        response = self.app.put("/recommendation", data={"recommendation_id": 3, "movie_name": "The Upside", "recommendation_number": 65})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        recommendation = Recommendation.query.filter_by(recommendation_id=3).first()
        self.assertEqual(recommendation.movie_name, "The Upside")
        self.assertEqual(recommendation.recommendation_number, 65)

    # Testing exist recommendation update by id
    def test_update_recommendation_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.put("/recommendation/update", data={"recommendation_id": 1,
                                                        "movie_name": "A star is born",
                                                        "recommendation_number": 10})

        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        recommendation = Recommendation.query.filter_by(recommendation_id=1).first()
        self.assertEqual(recommendation.recommendation_number, 10)

    # Testing exist recommendation update by id
    def test_update_recommendation_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.put("/recommendation/update", data={"recommendation_id": 1000000,
                                                        "movie_name": "Invalid Recommendation ID",
                                                        "recommendation_number": 555})

        self.assertEqual(response.status_code, 404)

    # Testing exist recommendation update by movie name
    def test_update_recommendation_without_id(self):
        # send the request and check the response status code
        response = self.app.put("/recommendation/update", data={"movie_name": "A star is born", "recommendation_number": 10})

        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        recommendation = Recommendation.query.filter_by(recommendation_id=1).first()
        self.assertEqual(recommendation.recommendation_number, 10)

    # Testing exist recommendation deletion
    def test_delete_recommendation_with_valid_id(self):

        # send the request and check the response status code
        create_response = self.app.put("/recommendation", data={"recommendation_id": 3, "movie_name": "The Upside", "recommendation_number": 65})
        self.assertEqual(create_response.status_code, 200)

        recommendation = Recommendation.query.filter_by(recommendation_id=3).first()
        self.assertEqual(recommendation.movie_name, "The Upside")
        self.assertEqual(recommendation.recommendation_number, 65)

        # send the request and check the response status code
        delete_response = self.app.put("/recommendation/delete", data={"recommendation_id": 3})
        self.assertEqual(delete_response.status_code, 200)

        recommendation = Recommendation.query.filter_by(recommendation_id=3).first()
        self.assertEqual(recommendation, None)

    # Testing non-exist recommendation deletion
    def test_delete_recommendation_with_invalid_id(self):
        # send the request and check the response status code
        delete_response = self.app.put("/recommendation/delete", data={"recommendation_id": 1000000})
        self.assertEqual(delete_response.status_code, 404)

