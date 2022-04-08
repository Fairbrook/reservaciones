from tkinter import *
import os
import sys
#from platillo import *

  
# setting path
sys.path.append('../')
from db import db

# Funcion para registrar usuario
def register(user_name, password):
    # Comprobación que el nombre de usuario es único
    query = "SELECT * FROM usuario WHERE nombre_usuario=%s LIMIT 1"
    cursor = db.cursor()
    cursor.execute(query, (user_name,))
    if len(list(cursor)) > 0:
        return (True, 'El nombre de usuario se encuentra en uso')
    query = "INSERT INTO usuario (nombre_usuario, contrasena) VALUES (%s,SHA2(%s,256))"
    cursor = db.cursor()
    cursor.execute(query, (user_name, password))
    db.commit()
    cursor.close()
    return (False, '')


    
# Función para inicio de sesión de usuario
def login(user_name, password):
    # Se comprueba que exista el usuario con el nombre y contraseña especificados
    query = "SELECT id_cliente, nombre_personal, nombre_usuario, correo FROM usuario WHERE nombre_usuario=%s AND contrasena=SHA2(%s,256)"
    cursor = db.cursor()
    cursor.execute(query, (user_name, password))
    users = list(cursor)
    user = None
    # Si existe, se le da formato como diccionario
    if len(users) > 0:
        (id_cliente, nombre_personal, nombre_usuario, correo) = users[0]
        user = {
            "id_cliente": id_cliente,
            "nombre_personal":nombre_personal,
            "nombre_usuario": nombre_usuario,
            "correo": correo
        }
    cursor.close()
    return user