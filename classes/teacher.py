import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *
from classes.user import User


class Teacher(User):
    def __init__(self, conn: odbc.Connection, user_id):
        super().__init__(conn, user_id)
        self._course = self.get_course(conn)
        self._students = self.get_students_grades_emails(conn)

    def get_course(self, conn: odbc.Connection) -> str:
        query = """ SELECT 
                        Teachers.course
                    FROM Teachers
                    JOIN Users ON Teachers.id = Users.id
                    WHERE Users.id = ?;
                """
        with conn.cursor() as cursor:
            cursor.execute(query, [self.info["id"]])
            course = cursor.fetchone()[0]
        return course

    def get_students_info(self, conn: odbc.Connection) -> list[dict]:
        query = """ SELECT 
                        Users.first_name + ' ' + Users.last_name,
                        Users.age,
                        Users.phone,
                        Users.city,
                        Users.gender
                    FROM Users
                    JOIN Grades ON Users.id = Grades.student_id
                    WHERE Grades.teacher_id = ?
                """
        students_info = []
        with conn.cursor() as cursor:
            cursor.execute(query, [self.info["id"]])
            for row in cursor:
                student = {
                    "name": row[0],
                    "age": row[1],
                    "phone": row[2],
                    "city": row[3],
                    "gender": row[4],
                }
                students_info.append(student)
        return students_info

    def get_students_grades_emails(self, conn: odbc.Connection) -> list[dict]:
        query = """ SELECT
                        Users.id AS ID,
                        Users.first_name + ' ' + Users.last_name AS 'Name',
                        Grades.grade AS Grade,
                        Users.email
                    FROM
                        Users
                    JOIN Grades ON Users.id = Grades.student_id
                    JOIN Teachers ON Grades.teacher_id = Teachers.id
                    WHERE Teachers.id = ?
                    ORDER BY Grade DESC;
                """
        students_list = []
        with conn.cursor() as cursor:
            cursor.execute(query, [self.info["id"]])
            for row in cursor:
                student_dict = {
                    "id": row[0],
                    "name": row[1],
                    "grade": row[2],
                    "email": row[3],
                }
                students_list.append(student_dict)
        return students_list

    def get_students_with_passing_grades(self) -> list[dict]:
        passed_test_students = []
        for student in self._students:
            if student["grade"] > 70:
                passed_test_students.append(student)
        return passed_test_students

    def update_grade_for_student(
        self, conn: odbc.Connection, student_id: int, grade: float
    ):
        query = """ UPDATE
                        Grades
                    SET
                        Grades.grade = ?
                    WHERE Grades.student_id = ?  and Grades.teacher_id = ?;
                           
                """
        cursor = conn.cursor()
        cursor.execute(query, [grade, student_id, self.info["id"]])
        conn.commit()
        cursor.close()

    def get_assignments(self, conn: odbc.Connection) -> list[dict]:
        query = """ SELECT 
                        Users.first_name + ' ' + Users.last_name,
                        Assignments.id,
                        Assignments.title,
                        Assignments.description
                    FROM Teachers
                    JOIN Assignments ON Teachers.id = Assignments.teacher_id
                    JOIN Users ON Assignments.teacher_id = Users.id
                    WHERE Teachers.id = ?
                """
        assignments_list = []
        with conn.cursor() as cursor:
            cursor.execute(query, [self.info["id"]])
            for row in cursor:
                assignment_dict = {
                    "name": row[0],
                    "id": row[1],
                    "title": row[2],
                    "description": row[3]
                }
                assignments_list.append(assignment_dict)
        return assignments_list
               
    def add_assignment(self, conn: odbc.Connection, data: dict[str]):
        query = """ INSERT INTO Assignments (teacher_id, title, [description])
                    VALUES (?, ?, ?)
                """
        with conn.cursor() as cursor:
            cursor.execute(query, [self.info["id"], data["title"], data["description"]])
            conn.commit()
    
    def edit_assigmnet(self, conn: odbc.Connection, data: dict[str]):
        query = """ UPDATE
                        Assignments
                    SET
                        title = ?,
                        [description] = ?
                    WHERE id = ? and teacher_id = ?
                """    
        with conn.cursor() as cursor:
            cursor.execute(query, [data["title"], data["description"], data["id"], self.info["id"]])
            conn.commit()
        
    def remove_assignmnet(self, conn: odbc.Connection, data: dict[int]):
        query = """ DELETE FROM Assignments 
                    WHERE id = ? 
                """
        with conn.cursor() as cursor:
            cursor.execute(query, [data["id"]])
            conn.commit()
            
