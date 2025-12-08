from app import create_app

def main():
    app = create_app()  # tables are created here
    app.run(debug=True)

# Run the app and create database
if __name__ == '__main__':
    main()