import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *
from classes.user import User
from classes.teacher import Teacher


class Manager(User):
    def __init__(self, conn: odbc.Connection, email: str) -> None:
        super().__init__(conn, email)
        self.teachers = self.get_teachers(conn)
        self.students = self.get_all_students(conn)
        self.GPA = self.get_GPA_for_each_student(conn)

    @staticmethod
    def get_teachers(conn: odbc.Connection) -> dict[str, str]:
        query = """ SELECT 
                        Users.first_name + ' ' + Users.last_name AS 'Name',
                        Teachers.course AS Course
                    FROM Users
                    JOIN Teachers ON Users.id = Teachers.id
                """
        teachers_dict = {}
        with conn.cursor() as cursor:
            cursor.execute(query)
            for row in cursor:
                teachers_dict[row[0]] = row[1]

        return teachers_dict

    @staticmethod
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

    def get_teachers_and_their_grades(self, conn: odbc.Connection) -> list[object]:
        query = """ SELECT 
                        Users.email AS Email
                    FROM Users
                    JOIN Teachers ON Users.id = Teachers.id
                """
        teachers_list = []
        with conn.cursor() as cursor:
            cursor.execute(query)
            emails = [row[0] for row in cursor.fetchall()]

        for email in emails:
            with connect_server() as new_conn:
                t = Teacher(new_conn, email)
                teachers_list.append(t)
        return teachers_list

    @staticmethod
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

    def best_student(self):
        values = list(self.GPA.values())
        keys = list(self.GPA.keys())
        best_student = keys[values.index(max(values))]
        return f"The best student is: {best_student}\nGPA: {self.GPA[best_student]}."

    def worst_student(self):
        values = list(self.GPA.values())
        keys = list(self.GPA.keys())
        worst_student = keys[values.index(min(values))]
        return f"The worst student is: {worst_student}\nGPA: {self.GPA[worst_student]}."

    def remove_student(self, conn: odbc.Connection, student_id):
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

        self.students = self.get_all_students(conn)

    def add_new_student(self, conn: odbc.Connection, student_info: object):
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

        self.students = self.get_all_students(conn)

    def add_new_teacher(self, conn: odbc.Connection, teacher_info: object):
        insert_into_Users_table = """ INSERT INTO Users (first_name, last_name, email, password, gender, role)
                                      VALUES (?, ?, ?, ?, ?, ?);
                                  """
        insert_into_Teacher_table = """ INSERT INTO Teachers (id, course)
                                        VALUES (?, ?);
                                    """
        try:
            conn.autocommit = False
            with conn.cursor() as cursor:
                cursor.execute(
                    insert_into_Users_table,
                    [
                        teacher_info.first_name,
                        teacher_info.last_name,
                        teacher_info.email,
                        teacher_info.password,
                        teacher_info.gender,
                        teacher_info.role,
                    ],
                )
                cursor.execute("SELECT @@IDENTITY AS new_id;")
                teacher_id = cursor.fetchone()["new_id"]
                cursor.execute(
                    insert_into_Teacher_table, [teacher_id, teacher_info.course]
                )
                conn.commit()

        except Exception as e:
            print(f"Error occurred: {e}")
            conn.rollback()

        self.teachers = self.get_teachers(conn)

    def analyze_the_teachers(self, conn: odbc.Connection):
        query = """ SELECT
                        Users.first_name + ' ' + Users.last_name AS 'Name',
                        AVG(Grades.grade) AS 'AVG'
                    FROM Grades
                    LEFT JOIN Users ON Grades.teacher_id = Users.id
                    GROUP BY Users.first_name, Users.last_name;
                """
        teachers_GPA_dict = {}
        with conn.cursor() as cursor:
            cursor.execute(query)
            for row in cursor:
                teachers_GPA_dict[row[0]] = row[1]

        return teachers_GPA_dict


class NewStudent:
    def __init__(self, first_name, last_name, email, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = "abcd12345"
        self.gender = gender
        self.role = "student"


class NewTeacher:
    def __init__(self, first_name, last_name, email, gender, course):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = "abcd12345"
        self.gender = gender
        self.role = "teacher"
        self.course = course
