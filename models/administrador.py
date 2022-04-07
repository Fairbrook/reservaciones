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
#funcion para realizar consulta a la base de datos
def consulta_BD(nombre_columna, valor): 
   #establecemos un cursor             
    cur = db.cursor()
    #sentencia sql para hacer la consulta
    sql = "SELECT * FROM administrador WHERE {} = '{}'".format(nombre_columna, valor)
    cur.execute(sql)
    #obtenemos los registros
    admin = cur.fetchall()
    #cerramos la conexion
    cur.close()
    #devolvemos los registros
    return admin

