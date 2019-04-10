from dependency import db


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # public_id will be put inside the token and prevent bad user supply the previous or next user
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return "<User {}: {}: {}: {}>".format(self.id, self.public_id, self.email, self.admin)





