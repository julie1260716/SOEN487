from flask import Flask, render_template
from user_service.database_user import db, DATABASE_URI, init_database
from user_service.view_user import users_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.app = app
db.init_app(app)
init_database()
app.register_blueprint(users_blueprint)


@app.errorhandler(403)
def page_not_found(e):
    """Render a 403 page"""
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    """Render a 404 page"""
    return render_template("404.html"), 404


@app.route('/')
@app.route('/homepage.html')
def index():
    return render_template("homepage.html")


@app.route('/login.html')
def login_page():
    return render_template("login.html")


@app.route('/signup.html')
def signup_page():
    return render_template("signup.html")


if __name__ == '__main__':
    # The port number of user service is set up as 5001
    app.run(host='127.0.0.1', port=5001, debug=True)
