from flask import Flask, render_template, jsonify
from recommendation_service.database_recommendation import db, DATABASE_URI, init_database
from recommendation_service.view_recommendation import recommendations_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
db.app = app
db.init_app(app)
init_database()
app.register_blueprint(recommendations_blueprint)


@app.errorhandler(403)
def page_not_found(e):
    """Render a 403 page"""
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    """Render a 404 page"""
    return render_template("404.html"), 404


@app.route('/booking.html')
def recommendation_page():
    return render_template("booking.html")


@app.route('/')
@app.route('/homepage.html')
def index():
    return render_template("homepage.html")


"""
# This is an example of using recommendation template for the recommendation service's use
@app.route('/')
def index():

    test_movie = {
        "name": "frozen",
        "description": "This movie is about...",
        "rating": "PG",
        "genres": ["Animation", "Adventure", "Comedy"],
        "actors": ["Kristen Bell", "Idina Menzel", "Jonathan Groff"],
        "directors": ["Chris Buck", "Jennifer Lee"],
        "studio": "Walt Disney Studios",
        "length": "1h 42min"}

    return render_template("recommendations.html", movie=test_movie)
"""

if __name__ == '__main__':
    # set different port number to differentiate services deployed on the same local server
    app.run(port=5003, debug=True)
