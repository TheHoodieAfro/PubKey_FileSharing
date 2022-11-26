Transferencia de archivos con chequeo de integridad con clave pública
=====================================================================
Juan Pablo Herrera

Christian Camilo Rivadeneira

Cristian Sanchez

Proceso
-------
"Deben desarrollarse dos programas, un cliente y un servidor. El programa servidor debe escuchar por un puerto determinado, y esperar la conexión del cliente. El cliente recibe un nombre de archivo como parámetro. Una vez conectados cliente y servidor, el servidor debe generar un par de claves RSA (pública y privada), y mandar la pública al cliente. El cliente debe entonces cifrar el archivo con la clave pública recibida, y transferirlo al servidor, quien procederá a descifrarlo con la respectiva clave privada. Al final del proceso el cliente debe calcular el hash SHA-256 del archivo que acaba de transmitir, y enviarlo al servidor. El servidor debe calcular el hash sobre el archivo recibido, y compararlo con el hash recibido del cliente. Si son iguales, debe indicarse que el archivo se transfirió adecuadamente."

Entendimiento del problema

El problema consiste en dos aspectos fundamentales, la separacion entre el cliente y servidor, y la generacion y calculo de los hashes y las llaves publicas y privadas. Primero debemos encontrar una libreria que nos ofrezca servicios de comunicacion entre dos programas. De esta manera enivaremos los archiovs y las confirmaciones. Segundo debemos encontrar librerias que nos proporcionen con funciones para poder generar un par de llaves (public y privada), ademas que nos ofresca una funcion para cifrar archivos y que nos permita cacular un hash SHA-256. Con estas especificaciones decidimos que la mejor alternativa para poder desarrollar este proyecto seria python. No solo por su facil uso sino ademas porque existen librerias amplias de criptografias que nos brindan las funciones que necesitamos. Al igual que la experiencia previa que tenemos manejando este tipo de lenguaje. 

Creacion de la conexion tcp

para poder crear la conexion mediante tcp utilizaremos la libreria socket de python. Socket nos permite conectar dos nodos en una red. De esta manera se pueden comunicar entre si. Esta librearia ademas nos permite especificar el protocolo de comunicacion que queremos (TCP). Ademas esta libreria nos permite de manera muy facil establecer la conexion y el envio de archivos entre nodos.

Creacion de las llaves

La creacion del par de llaves es hecha en el archivo encryption en el nodo del servidor. La creacion del par de llaves es hecho por un metodo que genera las llaves utilizando la libreria RSA del paquete Crytpo de python. Simplemente se le asignan las especificaciones deseadas y la direccion donde se queire que se creen las llaves y estas son generadas por la libreria.


Creacion de metodos de cifrado

El manejo de todas las funciones de encriptacion se encuentran en ambos servidor como cliente en un archivo llamado encriptacion. Este archivo importa funciones del paquete Cripto de python que le permite el acceso a funciones de encriptacion y decriptaicon. Creamos funciones que mediante metodos ofrecidos por esta libreria podamos encriptar y decriptar con las llaves publicas y privadas junto con el calculo de la funcion SHA - 256 para el cliente y el servidor.

Acoplado de todas las funcionalidades

Las estructura de la solucion esta compuesta por dos proyectos de python, Servidor y cliente. cada uno con sus respectivos archivos de encriptacion, y una clase principal donde se ejecuta el proceso desde la inicializacion de la conexion hasta terminar el intercambio. 

Dificultades
------------
Entender documentacion

Entender ejemplos y decidir cuales metodos eran utiles

Conclusiones
------------
Con los conocimientos correctos es mas facil de lo que parece
