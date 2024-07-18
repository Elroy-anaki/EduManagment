import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *
from utils import *

class User:
    def __init__(self, conn: odbc.Connection, email: str):
        self._id = get_id(conn, email)
        self._name = get_name(conn, email)
        
    @staticmethod    
    def _get_id(conn: odbc.Connection, email: str) -> int:
        query = """ SELECT
                        Users.id 
                    FROM Users 
                    WHERE Users.email = ?
                """
        with conn.cursor() as cursor:
            cursor.execute(query, [email])
            id = cursor.fetchone()
        return id[0] if id else None

    @staticmethod
    def _get_name(conn: odbc.Connection, email: str) -> str:
        query = """ SELECT
                        Users.first_name + ' ' + Users.last_name 
                    FROM Users 
                    WHERE Users.email = ?
                """
        with conn.cursor() as cursor:
            cursor.execute(query, [email])
            name = cursor.fetchone()
        return name[0] if name else None
    
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