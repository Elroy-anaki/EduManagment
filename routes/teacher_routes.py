from flask import Blueprint, render_template, request, session, jsonify
from utils import *
from services.teacher import *
 

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route("/teacher")
def teacher_page():
    teacher_id = session.get("id")
    db = connect_server()
    if not teacher_id or get_role(db, teacher_id) != "teacher":
        return "You are not a teacher!", 401

    teacher = Teacher(teacher_id)
    info = get_user_info(db, teacher_id)

    return render_template(
        "teacher.html",
        id=teacher_id,
        name=info["first_name"] + " " + info["last_name"],
        course=teacher.get_course(db),
        count_of_students=len(teacher.get_students_grades_emails(db)),
    )

@teacher_bp.route("/teacher/studentsInfo", methods=["GET"])
def students_info_button():
    if request.method == "GET":
        teacher_id = session.get("id")
        if teacher_id:
            db = connect_server()
            teacher = Teacher(teacher_id)
            students_info = teacher.get_students_info(db)

            return jsonify({"status": "success", "students": students_info}), 200
        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@teacher_bp.route("/teacher/studentsGrades", methods=["GET"])
def students_grades_button():
    if request.method == "GET":
        teacher_id = session.get("id")

        if teacher_id:
            db = connect_server()
            teacher = Teacher(teacher_id)
            students_list = teacher.get_students_grades_emails(db)
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

@teacher_bp.route("/editGrade", methods=["PUT"])
def edit_grade():
    if request.method == "PUT":
        teacher_id = session.get("id")
        if teacher_id:
            data = request.json
            student_id = data.get("id")
            new_grade = data.get("grade")
            teacher = Teacher(teacher_id)
            db = connect_server()
            teacher.update_grade_for_student(db, student_id, new_grade)
            return jsonify({"message": f"The grade is {new_grade} now"}), 200
    return jsonify({"status": "error", "message": "Unauthorized"}), 401


@teacher_bp.route("/teacher/passedStudents", methods=["GET"])
def passed_the_test_button():
    pass


# Assignmnet Button
@teacher_bp.route("/teacher/assignments", methods=["GET"])
def assignments_button():
    if request.method == "GET":
        teacher_id = session.get("id")
        if teacher_id:
            db = connect_server()
            teacher = Teacher(teacher_id)
            assignments_list = teacher.get_assignments(db)
            return jsonify({"assignments": assignments_list}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@teacher_bp.route("/teacher/Assignment/addAssignmnet", methods=["POST"])
def add_new_assignment():
    if request.method == "POST":
        teacher_id = session.get("id")
        if teacher_id:
            data = request.json
            teacher = Teacher(teacher_id)
            db = connect_server()
            teacher.add_assignment(db, data)
            return jsonify({"message": "Assignment successfully added!"}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@teacher_bp.route("/teacher/Assignment/editAssignmnet", methods=["POST"])
def edit_assignmnet_button():
    if request.method == "POST":
        teacher_id = session.get("id")
        if teacher_id:
            data = request.json
            teacher = Teacher(teacher_id)
            db = connect_server()
            teacher.edit_assigmnet(db, data)
            return jsonify({"message": "The assignment changed"}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


@teacher_bp.route("/teacher/Assignment/deleteAssignmnet", methods=["POST"])
def delete_assignment():
    if request.method == "POST":
        teacher_id = session.get("id")
        if teacher_id:
            data = request.json
            teacher = Teacher(teacher_id)
            db = connect_server()
            teacher.remove_assignmnet(db, data)
            return jsonify({"message": "The assignment removed!"}), 200

        return jsonify({"status": "error", "message": "Unauthorized"}), 401


# Profile Button
@teacher_bp.route("/teacher/profile")
def profile():
    teacher_id = session.get("id")
    db = connect_server()
    info = get_user_info(db, teacher_id)

    if teacher_id:
        return jsonify({"info": info}), 200


@teacher_bp.route("/teacher/profile/editPersonalInfo", methods=["PUT"])
def edit_personal_info():
    if request.method == "PUT":
        teacher_id = session.get("id")
        if teacher_id:
            data = request.json
            db = connect_server()
            change_details(db, teacher_id, data)
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
