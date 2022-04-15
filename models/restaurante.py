import re
from tkinter import *
import os
import sys
from tkinter import messagebox
from functools import partial
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


