from app import app

# a simple page that says hello
@app.route("/")
def hello():
        return "<h1>Home Page</h1>"