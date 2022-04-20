#funciones de administrador

import hashlib
import sys 
import os
from tkinter import *
from tkinter import messagebox
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

def ver_calificaciones_admin():
   
   global pantalla_ver_cal

   pantalla_ver_cal = Toplevel()
   pantalla_ver_cal.geometry("700x500")
   pantalla_ver_cal.title("Reseñas")

   main_frame = Frame(pantalla_ver_cal, bg="white")
   main_frame.pack(fill=BOTH, expand=1)

   my_canvas = Canvas(main_frame, bg="white")
   my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

   my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
   my_scrollbar.pack(side=RIGHT, fill=Y)

   my_canvas.configure(yscrollcommand=my_scrollbar.set)
   my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

   second_frame = Frame(my_canvas, bg= "white")
   
   my_canvas.create_window((0,0), window=second_frame, anchor="nw")

   #Queremos saber cual es el promedio actual de calificaciones
   cursor = db.cursor()
   sql_promedio = "SELECT AVG(calificacion) from resena"
   cursor.execute(sql_promedio)
   promedio = cursor.fetchone()[0]
   color = None

   #Dependiendo qué tan alta o baja sea la calificación, la desplegaremos en pantalla con color diferente
   if promedio >= 0.0 and promedio <= 2.0:
      color = "red"
   elif promedio >= 2.1 and promedio <= 3.9:
      color = "yellow"
   elif promedio >= 4.0 and promedio <= 5.0:
      color = "green"

   Label(second_frame, text = "Calificaciones y opiniones", font=("Arial, 15"), bg="white").grid(column=0, row=0, padx=100, pady=5)
   Label(second_frame, text ="Promedio: {}".format(promedio), font=("Arial", 25), bg="white", fg=color).grid(column=0, row=1, padx=100, pady=5)

   #Traemos una lista de todas las reseñas registradas
   
   sql_get_resenas = '''select id_cliente, calificacion, Date_format(fecha_calificacion, '%d/%m/%Y'), comentario
   from resena'''
   cursor.execute(sql_get_resenas)
   lista_resenas = cursor.fetchall()

   row = 2 #Comenzamos el conteo de filas desde 2

   #Por cada reseña, desglosamos datos
   for resena in lista_resenas:

      id_cliente = resena[0]
      calificacion = resena[1]
      fecha = resena[2]
      comentario = resena[3]
      #También queremos que se vea el nombre del usuario que hizo dicha reseña, por lo que lo traemos
      sql_get_nombreuser = '''select nombre_usuario from usuario where id_cliente = {}'''.format(id_cliente)
      cursor.execute(sql_get_nombreuser)
      nombre_user = cursor.fetchone()[0]

      texto = "Usuario: " + str(nombre_user) + "\nPuntuación: " + str(calificacion) + "\t" + str(fecha) +"\n" + comentario

      Label(second_frame, text = texto, justify=LEFT, wraplength=500, width=70, font= ("Lato", 11),
      relief=GROOVE, anchor="w").grid(column=0, row=row, pady=15, padx=5)

      row += 1

   cursor.close()