import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *
from utils import *


class Teacher:
    def __init__(self, conn: odbc.Connection, email: str):
        self._id = get_id(conn, email)
        self._name = get_name(conn, email)
        self._course = self.get_course(conn)
        self._students = self.get_students_list(conn)

    def __repr__(self) -> str:
        return f"{self._name}\nCourse: {self._course}"



    def get_course(self, conn: odbc.Connection) -> None:
        query = """ SELECT 
                        Teachers.course
                    FROM Teachers
                    JOIN Users ON Teachers.id = Users.id
                    WHERE Users.id = ?;
                """
        with conn.cursor() as cursor:
            cursor.execute(query, [self._id])
            course = cursor.fetchone()[0]
        return course

    def get_students_list(self, conn: odbc.Connection) -> list[object]:
        query = """ SELECT
                        Users.first_name + ' ' + Users.last_name AS 'Name',
                        Grades.grade AS Grade
                    FROM
                        Users
                    JOIN Grades ON Users.id = Grades.student_id
                    JOIN Teachers ON Grades.teacher_id = Teachers.id
                    WHERE Teachers.id = ?
                    ORDER BY Grade DESC;
                """
        students_list = []
        with conn.cursor() as cursor:
            cursor.execute(query, [self._id])
            for row in cursor:
                s = StudentForTeacher(row[0], row[1])
                students_list.append(s)
        return students_list

    def get_students_with_passing_grades(self) -> list[object]:
        passed_test_students = []
        for student in self._students:
            if student.grade > 70:
                passed_test_students.append(student)
        return sorted(passed_test_students)

    def change_password(self, conn, new_password: str):
        query = """ UPDATE 
                        Users 
                    SET [password] = ? 
                    WHERE Users.id = ?;
                """
        cursor = conn.cursor()
        cursor.execute(query, [new_password, self._id])
        conn.commit()
        cursor.close()


class StudentForTeacher:
    def __init__(self, name: str, grade: float):
        self.name = name
        self.grade = grade

    def __repr__(self) -> str:
        return f"{self.name} - {self.grade}"
