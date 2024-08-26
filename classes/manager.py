import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *



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
                    JOIN Grades ON Courses.id = Grades.course_id
                    GROUP BY Users.first_name, Users.last_name, Courses.[name], Users.email, Users.id
                """
    teachers_info = []
    with conn.cursor() as cursor:
        cursor.execute(query)
        for row in cursor:
            teacher_info_dict = {
                "id": row[0],
                "name": row[1],
                "course": row[2],
                "email": row[3],
                "number_of_students": row[4],
                "average_grade": row[5],
            }
            teachers_info.append(teacher_info_dict)
    return teachers_info


def get_all_students(conn: odbc.Connection) -> list[str]:
    query = """ SELECT 
                        Users.first_name + ' ' + Users.last_name AS 'Name'
                    FROM Users
                    WHERE Users.[role] = 'student'"""
    students_list = []
    with conn.cursor() as cursor:
        cursor.execute(query)
        for row in cursor:
            students_list.append(row)

    return students_list


def get_GPA_for_each_student(conn: odbc.Connection) -> dict[str, float]:
    query = """ SELECT
                        Users.first_name + ' ' + Users.last_name AS 'Name',
                        AVG(Grades.grade) As 'AVG'
                    FROM Users
                    JOIN Grades ON Users.id = Grades.student_id
                    GROUP BY Grades.student_id, Users.first_name, Users.last_name
                """
    GPA_dict = {}
    with conn.cursor() as cursor:
        cursor.execute(query)
        for row in cursor:
            GPA_dict[row[0]] = row[1]

    return GPA_dict


def remove_student(conn: odbc.Connection, student_id):
    delete_from_Grades_table = """ DELETE FROM 
                        Grades
                    WHERE Grades.student_id = ?;     
                """

    delete_from_Users_table = """ DELETE FROM 
                        Users
                    WHERE Users.id = ?;     
                """
    try:
        conn.autocommit = False
        with conn.cursor() as cursor:
            cursor.execute(delete_from_Grades_table, (student_id,))
            cursor.execute(delete_from_Users_table, (student_id,))
            conn.commit()

        print(f"Student with id {student_id} deleted successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()


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


def remove_teacher(conn: odbc.Connection, teacher_id) -> None:
    query = """DELETE FROM Users WHERE id = ?"""
    with conn.cursor() as cursor:
        cursor.execute(query, [teacher_id])
        conn.commit()
