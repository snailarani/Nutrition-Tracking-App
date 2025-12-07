from app import create_app, db

app = create_app()

# creates all tables
with app.app_context():
    db.create_all()
    print("All tables created!")