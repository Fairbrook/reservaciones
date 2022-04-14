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
    

    #1.- Buscamos en la bd si existe alguna reservacion ACTIVA de este cliente, en cuanto encuentra una, termina y devuelve resultado
    sql_validacion1 = "SELECT COUNT(*) from reservacion where id_cliente = {} and estatus = 'A' Limit 1".format(id_cliente)
    cursor.execute(sql_validacion1)
    no_valido_1 = cursor.fetchone()[0]

    if no_valido_1 == 1: #Si existió una reservación ACTIVA, no se acepta
        return False, "Este usuario ya cuenta con una reservación activa"
    else:
        #Ahora buscaremos que la última reservación terminada (ya sea TERMINADA o ASISTIDA) haya sido hace
        #más de 24 hrs, de otra manera no permitimos reservación
        sql_ultima_reservacion = '''Select MAX(hora_fecha) from reservacion where 
                                    id_cliente = {} and estatus = 'S' or estatus = 'T' '''.format(id_cliente)
        cursor.execute(sql_ultima_reservacion)
        fecha_ultima_reserva = cursor.fetchone()[0]

        if fecha_ultima_reserva == None: #No tiene ninguna última reservación terminada 
            no_valido_2 = False
        else:
            #Se considera terminada 2 horas después de comenzada
            sql_fecha_termino_reserva = "SELECT date_add('{}', interval 2 hour)".format(fecha_ultima_reserva)
            cursor.execute(sql_fecha_termino_reserva)
            termino_reserva = cursor.fetchone()[0]

            sql_validacion2 = '''SELECT '{}' > date_sub(now(), interval 24 hour)'''.format(termino_reserva)
            cursor.execute(sql_validacion2)
            no_valido_2 = cursor.fetchone()[0]

        if no_valido_2:
            return False, '''Su última reservación terminó hace menos de 24 horas\n
            Vuelva una vez se haya cumplido el plazo mínimo de espera\nSu última reservación terminó: {}'''.format(termino_reserva)
        else:
            print("NO HAY RESERVACION 24hrs :)")
            sql_validacion3 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') < now()".format(fecha_hora_db)
            cursor.execute(sql_validacion3)
            no_valido_3 = cursor.fetchone()[0]

            #Comprobamos que la reservacion sea en una fecha/hora futura
            if no_valido_3:
                return False, "La fecha y hora de esta reservación ya pasaron"
            else:
                
                sql_validacion4 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') > Date_add(now(), interval 8 day)".format(fecha_hora_db)
                cursor.execute(sql_validacion4)
                no_valido_4 = cursor.fetchone()[0]
                

                #Ahora comprobamos que la reserva no esté más lejana que una semana
                if no_valido_4:
                    return False, "La anticipación máxima de una reservación es de una semana"  
                else:
                    
                    sql_validacion_lugar = '''SELECT COUNT(*) from reservacion where hora_fecha = 
                                                str_to_date('{}', '%d/%m/%y %H:%i') and
                                                zona = {} and id_restaurante = {} and estatus = 'A' '''.format(fecha_hora_db,
                                                zona_db, id_restaurante)
                    cursor.execute(sql_validacion_lugar)
                    lugares_ocupados = cursor.fetchone()[0]
                    cursor.close()

                    print("CUPOS OCUPADOS: ", lugares_ocupados)

                    #POR ÚLTIMO, COMPROBAMOS QUE SI HAYA CUPOS DISPONIBLES PARA ESA ZONA, HORA Y FECHA
                    if lugares_ocupados >= limite_cupos:
                        print("ERROR CUPOS XXX")
                        return False, "Ya no quedan lugares disponible para dicha zona en esta fecha y hora"
                    else:
                        #Todo salio bien, se agenda reservacion 
                        resultado, mensaje = insertar_reservacion_bd(fecha_hora_db, cupos, zona_db, id_cliente, id_restaurante)
                        return resultado, mensaje
  
def insertar_reservacion_bd(fechayhora, personas, zona, id_cliente, id_restaurante):

    try:
        cursor = db.cursor()
        #POR AHORA OMITIRÉ QR HASTA SABER COMO LO GENERARAN
        sql = '''INSERT INTO reservacion(hora_fecha, zona, n_personas, id_cliente, id_restaurante, estatus)
                VALUES(STR_TO_DATE('{}', '%d/%m/%y %H:%i'), {}, {}, {}, {}, 'A')'''.format(fechayhora, zona, personas, id_cliente, id_restaurante)
        cursor.execute(sql)
        db.commit()
        cursor.close()
    except:
        return False, "Algo salió mal con la reservación"
    else:
        return True, "Éxito! Reservación fue agendada"

def cancelar_reservacion(id_cliente):
    
    try:
        cursor = db.cursor()
        sql = '''SELECT (id_reservacion) from reservacion where id_cliente = {} and estatus = 'A' '''.format(id_cliente)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()        

        if registro == None:
            messagebox.showerror("Error", "Usted no cuenta con ninguna reservación activa")
        else:
            registro = registro[0]

            cursor = db.cursor()
            sql = '''Update reservacion set estatus = 'C' where id_reservacion = {}'''.format(registro)
            cursor.execute(sql)
            db.commit()
            cursor.close()
    except:
        messagebox.showerror("Error", "Algo explotó de nuestro lado xc")

