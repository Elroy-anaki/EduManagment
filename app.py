from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from utils import *

app = Flask(__name__)

SERVER = connect_server()
app.secret_key = "anaki1912"


@app.route("/login")
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

    user_id = get_id(SERVER, email)
    role = get_role(SERVER, user_id)
    session["id"] = user_id

    if role == "student":
        return jsonify({"status": "success", "redirect": "/student"}), 200

    elif role == "teacher":

        return jsonify({"status": "success", "redirect": "/teacher"}), 200


@app.route("/teacher")
def teacher_page():
    user_id = session.get("id")
    if not user_id:
        return jsonify({"status": "error", "redirect": "/login"}), 401

    teacher = Teacher(SERVER, user_id)

    return render_template(
        "teacher.html",
        id=teacher.info["id"],
        name=teacher.info["first_name"] + " " + teacher.info["last_name"],
        course=teacher.get_course(SERVER),
        count_of_students=len(teacher.get_students_grades_emails(SERVER)),
    )


@app.route("/student")
def student_page():
    email = session.get("email")
    if not email:
        return jsonify({"status": "error", "redirect": "/login"}), 401

    s = Student(SERVER, email)
    return render_template("student.html", id=s._id, name=s._name, grades=s)


@app.route("/home", methods=["GET"])
def home_button():
    if request.method == "GET":
        user_id = session.get("id")
        if user_id:

            teacher = Teacher(SERVER, user_id)

            return render_template(
                "teacher.html",
                id=teacher.info["id"],
                name=teacher.info["first_name"] + " " + teacher.info["last_name"],
                course=teacher.get_course(SERVER),
                count_of_students=len(teacher.get_students_grades_emails(SERVER)),
            )


# Students Button
@app.route("/teacher/studentsInfo", methods=["GET"])
def students_info_button():
    if request.method == "GET":
        user_id = session.get("id")

        if user_id:
            teacher = Teacher(SERVER, user_id)
            students_info = teacher.get_students_info(SERVER)

            return jsonify({"status": "success", "students": students_info}), 200
        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/studentsGrades", methods=["GET"])
def students_grades_button():
    if request.method == "GET":
        user_id = session.get("id")

        if user_id:
            teacher = Teacher(SERVER, user_id)
            students_list = teacher.get_students_grades_emails(SERVER)
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
        user_id = session.get("id")
        if user_id:
            data = request.json
            student_id = data.get("id")
            new_grade = data.get("grade")
            teacher = Teacher(SERVER, user_id)
            teacher.update_grade_for_student(SERVER, student_id, new_grade)
            return jsonify({"message": f"The grade is {new_grade} now"}), 200
    return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/passedStudents", methods=["GET"])
def passed_the_test_button():
    if request.method == "GET":
        user_id = session.get("id")

        if user_id:
            teacher = Teacher(SERVER, user_id)
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


# Assignmnet Button
@app.route("/teacher/assignments", methods=["GET"])
def assignments_button():
    if request.method == "GET":
        user_id = session.get("id")
        if user_id:
            teacher = Teacher(SERVER, user_id)
            assignments_list = teacher.get_assignments(SERVER)
            return jsonify({"assignments": assignments_list}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/Assignment/addAssignmnet", methods=["POST"])
def add_new_assignment():
    if request.method == "POST":
        user_id = session.get("id")
        if user_id:
            data = request.json
            teacher = Teacher(SERVER, user_id)
            teacher.add_assignment(SERVER, data)
            return jsonify({"message": "Assignment successfully added!"}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/Assignment/editAssignmnet", methods=["POST"])
def edit_assignmnet_button():
    if request.method == "POST":
        user_id = session.get("id")
        if user_id:
            data = request.json
            teacher = Teacher(SERVER, user_id)
            teacher.edit_assigmnet(SERVER, data)
            return jsonify({"message": "The assignment changed"}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/Assignment/deleteAssignmnet", methods=["POST"])
def delete_assignment():
    if request.method == "POST":
        user_id = session.get("id")
        if user_id:
            data = request.json
            teacher = Teacher(SERVER, user_id)
            teacher.remove_assignmnet(SERVER, data)
            return jsonify({"message": "The assignment removed!"}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


# Profile Button
@app.route("/teacher/profile")
def profile():
    user_id = session.get("id")

    if user_id:
        teacher = Teacher(SERVER, user_id)
        return jsonify({"info": teacher.info}), 200


@app.route("/teacher/profile/editPersonalInfo", methods=["PUT"])
def edit_personal_info():
    if request.method == "PUT":
        user_id = session.get("id")
        if user_id:
            data = request.json
            change_details(SERVER, user_id, data)
            return (
                jsonify(
                    {
                        "message": "The details have been successfully changed",
                        "redirect": "/teacher",
                    }
                ),
                200,
            )

    return jsonify({"status": "error", "message": "Unauthorized"}), 401


# Logout button
@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"redirect": "/login"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
