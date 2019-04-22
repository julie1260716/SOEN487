from movie_service.app_movie import app as test_app
from movie_service.app_movie import db as test_db
from movie_service.database_movie import Movie, Movie
import unittest
import json

# test_app.config.from_object(TestConfig)

class TestMovie(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = test_db
        self.db.create_all()
        self.db.session.add(Movie(movie_id=1, movie_name="A star is born", movie_number=50))
        self.db.session.add(Movie(movie_id=2, movie_name="Escape Room", movie_number=30))
        self.db.session.commit()

        self.app = test_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Movie.query.delete()
        self.db.session.commit()

    def test_get_all_movies(self):
        # send the request and check the response status code
        response = self.app.get("/movie")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        movie_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(movie_list), list)
        self.assertDictEqual(movie_list[0], {"movie_id": "1", "movie_name": "A star is born", "movie_number": "50"})
        self.assertDictEqual(movie_list[1], {"movie_id": "2", "movie_name": "Escape Room", "movie_number": "30"})

    def test_get_movie_with_valid_name(self):
        # send the request and check the response status code
        response = self.app.get("/movie/Escape Room")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        person = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(person, {"movie_id": "2", "movie_name": "Escape Room", "movie_number": "30"})

    def test_get_movie_with_invalid_name(self):
        # send the request and check the response status code
        response = self.app.get("/movie/Silent Hill")
        self.assertEqual(response.status_code, 404)

    def test_get_movie_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/movie/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        movie = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(movie, {"movie_id": "1", "movie_name": "A star is born", "movie_number": "50"})

    def test_get_movie_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/movie/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this movie id."})

    # Testing new movie insertion
    def test_create_movie_with_new_id(self):

        # send the request and check the response status code
        response = self.app.put("/movie", data={"movie_id": 3, "movie_name": "The Upside", "movie_number": 65})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        movie = Movie.query.filter_by(movie_id=3).first()
        self.assertEqual(movie.movie_name, "The Upside")
        self.assertEqual(movie.movie_number, 65)

    # Testing exist movie update by id
    def test_update_movie_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.put("/movie/update", data={"movie_id": 1,
                                                        "movie_name": "A star is born",
                                                        "movie_number": 10})

        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        movie = Movie.query.filter_by(movie_id=1).first()
        self.assertEqual(movie.movie_number, 10)

    # Testing exist movie update by id
    def test_update_movie_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.put("/movie/update", data={"movie_id": 1000000,
                                                        "movie_name": "Invalid Movie ID",
                                                        "movie_number": 555})

        self.assertEqual(response.status_code, 404)

    # Testing exist movie update by movie name
    def test_update_movie_without_id(self):
        # send the request and check the response status code
        response = self.app.put("/movie/update", data={"movie_name": "A star is born", "movie_number": 10})

        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        movie = Movie.query.filter_by(movie_id=1).first()
        self.assertEqual(movie.movie_number, 10)

    # Testing exist movie deletion
    def test_delete_movie_with_valid_id(self):

        # send the request and check the response status code
        create_response = self.app.put("/movie", data={"movie_id": 3, "movie_name": "The Upside", "movie_number": 65})
        self.assertEqual(create_response.status_code, 200)

        movie = Movie.query.filter_by(movie_id=3).first()
        self.assertEqual(movie.movie_name, "The Upside")
        self.assertEqual(movie.movie_number, 65)

        # send the request and check the response status code
        delete_response = self.app.put("/movie/delete", data={"movie_id": 3})
        self.assertEqual(delete_response.status_code, 200)

        movie = Movie.query.filter_by(movie_id=3).first()
        self.assertEqual(movie, None)

    # Testing non-exist movie deletion
    def test_delete_movie_with_invalid_id(self):
        # send the request and check the response status code
        delete_response = self.app.put("/movie/delete", data={"movie_id": 1000000})
        self.assertEqual(delete_response.status_code, 404)

