import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSOWRD")
host = os.getenv("DB_HOST")
name = os.getenv("DB_NAME")

db = mysql.connector.connect(
    user=user, password=password, host=host, database=name)

#cursor = db.cursor() lo borré porque es mejor abrir el cursor dentro de cada función que involucre la bd


