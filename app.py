from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from main import *

app = Flask(__name__)

SERVER = connect_server()
app.secret_key = "anaki1912"


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return (
            jsonify({"status": "error", "message": "Email and Password are required"}),
            401,
        )

    if not does_email_exist(SERVER, email):
        return jsonify({"status": "error", "message": "This email doesn't exist!"}), 401

    if not is_correct_password(SERVER, email, password):
        return jsonify({"status": "error", "message": "Incorrect password"}), 401


    role = get_role(SERVER, email)
    session["email"] = email
    
    if role == "student":
        return jsonify({"status": "success", "redirect": "/student"}), 200

    elif role == "teacher":

        return jsonify({"status": "success", "redirect": "/teacher"}), 200


@app.route("/student")
def student_page():
    email = session.get("email")
    if not email:
        return jsonify({"status": "error", "redirect": "/"}), 401

    s = Student(SERVER, email)
    return render_template("student.html", id=s._id, name=s._name, grades=s)


@app.route("/teacher")
def teacher_page():
    email = session.get("email")
    if not email:
        return jsonify({"status": "error", "redirect": "/"}), 401

    teacher = Teacher(SERVER, email)
    return render_template(
        "teacher.html",
        id=teacher._id,
        name=teacher._name,
        course=teacher.get_course(SERVER),
        count_of_students=len(teacher.get_students_list(SERVER)),
        assignments=teacher.get_assignments(SERVER),
    )


@app.route("/teacher/students", methods=["GET"])
def students_button():
    if request.method == "GET":
        email = session.get("email")
        if email:
            teacher = Teacher(SERVER, email)
            students_list = teacher.get_students_list(SERVER)
            return jsonify({"status": "success", "students": students_list}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/passedStudents", methods=["GET"])
def passed_the_test_button():
    if request.method == "GET":
        email = session.get("email")
        if email:
            teacher = Teacher(SERVER, email)
            students = teacher.get_students_with_passing_grades()
        return jsonify(
            {"status": "success", "students": students, "students_count": len(students)}
        ), 200

@app.route("/teacher/profile")
def profile():
    email = session.get("email")
    if email:
        teacher = Teacher(SERVER, email)
        return jsonify({"name": teacher._name, "email": email, "pass": get_password(SERVER, email), "city": teacher._city}), 200

@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"redirect": "/"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
