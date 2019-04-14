from flask import Flask
from authentication_service.config import Config
from authentication_service.dependency import db, init_database
from authentication_service.views.authView import authView

app = Flask(__name__)
app.config.from_object(Config)
# Note: 'db.app = app' is add to fix 'RuntimeError: application not registered on db instance and no
# application bound to current context'
db.app = app
db.init_app(app)

with app.app_context():
    init_database()

app.register_blueprint(authView)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
