import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *


def get_role(conn: odbc.Connection, email: str) -> str:
    query = """ SELECT 
                    Users.role 
                FROM Users 
                WHERE Users.email = ?
            """
    cursor = conn.cursor()
    cursor.execute(query, [email])
    role = cursor.fetchone()
    cursor.close()
    return role[0] if role else None


def get_all_emails(conn: odbc.Connection) -> list[str]:
    query = """ SELECT 
                    Users.email 
                FROM Users
            """
    cursor = conn.cursor()
    cursor.execute(query)
    emails_list = [row[0] for row in cursor.fetchall()]
    cursor.close()

    return emails_list


def does_email_exist(conn: odbc.Connection, email: str) -> bool:
    emails = get_all_emails(conn)

    return email in emails


def get_password(conn: odbc.Connection, email: str) -> str:
    query = """ SELECT Users.[password]
                FROM Users
                WHERE Users.email = ?;
            """
    cursor = conn.cursor()
    cursor.execute(query, [email])
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None


def is_correct_password(conn: odbc.Connection, email: str, password: str) -> bool:
    correct_password = get_password(conn, email)

    return password == correct_password


def is_login_successful(conn: odbc.Connection, email: str, password: str) -> bool:
    if not does_email_exist(conn, email):
        print("This email doesn't exist!")
        return False

    if not is_correct_password(conn, email, password):
        print("Incorrect paswword")
        return False

    return True


def get_id(conn: odbc.Connection, email: str) -> int:
    query = """ SELECT
                    Users.id 
                FROM Users 
                WHERE Users.email = ?
            """
    with conn.cursor() as cursor:
        cursor.execute(query, [email])
        id = cursor.fetchone()
    return id[0] if id else None


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
