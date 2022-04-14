from tkinter import *
import os
import sys
from tkinter import messagebox
from functools import partial

sys.path.append('../')

from db import *

def validar_reservacion(id_cliente, fecha, hora, zona, cupos):

    #Damos formato adecuado a fecha y zona para interactuar con DB 
    fecha_hora_db = fecha + " " + hora

    if zona == "Zona Interior" :  #Zona interior será identificada como 1 y la Green como 2
        zona_db = 1
    else:
        zona_db = 2
    
    id_restaurante = 1 #Solo tenemos un restaurante, siempre será el número 1

    print("CLIENTE: ",id_cliente)
    print("FECHA HORA DB: ",fecha_hora_db)
    print("ZONA DB: ",zona_db)
    print("CUPOS",cupos)

    #Consultamos en la BD cuál es el número de mesas en total que se pueden ocupar (o sea, nuestro límite de reservaciones)
    #en la zona que requiere usuario
    cursor = db.cursor()
    sql = "SELECT (n_mesas_z{}) FROM restaurante where id_restaurante = {}".format(zona_db, id_restaurante)
    cursor.execute(sql)    
    limite_cupos = cursor.fetchone()[0]
    cursor.close()
    
    cursor = db.cursor()
    sql_validacion1 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') < now()".format(fecha_hora_db)
    cursor.execute(sql_validacion1)
    no_valido_1 = cursor.fetchone()[0]
    cursor.close()
    
    #Primero validamos que la reservación sea en una fecha futura
    if no_valido_1:
        return False, "La fecha y hora de esta reservación ya pasaron"
    else:
        
        cursor = db.cursor()
        sql_validacion2 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') > Date_add(now(), interval 8 day)".format(fecha_hora_db)
        cursor.execute(sql_validacion2)
        no_valido_2 = cursor.fetchone()[0]
        cursor.close()

        #Ahora comprobamos que la reserva no esté más lejana que un año
        if no_valido_2:
            return False, "La anticipación máxima de una reservación es de un año"  
        else:

            cursor = db.cursor()

            #Buscamos en la bd si existe alguna reservacion ACTIVA de este cliente, en cuanto encuentra una, termina y devuelve resultado
            sql_validacion3 = "SELECT COUNT(*) from reservacion where id_cliente = {} and estatus = 'A' Limit 1".format(id_cliente)
            cursor.execute(sql_validacion3)
            no_valido_3 = cursor.fetchone()[0]
            cursor.close()

            #Ahora comprobamos que este usuario no cuente con ninguna otra reservacion ACTIVA
            if no_valido_3 == 1: #Si existió una reservación ACTIVA, no se acepta
                return False, "Este usuario ya cuenta con una reservación activa"
            else:

                pass