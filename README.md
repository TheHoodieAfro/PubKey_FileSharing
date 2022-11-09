Transferencia de archivos con chequeo de integridad con clave pública
=====================================================================
Juan Pablo Herrera

Christian Camilo Rivadeneira

Cristian Sanchez

Proceso
-------
"Deben desarrollarse dos programas, un cliente y un servidor. El programa servidor debe escuchar por un puerto determinado, y esperar la conexión del cliente. El cliente recibe un nombre de archivo como parámetro. Una vez conectados cliente y servidor, el servidor debe generar un par de claves RSA (pública y privada), y mandar la pública al cliente. El cliente debe entonces cifrar el archivo con la clave pública recibida, y transferirlo al servidor, quien procederá a descifrarlo con la respectiva clave privada. Al final del proceso el cliente debe calcular el hash SHA-256 del archivo que acaba de transmitir, y enviarlo al servidor. El servidor debe calcular el hash sobre el archivo recibido, y compararlo con el hash recibido del cliente. Si son iguales, debe indicarse que el archivo se transfirió adecuadamente."

Entendimiento del problema

Creacion de la conexion tcp

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