from db import *
from lib2to3.pgen2.pgen import generate_grammar
import re
from tkinter import *
import os
import sys
from tkinter import messagebox
from functools import partial
import qrcode

sys.path.append('../')


def validar_reservacion(id_cliente, fecha, hora, zona, cupos):

    # Damos formato adecuado a fecha y zona para interactuar con DB
    fecha_hora_db = fecha + " " + hora

    if zona == "Zona Interior":  # Zona interior será identificada como 1 y la Green como 2
        zona_db = 1
    else:
        zona_db = 2

    id_restaurante = 1  # Solo tenemos un restaurante, siempre será el número 1

    print("CLIENTE: ", id_cliente)
    print("FECHA HORA DB: ", fecha_hora_db)
    print("ZONA DB: ", zona_db)
    print("CUPOS", cupos)

    # Consultamos en la BD cuál es el número de mesas en total que se pueden ocupar (o sea, nuestro límite de reservaciones)
    # en la zona que requiere usuario
    cursor = db.cursor()
    sql = "SELECT (n_mesas_z{}) FROM restaurante where id_restaurante = {}".format(
        zona_db, id_restaurante)
    cursor.execute(sql)
    limite_cupos = cursor.fetchone()[0]

    # 1.- Buscamos en la bd si existe alguna reservacion ACTIVA de este cliente, en cuanto encuentra una, termina y devuelve resultado
    sql_validacion1 = "SELECT COUNT(*) from reservacion where id_cliente = {} and estatus = 'A' Limit 1".format(id_cliente)
    cursor.execute(sql_validacion1)
    no_valido_1 = cursor.fetchone()[0]

    if no_valido_1 == 1:  # Si existió una reservación ACTIVA, no se acepta
        return False, "Este usuario ya cuenta con una reservación activa"
    else:
        # Ahora buscaremos que la última reservación terminada (ya sea TERMINADA o ASISTIDA) haya sido hace
        # más de 24 hrs, de otra manera no permitimos reservación

        sql_ultima_reservacion = '''Select MAX(hora_fecha) from reservacion where (id_cliente = {} and estatus = 'S') 
        or (estatus = 'T' and id_cliente = {}) '''.format(id_cliente, id_cliente)

        cursor.execute(sql_ultima_reservacion)
        fecha_ultima_reserva = cursor.fetchone()[0]

        if fecha_ultima_reserva == None:  # No tiene ninguna última reservación terminada
            no_valido_2 = False
        else:
            # Se considera terminada 2 horas después de comenzada
            sql_fecha_termino_reserva = "SELECT date_add('{}', interval 2 hour)".format(
                fecha_ultima_reserva)
            cursor.execute(sql_fecha_termino_reserva)
            termino_reserva = cursor.fetchone()[0]

            sql_validacion2 = '''SELECT '{}' > date_sub(now(), interval 24 hour)'''.format(
                termino_reserva)
            cursor.execute(sql_validacion2)
            no_valido_2 = cursor.fetchone()[0]

        if no_valido_2:
            return False, '''Su última reservación terminó hace menos de 24 horas. Vuelva una vez se haya cumplido el plazo mínimo de espera. Su última reservación terminó: {}'''.format(termino_reserva)
        else:
            sql_validacion3 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') < now()".format(
                fecha_hora_db)
            cursor.execute(sql_validacion3)
            no_valido_3 = cursor.fetchone()[0]

            # Comprobamos que la reservacion sea en una fecha/hora futura
            if no_valido_3:
                return False, "La fecha y hora de esta reservación ya pasaron"
            else:
                sql_validacion4 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') > Date_add(now(), interval 7 day)".format(
                    fecha_hora_db)
                cursor.execute(sql_validacion4)
                no_valido_4 = cursor.fetchone()[0]

                # Ahora comprobamos que la reserva no esté más lejana que una semana
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

                    # POR ÚLTIMO, COMPROBAMOS QUE SI HAYA CUPOS DISPONIBLES PARA ESA ZONA, HORA Y FECHA
                    if lugares_ocupados >= limite_cupos:
                        return False, "Ya no quedan lugares disponible para dicha zona en esta fecha y hora"
                    else:
                        # Todo salio bien, se agenda reservacion
                        cupos_disponibles = limite_cupos - lugares_ocupados
                        print("Cupos disponibles: ", cupos_disponibles)

                        resultado, mensaje = insertar_reservacion_bd(
                            fecha_hora_db, cupos, zona_db, id_cliente, id_restaurante)

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


def cupos_disp(fecha, hora, zona):
    # Damos formato adecuado a fecha y zona para interactuar con DB
    fecha_hora_db = fecha + " " + hora

    if zona == "Zona Interior":  # Zona interior será identificada como 1 y la Green como 2
        zona_db = 1
    else:
        zona_db = 2

    id_restaurante = 1  # Solo tenemos un restaurante, siempre será el número 1

    print("FECHA HORA DB: ", fecha_hora_db)
    print("ZONA DB: ", zona_db)

    # Consultamos en la BD cuál es el número de mesas en total que se pueden ocupar (o sea, nuestro límite de reservaciones)
    # en la zona que requiere usuario
    cursor = db.cursor()
    sql = "SELECT (n_mesas_z{}) FROM restaurante where id_restaurante = {}".format(
        zona_db, id_restaurante)
    cursor.execute(sql)
    limite_cupos = cursor.fetchone()[0]

    sql_validacion3 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') < (now()- INTERVAL 2 HOUR)".format(
        fecha_hora_db)
    cursor.execute(sql_validacion3)
    no_valido_3 = cursor.fetchone()[0]

    # Comprobamos que la reservacion sea en una fecha/hora futura
    if no_valido_3:
        messagebox.showerror("error", "La fecha de reservación ya pasó")
        fecha_venc = 'FC'
        return fecha_venc  # retornamos una variable mostrar el mensaje en el main

    else:
        sql_validacion4 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') > Date_add(now(), interval 8 day)".format(
            fecha_hora_db)
        cursor.execute(sql_validacion4)
        no_valido_4 = cursor.fetchone()[0]

        # Ahora comprobamos que la reserva no esté más lejana que una semana
        if no_valido_4:
            messagebox.showerror(
                "Error", "La anticipación máxima de busqueda es de una semana")
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

    # POR ÚLTIMO, COMPROBAMOS QUE SI HAYA CUPOS DISPONIBLES PARA ESA ZONA, HORA Y FECHA
            cupos_disponibles = limite_cupos - lugares_ocupados
            return cupos_disponibles


def cupos_disp_todos(fecha, hora, zona):
    # Damos formato adecuado a fecha y zona para interactuar con DB
    fecha_hora_db = fecha + " " + hora

    if zona == "Zona Interior":  # Zona interior será identificada como 1 y la Green como 2
        zona_db = 1
    else:
        zona_db = 2

    id_restaurante = 1  # Solo tenemos un restaurante, siempre será el número 1

    print("FECHA HORA DB: ", fecha_hora_db)
    print("ZONA DB: ", zona_db)

    # Consultamos en la BD cuál es el número de mesas en total que se pueden ocupar (o sea, nuestro límite de reservaciones)
    # en la zona que requiere usuario
    cursor = db.cursor()
    sql = "SELECT (n_mesas_z{}) FROM restaurante where id_restaurante = {}".format(
        zona_db, id_restaurante)
    cursor.execute(sql)
    limite_cupos = cursor.fetchone()[0]

    sql_validacion3 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') < (now()- INTERVAL 24 HOUR)".format(
        fecha_hora_db)
    cursor.execute(sql_validacion3)
    no_valido_3 = cursor.fetchone()[0]

    # Comprobamos que la reservacion sea en una fecha/hora futura
    if no_valido_3:
        messagebox.showerror("error", "La fecha de reservación ya pasó")
        fecha_venc = 'FC'
        return fecha_venc  # retornamos una variable mostrar el mensaje en el main

    else:
        sql_validacion4 = "SELECT STR_TO_DATE('{}', '%d/%m/%y %H:%i') > Date_add(now(), interval 8 day)".format(
            fecha_hora_db)
        cursor.execute(sql_validacion4)
        no_valido_4 = cursor.fetchone()[0]

        # Ahora comprobamos que la reserva no esté más lejana que una semana
        if no_valido_4:
            messagebox.showerror(
                "Error", "La anticipación máxima de busqueda es de una semana")
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

    # POR ÚLTIMO, COMPROBAMOS QUE SI HAYA CUPOS DISPONIBLES PARA ESA ZONA, HORA Y FECHA
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
        sql_id = '''SELECT id_reservacion from reservacion where id_cliente = {} and estatus = 'A' Limit 1'''.format(
            id_cliente)
        cursor.execute(sql_id)
        registro = cursor.fetchone()
        cursor.close()

        if registro == None:
            messagebox.showerror(
                "Error", "Usted no cuenta con ninguna reservación activa")
        else:
            cursor = db.cursor()
            id_cancelar = registro[0]
            sql_fecha = '''SELECT hora_fecha from reservacion where id_reservacion = {}'''.format(
                id_cancelar)
            cursor.execute(sql_fecha)
            fecha_hora_cancelar = cursor.fetchone()[0]
            cursor.close()

            # preguntamos al usuario si está seguro de querer cancelar
            confirmar = messagebox.askokcancel(
                "Confirmación", "Está seguro de cancelar su reservación para el {}?".format(fecha_hora_cancelar))

            if confirmar:
                cursor = db.cursor()
                sql = '''Update reservacion set estatus = 'C' where id_reservacion = {}'''.format(
                    id_cancelar)
                cursor.execute(sql)
                db.commit()
                cursor.close()
                messagebox.showinfo(
                    "Cancelación", "Su reservación para el {} ha sido cancelada".format(fecha_hora_cancelar))
            else:
                pass
    except:
        messagebox.showerror("Error", "Algo explotó de nuestro lado xc")


def generar_qr(id_cliente, fecha_hora, zona, id_reservacion):

    path_qr = os.getcwd() + '\imagenes' + \
        "\qr reservacion cliente {}.png".format(id_cliente)

    string_codigo = "id_reservacion: " + str(id_reservacion) + "Cliente: " + str(
        id_cliente) + " Fecha_hora: " + str(fecha_hora) + " Zona: " + str(zona)
    imagen_qr = qrcode.make(string_codigo)
    archivo_qr = open(path_qr, 'wb')
    imagen_qr.save(archivo_qr)
    archivo_qr.close()

    with open(path_qr, 'rb') as file:
        blob = file.read()
        file.close()

    # En cuanto ya obtenemos el blob para la BD, borramos el png del equipo
    try:
        os.remove(path_qr)
        print("QR eliminado de equipo: ", path_qr)
    except FileNotFoundError:
        print("QR a eliminar no encontrado")
    except:
        print("Pasó algo no esperado")

    return blob


def consulta_reservacion_qr(id_cliente):

    cursor = db.cursor()

    sql = "SELECT (qr) from reservacion where id_cliente = {} and estatus = 'A'".format(
        id_cliente)
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


def get_all_reservations():
    query = "SELECT reservacion.id_reservacion,\
        reservacion.hora_fecha, \
        reservacion.zona,\
        reservacion.n_personas,\
        reservacion.id_cliente,\
        reservacion.id_restaurante,\
        reservacion.qr, estatus,\
        usuario.nombre_personal, usuario.nombre_usuario FROM reservacion\
        INNER JOIN usuario ON usuario.id_cliente = reservacion.id_cliente "
    cursor = db.cursor()
    cursor.execute(query)
    reservaciones = []
    for reservacion in cursor:
        (id_reservacion, hora_fecha, zona, n_personas,
         id_cliente, id_restaurante, qr, estatus, usuario_nombre_personal, usuario_nombre_usuario) = reservacion
        reservaciones.append({
            "id": id_reservacion,
            "hora_fecha": hora_fecha,
            "zona": zona,
            "n_personas": n_personas,
            "cliente": id_cliente,
            "id_restaurante": id_restaurante,
            "qr": qr,
            "estatus": estatus,
            "cliente": {
                "id": id_cliente,
                "nombre_personal": usuario_nombre_personal,
                "nombre_usuario": usuario_nombre_usuario
            }
        })
    return reservaciones


def update_estatus(id, estatus):
    cursor = db.cursor()
    if estatus == 'S':
        query = "SELECT * FROM reservacion WHERE id_reservacion=%s"
        cursor.execute(query, (id,))
        user = list(cursor)[0][4]
        query = "UPDATE usuario SET cal_pendiente=True WHERE id_cliente=%s"
        cursor.execute(query, (user,))
    query = "UPDATE reservacion SET estatus=%s WHERE id_reservacion=%s"
    cursor.execute(query, (estatus, id))
    db.commit()
    cursor.close()


def get_estatus(id):
    query = "SELECT estatus FROM reservacion WHERE id_reservacion=%s"
    cursor = db.cursor()
    cursor.execute(query, (id,))
    reservations = list(cursor)
    cursor.close()
    if(len(reservations) > 0):
        (estatus,) = reservations[0]
        return estatus
    return ""


def get_reservation(id):
    query = "SELECT reservacion.id_reservacion,\
        reservacion.hora_fecha, \
        reservacion.zona,\
        reservacion.n_personas,\
        reservacion.id_cliente,\
        reservacion.id_restaurante,\
        reservacion.qr, estatus,\
        usuario.nombre_personal, usuario.nombre_usuario FROM reservacion\
        INNER JOIN usuario ON usuario.id_cliente = reservacion.id_cliente\
        WHERE reservacion.id_reservacion=%s"
    cursor = db.cursor()
    cursor.execute(query, (id,))
    reservations = list(cursor)
    cursor.close()
    if(len(reservations) > 0):
        (id_reservacion, hora_fecha, zona, n_personas,
         id_cliente, id_restaurante, qr, estatus, usuario_nombre_personal, usuario_nombre_usuario) = reservations[0]
        return{
            "id": id_reservacion,
            "hora_fecha": hora_fecha,
            "zona": zona,
            "n_personas": n_personas,
            "cliente": id_cliente,
            "id_restaurante": id_restaurante,
            "qr": qr,
            "cliente": {
                "id": id_cliente,
                "nombre_personal": usuario_nombre_personal,
                "nombre_usuario": usuario_nombre_usuario
            },
            "estatus": estatus
        }
