from flask import Flask, render_template, request, redirect
from main import *

app = Flask(__name__)

SERVER = connect_server()

s = Student(SERVER, "elanaki@gmail.com")

def num(x):
    return x

@app.route("/")
def student():
    return render_template("student.html", id=s._id, name=s._name, grades=s._courses_and_grades, gpa=num(4))

@app.route("/api/students")
def get_students():
    return {"name": "Nitay Caspi"}
@app.route("/login")
def render_login():
    return render_template("login.html")
@app.post("/api/login")
def login():
    data = request.form
    print(data)
    email = data["email"]
    password = data["password"]
    if not email or not password:
        return {"error": "email and password are required"}, 400
    if is_login_successful(SERVER, email, password):
        u = create_user(SERVER, email, password)
        if type(u) == Student:
            s = u
            return render_template("student.html", id=s._id, name=s._name, grades=s._courses_and_grades, gpa=num(4))
    return {"error": "wrong credentials"}, 401
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
