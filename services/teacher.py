import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *

class Teacher:
    def __init__(self, id) -> None:
        self._id = id
        

    def get_course(self, conn: odbc.Connection) -> str:
        query = """ SELECT 
                            Courses.[name]

                        FROM Courses
                        JOIN Teachers_Courses ON Courses.id = Teachers_Courses.course_id
                        JOIN Users ON Teachers_Courses.teacher_id = Users.id
                        WHERE Teachers_Courses.teacher_id = ?;
                    """
        with conn.cursor() as cursor:
            cursor.execute(query, [self._id])
            course = cursor.fetchone()[0]
        return course


    def get_course_id(self, conn: odbc.Connection) -> int:
        query = """ SELECT 
                            Teachers_Courses.course_id
                        FROM Teachers_Courses
                        WHERE Teachers_Courses.teacher_id = ?
                    """
        with conn.cursor() as cursor:
            cursor.execute(query, [self._id])
            course_id = cursor.fetchone()[0]
        return course_id


    def get_students_info(self, conn: odbc.Connection) -> list[dict]:
        query = """ SELECT 
                            Users.first_name + ' ' + Users.last_name,
                            Users.age,
                            Users.phone,
                            Users.city,
                            Users.gender
                        FROM Users
                        JOIN Grades ON Users.id = Grades.student_id
                        WHERE Grades.course_id = ?
                    """
        students_info = []
        with conn.cursor() as cursor:
            cursor.execute(query, [self.get_course_id(conn)])
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
                            Users.id AS ID, Users.first_name + ' ' + Users.last_name AS 'Name', 
                            Grades.grade AS Grade, Users.email 
                        FROM Users 
                        JOIN Grades ON Users.id = Grades.student_id 
                        JOIN Courses ON Grades.course_id = Courses.id 
                        JOIN Teachers_Courses ON Courses.id = Teachers_Courses.course_id 
                        WHERE Teachers_Courses.teacher_id = ?
                        ORDER BY Grade DESC;
                    """
        students_list = []
        with conn.cursor() as cursor:
            cursor.execute(query, [self._id])
            for row in cursor:
                student_dict = {
                    "id": row[0],
                    "name": row[1],
                    "grade": row[2],
                    "email": row[3],
                }
                students_list.append(student_dict)
        return students_list


    def update_grade_for_student(
        self, conn: odbc.Connection, student_id: int, grade: float
    ):

        query = """ UPDATE
                            Grades
                        SET
                            Grades.grade = ?
                        FROM Grades
                        WHERE Grades.student_id = ?  and Grades.course_id = ?;
                            
                    """
        
        cursor = conn.cursor()
        cursor.execute(query, [grade, student_id, self.get_course_id(conn)])
        conn.commit()
        cursor.close()


    def get_assignments(self, conn: odbc.Connection) -> list[dict]:
        query = """ SELECT 
                            Users.first_name + ' ' + Users.last_name,
                            Assignments.id,
                            Assignments.title,
                            Assignments.description
                        FROM Teachers_Courses
                        JOIN Assignments ON Teachers_Courses.teacher_id = Assignments.teacher_id
                        JOIN Users ON Assignments.teacher_id = Users.id
                        WHERE Teachers_Courses.teacher_id = ?
                    """
        assignments_list = []
        with conn.cursor() as cursor:
            cursor.execute(query, [self._id])
            for row in cursor:
                assignment_dict = {
                    "name": row[0],
                    "id": row[1],
                    "title": row[2],
                    "description": row[3],
                }
                assignments_list.append(assignment_dict)
        return assignments_list


    def add_assignment(self, conn: odbc.Connection, data: dict[str]):
        query = """ INSERT INTO Assignments (teacher_id, title, [description])
                        VALUES (?, ?, ?)
                    """
        with conn.cursor() as cursor:
            cursor.execute(query, [self._id, data["title"], data["description"]])
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
            cursor.execute(query, [data["title"], data["description"], data["id"], self._id])
            conn.commit()


    def remove_assignmnet(self, conn: odbc.Connection, data: dict[int]):
        query = """ DELETE FROM Assignments 
                        WHERE id = ? 
                    """
        with conn.cursor() as cursor:
            cursor.execute(query, [data["id"]])
            conn.commit()
