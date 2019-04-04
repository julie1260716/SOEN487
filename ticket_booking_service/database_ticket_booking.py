from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from datetime import datetime

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
    show_time = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Ticket {} {} {} {}>".format(self.ticket_id, self.movie_name, self.theater_loc, self.show_time)


# mysql-> booking table
class Booking(db.Model):
    """
      user_id: an unique id to locate an user
      ticket_id: an unique id to locate a ticket, this id needs to be existent in ticket table
      booking_time: the time an user booked a ticket
      ticket_qty: the number of tickets an user booked
    """
    user_id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.ticket_id"))
    ticket_qty = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "<Booking {} {} {} {}>".format(self.user_id, self.ticket_id, self.ticket_qty, self.booking_time)


# Define a ticket booking form to check the validation of inputs
class TicketBookingForm(FlaskForm):
    movie_name = StringField("movie_name", validators=[DataRequired(), Length(max=255)])
    theater_loc = StringField("theater_loc", validators=[DataRequired(), Length(max=255)])
    show_time = StringField("show_time", validators=[DataRequired(), Length(max=255)])


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
    db.session.add(Ticket(movie_name="Frozen", theater_loc="Montreal", show_time="May"))
    db.session.add(Ticket(movie_name="Frozen", theater_loc="Toronto", show_time="May"))
    db.session.add(Ticket(movie_name="Harry Potter", theater_loc="Montreal", show_time="May"))
    db.session.add(Ticket(movie_name="Harry Potter", theater_loc="Toronto", show_time="May"))
    db.session.add(Ticket(movie_name="Imitation", theater_loc="Montreal", show_time="May"))
    db.session.add(Ticket(movie_name="Imitation", theater_loc="Toronto", show_time="May"))
    db.session.commit()

