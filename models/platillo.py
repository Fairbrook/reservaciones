from msilib import text
from tkinter import *
from tkinter import filedialog
import os
import sys
from tkinter import messagebox
from tkinter.ttk import Style, Treeview
sys.path.append('../')

from db import *

path_imagenes = os.getcwd() + '\imagenes' #Path en el equipo para la carpeta de imagenes


#Primero declaramos las funciones que nos permiten realizar cambios o consultas sobre la BD
#El path de la imagen no será puesto directamente por el usuario, si no que será el resultado de que
#este elija la imagen mediante un explorador de archivos

def insertar_Platillo_bd(path_imagen, precio, descripcion, nombre_platillo):
    
    with open(path_imagen, "rb") as file: 
        binarydata = file.read() #Leemos la imagen de forma binaria, porque en la BD es así como se guardan imgs

    statement = "Insert into Platillo (precio, descripcion, nombre_platillo, foto) VALUES (%s,%s,%s,%s)"
    cursor.execute(statement,(precio,descripcion,nombre_platillo, binarydata, )) #Todos los parámetros pasados con este formato tienen que ir en una sola tupla
    db.commit()
    cursor.close()

def select_Platillos_bd():

    sql = "Select * from Platillo"
    cursor.execute(sql)
    platillos = cursor.fetchall()
    cursor.close()
    return platillos

def select_Platillos_Vista_sin_Img():

    sql = "Select (id_platillo, nombre_platillo, descripcion, precio) from Platillo"
    cursor.execute(sql)
    platillos = cursor.fetchall()
    cursor.close()
    return platillos

def borrar_platillo(id_eliminar):

    sql = "Delete from Platillo where id_platillo = {}".format(id_eliminar)
    cursor.execute(sql)
    db.commit()
    cursor.close()

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

  #--------------Funciones que se necesitarán para interactuar con la tabla y los registros en esta sección----------
    
    #Función para obtener info del registro en dicha fila
    def obtener_fila_tabla():
        current_item = tabla.focus()
        if not current_item:
            return
        global data_seleccionada, id_borrar
        data_seleccionada = tabla.item(current_item)
        id_borrar = data_seleccionada['values'][0]
    
    def borrar_platillo():
        fila = tabla.selection()

        if len(fila) !=0:        
            tabla.delete(fila)
            id = ("'"+ str(id_borrar) + "'")       
            borrar_platillo(id)
    
    def escoger_imagen():

        path_imagen = filedialog.askopenfilename(initialdir="/", title="Seleccione una imagen para el platillo", filetypes=(("Archivos png", "*.png"),))
        

    def agregar_platillo():

        print("Nombre: ",entry_nombre.get())
        print("Precio: ",entry_precio.get())
        print("Imagen: ", path_imagen)
        print(texto_descripcion.get(1.0, "end"))

#---------------------------------------------------------------------------------------------------------------------
    
    global pantalla_mod_menu
    pantalla_mod_menu = Toplevel()
    pantalla_mod_menu.title('Modificar menú de platillos')
    pantalla_mod_menu.geometry('1000x600')

    frame_superior = Frame(pantalla_mod_menu)
    frame_superior.grid(column=0, row=0)

    Label(frame_superior, text= "Agregar platillo", font=("Lato", 12)).grid(column=0, row=0, pady=10, padx=420)

    frame_botones = Frame(pantalla_mod_menu)
    frame_botones.grid(column=0, row=1, pady=10)

    frame_inferior = Frame(pantalla_mod_menu)
    frame_inferior.grid(column=0, row= 3)

    Button(frame_inferior, text = "Eliminar platillo seleccionado", bg = "red", fg = "white", font=("Lato", 10)).grid(column=0, row=0,pady=5,padx=5)
    Button(frame_inferior, text = "Visualizar carta de menú actual", bg = "yellow", fg = "black", font=("Lato", 10)).grid(column=1, row=0,pady=5,padx=5)

    entry_nombre = StringVar()
    entry_precio = StringVar()
    global path_imagen
    path_imagen = ""
    
    Label(frame_botones, text = "Nombre platillo: ", font=("Lato", 10)).grid(column=0, row=0, padx=5)
    Entry(frame_botones, textvariable=entry_nombre, width=20, font=("Lato", 10)).grid(column=1, row=0, padx=5)
    Label(frame_botones, text = "Descripción: ", font=("Lato", 10)).grid(column=2, row=0, padx=5)

    texto_descripcion = Text(frame_botones, height=2, width=28, font=("Lato", 10))
    texto_descripcion.grid(column=3, row=0, padx=5)

    Label(frame_botones, text = "Precio $: ", font=("Lato", 10)).grid(column=4, row=0, padx=5)
    Entry(frame_botones, textvariable=entry_precio, width=20, font=("Lato", 10)).grid(column=5, row=0, padx=5)
    Label(frame_botones, text =  "Seleccionar foto ", font=("Lato", 10)).grid(column=0, row=1, padx=10, pady=20)
    Button(frame_botones, text="Seleccionar archivo", font=("Lato", 10), bg= "#47525E", fg="white", command=escoger_imagen).grid(
        column=1, row=1, padx=10, pady=20)
    Button(frame_botones, text = "Agregar platillo", font = ("Lato", 10), bg = "green", fg = "white", width=25, command=agregar_platillo).grid(
        column=3, row=1, padx=10, pady=20, columnspan=2)
    


    #Comenzamos a configurar espacio y aspectos de la tabla
    frame_tabla = Frame(pantalla_mod_menu)
    frame_tabla.grid(column=0, row=2)

    tabla = Treeview(frame_tabla, height=15)
    tabla.grid(column=0, row=0, pady=10, padx=30)

    ladoy = Scrollbar(frame_tabla, orient =VERTICAL)
    ladox = Scrollbar(frame_tabla, orient= HORIZONTAL)
    ladox.grid(column=0, row = 1, sticky='ew') 
    ladoy.grid(column = 1, row = 0, sticky='ns')

    tabla.config(yscrollcommand = ladoy.set)
    tabla.config(xscrollcommand= ladox.set)
    ladoy.config(command=tabla.yview)
    ladox.config(command=tabla.xview)
    
    tabla['columns'] = ('ID_platillo','Nombre', 'Descripcion', 'Precio')

    #Acomodo y espaciado de columnas
    tabla.column('#0', minwidth=0, width=0, anchor='center')
    tabla.column('ID_platillo', minwidth=100, width=20 , anchor='center')
    tabla.column('Nombre', minwidth=100, width=300 , anchor='center')
    tabla.column('Descripcion', minwidth=100, width=480, anchor='center' )
    tabla.column('Precio', minwidth=100, width=100 , anchor='center')

    #Damos nombres a headers de columnas
    tabla.heading('ID_platillo', text='ID_platillo', anchor ='center')
    tabla.heading('Nombre', text='Nombre', anchor ='center')
    tabla.heading('Descripcion', text='Descripción', anchor ='center')
    tabla.heading('Precio', text='Precio', anchor ='center')

    #Damos diseño a columna
    estilo = Style(frame_tabla)
    estilo.theme_use('clam') 
    estilo.configure(".",font= ('lato', 10, 'bold'), foreground='black')        
    estilo.configure("Treeview", font= ('lato', 10, 'bold'), foreground='black',  background='white')
    estilo.map('Treeview',background=[('selected', 'lato')], foreground=[('selected','green')] )

    tabla.bind("<<TreeviewSelect>>", obtener_fila_tabla)  #Conectamos a la tabla con una función para obtener los datos de la fila seleccionada

    




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


