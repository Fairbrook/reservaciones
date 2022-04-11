# Proyecto de Ingeniería de Software __Reservaciones__

## Instalación de paquetes

El proyecto depende de múltiples librerías que están anotadas en requirements.txt y se pueden instalar con el siguiente comando

```
pip install -r requirements.txt
```

## Conección a la base de datos

Require un archivo .env en el root del proyecto con la siguiente forma

```
DB_USER=root
DB_PASSOWRD=
DB_HOST=127.0.0.1
DB_NAME=sistema_de_reservacion
```

## Creación de la base de datos

Para importar la base de datos, ejecuta el siguiente [Archivo SQL](https://drive.google.com/file/d/1SXEGZyuXuLekG3hM2PDAz7rPDBrtGa8U/view?usp=sharing)

## Credenciales para administrador

Para acceder al menu de administrador
ingrese

```
usuario: admin
contraseña: masterd10
```

## Funciones fronted

```
FrontEnd Equipo AmazonII

1.- Menu de inicio:
	-acceso normal para probar
	-user: admin, password: admin para el acceso al admin
2.-Registro:
	Solo picale a registrar para entrar en este modo nwn, en si es ejemplo para ver que sirva
3.-Menús
	-El de cliente
	-El de admin
	Contiene opciones de accion + el logotipo del equipo
4.-Informacion
	-El cliente ve la informacion
	-El admin modificara la info y se guardara al salir(no implementado, usaremos un .txt)
5.-Reservas
	5.1 Crear Reserva:
		-10 Cupos, estos se cambiaran por dos botones de + y -
		-Hay limites de 0 o maximo de cupos(falta lo ultimo y el tope es 10 temporalmente)
		-Al dar reservar desbloque nuevas funciones del menu reservas
	5.2 Ver Reserva:
		-Si no hay reserva muestra que no existe
		-Si hay una muestra "existe una"
	5.3 Cancelar Reserva:
		Crea un pop up dependiendo si:
		-Tiene reserva, Que ya la cancelo
		-No tiene, Eres tonto, reserva para cancelar
	5.4 Codigo QR:
		Genera un codigo de img que se desbloquea solo si se reservo
6.-Calificaciones
	Puede dar una puntuacion
	Puede ver el promedio
	NADA DE ESTO IMPLEMENTADO POR EL MOMENTO

TODO TIENE SU VOLVER ATRAS HASTA EL MENU PRINCIPAL, SI NO SE REQUERIRA BORRAR TODAS LAS VENTANAS Y HACER UNA NUEVA SESIÓN
```