from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange
from datetime import datetime
import uuid

# Define mysql database connection string
DATABASE_URI = "mysql+mysqlconnector://root:Sci123456@localhost/TicketBookingDB"

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()


# mysql-> ticket table
class Ticket(db.Model):
    """
      ticket_id: an unique id to locate a ticket
      movie_name: this movie name column will be populated with the data fetched from movie service
      theatre_loc: location of a theatre, a randomly generated data will be used to populate this column
      show_time: show time of a movie, a randomly generated data will be used to populate this column
    """
    ticket_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.Text, nullable=False)
    theater_loc = db.Column(db.Text, nullable=False)
    show_date = db.Column(db.Date, nullable=False)
    show_time = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Ticket {} {} {} {}>".format(self.ticket_id, self.movie_name, self.theater_loc, self.show_time)


# mysql-> booking table
class Booking(db.Model):
    """
      booking_id: an unique id to locate a row in the booking table
      user_id: an id to locate an user
      ticket_id: an id to locate a ticket, this id needs to be existent in ticket table
      booking_time: the time an user booked a ticket
      ticket_qty: the number of tickets an user booked
    """
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.ticket_id"))
    ticket_qty = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "<Booking {} {} {} {} {}>".format(self.booking_id, self.user_id,
                                                 self.ticket_id, self.ticket_qty, self.booking_time)


# Define a ticket booking form to check the validation of inputs
class TicketBookingForm(FlaskForm):
    """
      Note: To bypass the 'The CSRF token is missing' error while simulating users sending form data through
      python requests, it is a MUST to set csrf to False under class Meta. However, it is necessary to comment
      out the following two lines of code to protect cross-site request forgery attack in dev/product mode
    """
    class Meta:
        csrf = False

    movie_name = StringField("movie_name", validators=[DataRequired(message="Movie name is required"), Length(max=255)])
    theater_loc = StringField("theater_loc", validators=[DataRequired(message="Theatre location is required"), Length(max=255)])
    show_date = DateField("show_date", validators=[DataRequired(message="Date is required")])
    show_time = StringField("show_time", validators=[DataRequired(message="Show time is required"), Length(max=255)])
    ticket_qty = IntegerField("ticket_qty", validators=[DataRequired(message="Number of ticket is required"), NumberRange(min=1, max=40)])


# An auxiliary function convert row to dictionary form
def row2dict(row):
    return {col.name: str(getattr(row, col.name)) for col in row.__table__.columns}


# Initial database for ticket booking service
def init_database():
    db.drop_all()
    db.create_all()
    init_ticket_table()


# Populate the ticket table
def init_ticket_table():
    # Populate ticket table (hard coded version)
    # TODO: write code to automatically populate the ticket table with movie data fetched form movie service
    db.session.add(Ticket(movie_name="Frozen", theater_loc="Montreal", show_date="2019-04-25", show_time="17:30"))
    db.session.add(Ticket(movie_name="Frozen", theater_loc="Toronto", show_date="2019-04-25", show_time="19:00"))
    db.session.add(Ticket(movie_name="Harry Potter", theater_loc="Montreal", show_date="2019-04-20", show_time="17:30"))
    db.session.add(Ticket(movie_name="Harry Potter", theater_loc="Toronto", show_date="2019-04-20", show_time="19:00"))
    db.session.add(Ticket(movie_name="Imitation", theater_loc="Montreal", show_date="2019-04-27", show_time="20:30"))
    db.session.add(Ticket(movie_name="Imitation", theater_loc="Toronto", show_date="2019-04-27", show_time="22:00"))
    db.session.commit()

    # Populate booking data for displaying purpose
    db.session.add(Booking(user_id=str(uuid.uuid4()), ticket_id="1", ticket_qty="2"))
    db.session.add(Booking(user_id=str(uuid.uuid4()), ticket_id="1", ticket_qty="1"))
    db.session.add(Booking(user_id=str(uuid.uuid4()), ticket_id="3", ticket_qty="2"))
    db.session.add(Booking(user_id=str(uuid.uuid4()), ticket_id="2", ticket_qty="4"))
    db.session.add(Booking(user_id=str(uuid.uuid4()), ticket_id="1", ticket_qty="2"))

    db.session.commit()

