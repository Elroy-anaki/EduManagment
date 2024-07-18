import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *
from classes.user import User


class Student(User):
    def __init__(self, conn: odbc.Connection, email: str) -> None:
        super().__init__(conn, email)
        self._courses_and_grades = self.get_grades(conn)
        self.GPA = self.calculate_GPA()

    def __repr__(self) -> str:
        return f"{self._name}\nGrades {self._courses_and_grades}"

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

    def calculate_GPA(self) -> float:
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
