from flask import Flask, jsonify, make_response
from config import Config
from dependency import db
from views.userView import userView

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(userView)
#
# from views.productView import productView
# app.register_blueprint(productView)
#
# from views.cartView import cartView
# app.register_blueprint(cartView)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def soen487_a1():
    return jsonify({"title": "SOEN487 Assignment 1",
                    "student": {"id": "Your id#", "name": "Your name"}})


if __name__ == '__main__':
    app.run(debug=True)
