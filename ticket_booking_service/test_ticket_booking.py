from ticket_booking_service.app_ticket_booking import app as test_app
from ticket_booking_service.app_ticket_booking import db as test_db
from ticket_booking_service.database_ticket_booking import Ticket, Booking
import unittest
import json

# test_app.config.from_object(TestConfig)
# TODO: modify and update the test cases created in assignment 1


class TestTicket(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = test_db
        self.db.create_all()
        self.db.session.add(Ticket(ticket_id=1, movie_name="A star is born", ticket_number=50))
        self.db.session.add(Ticket(ticket_id=2, movie_name="Escape Room", ticket_number=30))
        self.db.session.commit()

        self.app = test_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Ticket.query.delete()
        self.db.session.commit()

    def test_get_all_tickets(self):
        # send the request and check the response status code
        response = self.app.get("/ticket")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        ticket_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(ticket_list), list)
        self.assertDictEqual(ticket_list[0], {"ticket_id": "1", "movie_name": "A star is born", "ticket_number": "50"})
        self.assertDictEqual(ticket_list[1], {"ticket_id": "2", "movie_name": "Escape Room", "ticket_number": "30"})

    def test_get_ticket_with_valid_name(self):
        # send the request and check the response status code
        response = self.app.get("/ticket/Escape Room")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        person = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(person, {"ticket_id": "2", "movie_name": "Escape Room", "ticket_number": "30"})

    def test_get_ticket_with_invalid_name(self):
        # send the request and check the response status code
        response = self.app.get("/ticket/Silent Hill")
        self.assertEqual(response.status_code, 404)

    def test_get_ticket_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/ticket/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        ticket = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(ticket, {"ticket_id": "1", "movie_name": "A star is born", "ticket_number": "50"})

    def test_get_ticket_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/ticket/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this ticket id."})

    # Testing new ticket insertion
    def test_create_ticket_with_new_id(self):

        # send the request and check the response status code
        response = self.app.put("/ticket", data={"ticket_id": 3, "movie_name": "The Upside", "ticket_number": 65})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        ticket = Ticket.query.filter_by(ticket_id=3).first()
        self.assertEqual(ticket.movie_name, "The Upside")
        self.assertEqual(ticket.ticket_number, 65)

    # Testing exist ticket update by id
    def test_update_ticket_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.put("/ticket/update", data={"ticket_id": 1,
                                                        "movie_name": "A star is born",
                                                        "ticket_number": 10})

        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        ticket = Ticket.query.filter_by(ticket_id=1).first()
        self.assertEqual(ticket.ticket_number, 10)

    # Testing exist ticket update by id
    def test_update_ticket_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.put("/ticket/update", data={"ticket_id": 1000000,
                                                        "movie_name": "Invalid Ticket ID",
                                                        "ticket_number": 555})

        self.assertEqual(response.status_code, 404)

    # Testing exist ticket update by movie name
    def test_update_ticket_without_id(self):
        # send the request and check the response status code
        response = self.app.put("/ticket/update", data={"movie_name": "A star is born", "ticket_number": 10})

        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        ticket = Ticket.query.filter_by(ticket_id=1).first()
        self.assertEqual(ticket.ticket_number, 10)

    # Testing exist ticket deletion
    def test_delete_ticket_with_valid_id(self):

        # send the request and check the response status code
        create_response = self.app.put("/ticket", data={"ticket_id": 3, "movie_name": "The Upside", "ticket_number": 65})
        self.assertEqual(create_response.status_code, 200)

        ticket = Ticket.query.filter_by(ticket_id=3).first()
        self.assertEqual(ticket.movie_name, "The Upside")
        self.assertEqual(ticket.ticket_number, 65)

        # send the request and check the response status code
        delete_response = self.app.put("/ticket/delete", data={"ticket_id": 3})
        self.assertEqual(delete_response.status_code, 200)

        ticket = Ticket.query.filter_by(ticket_id=3).first()
        self.assertEqual(ticket, None)

    # Testing non-exist ticket deletion
    def test_delete_ticket_with_invalid_id(self):
        # send the request and check the response status code
        delete_response = self.app.put("/ticket/delete", data={"ticket_id": 1000000})
        self.assertEqual(delete_response.status_code, 404)

