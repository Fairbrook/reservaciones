from tkinter import *
from tkinter import filedialog
import sys
from functools import partial
sys.path.append('../')

from db import *

def set_horarios_db(horario_inicio, ultimo_horario, id_restaurante):
   pass

def set_cupos_zonas_db(cupos_zona1, cupos_zona2, id_restaurante):
   pass

def get_horarios_db(id_restaurante):
    
    cursor = db.cursor()

    sql = "SELECT h_inicio, h_cierre"

def get_cupos_zonas_db(id_restaurante):
    pass
