#funciones de administrador

import hashlib
import sys 
import os
from dotenv import load_dotenv
load_dotenv()
#importamos el archivo db.py correspondiente a la conexion de la bd
path = os.getenv("PATH_DB")
sys.path.append(path)
  

from db import *

def login_admin(user_name, password): 
   #establecemos un cursor             
    cur = db.cursor()
    #sentencia sql para hacer la consulta
    sql = "SELECT * FROM administrador WHERE nombre_usuario=%s AND contrasena=SHA2(%s,256)"
    cur.execute(sql,(user_name,password))
    #obtenemos los registros
    admin = cur.fetchall()
    #cerramos la conexion
    cur.close()
    #devolvemos los registros
    return admin