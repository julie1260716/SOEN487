from flask import Flask, render_template
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


if __name__ == '__main__':
    # set different port number to differentiate services deployed on the same local server
    app.run(port=5004, debug=True)
