from flask import Flask, render_template, jsonify
from user_profile.database_profile import db, DATABASE_URI, init_database, MovieProfileForm
from user_profile.view_profile import profiles_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SECRET_KEY"] = "test"
db.app = app
db.init_app(app)
init_database()
app.register_blueprint(profiles_blueprint)


@app.errorhandler(403)
def page_not_found(e):
    """Render a 403 page"""
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    """Render a 404 page"""
    return render_template("404.html"), 404


@app.route('/profile.html')
def profile_page():
    form = MovieProfileForm()
    return render_template("profile.html", form=form)


@app.route('/')
@app.route('/homepage.html')
def index():
    return render_template("homepage.html")


if __name__ == '__main__':
    # set different port number to differentiate services deployed on the same local server
    app.run(port=5003, debug=True)
