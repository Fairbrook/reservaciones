import re
from tkinter import *
import os
import sys
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk
import qrcode

sys.path.append('../')

from db import *

def set_horarios_db(horario_inicio, ultimo_horario, id_restaurante):
    cursor = db.cursor()

    sql = "UPDATE restaurante set h_inicio = {}, h_cierre = {} where id_restaurante = {}".format(horario_inicio, ultimo_horario, id_restaurante)
    cursor.execute(sql)
    db.commit()
    cursor.close()


def set_cupos_zonas_db(cupos_zona1, cupos_zona2, id_restaurante):

    cursor = db.cursor()

    sql = "UPDATE restaurante set n_mesas_z1 = {}, n_mesas_z2 = {} where id_restaurante = {}".format(cupos_zona1, cupos_zona2, id_restaurante)
    cursor.execute(sql)
    db.commit()
    cursor.close()

def get_horarios_db(id_restaurante):
    
    cursor = db.cursor()

    sql = "SELECT h_inicio, h_cierre from restaurante where id_restaurante = {}".format(id_restaurante)
    cursor.execute(sql)
    valores = cursor.fetchone()
    cursor.close()

    if valores != None:
        return valores
    else:
        messagebox.showerror("ERROR", "Este restaurante no existe")

def get_cupos_zonas_db(id_restaurante):
    
    cursor = db.cursor()

    sql = "SELECT n_mesas_z1, n_mesas_z2 from restaurante where id_restaurante = {}".format(id_restaurante)
    cursor.execute(sql)
    valores = cursor.fetchone()
    cursor.close()

    if valores != None:
        return valores
    else:
        messagebox.showerror("ERROR", "Este restaurante no existe")


def get_horarios_formateados(id_restaurante):

    horarios = get_horarios_db(id_restaurante)

    inicio = horarios[0]
    fin = horarios[1]

    values = []

    current = inicio

    while current<=fin:

        horario_formateado = str(current) + ":00"
        values.append(horario_formateado)
        current += 2 #Saltamos de dos en dos horas
    
    return values

def get_logo_restaurante(id_restaurante):

    path_imagenes = os.getcwd() + '\imagenes'
    almacenar_en = path_imagenes + '\\logo_bd.png'
    cursor = db.cursor()
    query_select_logo = "SELECT logo from restaurante where id_restaurante = {}".format(id_restaurante)
    cursor.execute(query_select_logo)
    logo = cursor.fetchone()
    cursor.close()

    if logo != None:
        logoblob = logo[0]
        with open(almacenar_en, 'wb') as file: #En la carpeta Imagenes "escribimos" la imagen
            file.write(logoblob)
            file.close()
        
        imagen_logo = Image.open(almacenar_en)
        imagen_logo = imagen_logo.resize((150,200), Image.ANTIALIAS)
        logo_redimension = ImageTk.PhotoImage(imagen_logo)

        return logo_redimension