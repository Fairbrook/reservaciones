# -*- coding: utf-8 -*-

import tkinter
from tkinter import  messagebox
import os
from tkinter import *
import hashlib
from models.administrador import login_admin

from models.usuario import login, register
from models.platillo import ver_menu, modificar_menu

def inicio_sesion(): #pantalla al iniciar el programa, se encontrara el inicio de sesion
    global pantalla, user_verify, password_verify, user_entry, password_entry #variables globales
    global rol, cupos, reserva, estrellas #variables globales
    pantalla=Tk() #declaramos la pantalla principal
    pantalla.geometry("300x350") #tamaño de ventana
    pantalla.title("Login") #titulo de ventana
    user_verify=StringVar() #indicamos el tipo de variable
    password_verify=StringVar() #indicamos el tipo de variable
    cupos=IntVar() #indicamos el tipo de variable
    reserva=IntVar() #indicamos el tipo de variable
    
    cupos=10 #inicializamos (TEMPORALES PARA PRUEBAS)
    estrellas=5 #limite de estrellas a dar
    reserva=0
    
    #Label = etiqueta
    Label(pantalla, text="Ingrese su usuario y constraseña", bg="medium aquamarine", font="Arial,16,bold").pack()
    #Salto de linea para dar espacio
    Label(pantalla, text="").pack()

    #Entrada para dar un usuario
    Label(pantalla, text="Usuario:").pack()
    user_entry = Entry(pantalla, textvariable=user_verify, width="25")
    user_entry.pack()
    
    #Entrada para dar la contraseña, el show es un minicifrado visual
    Label(pantalla, text="Contraseña:").pack()
    password_entry = Entry(pantalla, show="*", textvariable=password_verify, width="25")
    password_entry.pack()

    #boton para iniciar sesion
    Label(pantalla, text="").pack()
    Button(pantalla, text='Iniciar Sesión', height="2", width="20", command=validar).pack()

    #boton para registrar
    Label(pantalla, text="").pack()
    Button(pantalla, text='¿No tienes cuenta? \n Registrate!', height="3", width="20", command=registro).pack()  

   #depuramos la pantalla como iniciador del programa 
    pantalla.mainloop()
    
def registro(): #Se despliega encima de iniciar sesion para dar un registro
    global pantalla_r, new_user, new_password
    pantalla_r = Toplevel(pantalla) #pantalla_r = pantalla registro
    pantalla_r.geometry("300x350")
    pantalla_r.title("Registro")
    user_entry.delete(first=0,last='end') #limpiamos campos
    password_entry.delete(first=0,last='end')
    
    Label(pantalla_r, text="Ingrese los datos para el registro", font="bold").pack()
    Label(pantalla_r, text="").pack()

    #Pide el nuevo usuario
    Label(pantalla_r, text="Usuario:").pack()
    new_user = Entry(pantalla_r, textvariable=user_verify, width="25")
    new_user.pack()

    #Pide la contraseña
    Label(pantalla_r, text="Contraseña:").pack()
    new_password = Entry(pantalla_r, show="*", textvariable=password_verify, width="25")
    new_password.pack()
    Label(pantalla_r, text="").pack()

    #Registra al nuevo usuario y contraseña
    Button(pantalla_r, text='REGISTRAR', height="3", width="20", command=registrar_bd).pack()
    
def menu_cliente(): #Menu a desplegar a todos estos usuarios de tipo cliente
    global pantalla_mc #Pantalla_mc = pantalla menu cliente 
    #pantalla.withdraw() #Cerramos la ventana de inicio de sesion
    pantalla_mc = Toplevel(pantalla) #Que aparezca encima de la de inicio de sesion
    imagen=PhotoImage(file="logop.png") #Importamos el Logo de nuestro equipo
    imagen.subsample(2,2) #No me acuerdo, pero es de la imagen
    pantalla_mc.geometry("300x500")
    pantalla_mc.title("Menu")
    
    #Los siguientes cuatro Button son para los botones que redirigen a los menus correspondientes al nombre
    #Boton llamado info (informacion) y sus caracteristicas
    info = Button(pantalla_mc, text="Informacion", 
                  height="3", width="300",
                  command=ver_info).pack()
    Label(pantalla_mc, text="").pack()
    #Boton llamado reserva y sus caracteristicas
    reserva = Button(pantalla_mc, text="Reservar",
                     height="3", width="300",
                     command=lambda:menu_reservaciones(0)).pack()
    Label(pantalla_mc, text="").pack()
    #Boton llamado calificar y sus caracteristicas
    calificar = Button(pantalla_mc, text="Calificar",
                       height="3", width="300",
                       command=lambda:menu_calificacion(0)).pack()
    Label(pantalla_mc, text="").pack()
    #Boton llamado menu y sus caracteristicas
    menu = Button(pantalla_mc, text="Menu",
                       height="3", width="300",
                       command=ver_menu).pack()                 
    Label(pantalla_mc, text="").pack()

    #Imagen de nuestro equipo
    Label(pantalla_mc, image=imagen).pack()

    pantalla_mc.mainloop()
    
def menu_admin(): #Menu a desplegar al usuario de tipo admin
    global pantalla_ma #pantalla_ma = pantalla menu admin
    #pantalla.withdraw()
    pantalla_ma = Toplevel(pantalla) #Aparece encima del inicio de sesion
    imagen=PhotoImage(file="logop.png")   #Importamos la imagen del equipo
    pantalla_ma.geometry("300x450")
    pantalla_ma.title("Administrador")
        
    #Texto lamebotas
    Label(pantalla_ma, text="Bienvenido Admin :D", 
          bg="medium aquamarine").pack

    #Igual, 4 bototones para las weas de acciones
    #Boton de informacion
    info = Button(pantalla_ma, text="Modificar\ninformación", 
                  height="3", width="300",
                  command=modificar_info).pack()
    Label(pantalla_ma, text="").pack()
    #Boton de reservaciones
    reserva = Button(pantalla_ma, text="Reservaciones",
                     height="3", width="300",
                     command=lambda:menu_reservaciones(1)).pack()
    Label(pantalla_ma, text="").pack()
    #Boton de calificaciones
    calificar = Button(pantalla_ma, text="Calificaciones",
                       height="3", width="300",
                       command=lambda:menu_calificacion(1)).pack()
    Label(pantalla_ma, text="").pack()
    #Boton de menu de comida
    menu = Button(pantalla_ma, text="Modificar menú",
                       height="3", width="300",
                       command=modificar_menu).pack()                   
    Label(pantalla_ma, text="").pack()

    #Cargamos la imagen en la ventana
    Label(pantalla_ma, image=imagen).pack()
    
    pantalla_ma.mainloop()

def ver_info():#Funcion para ver la informacion

    global pantalla_viewinfo #Variables globales

    pantalla_viewinfo = Toplevel() #Que aparezca encima de cualquier menu
    pantalla_viewinfo.geometry("590x600")
    pantalla_viewinfo.config(bg="white") #Fondo de la ventana
    pantalla_viewinfo.title("Visualizar información")
    pantalla_viewinfo.resizable(0,0)

    #Se declara un frame de fondo blanco
    frame_titulo = Frame(pantalla_viewinfo, bg = "white") 
    frame_titulo.grid(column=0,row=0)
    #Etiqueta de titulo del frame
    Label(frame_titulo, text="Información", font=("Arial", 20), fg="navy blue", bg="white").grid(column=0,row=0, padx=150, pady=10)

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
    
    texto_info.config(state='disabled') #El usuario no puede hacerle nada al texto, solo se muestra


def modificar_info(): #Funcion para el administrador, con el cual podra modificar el archivo
    #COnfiguracion previa al crear la ventana
    global pantalla_modificar_info 
    pantalla_modificar_info = Toplevel()
    pantalla_modificar_info.geometry("590x650")
    pantalla_modificar_info.config(bg="white")
    pantalla_modificar_info.title("Modificar información")
    pantalla_modificar_info.resizable(0,0)
    pantalla_modificar_info = Frame(pantalla_modificar_info, bg = "white")
    pantalla_modificar_info.grid(column=0,row=0)
    Label(pantalla_modificar_info, text="Información", font=("Arial", 20), fg="navy blue", bg="white").grid(column=0,row=0, padx=150, pady=10)

    #Se crea el frame donde se modificara la informacion
    frame_info = Frame(pantalla_modificar_info, bg= "white")
    frame_info.grid(column=0, row=1)
    frame_boton = Frame(pantalla_modificar_info, bg="white")
    frame_boton.grid(column=0, row=2)

    #Texto que contendra el frame
    texto_info = Text(frame_info, height=30, width=70, font=("Lato", 10))
    texto_info.grid(column=0,row=0, padx=20,pady=10)

    #Implementacion de la barra de scroll tanto vertical como horizontal
    ladoy = Scrollbar(frame_info, orient =VERTICAL)
    ladox = Scrollbar(frame_info, orient= HORIZONTAL)
    #Espaciado entre las casillas de la tabla
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
    
    #Funcion para modificar la informacion que esta mostrada
    def actualizar_info():
        archivo = open("informacion.txt", 'w') #W de write
        nuevo_texto = texto_info.get(1.0, "end")
        archivo.write(nuevo_texto)

    #Botones para ejecutar las dos funciones previas
    Button(frame_boton, text = "Actualizar info", bg= "#47525E", fg="white", command=actualizar_info).grid(column=0, row=0, pady=5, padx=5)
    Button(frame_boton, text = "Mostrar info", bg= "#47525E", fg="white", command=mostrar_info_actual).grid(column=1, row=0, pady=5, padx=5)

                    
    
def menu_reservaciones(user): #Funcion que despliega el menu de reservaciones, recibe como parametro la id del usuario
    global pantalla_rese
    if user==1: #1 es de admin, probablemente dependiendo de la BD cambiara a ser una funcion aparte
        pantalla_rese = Toplevel(pantalla_ma) #Encima de la pantalla de menu admin
    else: #else de cliente (TEMPORAL)
        pantalla_rese = Toplevel(pantalla_mc) #Encima de la pantalla de menu cliente
    pantalla_rese.geometry("300x350")
    pantalla_rese.title("Reservacion")
    
    if user!=1: #Si el usuario es cualquier cliente 
        #Se crean los botones de las funciones de reservar
        Button(pantalla_rese, text="Reservar",
               height="3", width="300",
               command=crear_reservacion).pack() #Boton de Crear reservacion
        Label(pantalla_rese, text="").pack()
        Button(pantalla_rese, text="Ver mi reservacion",
               height="3", width="300",
               command=ver_reservacion).pack() #Boton de Ver reservacion
        Label(pantalla_rese, text="").pack()
        Button(pantalla_rese, text="Cancelar reservacion",
               height="3", width="300").pack() #Boton de Borrar reservacion
        Label(pantalla_rese, text="").pack()
        Button(pantalla_rese, text="Obtener codigo", 
               height="3", width="300", command=codigo_reservacion).pack() #Boton Obtener el Codigo QR
        Label(pantalla_rese, text="").pack()
    else:
        #Botones para el admin relacionados con reservar
        Button(pantalla_rese, text="Ver reservaciones",
               height="3", width="300").pack() #Boton para Ver las reservaciones totales
        Label(pantalla_rese, text="").pack()
    volver = Button(pantalla_rese, text="Volver",
                    height="2", width="15",
                    command=pantalla_rese.destroy).pack(side="bottom") #Boton para regresar al menu de opciones

def codigo_reservacion(): #Funcion para obtener el codigo QR de la reservacion (TRATAR DE HACER UN GENERADOR)
    global qr, reserva 
    qr = Toplevel(pantalla_rese) #Encima de la ventana de reservaciones
    imagen_codigo=PhotoImage(file="QR.gif") #Importamos la imagen
    image=imagen_codigo.subsample(2,2)
    qr.geometry("200x200")
    qr.title("Codigo de reservacion")
    
    if reserva==0: #TEMPORAL comprobamos si tiene una reserva, sino se despliega un pop up de error
        Label(qr, text="No tiene una reserva").pack()
            #Falta el pop up ;p
    else:
        Label(qr, image=imagen_codigo).pack() #Si tiene reserva, se muestra el QR
    
    qr.mainloop() #Lo hacemos mainloop para que se muestre la imagen, se elimina al destruir la ventana al parecer
    
    
def crear_reservacion(): #Funcion para crear la reservacion
    global crear_rese, reserva
    crear_rese = Toplevel(pantalla_rese) #Encima de la ventana de reservaciones
    crear_rese.geometry("300x300")
    crear_rese.title("Crear reservacion")
    
    Label(crear_rese, text="¿Cuantas mesas ocupara?", 
          font="15,bold").grid(column=1) #Texto de pregunta
    Label(crear_rese, text="Existen: "+str(cupos)+" disponibles",
          font="15,bold").grid(column=1) #Muestra los cupos disponibles

    #Una etiqueta con dos botones adyacentes para subir o disminuir el numero de cupos a reservar
    mostrar_cupos = Label(crear_rese, text=str(cupos),
                          height="2", width="4",
                          font="18").grid(row=3, column=1) #Estara en el centro, son los cupos existentes
    
    def cupos_disp(operacion): #Funcion para ver los cupos disponibles y delimitar los botones
        global cupos
        if operacion==0 and cupos>0: #Si es 0 o menor no se puede disminuir
            cupos=cupos-1
            mostrar_cupos = Label(crear_rese, text=str(cupos),
                                  height="2", width="4",
                                  font="18").grid(row=3, column=1) #muestra los cupos 
        elif operacion==1 and cupos<10: #Si es 10 o mas no se puede aumentar
            cupos=cupos+1
            mostrar_cupos = Label(crear_rese, text=str(cupos),
                                  height="2", width="4",
                                  font="18").grid(row=3, column=1) #muestra los cupos
    
    resta = Button(crear_rese, text="-",
                   height="2", width="4",
                   font="18", command=lambda:cupos_disp(0)).grid(row=3, column=0, padx=3) #Boton de resta
    suma = Button(crear_rese, text="+",
                  height="2", width="4",
                  font="18", command=lambda:cupos_disp(1)).grid(row=3, column=2) #Boton de suma
    reservar = Button(crear_rese, text="RESERVAR",
                      heigh="3",
                      font="18", command=ocupar).grid(row=5, column=1) #Boton para reservar y finalizar
    
def ver_reservacion(): #Funcion para Ver la Reservacion
    global ver_rese, reserva #ver rese = pantalla de ver reserva
    ver_rese = Toplevel(pantalla_rese) #Encima de la ventana de reservaciones
    ver_rese.geometry("300x300")
    ver_rese.title("Ver reservacion")
    
    if reserva==0: #No existe reservacion
        Label(ver_rese, text="No tiene una reserva").pack() #se cambiara a un pop up
    else:
        Label(ver_rese, text="Su reserva es:").pack() #pop up donde se muestra la info PROXUMAMENTE
    
def menu_calificacion(user): #Interfaz de las calificaciones
    global pantalla_cali #pantalla cali = pantalla calificaciones
    if user==1: #Si es admin
        pantalla_cali = Toplevel(pantalla_ma)
    else: #Si es cliente
        pantalla_cali = Toplevel(pantalla_mc)
    pantalla_cali.geometry("300x300")
    pantalla_cali.title("Calificacion")
    
    if user!=1: #Si el usuario no es admin se muestra la opcion de calificar
        Button(pantalla_cali, text="Calificar",
               height="3", width="300",
               command=crear_calificacion).pack()
        Label(pantalla_cali, text="").pack()

    Button(pantalla_cali, text="Ver calificacion",
           height="3", width="300").pack() #Boton para ver la calificacion
    Label(pantalla_cali, text="").pack()

    puntuacion = Label(pantalla_cali, text="...").pack() #Promedio de calificacion no visible
    Label(pantalla_cali, text="").pack()

    Button(pantalla_cali, text="Ver Opiniones",
           height="3", width="300").pack() #Boton para ver las opiniones
    Label(pantalla_cali, text="").pack()

    volver = Button(pantalla_cali, text="Volver",
                    height="2", width="15",
                    command=pantalla_cali.destroy).pack(side="bottom") #Boton para regresar al menu de opciones

def crear_calificacion():
    global pantalla_crear_cali, new_opinion #pantalla_crear_cali = pantalla crear calificacion
    pantalla_crear_cali = Toplevel(pantalla_cali)
    pantalla_crear_cali.geometry("290x300")
    pantalla_crear_cali.title("Crear Calificacion")

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
                   font="18", command=lambda:dar_puntos(0)).grid(row=3, column=0, padx=3) #Boton de resta
    suma = Button(pantalla_crear_cali, text="+",
                  height="2", width="4",
                  font="18", command=lambda:dar_puntos(1)).grid(row=3, column=2) #Boton de suma

    Label(pantalla_crear_cali, text="").grid(column=0, columnspan=3)
    Label(pantalla_crear_cali, text="Comentario:",
          font="15,bold").grid(column=0, columnspan=3)
    new_opinion = Entry(pantalla_crear_cali, textvariable=user_verify, width="30")
    new_opinion.grid(column=1)
    Label(pantalla_crear_cali, text="").grid(column=0, columnspan=3)

    submit = Button(pantalla_crear_cali, text="Registrar calificacion",
                    height="3", width="20",
                    command=pantalla_crear_cali.destroy).grid(column=1)
    Label(pantalla_crear_cali, text="").grid(column=0, columnspan=3)
    
    volver = Button(pantalla_crear_cali, text="Volver",
                    height="2", width="15",
                    command=pantalla_crear_cali.destroy).grid(column=1) #Boton para regresar al menu de calificar
    


# Funcion para hacer validaciones e iniciar sesión
def validar(): 

    
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
            menu_cliente()
        else:
        #Inicio sesion admin
          admin = login_admin(usuariovalidar,contraseñavalidar)
        #revisamos si hay concidencias
          if len(admin) != 0:    
        #si hay concidencias se muestra el menu de admin
            pantalla.iconify()
            menu_admin()
          elif user == None:
            messagebox.showwarning("Error", "Usuario y/o contrseña incorrectos")
    except:
        messagebox.showwarning("Error", "Hubo un error inesperado")
        return
   

        
def pop_ups(texto): #Funcion para los pop ups
    global pop_up
    pop_up = Toplevel() #Encima de cualquier cosa
    imagen_cheems=PhotoImage(file="cheems.png") #Importamos la imagen
    image=imagen_cheems.subsample(2,2)
    pop_up.geometry("550x330")
    pop_up.title("Errorm")
    pop_up.configure(bg="white") #fondo blanco limdom
    
    #Ponemos la label en la segunda columna, para que en la primera este la imagen
    Label(pop_up, text="¡Oh no!", height="3",
         font="Arial,48,bold", bg="white").grid(row=0, column=1)
    Label(pop_up, text="Emcomtramste el errorm:\n"+str(texto),
         height="3", font="Arial,32,bold", bg="white").grid(row=1, column=1)
    Label(pop_up, text="Emstamos trabajandom\npara remparmlo",
         height="3", font="Arial,32,bold", bg="white").grid(row=2, column=1)

    #Boton para que se cierre con picar el boton
    Entendido = Button(pop_up, text="Entendido",
                    height="3", width="15",
                    command=pop_up.destroy).grid(row=3, column=1)
    
    #Imagen
    Label(pop_up, image=imagen_cheems, bg="white").grid(row=0, column=0, rowspan=4)

    pop_up.mainloop()


            
def registrar_bd(): #Funcion para el registro

    user_name = new_user.get() #Obtencion de datos
    if len(user_name) == 0:
        messagebox.showwarning("Error", "Introduzca su nombre de usuario")
        return

    password = new_password.get() #Obtencion de datos
    if len(password) == 0:
        messagebox.showwarning("Error", "Introduzca su contraseña")
        return

    try:
        has_error, error_msg = register(user_name, password)
        if has_error:
            messagebox.showwarning("Error", error_msg)
            return
    except:
        messagebox.showwarning("Error", "Hubo un error inesperado")
        return

    user_entry.delete(first=0,last='end') #Se limpia
    password_entry.delete(first=0,last='end') #Se limpia despues del uso
    pantalla_r.destroy()
    
def ocupar(): #POr si se ocupa la reserva, calidacion
    global reserva
    reserva=reserva+1
    
    
inicio_sesion()
#app=aplication()