from utils import *


def create_user(conn: odbc.Connection, email: str, password: str) -> object:
    global ROLE_CLASSES
    while not is_login_successful(conn, email, password):
        email = input("Enter Email: ")
        password = input("Enter Password: ")
    role = get_role(conn, email)
    return ROLE_CLASSES[role](conn, email)


SERVER = connect_server()
ROLE_CLASSES = {"student": Student, "teacher": Teacher}
user_email = input("Enter Email: ")
user_password = input("Enter Password: ")
user = create_user(SERVER, user_email, user_password)
for student in user._students:
    print(student)
user.change_password(SERVER, "123456abc")
