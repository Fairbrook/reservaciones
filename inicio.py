
# -- coding: utf-8 --
from dataclasses import InitVar
from msilib import text
from re import L
import tkinter
from tkinter import  messagebox
from tkinter import  ttk
import os
from tkinter import *
from tkcalendar import Calendar 
import qrcode
from PIL import Image, ImageTk
#from models.administrador import consulta_BD
import hashlib
from models.administrador import login_admin
from models.restaurante import get_cupos_zonas_db, get_horarios_db, set_cupos_zonas_db, set_horarios_db, get_horarios_formateados
from models.usuario import login, register
from models.platillo import ver_menu, modificar_menu
from models.reservacion import consultar_reservacion, validar_reservacion, cancelar_reservacion, consulta_reservacion_qr,cupos_disp

def inicio_sesion(): #pantalla al iniciar el programa, se encontrara el inicio de sesion
    global pantalla, user_verify, password_verify, user_entry, password_entry #variables globales
    global cupos_max, cupos, reserva, estrellas, zona, fecha, hora, uso_f, uso_h, uso_z, fecha1,hora1,zona1
    pantalla=Tk() #declaramos la pantalla principal
    pantalla.geometry("300x350") #tamaño de ventana
    pantalla.title("Login") #titulo de ventana
    user_verify=StringVar() #indicamos el tipo de variable
    cupos_max=IntVar()
    password_verify=StringVar() #indicamos el tipo de variable
    cupos=IntVar() #indicamos el tipo de variable
    reserva=IntVar() #indicamos el tipo de variable
    uso_f=IntVar()
    uso_h=IntVar()
    uso_z=IntVar()
    zona=StringVar() #indicamos el tipo de variable
    fecha=StringVar() #indicamos el tipo de variable
    hora=StringVar() #indicamos el tipo de variable
    cupos_max=6
    
    zona1=StringVar() #indicamos el tipo de variable
    fecha1=StringVar() #indicamos el tipo de variable
    hora1=StringVar() #indicamos el tipo de variable
    
    resultado_cup = IntVar()
    resultado_cup = 0
    cupos=1 #inicializamos (TEMPORALES PARA PRUEBAS)
    uso_f=0
    uso_h=0
    uso_z=0
    uso_f1=0
    uso_h1=0
    uso_z1=0
    
    estrellas=1 #limite de estrellas a dar
    reserva=1

    #Configuracion para escalar los elementos de la ventana
    rowconfigure(pantalla,11)
    columnconfigure(pantalla,1)
    #Label = etiqueta
    Label(pantalla, text="Ingrese su usuario y constraseña", bg="medium aquamarine",
        font="Arial,16,bold").grid(sticky="NSEW")
    #Label en blanco para salto, definida en su funcion
    blanklabel(pantalla)
    #Entrada para dar un usuario
    Label(pantalla, text="Usuario:").grid(sticky="NSEW")
    user_entry = Entry(pantalla, textvariable=user_verify, width="25")
    user_entry.grid(padx=20, sticky="NSEW")
    blanklabel(pantalla)
    
    #Entrada para dar la contraseña, el show es un minicifrado visual
    Label(pantalla, text="Contraseña:").grid(sticky="NSEW")
    password_entry = Entry(pantalla, show="*", textvariable=password_verify, width="25")
    password_entry.grid(padx=20, sticky="NSEW")
    blanklabel(pantalla)
    #boton para iniciar sesion
    Button(pantalla, text='Iniciar Sesión',
             height="2", width="20",
             bg= "#30B68B",
             command=validar).grid(padx=60, sticky="NSEW")
    blanklabel(pantalla)
    #boton para registrar
    Button(pantalla, text='¿No tienes cuenta? \n Registrate!',
             height="3", width="20",
             bg= "#BCEBE0",
             command=registro).grid(padx=60, sticky="NSEW")  
    
    blanklabel(pantalla)
   #depuramos la pantalla como iniciador del programa 
    pantalla.mainloop()
    
def registro(): #Se despliega encima de iniciar sesion para dar un registro
    global pantalla_r, new_user_entry, new_password_entry, new_name_entry, new_lastname_entry
    global new_user_verify, new_password_verify, new_name_verify, new_lastname_verify
    pantalla_r = Toplevel(pantalla) #pantalla_r = pantalla registro
    pantalla_r.geometry("300x350")
    pantalla_r.title("Registro")
    new_user_verify=StringVar() #Indicamos el tipo de variable
    new_password_verify=StringVar() #Indicamos el tipo de variable
    new_name_verify=StringVar() #Indicamos el tipo de variable
    rowconfigure(pantalla_r,13)
    columnconfigure(pantalla_r,1)
    Label(pantalla_r, text="Ingrese los datos para el registro", font="bold").grid(sticky="NSEW")
    blanklabel(pantalla_r)
    #Pide el nombre de la persona
    Label(pantalla_r, text="Nombre(s):").grid(sticky="NSEW")
    new_name_entry = Entry(pantalla_r, textvariable=new_name_verify, width="25")
    new_name_entry.grid(padx=20, sticky="NSEW")
    
    blanklabel(pantalla_r)
    #Pide el nuevo usuario
    Label(pantalla_r, text="Usuario:").grid(sticky="NSEW")
    new_user_entry = Entry(pantalla_r, textvariable=new_user_verify, width="25")
    new_user_entry.grid(padx=20, sticky="NSEW")
    #Pide la contraseña
    Label(pantalla_r, text="Contraseña:").grid(sticky="NSEW")
    new_password_entry = Entry(pantalla_r, show="*", textvariable=new_password_verify, width="25")
    new_password_entry.grid(padx=20, sticky="NSEW")
    
    blanklabel(pantalla_r)
    #Registra al nuevo usuario y contraseña
    Button(pantalla_r, text='REGISTRAR',
             height="3", width="20",
             bg= "#30B68B",
             command=registrar_bd).grid(padx=60, sticky="NSEW")
    
    blanklabel(pantalla_r)
    
def menu_cliente(id_cliente): #Menu a desplegar a todos estos usuarios de tipo cliente
    global pantalla_mc #Pantalla_mc = pantalla menu cliente 
    #pantalla.withdraw() #Cerramos la ventana de inicio de sesion
    pantalla_mc = Toplevel(pantalla) #Que aparezca encima de la de inicio de sesion
    imagen=PhotoImage(file="logop.png") #Importamos el Logo de nuestro equipo
    imagen.subsample(2,2) #No me acuerdo, pero es de la imagen
    pantalla_mc.geometry("300x500")
    pantalla_mc.title("Menu")
    rowconfigure(pantalla_mc,10)
    columnconfigure(pantalla_mc,1)
    #Los siguientes cuatro Button son para los botones que redirigen a los menus correspondientes al nombre
    #Boton llamado info (informacion) y sus caracteristicas
    info = Button(pantalla_mc, text="Informacion", 
                  height="3", width="300",
                  bg= "#BCEBE0",
                  command=ver_info).grid(padx=60, sticky="NSEW")
    blanklabel(pantalla_mc)
    #Boton llamado reserva y sus caracteristicas
    reserva = Button(pantalla_mc, text="Reservaciones",
                     height="3", width="300",
                     bg= "#BCEBE0",
                     command=lambda:menu_reservaciones(0,id_cliente)).grid(padx=60, sticky="NSEW")
    
    blanklabel(pantalla_mc)
    #Boton llamado calificar y sus caracteristicas
    calificar = Button(pantalla_mc, text="Calificar",
                       height="3", width="300",
                       bg= "#BCEBE0",
                       command=lambda:menu_calificacion(0)).grid(padx=60, sticky="NSEW")
    
    blanklabel(pantalla_mc)
    #Boton llamado menu y sus caracteristicas
    menu = Button(pantalla_mc, text="Menu",
                       height="3", width="300",
                       bg= "#BCEBE0",                  
                       command=ver_menu).grid(padx=60, sticky="NSEW")                 
    
    blanklabel(pantalla_mc)
    #Imagen de nuestro equipo
    Label(pantalla_mc, image=imagen).grid()
    blanklabel(pantalla_mc)
    pantalla_mc.mainloop()
    
def menu_admin(id_admin): #Menu a desplegar al usuario de tipo admin
    global pantalla_ma #pantalla_ma = pantalla menu admin
    #pantalla.withdraw()
    pantalla_ma = Toplevel(pantalla) #Aparece encima del inicio de sesion
    imagen=PhotoImage(file="logop.png")   #Importamos la imagen del equipo
    pantalla_ma.geometry("300x450")
    pantalla_ma.title("Administrador")
        
    rowconfigure(pantalla_ma,11)
    columnconfigure(pantalla_ma,1)
    #Igual, 4 bototones para las weas de acciones
    #Boton de informacion
    info = Button(pantalla_ma, text="Modificar\ninformación", 
                  height="3", width="300",
                  bg= "#BCEBE0",
                  command=modificar_info).grid(padx=60, sticky="NSEW")
    
    blanklabel(pantalla_ma)
    #Boton de reservaciones
    reserva = Button(pantalla_ma, text="Reservaciones",
                     height="3", width="300",
                     bg= "#BCEBE0",
                     command=lambda:menu_reservaciones(1,id_admin)).grid(padx=60, sticky="NSEW")
    
    blanklabel(pantalla_ma)
    #Boton de calificaciones
    calificar = Button(pantalla_ma, text="Calificaciones",
                       height="3", width="300",
                       bg= "#BCEBE0",
                       command=lambda:menu_calificacion(1)).grid(padx=60, sticky="NSEW")
    
    blanklabel(pantalla_ma)
    #Boton de menu de comida
    menu = Button(pantalla_ma, text="Modificar menú",
                       height="3", width="300",
                       bg= "#BCEBE0",                   
                       command=modificar_menu).grid(padx=60, sticky="NSEW")                   
    
    blanklabel(pantalla_ma)
    #Cargamos la imagen en la ventana
    Label(pantalla_ma, image=imagen).grid()
    
    blanklabel(pantalla_ma)
    pantalla_ma.mainloop()

def ver_info():#Funcion para ver la informacion
    global pantalla_viewinfo #Variables globales
    pantalla_viewinfo = Toplevel() #Que aparezca encima de cualquier menu
    pantalla_viewinfo.geometry("590x600")
    pantalla_viewinfo.config(bg="white") #Fondo de la ventana
    pantalla_viewinfo.title("Visualizar información")
    pantalla_viewinfo.resizable(0,0)
    rowconfigure(frame_info, 2)
    columnconfigure(frame_info, 2)
    #Se declara un frame de fondo blanco
    frame_titulo = Frame(pantalla_viewinfo, bg = "white") 
    frame_titulo.grid(column=0,row=0)
    #Etiqueta de titulo del frame
    Label(frame_titulo, text="Información", font=("Arial", 20),
          fg="navy blue", bg="white").grid(column=0,row=0, padx=150, pady=10)
    frame_info = Frame(pantalla_viewinfo, bg= "white")
    frame_info.grid(column=0, row=1)
    #Texto que contendra el frame
    texto_info = Text(frame_info, height=30, width=70, font=("Lato", 10))
    texto_info.grid(column=0,row=0, padx=20,pady=10)
    #Implementacion de la barra de scroll tanto vertical como horizontal
    ladoy = Scrollbar(frame_info, orient =VERTICAL)
    ladox = Scrollbar(frame_info, orient= HORIZONTAL)
    #espaciado entre casillas de la "tabla"
    ladox.grid(column=0, row = 1, sticky='ew') 
    ladoy.grid(column = 1, row = 0, sticky='ns')
    #Configura el texto junto al scroll
    texto_info.config(yscrollcommand = ladoy.set)
    texto_info.config(xscrollcommand= ladox.set)
    ladoy.config(command=texto_info.yview)
    ladox.config(command=texto_info.xview)
    #Leeremos toda la informacion a travez de un .txt
    archivo = open("informacion.txt", 'r') #Abrimos el archivo
    texto_info.delete("1.0", "end") #Limpiamos pantalla por si acaso
    for linea in archivo:
        texto_info.insert("end", linea) #Declaramos las lineas y las guardamos
    
    horarios = get_horarios_db(1)
    inicio = horarios[0]
    ultimo = horarios[1]
    cupos = get_cupos_zonas_db(1)
    zona1 = cupos[0]
    op_zona = cupos[1]

    texto_info.insert("end", "Horario: de "+str(inicio)+" a "+str(ultimo)+" horas\n" )
    texto_info.insert("end", "Cupos:\nZona interior cuenta con "+str(zona1) + " mesas" + "\nGreen garden cuenta con "+str(op_zona)+" mesas")    
    texto_info.config(state='disabled') #El usuario no puede hacerle nada al texto, solo se muestra

def modificar_info(): #Funcion para el administrador, con el cual podra modificar el archivo
    #COnfiguracion previa al crear la ventana
    rowconfigure(frame_info, 2)
    columnconfigure(frame_info, 2)
    global pantalla_modificar_info
    pantalla_modificar_info = Toplevel()
    pantalla_modificar_info.geometry("630x650")
    pantalla_modificar_info.config(bg="white")
    pantalla_modificar_info.title("Modificar información")
    pantalla_modificar_info.resizable(0,0)
    pantalla_modificar_info = Frame(pantalla_modificar_info, bg = "white")
    pantalla_modificar_info.grid(column=0,row=0)
    Label(pantalla_modificar_info, text="Información", font=("Arial", 20), fg="navy blue", bg="white").grid(column=0,row=0, padx=150, pady=10)
    #Se crea el frame donde se modificara la informacion general (sin incluir horarios ni cupos)
    frame_info = Frame(pantalla_modificar_info, bg= "white")
    frame_info.grid(column=0, row=1)
    #Se crea frame donde se visualizan cupos y horarios, es en un lugar diferente porque son variables indepenndientes
    frame_horarios_cupos = Frame(pantalla_modificar_info, bg="white")
    frame_horarios_cupos.grid(column=0, row=2)
    #Frame donde estarán los spinbox de la información (cupos, horario inicio y horario cierre)
    frame_variables = Frame(pantalla_modificar_info, bg = "white")
    frame_variables.grid(column=0, row=3)

    entry_z1 = IntVar() #Entry Spinbox zona 1
    entry_z2 = IntVar() #Entry Spinbox zona 2
    entry_h1 = IntVar() #Entry Spinbox horario de inicio
    entry_h2 = IntVar() #Entry Spinbox ultimo horario

    Label(frame_variables, text="Seleccione el primer y último horario disponible para el cliente (Formato 24hrs)", font=("Arial", 10), bg="white").grid(column=0, row=0, columnspan=4, pady=10)

    opciones_spin_inicio = (8,10,12,14,16,18,20) #Opciones que tendrán los spinbox de horarios
    opciones_spin_fin = (10,12,14,16,18,20,22)

    Label(frame_variables,text="1er horario (Formato 24hrs): ", font=("Lato", 8), bg="white").grid(column=0, row=1)
    spin_inicio = Spinbox(frame_variables, textvariable= entry_h1, values=opciones_spin_inicio).grid(column=1, row=1, padx=5)

    Label(frame_variables,text="último horario (Formato 24hrs): ", font=("Lato", 8), bg="white").grid(column=2, row=1)
    spin_fin = Spinbox(frame_variables, textvariable= entry_h2 ,values=opciones_spin_fin).grid(column=3, row=1, padx=5)

    Label(frame_variables, text="Mesas en zona interior: ", font=("Lato", 8), bg="white").grid(column=0, row=2, padx=5, pady=8)
    spin_zona1 = Spinbox(frame_variables, textvariable=entry_z1 ,from_=1, to=50).grid(column=1, row=2, padx=5)
    
    Label(frame_variables, text="Mesas en Green Garden: ", font=("Lato", 8), bg="white").grid(column=2, row=2, padx=5, pady=8)
    spin_zona2 = Spinbox(frame_variables, textvariable=entry_z2 ,from_=1, to=50).grid(column=3, row=2, padx=5)
    
    #Frame para botones
    frame_boton = Frame(pantalla_modificar_info, bg="white")
    frame_boton.grid(column=0, row=4)
    #Texto que contendra info general
    texto_info = Text(frame_info, height=15, width=70, font=("Lato", 10))
    texto_info.grid(column=0,row=0, padx=20,pady=10)
    #Texto que contendrá info sobre cupos y horarios
    texto_horarios_cupos = Text(frame_horarios_cupos, height=4, width=70, font=("Lato", 10))
    texto_horarios_cupos.grid(column=0, row=0, padx=20,pady=10)
    #Implementacion de la barra de scroll tanto vertical como horizontal
    ladoy = Scrollbar(frame_info, orient =VERTICAL)
    ladox = Scrollbar(frame_info, orient= HORIZONTAL)
    #Ubicamos los scroll en panntalla
    ladox.grid(column=0, row = 1, sticky='ew') 
    ladoy.grid(column = 1, row = 0, sticky='ns')
    #Configura el texto junto al scroll
    texto_info.config(yscrollcommand = ladoy.set)
    texto_info.config(xscrollcommand= ladox.set)
    ladoy.config(command=texto_info.yview)
    ladox.config(command=texto_info.xview)

    #Funcion para mostrar la informacion que existe actualmente
    def mostrar_info_actual():
        archivo = open("informacion.txt", 'r') #R de read
        texto_info.delete("1.0", "end") #Limpiamos pantalla por si acaso
        for linea in archivo:
            texto_info.insert("end", linea)
        
        archivo.close()

        horarios = get_horarios_db(1)
        inicio = horarios[0]
        ultimo = horarios[1]
        cupos = get_cupos_zonas_db(1)
        zona1 = cupos[0]
        op_zona = cupos[1]

        texto_horarios_cupos.delete("1.0", "end")
        texto_horarios_cupos.insert("end", "Horario: de "+str(inicio)+" a "+str(ultimo)+" horas\n" )
        texto_horarios_cupos.insert("end", "Cupos:\nZona interior cuenta con "+str(zona1) + " mesas" + "\nGreen garden cuenta con "+str(op_zona)+" mesas")

    
    #Funcion para modificar la informacion que esta mostrada
    def actualizar_info():
        rowconfigure(frame_boton, 1)
        columnconfigure(frame_boton, 2)
        mostrar_info_actual()
        archivo = open("informacion.txt", 'w') #W de write
        nuevo_texto = texto_info.get(1.0, "end")
        archivo.write(nuevo_texto)
        archivo.close()

        primer_horario = entry_h1.get()
        ultimo_horario = entry_h2.get()
        cupos_zona1 = entry_z1.get()
        cupos_zona2 = entry_z2.get()

        if primer_horario > ultimo_horario:
            pop_ups("El horario de inicio no puede ser más tarde que el último horario disponible")
        else:
            set_cupos_zonas_db(cupos_zona1, cupos_zona2, 1) #id restaurante es siempre 1 en nuestro proyecto
            set_horarios_db(primer_horario, ultimo_horario, 1)


    #Botones para ejecutar las dos funciones previas
    Button(frame_boton, text = "Actualizar info",
            bg= "#47525E", fg="white", 
            command=actualizar_info).grid(column=0, row=0, pady=5, padx=5)
    Button(frame_boton, text = "Mostrar info",
            bg= "#47525E", fg="white", 
            command=mostrar_info_actual).grid(column=1, row=0, pady=5, padx=5)
                   
    
def menu_reservaciones(user, id): #Funcion que despliega el menu de reservaciones, recibe como parametro la id del usuario
    global pantalla_rese
    if user==1: #1 es de admin, probablemente dependiendo de la BD cambiara a ser una funcion aparte
        pantalla_rese = Toplevel(pantalla_ma) #Encima de la pantalla de menu admin
        rowconfigure(pantalla_rese,3)
        columnconfigure(pantalla_rese,1)
    else: #else de cliente (TEMPORAL)
        pantalla_rese = Toplevel(pantalla_mc) #Encima de la pantalla de menu cliente
        rowconfigure(pantalla_rese,9)
        columnconfigure(pantalla_rese,1)
    pantalla_rese.geometry("300x400")
    pantalla_rese.title("Reservacion")
    
    if user!=1: #Si el usuario es cualquier cliente 
        #Se crean los botones de las funciones de reservar
        Button(pantalla_rese, text="Reservar",
               height="3", width="300",
               bg= "#BCEBE0",
               command=lambda:crear_reservacion(id)).grid(padx=60, sticky="NSEW") #Boton de Crear reservacion
        
        blanklabel(pantalla_rese)
        Button(pantalla_rese, text="Ver mi reservacion",
               height="3", width="300",
               bg= "#BCEBE0",
               command=lambda:ver_reservacion(id)).grid(padx=60, sticky="NSEW") #Boton de Ver reservacion
        
        blanklabel(pantalla_rese)
        Button(pantalla_rese, text="Cupos disponibles",
               height="3", width="300",
               bg= "#BCEBE0",
               command=lambda:cupos_disponibles(id)).grid(padx=60, sticky="NSEW") #Boton de Ver cupos disponicles
       
        blanklabel(pantalla_rese)
        
        Button(pantalla_rese, text="Cancelar reservacion",
               height="3", width="300",
               bg= "#BCEBE0", command=lambda:cancelar_reservacion(id)).grid(padx=60, sticky="NSEW") #Boton de Borrar reservacion
        
        blanklabel(pantalla_rese)
        Button(pantalla_rese, text="Obtener codigo", 
               height="3", width="300",
               bg= "#BCEBE0",
               command=lambda:codigo_reservacion_pantalla(id)).grid(padx=60, sticky="NSEW") #Boton Obtener el Codigo QR
        
        blanklabel(pantalla_rese)
    else:
        #Botones para el admin relacionados con reservar
        Button(pantalla_rese, text="Ver reservaciones",
               height="3", width="300",
               bg= "#BCEBE0").grid(padx=60, sticky="NSEW") #Boton para Ver las reservaciones totales
        
        blanklabel(pantalla_rese)

        Button(pantalla_rese, text="Modificar parametros",
               height="3", width="300",
               bg= "#BCEBE0").grid(padx=60, sticky="NSEW") #Boton para Ver las reservaciones totales
        
        blanklabel(pantalla_rese)
    volver = Button(pantalla_rese, text="Volver",
                    height="2", width="15",
                    bg= "#47525E", fg="white",
                    command=pantalla_rese.destroy).grid(padx=80, sticky="NSEW") #Boton para regresar al menu de opciones

def codigo_reservacion_pantalla(id_cliente): #Funcion para obtener el codigo QR de la reservacion (TRATAR DE HACER UN GENERADOR)
    global qr, reserva 
    
    tiene_reservacion, qr_blob = consulta_reservacion_qr(id_cliente)

    if not tiene_reservacion:
        pop_ups("Esta cuenta no posee una reservación activa! :c")
    else:

        path_almacen_temporal = os.getcwd() + "\imagenes\qr_reservacion_cliente{}.png".format(id_cliente)

        with open(path_almacen_temporal, 'wb') as file:
            file.write(qr_blob)
            file.close()

        imagen = Image.open(path_almacen_temporal) 
        imagen = ImageTk.PhotoImage(imagen)

        qr = Toplevel(pantalla_rese) #Encima de la ventana de reservaciones
        Label(qr, image=imagen).pack()

        try:
            os.remove(path_almacen_temporal)
            print("QR eliminado de equipo: ",path_almacen_temporal)
        except FileNotFoundError:
            print("QR a eliminar no encontrado")

        qr.mainloop() #Lo hacemos mainloop para que se muestre la imagen, se elimina al destruir la ventana al parecer

    # if reserva==0: #TEMPORAL comprobamos si tiene una reserva, sino se despliega un pop up de error
    #     pop_ups("No tiene reserva")
    #         #Falta el pop up ;p
    # else:
    #     imagen_codigo=PhotoImage(file="QR.gif") #Importamos la imagen
    #     image=imagen_codigo.subsample(2,2)
    #     cadena = "wenaswenas"
    #     imagen_codigo = qrcode.make(cadena) #Importamos la imagen
    #     archivo_imagen = open("Codigo Reservacion",'wb')
    #     imagen_codigo.save(archivo_imagen)
    #     archivo_imagen.close()

    #     codigoqr=PhotoImage(file="Codigo Reservacion") #Importamos el Logo de nuestro equipo
    #     codigoqr.subsample(2,2) #No me acuerdo, pero es de la imagen        

    #     image=codigoqr.subsample(2,2)
    #     qr.geometry("200x200")
    #     qr.title("Codigo de reservacion")
    #     Label(qr, image=imagen_codigo).pack() #Si tiene reserva, se muestra el QR
    #     Label(qr, image=codigoqr).pack() #Si tiene reserva, se muestra el QR

#Funciones de cupos
def validar_cupos_aux(fecha,hora,zona): 
    global resultado_cup
    try:
        fecha= cale.get_date() #Variables y su asignacion de procedencia
        zona = selec_zona.get()
        hora = selec_hora.get()
        
        if uso_f1 == 0 or uso_h1 == 0 or uso_z1 == 0: #Si falta un campo no se realiza la busqueda
            print("ERROR IF")
            messagebox.showwarning("Error", "Fallo en la busqueda\nTiene uno o mas campos vacios")
            resultado_cup = ''
            fecha = ''
            zona = ''
            hora = ''
        else:
            resultado_cup = cupos_disp(fecha, hora, zona)
        
    except:
        print("ERROR EXCEPT")
        messagebox.showwarning("Error", "Fallo en la busqueda\nCuenta con uno o más campos vacios")
        
    print(resultado_cup)

def validar_cupos_aux_todos(fecha,hora,zona): 
    global resultado_cup
        
    try:
        fecha= cale.get_date() #Variables y su asignacion de procedencia
        zona = op_zona
        hora = hora_values
        
        if uso_f1 == 0: #Si falta campo de fecha no se realiza la busqueda
            print("ERROR IF")
            messagebox.showwarning("Error", "No seleccionó una fecha")
        else:
            resultado_cup = cupos_disp(fecha, hora, zona)
        
    except:
        print("ERROR EXCEPT")
        messagebox.showwarning("Error", "Fallo en la busqueda\nCuenta con uno o más campos vacios")
        
    print(resultado_cup)



def cupos_disponibles(id_cliente):
    global cupos_dis,selec_hora, selec_zona, uso_h1, uso_f1, uso_z1,frame_calendario
    cupos_dis = Toplevel(pantalla_rese) #Encima de la ventana de reservaciones
    cupos_dis.geometry("550x600")
    cupos_dis.title("Cupos disponibles")
    

    frame_tabla = Frame(cupos_dis)
    frame_tabla.grid(column=0, row= 7)
    #frame titulo
    frame_titulo = Frame(cupos_dis) 
    frame_titulo.grid(column=0,row=0)
    
    #Etiqueta de titulo del frame
    Label(frame_titulo, text="Cupos Disponibles", font=("Lato", 20),
          fg="Black").grid(column=0,row=0, padx=150, pady=10)
    frame_info = Frame(cupos_dis)
    frame_info.grid(column=0, row=1)
    #Frame 
  #  texto_info = Text(frame_info, height=30, width=70, font=("Lato", 10))
   # texto_info.grid(column=0,row=0, padx=20,pady=10)
    

    #Tabla cupos
    tabla = ttk.Treeview(frame_tabla, height=7)
    tabla.grid(column=0, row=6,pady=20)
    tabla['columns'] = ('horario','zona','Cupos Disponibles')

    tabla.column('#0', minwidth=0, width=0, anchor='center')
    tabla.column('horario', minwidth=40, width=50 , anchor='center')
    tabla.column('zona', minwidth=120, width=160 , anchor='center')
    tabla.column('Cupos Disponibles', minwidth=120, width=160 , anchor='center')
    

    tabla.heading('horario', text='Horario', anchor ='center')
    tabla.heading('zona', text='zona', anchor ='center')
    tabla.heading('Cupos Disponibles', text='Cupos Disponibles', anchor ='center')
    
    estilo = ttk.Style(cupos_dis)
    estilo.theme_use('clam') #  ('clam', 'alt', 'default', 'classic')
    estilo.configure(".",font= ('lato', 10, 'bold'), foreground='black')        
    estilo.configure("Treeview", font= ('lato', 10, 'bold'), foreground='black',  background='white')
    estilo.map('Treeview',background=[('selected', 'lato')], foreground=[('selected','green')] )

    a=0
    #reiniciamos variables
    uso_h1 = 0
    uso_z1 = 0
    uso_f1 = 0
    #frame boton cupos disponibles
    frame_boton_cupos = Frame(cupos_dis)
    frame_boton_cupos.grid(column=0, row=8)
    blanklabel(cupos_dis)
   
    
    #Calendario de seleccion de día para la reserva
    frame_calendario = Frame(cupos_dis)
    frame_calendario.grid(column=0, row=3 )
    #frame zona y hora
    frame_zh = Frame(cupos_dis, bg="white")
    frame_zh.grid(column=0, row=4 )
    Label(frame_calendario, text="Seleccione una Fecha", 
          font="15,bold").grid(column=0,row =1) #Seleccion del día
   
    blanklabel(cupos_dis)
    dia_cupo = Button(frame_calendario, text="Día:",#Boton que indica zona de reservacion adentro
                      font="18,bold", bg= "#37E3AC",
                      command=Calendario_cupos,  width = 20).grid(row=3, column=0)
       
    
    #imagen_empleado = PhotoImage(file = "cupos.png")
    #Label(cupos_dis, image=imagen_empleado, bg="white").grid(padx=60, sticky="NSEW")
    #imagen_empleado1 = ImageTk.PhotoImage(imagen_empleado)
 #Hora de reserva
    Label(frame_zh, text="Seleccione la hora:", 
          font="15,bold").grid(column=0) #Seleccion de zonas
    
    values_horarios = get_horarios_formateados(1)
    print(values_horarios)

    def hora_nueva(event): #Funcion para otorgar la hora a esa variable
        global uso_h1
        hora1 = selec_hora.get() #Obtiene el valor del combox
        uso_h1=uso_h1+1 #Cambio de bandera
    selec_hora = ttk.Combobox(frame_zh, #Crea la lista desplegable en esta ventana
        state="readonly", #No se puede editar por el usuario
        values=values_horarios) #Opciones
    selec_hora.grid(column=0, sticky="NSEW") #Lo de posicionamiento
    selec_hora.bind("<<ComboboxSelected>>",hora_nueva) #Cambia conforme las selecciones
    
    #Zona de reserva
    Label(frame_zh, text="Seleccione la zona:", 
          font="15,bold").grid(column=0) #Seleccion de zonas
    
    def zona_nueva(event): #Funcion para otorgar la hora a esa variable
        global uso_z1
        zona1 = selec_zona.get() #Obtiene el valor del combox
        uso_z1=uso_z1+1 #Cambio de bandera
    selec_zona = ttk.Combobox(frame_zh, #Crea la lista desplegable en esta ventana
            state="readonly", #No se puede editar por el usuario
            values=["Seleccione una zona", "Green Garden", "Zona Interior"]) #Opciones
    selec_zona.grid(column=0, sticky="NSEW") #Lo de posicionamiento
    selec_zona.bind("<<ComboboxSelected>>",zona_nueva) #Cambia conforme las selecciones
    blanklabel(cupos_dis)
   
    
    def boton():
        tabla.delete(*tabla.get_children())
        
        validar_cupos_aux(fecha1,hora1,zona1)
        
        cupos_individual = resultado_cup
        if cupos_individual != 'FC' and cupos_individual != 'NC':
            tabla.insert('', 1, text="", values = (selec_hora.get(),selec_zona.get(),cupos_individual))
            print(selec_zona.get())  
       
    def boton_todos():
        tabla.delete(*tabla.get_children())
        global i,j
        global hora_values,op_zona
        i=0
        j=0
        zona_cupos = ["Zona Interior","Green Garden"]
       
        for op_zona_cpy in zona_cupos:
            op_zona= zona_cupos[j] 
            op_zona_cpy =op_zona
            i=0
            for horarios in values_horarios:   
                hora_values = values_horarios[i]
                horarios = hora_values
                
                validar_cupos_aux_todos(horarios,fecha1,op_zona_cpy)
                cupos_general = resultado_cup
                if cupos_general != 'FC' and cupos_general != 'NC':#posible valor de retorno de la funcion validar_cupos en reservacion.impide que el usuario vea la fecha de mas de 7 dias.
                    
                    tabla.insert('',i, text="", values = (hora_values,op_zona,cupos_general))
                    i=i+1
                else:
                    break
            if cupos_general != 'FC' and cupos_general != 'NC':
                
                j=j+1
            else:
                break
            
                  
    blanklabel(cupos_dis)
       
    ver_cupos = Button(frame_boton_cupos, text="ver cupos",
                      heigh="2",
                      font="18", bg= "#30B68B",
                      command=boton).grid(column=1, row = 10 ,padx=10, pady=30) #Boton para reservar y finalizar
    todos = Button(frame_boton_cupos, text="Todos los cupos",
                      heigh="2",
                      font="18", bg= "#30B68B",command = boton_todos
                      ).grid(column=2, row =10, pady=30) #Boton para reservar y finalizar
         
        
    volver = Button(cupos_dis, text="Volver",
                    height="2", width="30",
                    bg= "#47525E", fg="white",
                    command=cupos_dis.destroy).grid(column=0,row =9) #Boton para regresar al menu de opciones
    
    
        

def Calendario_cupos():
    global fecha1, calendario_cupos, cale
    calendario_cupos=Toplevel()
    calendario_cupos.title("Calendario")
    cale = Calendar(calendario_cupos, selectmode = 'day', 
            year = 2022, month = 5, 
            day = 24, locale ='es')
    cale.grid(pady = 20)
    def definir_fecha_cupos():
        global uso_f1
        fecha1=cale.get_date()
        calendario_cupos.destroy()
        uso_f1=uso_f1+1
        dia_cupos = Button(frame_calendario, text="Día: "+fecha1,#Boton que indica zona de reservacion adentro
                    font="18,bold", bg= "#BCEBE0",
                    command=Calendario_cupos,width = 20).grid(row=3, column=0)
    Button(calendario_cupos, text="Definir Fecha", command=definir_fecha_cupos).grid()
   
  
def crear_reservacion(id_cliente): #Funcion para crear la reservacion
    global crear_rese, seleccion_hora, seleccion_zona, uso_h, uso_f, uso_z
    crear_rese = Toplevel(pantalla_rese) #Encima de la ventana de reservaciones
    crear_rese.geometry("450x500")
    crear_rese.title("Crear reservacion")
    #reiniciamos variables
    uso_h = 0
    uso_z = 0
    uso_f = 0
    #Configuracion de escalabilidad
    rowconfigure(crear_rese,11)
    columnconfigure(crear_rese,3)
    #Calendario de seleccion de día para la reserva
    Label(crear_rese, text="Seleccione el día:", 
          font="15,bold").grid(column=1) #Seleccion del día
    
    dia_rese = Button(crear_rese, text="Día:",#Boton que indica zona de reservacion adentro
                      font="18,bold", bg= "#37E3AC",
                      command=Calendario).grid(row=1, column=1, sticky="NSEW")
    #Hora de reserva
    Label(crear_rese, text="Seleccione la hora:", 
          font="15,bold").grid(column=1) #Seleccion de zonas
    
    values_horarios = get_horarios_formateados(1)
    print(values_horarios)

    def hora_nueva(event): #Funcion para otorgar la hora a esa variable
        global uso_h
        hora = seleccion_hora.get() #Obtiene el valor del combox
        uso_h=uso_h+1 #Cambio de bandera
    seleccion_hora = ttk.Combobox(crear_rese, #Crea la lista desplegable en esta ventana
        state="readonly", #No se puede editar por el usuario
        values=values_horarios) #Opciones
    seleccion_hora.grid(column=1, sticky="NSEW") #Lo de posicionamiento
    seleccion_hora.bind("<<ComboboxSelected>>",hora_nueva) #Cambia conforme las selecciones
    
    #Zona de reserva
    Label(crear_rese, text="Seleccione la zona:", 
          font="15,bold").grid(column=1) #Seleccion de zonas
    
    def zona_nueva(event): #Funcion para otorgar la hora a esa variable
        global uso_z
        zona = seleccion_zona.get() #Obtiene el valor del combox
        uso_z=uso_z+1 #Cambio de bandera
    seleccion_zona = ttk.Combobox(crear_rese, #Crea la lista desplegable en esta ventana
            state="readonly", #No se puede editar por el usuario
            values=["Seleccione una zona", "Green Garden", "Zona Interior"]) #Opciones
    seleccion_zona.grid(column=1, sticky="NSEW") #Lo de posicionamiento
    seleccion_zona.bind("<<ComboboxSelected>>",zona_nueva) #Cambia conforme las selecciones
    
    #Personas para la reserva
    Label(crear_rese, text="¿Cuantas personas?\nCupo Maximo: 6", 
          font="15,bold").grid(column=1) #Texto de pregunta
    #Una etiqueta con dos botones adyacentes para subir o disminuir el numero de cupos a reservar
    mostrar_cupos = Label(crear_rese, text=str(cupos),
                          height="2", width="4",
                          font="18").grid(row=7, column=1) #Estara en el centro, son los cupos existentes
    
    def cupos_disp(operacion): #Funcion para ver los cupos disponibles y delimitar los botones
        global cupos, cupos_max
        if operacion==0 and cupos>0: #Si es 0 o menor no se puede disminuir
            cupos=cupos-1
            mostrar_cupos = Label(crear_rese, text=str(cupos),
                                  height="2", width="4",
                                  font="18").grid(row=7, column=1) #muestra los cupos 
        elif operacion==1 and cupos<cupos_max: #Si es 10 o mas no se puede aumentar
            cupos=cupos+1
            mostrar_cupos = Label(crear_rese, text=str(cupos),
                                  height="2", width="4",
                                  font="18").grid(row=7, column=1) #muestra los cupos
    
    resta = Button(crear_rese, text="-",
                   height="2", width="4",
                   font="18", bg= "#BCEBE0",
                   command=lambda:cupos_disp(0)).grid(row=7, column=0, padx=15, sticky="NSEW") #Boton de resta
    suma = Button(crear_rese, text="+",
                  height="2", width="4",
                  font="18", bg= "#BCEBE0",
                  command=lambda:cupos_disp(1)).grid(row=7, column=2, padx=15, sticky="NSEW") #Boton de suma
    blanklabel(crear_rese)
    reservar = Button(crear_rese, text="Hacer reservación",
                      heigh="3",
                      font="18", bg= "#30B68B",
                      command=lambda:validar_reservacion_aux(id_cliente,fecha,hora,zona,cupos)).grid(column=1, sticky="NSEW") #Boton para reservar y finalizar
    
    volver = Button(crear_rese, text="Volver",
                    height="2", width="15",
                    bg= "#47525E", fg="white",
                    command=crear_rese.destroy).grid(column=1, padx=80, sticky="NSEW") #Boton para regresar al menu de opciones
    
    
def ver_reservacion(id_cliente): #Funcion para Ver la Reservacion
    #global ver_rese, reserva, fecha, cupos, zona, hora #ver rese = pantalla de ver reserva
    global ver_rese

    resultado = consultar_reservacion(id_cliente)

    if resultado == None: #No existe reservacion
        pop_ups("No tiene una reserva") #se cambiara a un pop up
    else:
        ver_rese = Toplevel(pantalla_rese) #Encima de la ventana de reservaciones
        ver_rese.geometry("300x300")
        ver_rese.title("Ver reservacion")

        id_reserva = resultado[0]
        fecha_hora = resultado[1]
        zona = resultado[2]
        if zona == 1:
            zona = "Zona Interior"
        else:
            zona = "Green Garden"
        personas = resultado[3]


        rowconfigure(ver_rese, 8)
        columnconfigure(ver_rese, 1)
        Label(ver_rese, text="Información de su reservación:").grid(column=0, row=0, pady=10) #pop up donde se muestra la info PROXUMAMENTE
        Label(ver_rese, text="ID de reservación: " + str(id_reserva)).grid(column=0, row=1, pady=10)
        Label(ver_rese, text="Fecha y hora: "+ str(fecha_hora)).grid(column=0, row= 2, pady=10)
        Label(ver_rese, text="Su zona es: "+ str(zona)).grid(column=0, row=3, pady=10)
        Label(ver_rese, text="Mesa para " + str(personas) + " personas").grid(column=0, row=4, pady=10)
        blanklabel(ver_rese)
        Button(ver_rese, text="Volver",
                heigh="3", font="18",
                bg= "#47525E", fg="white",
                command=ver_rese.destroy).grid(column=0, row = 5,padx=80, sticky="NSEW")
    
def menu_calificacion(user): #Interfaz de las calificaciones
    global pantalla_cali #pantalla cali = pantalla calificaciones
    if user==1: #Si es admin
        pantalla_cali = Toplevel(pantalla_ma)
        rowconfigure(pantalla_cali, 7)
        columnconfigure(pantalla_cali, 1)
    else: #Si es cliente
        pantalla_cali = Toplevel(pantalla_mc)
        rowconfigure(pantalla_cali, 9)
        columnconfigure(pantalla_cali, 1)
    pantalla_cali.geometry("300x320")
    pantalla_cali.title("Calificacion")
    
    if user!=1: #Si el usuario no es admin se muestra la opcion de calificar
        Button(pantalla_cali, text="Calificar",
               height="3", width="300",
               bg= "#BCEBE0",
               command=crear_calificacion).grid(padx=60, sticky="NSEW")
        
        blanklabel(pantalla_cali)
    Button(pantalla_cali, text="Ver calificacion",
           height="3", width="300",
           bg= "#BCEBE0").grid(padx=60, sticky="NSEW") #Boton para ver la calificacion
    
    blanklabel(pantalla_cali)
    puntuacion = Label(pantalla_cali, text="...").grid() #Promedio de calificacion no visible
    
    blanklabel(pantalla_cali)
    Button(pantalla_cali, text="Ver Opiniones",
           height="3", width="300",
           bg= "#BCEBE0").grid(padx=60, sticky="NSEW") #Boton para ver las opiniones
    
    blanklabel(pantalla_cali)
    volver = Button(pantalla_cali, text="Volver",
                    height="2", width="15",
                    bg= "#47525E", fg="white",
                    command=pantalla_cali.destroy).grid(padx=80, sticky="NSEW") #Boton para regresar al menu de opciones

def crear_calificacion():
    global pantalla_crear_cali, new_opinion, opinion_entry #pantalla_crear_cali = pantalla crear calificacion
    pantalla_crear_cali = Toplevel(pantalla_cali)
    pantalla_crear_cali.geometry("450x300")
    pantalla_crear_cali.title("Crear Calificacion")
    new_opinion=StringVar()
    rowconfigure(pantalla_crear_cali,10)
    columnconfigure(pantalla_crear_cali,3)
    Label(pantalla_crear_cali, text="Seleccione la Puntuacion:",
          font="15,bold").grid(column=1) #Muestra los cupos disponibles
    #Una etiqueta con dos botones adyacentes para subir o disminuir el numero de cupos a reservar
    puntuacion = Label(pantalla_crear_cali, text=str(estrellas),
                          height="2", width="4",
                          font="18").grid(row=3, column=1) #Estara en el centro, son los cupos existentes
    
    def dar_puntos(operacion): #Funcion para ver los cupos disponibles y delimitar los botones
        global estrellas
        if estrellas==0 and estrellas>0: #Si es 0 o menor no se puede disminuir
            estrellas=estrellas-1
            puntuacion = Label(pantalla_crear_cali, text=str(estrellas),
                                  height="2", width="4",
                                  font="18").grid(row=3, column=1) #muestra las estrellas
        elif operacion==1 and estrellas<5: #Si es 5 o mas no se puede aumentar
            estrellas=estrellas+1
            puntuacion = Label(pantalla_crear_cali, text=str(estrellas),
                                  height="2", width="4",
                                  font="18").grid(row=3, column=1) #muestra las estrellas
    resta = Button(pantalla_crear_cali, text="-",
                   height="2", width="4",
                   bg= "#BCEBE0",
                   font="18", command=lambda:dar_puntos(0)).grid(row=3, column=0, padx=15, sticky="NSEW") #Boton de resta
    suma = Button(pantalla_crear_cali, text="+",
                  height="2", width="4",
                  bg= "#BCEBE0",
                  font="18", command=lambda:dar_puntos(1)).grid(row=3, column=2, padx=15, sticky="NSEW") #Boton de suma
    blanklabel(pantalla_crear_cali)
    Label(pantalla_crear_cali, text="Comentario:",
          font="15,bold").grid(column=0, columnspan=3) #Para ingresar un comentario
    opinion_entry = Entry(pantalla_crear_cali, textvariable=new_opinion, width="30")
    opinion_entry.grid(column=1)
    blanklabel(pantalla_crear_cali)
    submit = Button(pantalla_crear_cali, text="Registrar calificacion",
                    height="3", width="20",
                    bg= "#30B68B",
                    command=pantalla_crear_cali.destroy).grid(column=1)
    Label(pantalla_crear_cali, text="").grid(column=0, columnspan=3, padx=60, sticky="NSEW")
    
    volver = Button(pantalla_crear_cali, text="Volver",
                    height="2", width="15",
                    bg= "#47525E", fg="white",
                    command=pantalla_crear_cali.destroy).grid(column=1, padx=80, sticky="NSEW") #Boton para regresar al menu de calificar
    
# Funcion para hacer validaciones e iniciar sesión
def validar(): 
    """
    #BORRAR ESTE UNA VEZ SE COMPLETE EL LOGIN DE ADMIN APROPIADAMENTE, ESTO ES SOLO PARA ACCEDER RÁPIDO EN PRUEBAS
    #NO LO BORREN PARA QUE FRONTEND PUEDA HACER PRUEBAS * C MUERE POR POBRE *
    if password_entry.get() == 'admin' and user_entry.get() == 'admin':
        menu_admin()
    else:
        menu_cliente()
    # Obtenemos los valores igresados en las cajas de texto
    """
    # Validar nombre de usuario
    usuariovalidar=user_entry.get()
    if len(usuariovalidar) == 0:
        messagebox.showwarning("Error", "Introduzca su nombre de usuario")
        return
    # Validar contraseña
    contraseñavalidar=password_entry.get()
    if len(contraseñavalidar) == 0:
        messagebox.showwarning("Error", "Introduzca su contraseña")
        return
    # Inicio de sesión
    try:
        #funcion para login
        user = login(usuariovalidar, contraseñavalidar)
        if user!=None:
            pantalla.iconify()
            id_current_user = user["id_cliente"]#<----ID es necesario para varias operaciones, es de suma importancia
            menu_cliente(id_current_user)
        else:
        #Inicio sesion admin
          admin = login_admin(usuariovalidar,contraseñavalidar)
        #revisamos si hay concidencias
          if len(admin) != 0:    
        #si hay concidencias se muestra el menu de admin
            pantalla.iconify()
            id_admin = admin[0][0] #<--- admin es una lista de una tupla, [0][0] retorna solo id del admin
            menu_admin(id_admin)
          elif user == None:
            messagebox.showwarning("Error", "Usuario y/o contraseña incorrectos")
    except:
        messagebox.showwarning("Error", "Hubo un error inesperado")
        return
    
    user_entry.delete(first=0,last='end') #Se limpia
    password_entry.delete(first=0,last='end') #Se limpia despues del uso

def pop_ups(texto): #Funcion para los pop ups
    global pop_up
    pop_up = Toplevel() #Encima de cualquier cosa
    imagen_cheems=PhotoImage(file="cheems.png") #Importamos la imagen
    image=imagen_cheems.subsample(2,2)
    pop_up.geometry("650x330")
    pop_up.title("Errorm")
    pop_up.configure(bg="white") #fondo blanco limdom
    rowconfigure(pop_up,4)
    columnconfigure(pop_up,2)
    
    #Ponemos la label en la segunda columna, para que en la primera este la imagen
    Label(pop_up, text="¡Oh no!", height="3",
         font="Arial,48,bold", bg="white").grid(row=0, column=1, sticky="NSEW")
    Label(pop_up, text="Emcomtramste el errorm:\n"+str(texto),
         height="3", font="Arial,32,bold", bg="white").grid(row=1, column=1, sticky="NSEW")
    Label(pop_up, text="Emstamos trabajandom\npara remparmlo",
         height="3", font="Arial,32,bold", bg="white").grid(row=2, column=1, sticky="NSEW")
    #Boton para que se cierre con picar el boton
    Entendido = Button(pop_up, text="Entendido",
                    height="3", width="15",
                    command=pop_up.destroy).grid(row=3, column=1, sticky="NSEW")
    
    #Imagen
    Label(pop_up, image=imagen_cheems, bg="white").grid(row=0, column=0, rowspan=4, sticky="NS")
    pop_ups.mainloop()
            
def registrar_bd(): #Funcion para el registro
    new_name = new_name_entry.get() #Obtencion de datos
    new_user = new_user_entry.get() #Obtencion de datos
    new_password = new_password_entry.get() #Obtencion de datos
    if len(new_name) == 0:
        messagebox.showwarning("Error", "Introduzca su(s) nombre(s)")
        return
    if len(new_user) == 0:
        messagebox.showwarning("Error", "Introduzca su nombre de usuario")
        return
        
    if len(new_password) == 0:
        messagebox.showwarning("Error", "Introduzca su contraseña")
        return
    try:
        has_error, error_msg = register(new_user, new_password)
        if has_error:
            messagebox.showwarning("Error", error_msg)
            return
    except:
        pop_ups("Hubo un error inesperado en el Registro")
        return
    new_name_entry.delete(first=0,last='end') #Se limpia
    new_user_entry.delete(first=0,last='end') #Se limpia despues del uso
    new_password_entry.delete(first=0,last='end') #Se limpia despues del uso
    pantalla_r.destroy()
    
#Funciones de Reservacion
def validar_reservacion_aux(id_cliente,fecha,hora,zona,cupos): #Por si se ocupa la reserva, validacion
    try:
        fecha=cal.get_date() #Variables y su asignacion de procedencia
        zona = seleccion_zona.get()
        hora = seleccion_hora.get()
        if uso_f == 0 or uso_h == 0 or uso_z == 0 or cupos == 0: #Si falta un campo no se reserva
            print("ERROR IF")
            messagebox.showwarning("Error", "Fallo en la reserva\nTiene uno o mas campos vacios")
        else:
            confirmacion, mensaje = validar_reservacion(id_cliente, fecha, hora, zona, cupos)
            if confirmacion:
                messagebox.showinfo("Éxito", mensaje) #Si esta todo, se reserva
            else:
                messagebox.showwarning("Error", mensaje)
            crear_rese.destroy()
    except:
        print("ERROR EXCEPT")
        messagebox.showwarning("Error", "Fallo en la reserva\nCuenta con uno o más campos vacios")

def Calendario():
    global fecha, calendario, cal
    calendario=Toplevel()
    calendario.title("Calendario")
    cal = Calendar(calendario, selectmode = 'day', 
            year = 2022, month = 5, 
            day = 24, locale ='es')
    cal.grid(pady = 20)
    def definir_fecha():
        global uso_f
        fecha=cal.get_date()
        calendario.destroy()
        uso_f=uso_f+1
        dia_rese = Button(crear_rese, text="Día: "+fecha,#Boton que indica zona de reservacion adentro
                    font="18,bold", bg= "#BCEBE0",
                    command=Calendario).grid(row=1, column=1, sticky="NSEW")
    Button(calendario, text="Definir Fecha", command=definir_fecha).grid()
def blanklabel(ventana): #Para no escribir mucho, esta funcion crea el salto de linea
    Label(ventana, text="").grid() #Lit crea una etiqueta en blanco que se puede usar para separar elementos
#Funciones para automatizar los escalados
def rowconfigure(ventana, row): #Escalado de filas, se requiere las filas que se usaran
    for x in range(row):
        Grid.rowconfigure(ventana,x,weight=1) #Da un peso que escala
def columnconfigure(ventana, column): #Escalado de columnas, se requiere las columnas que se usaran
    for x in range(column):
        Grid.columnconfigure(ventana,x,weight=1) #Da un peso que escala
    
inicio_sesion()
#app=aplication()