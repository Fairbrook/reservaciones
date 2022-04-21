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
   
   global pantalla_ver_cal_admin

   pantalla_ver_cal_admin = Toplevel()
   pantalla_ver_cal_admin.geometry("700x600")
   pantalla_ver_cal_admin.title("Reseñas")

   main_frame = Frame(pantalla_ver_cal_admin, bg="white")
   main_frame.pack(fill=BOTH, expand=1)

   my_canvas = Canvas(main_frame, bg="white")
   my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

   my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
   my_scrollbar.pack(side=RIGHT, fill=Y)

   my_canvas.configure(yscrollcommand=my_scrollbar.set)
   my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

   second_frame = Frame(my_canvas, bg= "white")
   
   my_canvas.create_window((0,0), window=second_frame, anchor="nw")
   frame_operaciones = Frame(pantalla_ver_cal_admin, bg = "#71938E")
   frame_operaciones.pack(fill=BOTH, expand=1)

   def mostrar_resenas():
      #Queremos saber cual es el promedio actual de calificaciones

      #Limpiamos todas las etiquetas contenidas en second frame para tener vista más actualizada
      for widgets in second_frame.winfo_children():
         widgets.destroy()

      cursor = db.cursor()
      sql_promedio = "SELECT AVG(calificacion) from resena" #Obtenemos promedio actual
      cursor.execute(sql_promedio)
      promedio = cursor.fetchone()[0]

      if promedio == None:
         promedio = "No hay calificaciones"
         color = "black"
      else:
         promedio = round(promedio, 1)
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
      sql_get_resenas = '''select id_resena, id_cliente, calificacion, Date_format(fecha_calificacion, '%d/%m/%Y'), comentario
      from resena'''
      cursor.execute(sql_get_resenas)
      lista_resenas = cursor.fetchall()

      row = 2 #Comenzamos el conteo de filas desde 2

      #Por cada reseña, desglosamos datos
      for resena in lista_resenas:

         id_resena = resena[0]
         id_cliente = resena[1]
         calificacion = resena[2]
         fecha = resena[3]
         comentario = resena[4]
         #También queremos que se vea el nombre del usuario que hizo dicha reseña, por lo que lo traemos
         sql_get_nombreuser = '''select nombre_usuario from usuario where id_cliente = {}'''.format(id_cliente)
         cursor.execute(sql_get_nombreuser)
         nombre_user = cursor.fetchone()[0]

         texto = "ID reseña: " + str(id_resena) + "\nUsuario: " + str(nombre_user) + "\nPuntuación: " + str(calificacion) + "\t" + str(fecha) +"\n" + comentario

         #Mostramos el resumen de datos en Labels
         Label(second_frame, text = texto, justify=LEFT, wraplength=500, width=70, font= ("Lato", 11),
         relief=GROOVE, anchor="w").grid(column=0, row=row, pady=15, padx=5)

         row += 1

      cursor.close()
   
   mostrar_resenas() #Por default mostramos todo al entrar

   id_borrar = StringVar()

   Label(frame_operaciones, text="Gestión de reseñas", bg="#71938E", font=("Lato", 12)).place(x=270, y= 20)
   Label(frame_operaciones, text = "ID de reseña a borrar: ", bg="#71938E", font=("Lato", 12)).place(x = 200, y = 60)
   Entry(frame_operaciones, textvariable=id_borrar).place(x=380, y = 60)
   Button(frame_operaciones, text="Borrar reseña", font = ("Lato",12), bg = "red", fg= "white", 
   command=lambda:borrar_resena(id_borrar.get())).place(x=200, y = 100)
   Button(frame_operaciones, text="Actualizar reseñas", font = ("Lato",12), bg = "navy blue", fg= "white",
   command=mostrar_resenas).place(x = 350, y = 100)

   
def borrar_resena(id_resena):

   cursor = db.cursor()
   sql_borrar = "Delete from resena where id_resena = {}".format(id_resena)
   cursor.execute(sql_borrar)
   db.commit()
   cursor.close()