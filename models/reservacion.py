from lib2to3.pgen2.pgen import generate_grammar
import re
from tkinter import *
import os
import sys
from tkinter import messagebox
from functools import partial
import qrcode

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

        sql_ultima_reservacion = '''Select MAX(hora_fecha) from reservacion where (id_cliente = {} and estatus = 'S') 
        or (estatus = 'T' and id_cliente = {}) '''.format(id_cliente, id_cliente)

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
            return False, '''Su última reservación terminó hace menos de 24 horas. Vuelva una vez se haya cumplido el plazo mínimo de espera. Su última reservación terminó: {}'''.format(termino_reserva)
        else:
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

                    #POR ÚLTIMO, COMPROBAMOS QUE SI HAYA CUPOS DISPONIBLES PARA ESA ZONA, HORA Y FECHA
                    if lugares_ocupados >= limite_cupos:
                        return False, "Ya no quedan lugares disponible para dicha zona en esta fecha y hora"
                    else:
                        #Todo salio bien, se agenda reservacion 
                        cupos_disponibles = limite_cupos - lugares_ocupados
                        print("Cupos disponibles: ",cupos_disponibles)
    
                        resultado, mensaje = insertar_reservacion_bd(fecha_hora_db, cupos, zona_db, id_cliente, id_restaurante)
   
                        return resultado, mensaje
'''def cupos_general():
     #Consultamos en la BD cuál es el número de mesas en total que se pueden ocupar (o sea, nuestro límite de reservaciones)
    #en la zona que requiere usuario
    cursor = db.cursor()
    sql = "SELECT (n_mesas_z1) FROM restaurante where id_restaurante = {}".format(id_restaurante=1)
    cursor.execute(sql)    
    limite_cupos_general = cursor.fetchone()
    return limite_cupos_general
   '''
def cupos_disp(fecha,hora,zona):
    #Damos formato adecuado a fecha y zona para interactuar con DB 
    fecha_hora_db = fecha + " " + hora

    if zona == "Zona Interior" :  #Zona interior será identificada como 1 y la Green como 2
        zona_db = 1
    else:
        zona_db = 2
    
    id_restaurante = 1 #Solo tenemos un restaurante, siempre será el número 1

    print("FECHA HORA DB: ",fecha_hora_db)
    print("ZONA DB: ",zona_db)
    

    #Consultamos en la BD cuál es el número de mesas en total que se pueden ocupar (o sea, nuestro límite de reservaciones)
    #en la zona que requiere usuario
    cursor = db.cursor()
    sql = "SELECT (n_mesas_z{}) FROM restaurante where id_restaurante = {}".format(zona_db, id_restaurante)
    cursor.execute(sql)    
    limite_cupos = cursor.fetchone()[0]

    sql_validacion3 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') < (now()- INTERVAL 2 HOUR)".format(fecha_hora_db)
    cursor.execute(sql_validacion3)
    no_valido_3 = cursor.fetchone()[0]

            #Comprobamos que la reservacion sea en una fecha/hora futura
    if no_valido_3:
         messagebox.showerror("error", "La fecha de reservación ya pasó")
         fecha_venc = 'FC'
         return fecha_venc #retornamos una variable mostrar el mensaje en el main
         
    else:
        sql_validacion4 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') > Date_add(now(), interval 8 day)".format(fecha_hora_db)
        cursor.execute(sql_validacion4)
        no_valido_4 = cursor.fetchone()[0]
                

            #Ahora comprobamos que la reserva no esté más lejana que una semana
        if no_valido_4:
                messagebox.showerror( "Error", "La anticipación máxima de busqueda es de una semana")
                fecha_antic = 'NC'  
                return fecha_antic 
        else:
                sql_validacion_lugar = '''SELECT COUNT(*) from reservacion where hora_fecha = 
                                                str_to_date('{}', '%d/%m/%y %H:%i') and
                                                zona = {} and id_restaurante = {} and estatus = 'A' '''.format(fecha_hora_db,
                                                zona_db, id_restaurante)
                cursor.execute(sql_validacion_lugar)
                lugares_ocupados = cursor.fetchone()[0]
                cursor.close()

   
    #POR ÚLTIMO, COMPROBAMOS QUE SI HAYA CUPOS DISPONIBLES PARA ESA ZONA, HORA Y FECHA
                cupos_disponibles = limite_cupos - lugares_ocupados
                return cupos_disponibles
                
def cupos_disp_todos(fecha,hora,zona):
    #Damos formato adecuado a fecha y zona para interactuar con DB 
    fecha_hora_db = fecha + " " + hora

    if zona == "Zona Interior" :  #Zona interior será identificada como 1 y la Green como 2
        zona_db = 1
    else:
        zona_db = 2
    
    id_restaurante = 1 #Solo tenemos un restaurante, siempre será el número 1

    print("FECHA HORA DB: ",fecha_hora_db)
    print("ZONA DB: ",zona_db)
    

    #Consultamos en la BD cuál es el número de mesas en total que se pueden ocupar (o sea, nuestro límite de reservaciones)
    #en la zona que requiere usuario
    cursor = db.cursor()
    sql = "SELECT (n_mesas_z{}) FROM restaurante where id_restaurante = {}".format(zona_db, id_restaurante)
    cursor.execute(sql)    
    limite_cupos = cursor.fetchone()[0]

    sql_validacion3 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') < (now()- INTERVAL 24 HOUR)".format(fecha_hora_db)
    cursor.execute(sql_validacion3)
    no_valido_3 = cursor.fetchone()[0]

            #Comprobamos que la reservacion sea en una fecha/hora futura
    if no_valido_3:
         messagebox.showerror("error", "La fecha de reservación ya pasó")
         fecha_venc = 'FC'
         return fecha_venc #retornamos una variable mostrar el mensaje en el main
         
    else:
        sql_validacion4 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') > Date_add(now(), interval 8 day)".format(fecha_hora_db)
        cursor.execute(sql_validacion4)
        no_valido_4 = cursor.fetchone()[0]
                

            #Ahora comprobamos que la reserva no esté más lejana que una semana
        if no_valido_4:
                messagebox.showerror( "Error", "La anticipación máxima de busqueda es de una semana")
                fecha_antic = 'NC'  
                return fecha_antic 
        else:
                sql_validacion_lugar = '''SELECT COUNT(*) from reservacion where hora_fecha = 
                                                str_to_date('{}', '%d/%m/%y %H:%i') and
                                                zona = {} and id_restaurante = {} and estatus = 'A' '''.format(fecha_hora_db,
                                                zona_db, id_restaurante)
                cursor.execute(sql_validacion_lugar)
                lugares_ocupados = cursor.fetchone()[0]
                cursor.close()

   
    #POR ÚLTIMO, COMPROBAMOS QUE SI HAYA CUPOS DISPONIBLES PARA ESA ZONA, HORA Y FECHA
                cupos_disponibles = limite_cupos - lugares_ocupados
                return cupos_disponibles

def insertar_reservacion_bd(fechayhora, personas, zona, id_cliente, id_restaurante):

    cursor = db.cursor()
    sql = '''INSERT INTO RESERVACION (hora_fecha, zona, n_personas, id_cliente, id_restaurante, estatus)
            VALUES(STR_TO_DATE('{}', '%d/%m/%y %H:%i'), {}, {}, {}, {}, 'A')'''.format(fechayhora, zona, personas, id_cliente, id_restaurante)
    cursor.execute(sql)
    db.commit()
    cursor.close()

    cursor = db.cursor()
    sql_id = '''SELECT id_reservacion from reservacion where id_cliente = {} and id_restaurante = {} and 
    hora_fecha = STR_TO_DATE('{}', '%d/%m/%y %H:%i') and zona = {}'''.format(id_cliente, id_restaurante, fechayhora, zona)
    cursor.execute(sql_id)
    id_reservacion = cursor.fetchone()
    cursor.close()

    try:
        id_reservacion = id_reservacion[0]
    except:
        return False, "Algo salió mal con la reservacion (id invalido)"
    else:
        
        qr_generado = generar_qr(id_cliente, fechayhora, zona, id_reservacion)

        try:
            cursor = db.cursor()
            sql_agregar_qr = '''UPDATE reservacion set qr = %s where id_reservacion = %s'''
            cursor.execute(sql_agregar_qr, (qr_generado, id_reservacion, ))
            db.commit()
            cursor.close()
        except:
            return False, "Insercion de qr fallida"
        else:
            return True, "Reservacion exitosa"

def cancelar_reservacion(id_cliente):
    
    try:
        cursor = db.cursor()
        sql_id = '''SELECT id_reservacion from reservacion where id_cliente = {} and estatus = 'A' Limit 1'''.format(id_cliente)
        cursor.execute(sql_id)
        registro = cursor.fetchone()
        cursor.close()        

        if registro == None:
            messagebox.showerror("Error", "Usted no cuenta con ninguna reservación activa")
        else:
            cursor = db.cursor()
            id_cancelar = registro[0]
            sql_fecha = '''SELECT hora_fecha from reservacion where id_reservacion = {}'''.format(id_cancelar)
            cursor.execute(sql_fecha)
            fecha_hora_cancelar = cursor.fetchone()[0]
            cursor.close()

            #preguntamos al usuario si está seguro de querer cancelar
            confirmar = messagebox.askokcancel("Confirmación", "Está seguro de cancelar su reservación para el {}?".format(fecha_hora_cancelar))

            if confirmar:
                cursor = db.cursor()
                sql = '''Update reservacion set estatus = 'C' where id_reservacion = {}'''.format(id_cancelar)
                cursor.execute(sql)
                db.commit()
                cursor.close()
                messagebox.showinfo("Cancelación", "Su reservación para el {} ha sido cancelada".format(fecha_hora_cancelar))
            else:
                pass
    except:
        messagebox.showerror("Error", "Algo explotó de nuestro lado xc")

def generar_qr(id_cliente, fecha_hora, zona, id_reservacion):
    
    path_qr = os.getcwd() + '\imagenes' + "\qr reservacion cliente {}.png".format(id_cliente)

    string_codigo = "id_reservacion: " + str(id_reservacion) + "Cliente: " + str(id_cliente) + " Fecha_hora: " + str(fecha_hora) + " Zona: " + str(zona) 
    imagen_qr = qrcode.make(string_codigo)
    archivo_qr = open(path_qr, 'wb')
    imagen_qr.save(archivo_qr)
    archivo_qr.close()

    with open(path_qr, 'rb') as file:
        blob = file.read()
        file.close()

    #En cuanto ya obtenemos el blob para la BD, borramos el png del equipo
    try:
        os.remove(path_qr)
        print("QR eliminado de equipo: ",path_qr)
    except FileNotFoundError:
        print("QR a eliminar no encontrado")
    except:
        print("Pasó algo no esperado")

    return blob

def consulta_reservacion_qr(id_cliente):
    
    cursor = db.cursor()

    sql = "SELECT (qr) from reservacion where id_cliente = {} and estatus = 'A'".format(id_cliente)
    cursor.execute(sql)
    qr_blob = cursor.fetchone()

    if qr_blob == None:
        return False, None
    else:
        qr_blob = qr_blob[0]
        return True, qr_blob

def consultar_reservacion(id_cliente):

    cursor = db.cursor()

    sql = '''SELECT id_reservacion, hora_fecha, zona, n_personas 
    from reservacion where id_cliente = {} and estatus = 'A' '''.format(id_cliente)
    cursor.execute(sql)
    registro = cursor.fetchone()
    cursor.close()

    if registro == None:
        return None
    else:
        return registro

def registrar_asistencia():
    
    global pantalla_registrar_asis

    pantalla_registrar_asis = Toplevel()
    pantalla_registrar_asis.title("Registrar asistencia")
    pantalla_registrar_asis.geometry("500x400")
    
    frame_1 = Frame(pantalla_registrar_asis)
    frame_1.grid(column=0, row=0)

    frame_2 = Frame(pantalla_registrar_asis)
    frame_2.grid(column=0, row=1)

    id_reservacion = StringVar()

    def confirmar(): #Función invocada por el boton de confirmar asistencia (Hace todo lo importante c:)

        id = id_reservacion.get()
        cursor = db.cursor()
        #Traemos la información más importante de la reservación para ser mostrada a la hora de confirmar
        sql_reservacion = "SELECT id_cliente, hora_fecha, zona, estatus from reservacion where id_reservacion = {}".format(id)
        cursor.execute(sql_reservacion)
        reservacion_info = cursor.fetchone()
        cursor.close()

        #El id de la reservación a registrar por asistida es erroneo
        if reservacion_info == None:
            messagebox.showwarning("Ninguna coincidencia", "No hay ninguna reservación con el id {}".format(id))
        #Si se encontró esta reservacion
        else:
            #Obtenemos datos de la consulta
            id_cliente = reservacion_info[0]
            fecha = reservacion_info[1]
            zona = reservacion_info[2]
            estatus = reservacion_info[3]

            if zona == 1:
                zona = "Zona interior"
            elif zona == 2:
                zona = "Green Garden"
            
            if estatus == 'S': #Si esta reservación ya se había confirmado que se habia asistido, avisamos
                messagebox.showerror("ERROR", "Esta reservación ya había sido confirmada como atendida")
            elif estatus == 'C':
                messagebox.showerror("ERROR", "Esta reservación ya había sido cancelada")
            else:
                #como queremos mostrar el nombre real de la persona y no solo su id, consultaremos su nombre
                cursor = db.cursor()
                sql_nombre = "Select nombre_personal from usuario where id_cliente = {}".format(id_cliente)
                cursor.execute(sql_nombre)
                nombre_cliente = cursor.fetchone()[0]
                cursor.close()
                #Desplegamos un cuadro de aviso, dando detalles de la reservación y preguntando si se desea continuar
                proceder = messagebox.askokcancel("Confirmar", '''Información de reservación a confirmar:\nId cliente: {}\nNombre: {}\nZona: {}\nFecha y hora de reservación: {}\n¿Continuar con registro de asistencia?'''.
                format(id_cliente, nombre_cliente, zona, fecha))

                if proceder:
                    cursor = db.cursor()
                    #Si todo sale bien, entonces confirmamos asistencia y establecemos que usuario tiene calificación pendiente que dar para su sig login
                    sql_poner_cal_pendiente = "Update usuario set cal_pendiente = True where id_cliente = {}".format(id_cliente)
                    cursor.execute(sql_poner_cal_pendiente)
                    db.commit()
                    #Marcamos esta reservación como 'S' (si hubo asistencia)
                    sql_estatus_nuevo = "Update reservacion set estatus = 'S' where id_reservacion = {}".format(id)
                    cursor.execute(sql_estatus_nuevo)
                    db.commit()
                    cursor.close()

                    messagebox.showinfo("Éxito", "Asistencia confirmada")
                else:
                    pass


    Label(frame_1, text = "Registro de asistencia", font = ("Lato", 20), fg = "navy blue").grid(column=0, row=0, pady=20, padx=100)
    Label(frame_1, text = "Ingrese el ID de la reservación\nen la cual se registrará asistencia", font = ("Lato", 15), fg = "black").grid(column=0, row=1, pady=5, padx=100)

    Label(frame_2, text = "Id reservación: ").grid(column=0, row=0)
    Entry(frame_2, textvariable=id_reservacion, width=30).grid(column=1, row=0, padx=5, pady=20)
    Button(frame_2, text= "Confirmar asistencia", bg = "#404040", fg="white", command=confirmar).grid(column=0, row=1, pady=6, columnspan=2)

    
def get_all_reservations():
    query = "SELECT * FROM reservacion"
    cursor = db.cursor()
    cursor.execute(query)
    reservaciones = []
    for reservacion in cursor:
        (id_reservacion, hora_fecha, zona, n_personas, id_cliente, id_restaurante, qr, estatus) = reservacion
        reservaciones.append({
            "id": id_reservacion,
            "hora_fecha": hora_fecha,
            "zona": zona,
            "n_personas": n_personas,
            "cliente": id_cliente,
            "id_restaurante": id_restaurante,
            "qr": qr,
            "estatus": estatus
        })
    return reservaciones

def update_estatus(id, estatus):
    query = "UPDATE reservacion SET estatus=%s WHERE id_reservacion=%s"
    cursor = db.cursor()
    cursor.execute(query, (estatus, id))
    db.commit()
    cursor.close()

def get_estatus(id):
    query = "SELECT estatus FROM reservacion WHERE id_reservacion=%s"
    cursor = db.cursor()
    cursor.execute(query,(id,))
    reservations = list(cursor)
    cursor.close()
    if(len(reservations)>0):
        (estatus,) = reservations[0]
        return estatus
    return ""

def get_reservation(id):
    query = "SELECT * FROM reservacion WHERE id_reservacion=%s"
    cursor = db.cursor()
    cursor.execute(query,(id,))
    reservations = list(cursor)
    cursor.close()
    if(len(reservations)>0):
        (id_reservacion, hora_fecha, zona, n_personas, id_cliente, id_restaurante, qr, estatus) = reservations[0]
        return{
            "id": id_reservacion,
            "hora_fecha": hora_fecha,
            "zona": zona,
            "n_personas": n_personas,
            "cliente": id_cliente,
            "id_restaurante": id_restaurante,
            "qr": qr,
            "estatus": estatus
        }