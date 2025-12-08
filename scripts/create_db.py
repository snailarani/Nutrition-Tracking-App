from app import create_app, db

def main():
    app = create_app()

    with app.app_context():
        # Must import models before running create_all otherwise flask_sqlalchemy will not know them
        import app.models
        db.create_all()  # creates tables