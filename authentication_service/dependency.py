from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# Initial database for ticket booking service
def init_database():
    db.drop_all()
    db.create_all()