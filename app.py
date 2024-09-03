from flask import Flask
from routes import *

app = Flask(__name__)
app.secret_key = "anaki1912"


@app.before_request
def before_request():
    g.db = connect_server()


@app.teardown_request
def teardown_request(exception=None):
    if hasattr(g, "db"):
        g.db.close()


register_blueprints(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
