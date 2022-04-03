# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 09:56:58 2021

@author: Oscar
"""

import tkinter
from tkinter import *
import re

def inicio_sesion():
    global pantalla, user_verify, password_verify, user_entry, password_entry, rol, cupos, reserva
    pantalla=Tk()
    pantalla.geometry("300x350")
    pantalla.title("Login")
    user_verify=StringVar()
    password_verify=StringVar()
    cupos=IntVar()
    reserva=IntVar()
    
    cupos=10
    reserva=0
    
    Label(pantalla, text="Ingrese su usuario y constraseña", bg="medium aquamarine", font="Arial,16,bold").pack()
    Label(pantalla, text="").pack()
    Label(pantalla, text="Usuario:").pack()
    user_entry = Entry(pantalla, textvariable=user_verify, width="25")
    user_entry.pack()
    Label(pantalla, text="Contraseña:").pack()
    password_entry = Entry(pantalla, show="*", textvariable=password_verify, width="25")
    password_entry.pack()
    Label(pantalla, text="").pack()
    Button(pantalla, text='Iniciar Sesión', height="2", width="20", command=lambda:validar(1)).pack()
    Label(pantalla, text="").pack()
    Button(pantalla, text='¿No tienes cuenta? \n Registrate!', height="3", width="20", command=registro).pack()  
    
    pantalla.mainloop()
    
def registro():
    global pantalla_r, new_user, new_password
    pantalla_r = Toplevel(pantalla)
    pantalla_r.geometry("300x350")
    pantalla_r.title("Registro")
    user_entry.delete(first=0,last='end')
    password_entry.delete(first=0,last='end')
    
    Label(pantalla_r, text="Ingrese los datos para el registro", font="bold").pack()
    Label(pantalla_r, text="").pack()
    Label(pantalla_r, text="Usuario:").pack()
    new_user = Entry(pantalla_r, textvariable=user_verify, width="25")
    new_user.pack()
    Label(pantalla_r, text="Contraseña:").pack()
    new_password = Entry(pantalla_r, show="*", textvariable=password_verify, width="25")
    new_password.pack()
    Label(pantalla_r, text="").pack()
    Button(pantalla_r, text='REGISTRAR', height="3", width="20", command=registrar_bd).pack()
    
def menu_cliente():
    global pantalla_mc
    pantalla_mc = Toplevel(pantalla)
    imagen=PhotoImage(file="logop.png")
    imagen.subsample(2,2)
    pantalla_mc.geometry("300x500")
    pantalla_mc.title("Menu")
    
    info = Button(pantalla_mc, text="Informacion", 
                  height="3", width="300",
                  command=lambda:menu_informacion(0)).pack()
    Label(pantalla_mc, text="").pack()
    reserva = Button(pantalla_mc, text="Reservar",
                     height="3", width="300",
                     command=lambda:menu_reservaciones(0)).pack()
    Label(pantalla_mc, text="").pack()
    calificar = Button(pantalla_mc, text="Calificar",
                       height="3", width="300",
                       command=lambda:menu_calificacion(0)).pack()
    Label(pantalla_mc, text="").pack()
    menu = Button(pantalla_mc, text="Menu",
                       height="3", width="300",
                       command=lambda:menu_calificacion(0)).pack()
                       
    Label(pantalla_mc, text="").pack()
    Label(pantalla_mc, image=imagen).pack()

    pantalla_mc.mainloop()
    
def menu_admin():
    global pantalla_ma
    pantalla_ma = Toplevel(pantalla)
    imagen=PhotoImage(file="logop.png")   
    pantalla_ma.geometry("300x350")
    pantalla_ma.title("Administrador")
        
    Label(pantalla_ma, text="Bienvenido Admin :D", 
          bg="medium aquamarine").pack
    info = Button(pantalla_ma, text="Informacion", 
                  height="3", width="300",
                  command=lambda:menu_informacion(1)).pack()
    Label(pantalla_ma, text="").pack()
    reserva = Button(pantalla_ma, text="Reservar",
                     height="3", width="300",
                     command=lambda:menu_reservaciones(1)).pack()
    Label(pantalla_ma, text="").pack()
    calificar = Button(pantalla_ma, text="Calificar",
                       height="3", width="300",
                       command=lambda:menu_calificacion(1)).pack()
    Label(pantalla_ma, text="").pack()
    Label(pantalla_ma, image=imagen).pack()
    
    pantalla_ma.mainloop()

def menu_informacion(user):
    global pantalla_info
    if user==1:
        pantalla_info = Toplevel(pantalla_ma)
    else:
        pantalla_info = Toplevel(pantalla_mc)
    pantalla_info.geometry("300x600")
    pantalla_info.title("Informacion")
    
    Label(pantalla_info, text="").pack()
    volver = Button(pantalla_info, text="Volver",
                    height="2", width="15",
                    command=pantalla_info.destroy).pack(side="bottom")
    
def menu_reservaciones(user):
    global pantalla_rese
    if user==1:
        pantalla_rese = Toplevel(pantalla_ma)
    else:
        pantalla_rese = Toplevel(pantalla_mc)
    pantalla_rese.geometry("300x350")
    pantalla_rese.title("Reservacion")
    
    if user!=1:
        Button(pantalla_rese, text="Reservar",
               height="3", width="300",
               command=crear_reservacion).pack()
        Label(pantalla_rese, text="").pack()
        Button(pantalla_rese, text="Ver mi reservacion",
               height="3", width="300",
               command=ver_reservacion).pack()
        Label(pantalla_rese, text="").pack()
        Button(pantalla_rese, text="Cancelar reservacion",
               height="3", width="300").pack()
        Label(pantalla_rese, text="").pack()
        Button(pantalla_rese, text="Obtener codigo",
               height="3", width="300", command=codigo_reservacion).pack()
        Label(pantalla_rese, text="").pack()
    else:
        Button(pantalla_rese, text="Ver reservaciones",
               height="3", width="300").pack()
        Label(pantalla_rese, text="").pack()
    volver = Button(pantalla_rese, text="Volver",
                    height="2", width="15",
                    command=pantalla_rese.destroy).pack(side="bottom")

def codigo_reservacion():
    global qr, reserva
    qr = Toplevel(pantalla_rese)
    imagen_codigo=PhotoImage(file="QR.gif")
    image=imagen_codigo.subsample(2,2)
    qr.geometry("200x200")
    qr.title("Codigo de reservacion")
    
    if reserva==0:
        Label(qr, text="No tiene una reserva").pack()
    else:
        Label(qr, image=imagen_codigo).pack()
    
    qr.mainloop()
    
    
def crear_reservacion():
    global crear_rese, reserva
    crear_rese = Toplevel(pantalla_rese)
    crear_rese.geometry("300x300")
    crear_rese.title("Crear reservacion")
    
    Label(crear_rese, text="¿Cuantas mesas ocupara?",
          font="15,bold").grid(column=1)
    Label(crear_rese, text="Existen: "+str(cupos)+" disponibles",
          font="15,bold").grid(column=1)
    mostrar_cupos = Label(crear_rese, text=str(cupos),
                          height="2", width="4",
                          font="18").grid(row=3, column=1)
    
    def cupos_disp(operacion):
        global cupos
        if operacion==0 and cupos>0:
            cupos=cupos-1
            mostrar_cupos = Label(crear_rese, text=str(cupos),
                                  height="2", width="4",
                                  font="18").grid(row=3, column=1)
        elif operacion==1 and cupos<10:
            cupos=cupos+1
            mostrar_cupos = Label(crear_rese, text=str(cupos),
                                  height="2", width="4",
                                  font="18").grid(row=3, column=1)
    
    resta = Button(crear_rese, text="-",
                   height="2", width="4",
                   font="18", command=lambda:cupos_disp(0)).grid(row=3, column=0, padx=3)
    suma = Button(crear_rese, text="+",
                  height="2", width="4",
                  font="18", command=lambda:cupos_disp(1)).grid(row=3, column=2)
    reservar = Button(crear_rese, text="RESERVAR",
                      heigh="3",
                      font="18", command=ocupar).grid(row=5, column=1)
    
def ver_reservacion():
    global ver_rese, reserva
    ver_rese = Toplevel(pantalla_rese)
    ver_rese.geometry("300x300")
    ver_rese.title("Ver reservacion")
    
    if reserva==0:
        Label(ver_rese, text="No tiene una reserva").pack()
    else:
        Label(ver_rese, text="Su reserva es:").pack()
    
def menu_calificacion(user):
    global pantalla_cali
    if user==1:
        pantalla_cali = Toplevel(pantalla_ma)
    else:
        pantalla_cali = Toplevel(pantalla_mc)
    pantalla_cali.geometry("300x250")
    pantalla_cali.title("Calificacion")
    
    if user!=1:
        Button(pantalla_cali, text="Calificar",
               height="3", width="300").pack()
        Label(pantalla_cali, text="").pack()
    Button(pantalla_cali, text="Ver calificacion",
           height="3", width="300").pack()
    Label(pantalla_cali, text="").pack()
    puntuacion = Label(pantalla_cali, text="...").pack()
    Label(pantalla_cali, text="").pack()
    volver = Button(pantalla_cali, text="Volver",
                    height="2", width="15",
                    command=pantalla_cali.destroy).pack(side="bottom")
    
def validar(numero):
    if numero==1: #1 para el inicio de sesion
        usuariovalidar=user_entry.get()
        contraseñavalidar=password_entry.get()
        if usuariovalidar=="admin" and contraseñavalidar=="admin":
            menu_admin()
        else:
            menu_cliente()
            
def registrar_bd():
    new_user.get()
    new_password.get()
    user_entry.delete(first=0,last='end')
    password_entry.delete(first=0,last='end')
    pantalla_r.destroy()
    
def ocupar():
    global reserva
    reserva=reserva+1
    
    
inicio_sesion()
app=aplication()