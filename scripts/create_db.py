import os.path as path
from app import create_app, db

def main():
    app = create_app()

    if not path.exists("instance/database.db"):
        with app.app_context():
            # Must import models before running create_all otherwise flask_sqlalchemy will not know them
            import app.models
            db.create_all()  # creates tables
            print("Database created successfully!")

if __name__ == "__main__":
    main()