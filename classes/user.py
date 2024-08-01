import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *
from utils import *


class User:
    def __init__(self, conn: odbc.Connection, email: str, password: str):
        self.info = get_user_info(conn, email, password)

    
    def change_detail(self, conn, key: str, value:any):
        query = f""" UPDATE 
                        Users 
                    SET {key} = ? 
                    WHERE Users.id = ?;
                """
        cursor = conn.cursor()
        cursor.execute(query, [value, self.info['id']])
        conn.commit()
        cursor.close()
