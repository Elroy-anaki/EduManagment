from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from utils import *
from classes.manager import *
from classes.teacher import *

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

    elif role == "manager":
        return jsonify({"status": "success", "redirect": "/manager"}), 200


@app.route("/teacher")
def teacher_page():
    print("SESSION", session)
    teacher_id = session.get("id")
    if not teacher_id:
        return jsonify({"status": "error", "redirect": "/login"}), 401
    info = get_user_info(SERVER, teacher_id)

    return render_template(
        "teacher.html",
        id=teacher_id,
        name=info["first_name"] + " " + info["last_name"],
        course=get_course(SERVER, teacher_id),
        count_of_students=len(get_students_grades_emails(SERVER, teacher_id)),
    )


@app.route("/student")
def student_page():
    email = session.get("email")
    if not email:
        return jsonify({"status": "error", "redirect": "/login"}), 401

    s = Student(SERVER, email)
    return render_template("student.html", id=s._id, name=s._name, grades=s)


# Students Button
@app.route("/teacher/studentsInfo", methods=["GET"])
def students_info_button():
    if request.method == "GET":
        teacher_id = session.get("id")
        if teacher_id:
            course_id = get_course_id(SERVER, teacher_id)
            students_info = get_students_info(SERVER, course_id)

            return jsonify({"status": "success", "students": students_info}), 200
        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/studentsGrades", methods=["GET"])
def students_grades_button():
    if request.method == "GET":
        teacher_id = session.get("id")

        if teacher_id:
            students_list = get_students_grades_emails(SERVER, teacher_id)
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
        teacher_id = session.get("id")
        if teacher_id:
            data = request.json
            student_id = data.get("id")
            new_grade = data.get("grade")
            course_id = get_course_id(SERVER, teacher_id)
            update_grade_for_student(SERVER, student_id, course_id, new_grade)
            return jsonify({"message": f"The grade is {new_grade} now"}), 200
    return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/passedStudents", methods=["GET"])
def passed_the_test_button():
    if request.method == "GET":
        user_id = session.get("id")


# Assignmnet Button
@app.route("/teacher/assignments", methods=["GET"])
def assignments_button():
    if request.method == "GET":
        teacher_id = session.get("id")
        if teacher_id:
            assignments_list = get_assignments(SERVER, teacher_id)
            return jsonify({"assignments": assignments_list}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/Assignment/addAssignmnet", methods=["POST"])
def add_new_assignment():
    if request.method == "POST":
        teacher_id = session.get("id")
        if teacher_id:
            data = request.json
            add_assignment(SERVER, teacher_id, data)
            return jsonify({"message": "Assignment successfully added!"}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/Assignment/editAssignmnet", methods=["POST"])
def edit_assignmnet_button():
    if request.method == "POST":
        teacher_id = session.get("id")
        if teacher_id:
            data = request.json
            edit_assigmnet(SERVER, data, teacher_id)
            return jsonify({"message": "The assignment changed"}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@app.route("/teacher/Assignment/deleteAssignmnet", methods=["POST"])
def delete_assignment():
    if request.method == "POST":
        teacher_id = session.get("id")
        if teacher_id:
            data = request.json
            remove_assignmnet(SERVER, data)
            return jsonify({"message": "The assignment removed!"}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


# Profile Button
@app.route("/teacher/profile")
def profile():
    teacher_id = session.get("id")
    info = get_user_info(SERVER, teacher_id)

    if teacher_id:
        return jsonify({"info": info}), 200


@app.route("/teacher/profile/editPersonalInfo", methods=["PUT"])
def edit_personal_info():
    if request.method == "PUT":
        teacher_id = session.get("id")
        if teacher_id:
            data = request.json
            change_details(SERVER, teacher_id, data)
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


@app.route("/manager")
def manager_page():
    manager_id = session.get("id")
    if manager_id and get_role(SERVER, manager_id) == "manager":
        info = get_user_info(SERVER, manager_id)
        teachers = get_info_on_teachers(SERVER)
        return render_template(
            "manager.html",
            name=info["first_name"] + " " + info["last_name"],
            teachers=teachers,
        ), 200
    return render_template("error.html")


@app.route("/manager/deleteUser", methods=["PUT"])
def delete_user():
    if request.method == "PUT":
        manager_id = session.get("id")
        if get_role(SERVER, manager_id) == "manager":
            data = request.json
            teacher_id = data.get("teacherID")
            remove_teacher(SERVER, teacher_id)
            return jsonify({"message": "The user removed!"}), 200
        return jsonify({"message": "You are not the manager!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
