from flask import Blueprint, render_template, request, session, jsonify, g, redirect, url_for
from utils import *
from services.manager import *

manager_bp = Blueprint("manager", __name__)


@manager_bp.route("/manager")
def manager_page():
    user_id = session.get("id")
    if session.get("role") == "manager":

        info = get_user_info(g.db, user_id)
        return (
            render_template(
                "manager.html",
                name=info["first_name"] + " " + info["last_name"],
                teachers=get_info_on_teachers(g.db),
                all_courses=get_info_on_courses(g.db),
                free_courses=get_free_courses(g.db),
                students=get_info_on_students(g.db),
            ),
            200,
        )
    return "You are not a manager!", 401


@manager_bp.route("/manager/deleteUser", methods=["PUT"])
def delete_user():
    if request.method == "PUT":
        manager_id = session.get("id")
        if get_role(g.db, manager_id) == "manager":
            data = request.json
            user_id = data.get("userID")
            remove_user(g.db, user_id)
            return jsonify({"message": "Deleted successfully"}), 200
        return jsonify({"message": "You are not the manager!"})


@manager_bp.route("/manager/AddTeacher", methods=["PUT"])
def add_teacher():
    if request.method == "PUT":
        data = request.json
        new_user_id = create_new_user(g.db, data)
        connect_teacher_to_course(g.db, new_user_id, data["courseID"]), 200
        return jsonify({"message": "OK", "redirect": "/manager"})

    return jsonify({"message": "NOT OK"}), 401


@manager_bp.route("/manager/courses/updateDescription", methods=["PUT"])
def save_description():
    if request.method == "PUT":
        data = request.json
        edit_course_description(g.db, data["courseID"], data["description"])
        return jsonify({"message": "The course's description changed!"}), 200
    return render_template("error.html")


@manager_bp.route("/manager/courses/addNewCourses", methods=["PUT"])
def save_new_course():
    if request.method != "PUT":
        return jsonify({"message": "Invalid request"}), 401
    if get_role(g.db, session["id"]) != "manager":
        return render_template("error.html")

    data = request.json
    create_new_course(g.db, data["name"], data["description"])
    return jsonify({"message": "New Course Added!"}), 200


@manager_bp.route("/manager/students/allStudents", methods=["GET"])
def get_all_students():
    if request.method != "GET":
        return jsonify({"message": "Invalid request"}), 401
    manager_id = session.get("id")
    if get_role(g.db, manager_id) != "manager":
        return "you are not the manager", 401

    students = get_info_on_students(g.db)
    return jsonify({"students": students}), 200


@manager_bp.route("/manager/students/getGrade", methods=["POST"])
def get_student():
    if request.method != "POST":
        return render_template("error.html")
    data = request.json
    return jsonify(
        {
            "student": get_user_grade_by_name_and_course(
                g.db, data.get("name"), data.get("courseID")
            )
        }
    )


@manager_bp.route("/manager/AddStudent", methods=["POST"])
def add_student():
    print("Received a POST request")
    if request.method == "POST":
        data = {
            "firstName": request.form.get("first_name"),
            "lastName": request.form.get("last_name"),
            "email": request.form.get("email"),
        }
        selected_courses = request.form.getlist("courses")
    
    new_user_id = create_new_user(g.db, data)
    for i in range(len(selected_courses)):
        connect_student_to_courses(g.db, new_user_id, selected_courses[i])
    
    return redirect(url_for('manager.manager_page'))
    
