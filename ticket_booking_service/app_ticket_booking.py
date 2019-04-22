from flask import Flask, render_template
from ticket_booking_service.database_ticket_booking import db, DATABASE_URI, init_database, TicketBookingForm
from ticket_booking_service.view_ticket_booking import tickets_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = "test"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.app = app
db.init_app(app)
init_database()
app.register_blueprint(tickets_blueprint)


@app.errorhandler(403)
def page_not_found(e):
    """Render a 403 page"""
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    """Render a 404 page"""
    return render_template("404.html"), 404


@app.route('/booking.html')
def ticket_booking_page():
    form = TicketBookingForm()
    return render_template("booking.html", form=form)


@app.route('/')
@app.route('/homepage.html')
def index():
    return render_template("homepage.html")


if __name__ == '__main__':
    # set different port number to differentiate services deployed on the same local server
    app.run(port=5005, debug=True)
