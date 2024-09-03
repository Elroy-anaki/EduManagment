import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *


def x(n):
    if n == None:
        return "There are no students yet"
    return n


def get_info_on_courses(conn: odbc.Connection) -> list[dict]:
    query = """ SELECT * FROM Courses """
    courses = []
    with conn.cursor() as cursor:
        cursor.execute(query)
        for row in cursor:
            course = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
            }
            courses.append(course)
    return courses


def get_free_courses(conn: odbc.Connection) -> list:
    query = """ SELECT 
                    *
                FROM Courses
                WHERE Courses.id NOT IN ( SELECT Teachers_Courses.course_id FROM Teachers_Courses)
            """
    free_courses = []
    with conn.cursor() as cursor:
        cursor.execute(query)
        for row in cursor:
            course = {
                "id": row[0],
                "name": row[1],
                "title": row[2],
            }
            free_courses.append(course)
    return free_courses


def get_info_on_teachers(conn: odbc.Connection) -> list[dict]:
    query = """ SELECT 
                        Users.id,
                        Users.first_name + ' ' + Users.last_name,
                        Courses.[name],
                        Users.email,
                        COUNT(Grades.course_id),
                        AVG(Grades.grade)
                                            

                    FROM Users
                    JOIN Teachers_Courses ON Users.id =  Teachers_Courses.teacher_id
                    JOIN Courses ON Teachers_Courses.course_id = Courses.id
                    LEFT JOIN Grades ON Courses.id = Grades.course_id
                    GROUP BY Users.first_name, Users.last_name, Courses.[name], Users.email, Users.id
                """
    teachers_info = []
    with conn.cursor() as cursor:
        cursor.execute(query)
        for row in cursor:
            teacher = {
                "id": row[0],
                "name": row[1],
                "course": row[2],
                "email": row[3],
                "number_of_students": row[4],
                "average_grade": x(row[5]),
            }
            teachers_info.append(teacher)
    return teachers_info


def get_info_on_students(conn: odbc.Connection) -> list[dict]:
    query = """ SELECT 
                    Users.id,
                    Users.first_name + ' ' + Users.last_name,
                    Users.email,                    
                    AVG(Grades.grade),
                    COUNT(Grades.course_id)
                FROM Users
                JOIN Grades ON Users.id = Grades.student_id
                GROUP BY Users.id, Users.first_name, Users.last_name, Users.email
                ORDER BY AVG(Grades.grade) DESC
            """
    students_info = []
    with conn.cursor() as cursor:
        cursor.execute(query)
        for row in cursor:
            student = {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "GPA": row[3],
                "number_of_courses": row[4],
            }
            students_info.append(student)

    return students_info


def add_new_student(conn: odbc.Connection, student_info: object):
    query = """ INSERT INTO Users (first_name, last_name, email, password, gender, role)
                    VALUES (?, ?, ?, ?, ?, ?);
                """
    with conn.cursor() as cursor:
        cursor.execute(
            query,
            [
                student_info.first_name,
                student_info.last_name,
                student_info.email,
                student_info.password,
                student_info.gender,
                student_info.role,
            ],
        )
        conn.commit()


def remove_user(conn: odbc.Connection, user_id) -> None:
    query = """DELETE FROM Users WHERE id = ?"""
    with conn.cursor() as cursor:
        cursor.execute(query, [user_id])
        conn.commit()


def create_new_user(conn: odbc.Connection, user_data) -> int:
    query = """ INSERT INTO Users (first_name, last_name, age, phone, city, [role], email, [password])
                VALUES (?, ?, null, null, null, 'teacher', ?, 'EDUMANAGMENT') 
            """
    with conn.cursor() as cursor:
        cursor.execute(
            query, [user_data["firstName"], user_data["lastName"], user_data["email"]]
        )
        conn.commit()
        query = "SELECT IDENT_CURRENT('Users') AS LastInsertedID"
        cursor.execute(query)

        last_id = cursor.fetchone()[0]
    return last_id

def connect_student_to_courses(conn: odbc.Connection, student_id, course_id):
    query = """ INSERT INTO Grades(student_id, course_id, grade)
                VALUES (?, ?, 0)
            """
    with conn.cursor() as cursor:
        cursor.execute(query, [student_id, course_id])
        conn.commit()
    return None
        
def connect_teacher_to_course(conn: odbc.Connection, teacher_id, course_id) -> None:
    query = """ INSERT INTO Teachers_Courses (teacher_id, course_id)
                VALUES (?, ?)
            """
    with conn.cursor() as cursor:
        cursor.execute(query, [teacher_id, course_id])
        conn.commit()

    return None


def edit_course_description(conn: odbc.Connection, course_id, new_description) -> None:
    query = """ UPDATE 
                    Courses
                SET 
                    Courses.[description] = ?
                WHERE Courses.id = ?
            """
    with conn.cursor() as cursor:
        cursor.execute(query, [new_description, course_id])
        conn.commit()
    return None


def create_new_course(conn: odbc.Connection, name, description) -> None:
    query = """ INSERT INTO Courses ([name], [description])
                VALUES(?, ?)
            """
    with conn.cursor() as cursor:
        cursor.execute(query, [name, description])
        conn.commit()
    return None


def get_user_grade_by_name_and_course(conn: odbc.Connection, name, course_id) -> dict:
    query = """ SELECT 
                    Users.id,
                    first_name + ' ' + Users.last_name AS 'Name',
                    Users.email,                    
                    Grades.grade
                FROM Users
                JOIN Grades ON Users.id = Grades.student_id
                WHERE Grades.course_id = ? and first_name + ' ' + Users.last_name = ?
            """
    with conn.cursor() as curosr:
        curosr.execute(query, [course_id, name])
        student = {}
        for row in curosr:
            student["id"] = row[0]
            student["name"] = row[1]
            student["email"] = row[2]
            student["grade"] = row[3]
    return student
