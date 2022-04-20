from email import message
from string import punctuation
from tkinter import *
import os
import sys
from tkinter import messagebox
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

def crear_calificacion(id_cliente):

    global pantalla_crear_cali, puntuacion #pantalla_crear_cali = pantalla crear calificacion
    puntuacion = 5.0
    pantalla_crear_cali = Toplevel()
    pantalla_crear_cali.geometry("500x350")
    pantalla_crear_cali.title("Crear Calificacion")

    rowconfigure(pantalla_crear_cali,10)
    columnconfigure(pantalla_crear_cali,3)

    Label(pantalla_crear_cali, text="Por favor, denos unos segundos para calificar su experiencia\nen la reservación pasada",
            font = "12,bold").grid(column=0, pady=5, columnspan=3)

    Label(pantalla_crear_cali, text="Seleccione la Puntuacion:",
          font="10,bold").grid(column=1, pady=8)


    Label(pantalla_crear_cali, text=str(puntuacion), #5.0 es la calificación sugerida inicialmente
            height="2", width="4",
            font="18").grid(row=3, column=1) #Muestra la puntación actual a ofrecer

    resta = Button(pantalla_crear_cali, text="-",
                   height="2", width="4",
                   bg= "#EC2926", fg= "white",
                   font="18", command=lambda:dar_puntos(0)).grid(row=3, column=0, padx=15, sticky="NSEW") #Boton de resta
    suma = Button(pantalla_crear_cali, text="+",
                  height="2", width="4",
                  bg= "#29AE36",
                  font="18", command=lambda:dar_puntos(1)).grid(row=3, column=2, padx=15, sticky="NSEW") #Boton de suma
    blanklabel(pantalla_crear_cali)

    Label(pantalla_crear_cali, text="Comentario :",
          font="15,bold").grid(column=0, columnspan=3, pady=5) #Para ingresar un comentario

    opinion_text = Text(pantalla_crear_cali, width=45, height=3)
    opinion_text.grid(column=0, columnspan=3, padx=30)

    blanklabel(pantalla_crear_cali)
    submit = Button(pantalla_crear_cali, text="Registrar calificacion",
                    height="3", width="20",
                    bg= "#30B68B",
                    command=lambda:registrar_feedback(puntuacion, opinion_text.get(1.0, "end"), id_cliente)).grid(column=1)
    Label(pantalla_crear_cali, text="").grid(column=0, columnspan=3, padx=60, sticky="NSEW")
    

def dar_puntos(operacion): #Funcion para ver los cupos disponibles y delimitar los botones
    
    global puntuacion
    if operacion==0 and puntuacion>0: #Si es 0 o menor no se puede disminuir
        puntuacion=puntuacion - 0.5
        Label(pantalla_crear_cali, text=str(puntuacion),
                height="2", width="4",
                font="18").grid(row=3, column=1) #muestra la puntuacion actual

    elif operacion==1 and puntuacion<5: #Si es 5 o mas no se puede aumentar
        puntuacion=puntuacion + 0.5
        Label(pantalla_crear_cali, text=str(puntuacion),
                height="2", width="4",
                font="18").grid(row=3, column=1) #muestra la puntuacion actual

def registrar_feedback(calificacion, comentario, id_cliente):
    
    try:
        cursor = db.cursor()
        sql = '''Insert into resena (fecha_calificacion, calificacion, id_cliente, comentario)
                Values (curdate(), {}, {}, '{}')'''.format(calificacion, id_cliente, comentario)
        cursor.execute(sql)
        db.commit()

        sql_cal_pendiente = "Update usuario set cal_pendiente = False where id_cliente = {}".format(id_cliente)
        cursor.execute(sql_cal_pendiente)
        db.commit()
        cursor.close()
    except:
        messagebox.showerror("ERROR", "Ocurrió un error de nuestro lado, una disculpa :c")
    else:
        messagebox.showinfo("Calificación", "Muchas gracias por su retroalimentación, conocer su experiencia es importante para nosostros!")
        pantalla_crear_cali.destroy()


def blanklabel(ventana): #Para no escribir mucho, esta funcion crea el salto de linea
    Label(ventana, text="").grid() #Lit crea una etiqueta en blanco que se puede usar para separar elementos
#Funciones para automatizar los escalados
def rowconfigure(ventana, row): #Escalado de filas, se requiere las filas que se usaran
    for x in range(row):
        Grid.rowconfigure(ventana,x,weight=1) #Da un peso que escala
def columnconfigure(ventana, column): #Escalado de columnas, se requiere las columnas que se usaran
    for x in range(column):
        Grid.columnconfigure(ventana,x,weight=1) #Da un peso que escala
    