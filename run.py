from app import create_app
from scripts.populate_food import populate_food_database


def main():
    app = create_app()  # tables are created here

    with app.app_context():  # required to access db
        populate_food_database()     # populate tables

    app.run(debug=True)

# Run the app and create database
if __name__ == '__main__':
    main()