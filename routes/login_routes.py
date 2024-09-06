from __init__ import *
from flask import Blueprint, g


login_bp = Blueprint("login", __name__)

@login_bp.route("/")
def home_page():
    return render_template("home.html")

@login_bp.route("/login")
def login():
    session.clear()
    return render_template("login.html")


@login_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return (
            jsonify({"status": "error", "message": "Email and Password are required"}),
            401,
        )

    if not does_email_exist(g.db, email):
        return jsonify({"status": "error", "message": "This email doesn't exist!"}), 401

    if not is_correct_password(g.db, email, password):
        return jsonify({"status": "error", "message": "Incorrect password"}), 401

    user_id = get_id(g.db, email)
    role = get_role(g.db, user_id)
    session["id"] = user_id

    if role == "student":
        return jsonify({"status": "success", "redirect": "/student"}), 200

    elif role == "teacher":
        return jsonify({"status": "success", "redirect": "/teacher"}), 200

    elif role == "manager":
        session["role"] = "manager"
        return jsonify({"status": "success", "redirect": "/manager"}), 200


@login_bp.route("/logout")
def logout():
    session.clear()
    return jsonify({"redirect": "/login"}), 200
