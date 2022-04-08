from tkinter import *
import os
import sys

sys.path.append('../')

from db import *

path_imagenes = os.getcwd() + '\imagenes' #Path en el equipo para la carpeta de imagenes

#Para insertar un platillo, se le pedirán al usuario todos los elementos,
#incluyendo el path de donde se encuentra contenida la imagen que desea insertar para el platillo

def insertar_Platillo_bd(path_imagen, precio, descripcion, nombre_platillo):
    
    with open(path_imagen, "rb") as file: 
        binarydata = file.read() #Leemos la imagen de forma binaria, porque en la BD es así como se guardan imgs

    statement = "Insert into Platillo (precio, descripcion, nombre_platillo, foto) VALUES (%s,%s,%s,%s)"
    cursor.execute(statement,(precio,descripcion,nombre_platillo, binarydata, )) #Todos los parámetros pasados con este formato tienen que ir en una sola tupla
    db.commit()

def select_Platillos_bd():

    statement = "Select * from Platillo"
    cursor.execute(statement)
    platillos = cursor.fetchall()

    return platillos

def ver_menu():
    
    global pantalla_menu_cliente, imagen
    pantalla_menu_cliente = Toplevel()
    pantalla_menu_cliente.title('Menú')
    pantalla_menu_cliente.geometry("1200x600")

    main_frame = Frame(pantalla_menu_cliente)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

    second_frame = Frame(my_canvas)

    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    Label(second_frame, text="Nombre", font=("Lato", 10), width=20).grid(column=0, row=0, padx=5, pady=8)
    Label(second_frame, text="Precio", font=("Lato", 10), width=10).grid(column=1, row=0, padx=5, pady=8)
    Label(second_frame, text="Descripción", font=("Lato", 10), width=50).grid(column=2, row=0, padx=5, pady=8)
    Label(second_frame, text="Imagen", font=("Lato", 10), width=50).grid(column=3, row=0, padx=5, pady=8)

    row = 1


def modificar_menu():
    
    global pantalla_mod_menu
    pantalla_mod_menu = Toplevel()
    pantalla_mod_menu.title('Modificar menú de platillos')
    pantalla_mod_menu.geometry('1000x600')

    frame_superior = Frame(pantalla_mod_menu)
    frame_superior.grid(column=0, row=0)

    frame_tabla = Frame(pantalla_mod_menu)
    frame_tabla.grid(column=0, row=1)





'''
platillos = select_Platillos_bd()

for platillo in platillos:
    nombre = platillo[3]
    id = platillo[0]
    descripcion = platillo[2]
    precio = platillo[1]
    imagen = platillo[4]

    print("Nombre: {}   id: {}   descripcion: {}    precio: {}".format(nombre, id, descripcion, precio))
    almacenar_en = path_imagenes + '\\{}.png'.format(id)

    with open(almacenar_en, "wb") as file:
        file.write(imagen)
        file.close()

 '''


