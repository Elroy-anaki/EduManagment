import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *


class Student:
    def __init__(self, conn: odbc.Connection, email: str) -> None:
        self._id = self.get_id(conn, email)
        self._name = self.get_name(conn, email)
        self._courses_and_grades = self.get_grades(conn)

    @staticmethod
    def get_id(conn: odbc.Connection, email: str) -> int:
        query = """SELECT Users.id FROM Users WHERE Users.email = ?"""
        cursor = conn.cursor()
        cursor.execute(query, [email])
        id = cursor.fetchone()
        cursor.close()
        return id[0] if id else None

    @staticmethod
    def get_name(conn: odbc.Connection, email: str) -> str:
        query = """SELECT Users.first_name + ' ' + Users.last_name FROM Users WHERE Users.email = ?"""
        cursor = conn.cursor()
        cursor.execute(query, [email])
        name = cursor.fetchone()
        cursor.close()
        return name[0] if name else None

    def __repr__(self) -> str:
        return f"{self._name}\nGrades {self._courses_and_grades}"

    def change_password(self, conn: odbc.Connection, new_password: str):
        query = "UPDATE Users SET [password] = ? WHERE Users.id = ?;"
        cursor = conn.cursor()
        cursor.execute(query, [new_password, self._id])
        conn.commit()
        cursor.close()

    def get_grades(self, conn: odbc.Connection):
        query = """ SELECT Teachers.course,  Grades.grade
                    FROM Teachers
                    JOIN Grades ON Teachers.id = Grades.teacher_id
                    WHERE Grades.student_id = ?;
                """
        cursor = conn.cursor()
        cursor.execute(query, [self._id])
        grades_dict = {}
        for row in cursor:
            grades_dict[row[0]] = row[1]
        cursor.close()

        return grades_dict

    def get_GPA(self) -> float:
        sum_grades = 0
        for course in self._courses_and_grades:
            sum_grades += self._courses_and_grades[course]

        return round(sum_grades / len(self._courses_and_grades), 2)

    def get_teachers_details(self, conn: odbc.Connection) -> None:
        query = """ SELECT
                        Teachers.course AS 'Course',
                        Users.first_name + ' ' + Users.last_name AS 'Name',
                        Users.email AS 'Email'
                    FROM Users
                    JOIN Teachers ON Users.id = Teachers.id
                    JOIN Grades ON Teachers.id = Grades.teacher_id
                    WHERE Grades.student_id = ?;
                """
        cursor = conn.cursor()
        cursor.execute(query, [self._id])
        for row in cursor:
            print(row)
        cursor.close()
