import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *
from utils import *


class User:
    def __init__(self, conn: odbc.Connection, user_id):
        self.info = get_user_info(conn, user_id)

    
    
