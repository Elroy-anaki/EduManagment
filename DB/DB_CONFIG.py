import pypyodbc as odbc
import os
from dotenv import load_dotenv

load_dotenv()


def connect_server():
    """This function connects to the database"""
    DRIVER_NAME = os.getenv("DRIVER_NAME")
    SERVER_NAME = os.getenv("SERVER_NAME")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    connection_string = f"""
                DRIVER={{{DRIVER_NAME}}};
                SERVER={SERVER_NAME};
                DATABASE={DATABASE_NAME};
                Trust_Connection=yes;
                "ConnectionPooling=True;"
                "Max Pool Size=20;"

        """
    conn = odbc.connect(connection_string)
    return conn
