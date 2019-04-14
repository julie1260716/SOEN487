from authentication_service.main import app
from authentication_service.models import db, Auth


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Auth=Auth)
