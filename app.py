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
    session["password"] = password

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
    password = session.get("password")
    if not email:
        return jsonify({"status": "error", "redirect": "/"}), 401

    teacher = Teacher(SERVER, email, password)

    return render_template(
        "teacher.html",
        id=teacher.info["id"],
        name=teacher.info["name"],
        course=teacher.get_course(SERVER),
        count_of_students=len(teacher.get_students_list(SERVER)),
        assignments=teacher.get_assignments(SERVER),
    )


@app.route("/teacher/studentsInfo", methods=["GET"])
def students_info_button():
    if request.method == "GET":
        email = session.get("email")
        if email:
            password = session.get("password")
            teacher = Teacher(SERVER, email, password)
            students_info = teacher.get_students_info(SERVER)
            return jsonify({"status": "success", "students": students_info}), 200
        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/studentsGrades", methods=["GET"])
def students_grades_button():
    if request.method == "GET":
        email = session.get("email")
        if email:
            password = session.get("password")
            teacher = Teacher(SERVER, email, password)
            students_list = teacher.get_students_list(SERVER)
            return (
                jsonify(
                    {
                        "status": "success",
                        "students": students_list,
                        "count": len(students_list),
                    }
                ),
                200,
            )

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/editGrade", methods=["PUT"])
def edit_grade():
    if request.method == "PUT":
        email = session.get("email")
        if email:
            password = session.get("password")
            data = request.json
            student_id = data.get("id")
            new_grade = data.get("grade")
            teacher = Teacher(SERVER, email, password)
            teacher.update_grade_for_student(SERVER, student_id, new_grade)
            return jsonify({"message": f"The grade is {new_grade} now"}), 200
    return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/passedStudents", methods=["GET"])
def passed_the_test_button():
    if request.method == "GET":
        email = session.get("email")
        if email:
            password = session.get("password")
            teacher = Teacher(SERVER, email, password)
            students = teacher.get_students_with_passing_grades()
        return (
            jsonify(
                {
                    "status": "success",
                    "students": students,
                    "students_count": len(students),
                }
            ),
            200,
        )


@app.route("/teacher/profile")
def profile():
    email = session.get("email")

    if email:
        password = session.get("password")
        teacher = Teacher(SERVER, email, password)
        return jsonify({"info": teacher.info}), 200


@app.route("/editValue", methods=["PUT"])
def edit_value():
    if request.method == "PUT":
        data = request.json
        key = data.get("key")
        new_val = input("Enter a new value: ")
        email = session.get("email")
        password = session.get("password")

        teacher = Teacher(SERVER, email, password)
        teacher.change_detail(SERVER, key, new_val)
        return jsonify({"status": "success", "message": key}), 200


@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"redirect": "/"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
