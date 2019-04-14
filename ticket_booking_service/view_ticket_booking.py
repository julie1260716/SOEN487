from flask import jsonify, request, make_response, render_template, redirect
from ticket_booking_service.database_ticket_booking import db, row2dict, Ticket, Booking, TicketBookingForm
from flask import Blueprint
from functools import wraps
import requests
import sqlalchemy.exc

tickets_blueprint = Blueprint("tickets", __name__)

AUTH_URL = 'http://127.0.0.1:5000/auth/check'


def token_required(func):
    """
    verify token
    """
    @wraps(func)
    def wrapper(*arg, **keywordargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            form = TicketBookingForm()
            return render_template("booking.html", form=form, user_not_login=True)

        headers = {'content-type': 'application/json', 'x-access-token': token}

        try:
            response = requests.get(AUTH_URL, headers=headers)
            current_user = response.json()["current_user_info"]
            if response.status_code == 401:
                form = TicketBookingForm()
                return render_template("booking.html", form=form, user_not_login=True)
            return func(current_user, *arg, **keywordargs)
        except Exception as e:
            return make_response(jsonify({'code': 500, 'msg': str(e)}), 500)
        return func(current_user, *arg, **keywordargs)
    return wrapper


@tickets_blueprint.route("/ticket")
def get_all_tickets():
    """Return information for all tickets stored in the database"""
    ticket_list = Ticket.query.all()
    return jsonify([row2dict(ticket) for ticket in ticket_list])


@tickets_blueprint.route("/ticket/<movie_name>")
def get_ticket_by_name(movie_name):
    """Return ticket information by movie name of a ticket"""
    ticket = Ticket.query.filter_by(movie_name=movie_name).first()
    if ticket:
        return jsonify(row2dict(ticket))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find the ticket with this movie name."}), 404)


@tickets_blueprint.route("/ticket/<int:ticket_id>")
def get_ticket(ticket_id):
    """Return ticket information by ticket id, this function is created for administer's use"""
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    if ticket:
        return jsonify(row2dict(ticket))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this ticket id."}), 404)


@tickets_blueprint.route("/ticket", methods={"POST"})
def create_ticket():
    """This function is created for administer's use"""
    movie_name = request.form.get("movie_name")
    theater_loc = request.form.get("theater_loc")
    show_time = request.form.get("show_time")

    if not movie_name:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put ticket. Missing mandatory fields."}), 403)

    # check if the ticket with the given movie has existed
    ticket = Ticket.query.filter_by(movie_name=movie_name).first()
    if ticket:
        return make_response(jsonify({"code": 403,
                                      "msg": "Ticket with this movie name has existed"}), 403)
    else:
        ticket = Ticket(movie_name=movie_name, theater_loc=theater_loc, show_time=show_time)

    db.session.add(ticket)

    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as error:
        return make_response(jsonify({"code": 404, "msg": str(error)}), 404)
    return jsonify({"code": 200, "msg": "success"})


@tickets_blueprint.route("/ticket/update", methods={"PUT"})
def update_ticket():
    """Update ticket by id or movie name, this function is created for administer's use"""
    # get the movie name first, if no movie name then fail
    ticket_id = request.form.get("ticket_id")
    movie_name = request.form.get("movie_name")
    theater_loc = request.form.get("theater_loc")
    show_time = request.form.get("show_time")

    if not ticket_id and not movie_name:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot update ticket. Missing mandatory fields."}), 403)

    if ticket_id:
        ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    else:
        ticket = Ticket.query.filter_by(movie_name=movie_name).first()

    if not ticket:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this ticket."}), 404)

    if theater_loc:
        ticket.theater_loc = theater_loc
    if show_time:
        ticket.show_time = show_time

    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as error:
        return make_response(jsonify({"code": 500, "msg": str(error)}), 500)
    return jsonify({"code": 200, "msg": "success"})


@tickets_blueprint.route("/ticket/delete", methods={"POST"})
def delete_ticket():
    """Delete ticket by id, this function is created for administer's use"""
    ticket_id = request.form.get("ticket_id")
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    if ticket:
        db.session.delete(ticket)
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as error:
            return make_response(jsonify({"code": 500, "msg": str(error)}), 500)
        return jsonify({"code": 200, "msg": "ticket is successfully deleted"})
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this ticket id."}), 404)


@tickets_blueprint.route("/ticket-booking", methods={"POST"})
@token_required
def book_ticket(current_user):
    # Step 1: locate the ticket based on the data sent from the form
    form = TicketBookingForm()

    if form.validate_on_submit():
        movie_name = form.movie_name.data
        theater_loc = form.theater_loc.data
        show_date = form.show_date.data
        show_time = form.show_time.data
        ticket_qty = form.ticket_qty.data

        ticket = Ticket.query.filter_by(movie_name=movie_name,
                                        theater_loc=theater_loc,
                                        show_date=show_date,
                                        show_time=show_time).first()
        if ticket:
            # print("Ticket Found, Ticket ID: {}".format(ticket.ticket_id))
            # Step 2: insert the ticket booking data to booking table
            user_id = current_user["public_id"]
            ticket_id = ticket.ticket_id
            booking_data = Booking(user_id=user_id, ticket_id=ticket_id, ticket_qty=ticket_qty)

            db.session.add(booking_data)

            try:
                db.session.commit()
            except sqlalchemy.exc.SQLAlchemyError as error:
                return make_response(jsonify({"code": 500, "msg": str(error)}), 500)

            return render_template("booking.html", alertMsg='success')
        else:
            return render_template("booking.html", alertMsg='warning')
    else:
        print(form.errors.items())  # display the form errors
        # probably add code to display a message box saying invalid input
        return render_template("booking.html", form=form)


@tickets_blueprint.route("/booking-table")
def get_all_booking_data():
    """Return all booking data stored in the database"""
    booking_list = Booking.query.all()
    return jsonify([row2dict(booking_data) for booking_data in booking_list])


@tickets_blueprint.route('/booking_table.html')
def booking_table_page():
    """Return all booking data stored in the database and display them in HTML page"""
    booking_list = Booking.query.all()
    booking_data = [row2dict(booking_data) for booking_data in booking_list]
    return render_template("booking_table.html", booking_data=booking_data)
