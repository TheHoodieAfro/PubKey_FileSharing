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

para poder crear la conexion mediante tcp utilizaremos la libreria socket de python. 

Creacion de las llaves

Creacion de metodos de cifrado

Creacion de metodos de decifrado

Acoplado de todas las funcionalidades

Dificultades
------------
Entender documentacion

Entender ejemplos y decidir cuales metodos eran utiles

Conclusiones
------------
Con los conocimientos correctos es mas facil de lo que parece
