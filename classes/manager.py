import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *
from classes.teacher import Teacher


class Manager:
    def __init__(self, conn: odbc.Connection, email: str) -> None:
        self.name = self.get_name(conn, email)
        self.teachers = self.get_teachers(conn)
        self.students = self.get_all_students(conn)
        self.GPA = self.get_GPA_for_each_student(conn)

    def __repr__(self) -> str:
        return f"{self.name}"

    @staticmethod
    def get_name(conn: odbc.Connection, email: str) -> str:
        query = """ SELECT
                        Users.first_name + ' ' + Users.last_name 
                    FROM Users 
                    WHERE Users.email = ?
                """
        with conn.cursor() as cursor:
            cursor.execute(query, [email])
            name = cursor.fetchone()
        return name[0] if name else None

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
                print(row)

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
        
