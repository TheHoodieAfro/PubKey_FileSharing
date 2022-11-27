Transferencia de archivos con chequeo de integridad con clave pública
=====================================================================
Juan Pablo Herrera

Christian Camilo Rivadeneira

Cristian Sanchez

Proceso
-------
"Deben desarrollarse dos programas, un cliente y un servidor. El programa servidor debe escuchar por un puerto determinado, y esperar la conexión del cliente. El cliente recibe un nombre de archivo como parámetro. Una vez conectados cliente y servidor, el servidor debe generar un par de claves RSA (pública y privada), y mandar la pública al cliente. El cliente debe entonces cifrar el archivo con la clave pública recibida, y transferirlo al servidor, quien procederá a descifrarlo con la respectiva clave privada. Al final del proceso el cliente debe calcular el hash SHA-256 del archivo que acaba de transmitir, y enviarlo al servidor. El servidor debe calcular el hash sobre el archivo recibido, y compararlo con el hash recibido del cliente. Si son iguales, debe indicarse que el archivo se transfirió adecuadamente."

### Entendimiento del problema

El problema consta de dos aspectos fundamentales, la separación entre el cliente y servidor, y la generacion y calculo de los hashes y las llaves públicas y privadas. Primero debemos encontrar una libreria que nos ofrezca servicios de comunicación entre dos programas. De esta manera enivaremos los archivos y las confirmaciones. Segundo debemos encontrar librerias que nos proporcionen con funciones para poder generar un par de llaves (pública y privada), ademas que nos ofrezcan una funciónn para cifrar archivos y nos permitan cacular un hash SHA-256. Con estas especificaciones decidimos que la mejor alternativa para poder desarrollar este proyecto sería python. No solo por su facil uso sino ademas porque existen varias librerias de criptografías que nos brindan las funciones que necesitamos. Al igual que la experiencia previa que tenemos manejando este tipo de lenguaje. 

### Creación de la conexion TCP

para poder crear la conexión mediante tcp utilizaremos la libreria socket de python. Socket nos permite conectar dos nodos en una red. De esta manera se pueden intercambiar información entre si. Esta libreria, además, nos permite especificar el protocolo de comunicación que queremos (TCP). Tambien consigue de manera muy fácil establecer la conexión y el envio de archivos entre nodos.

### Creación de las llaves

La creación del par de llaves es hecha en el archivo *encryption* en el nodo del servidor. La creación del par de llaves es realiada por un método que genera las llaves utilizando la líbreria RSA del paquete Crytpo de python. Simplemente se le asignan las especificaciones deseadas y la dirección donde se quiere que se creen las llaves y estas son generadas por la líbreria.

### Creación de métodos de cifrado

El manejo de todas las funciones de encriptación se encuentran en ambos, servidor y cliente, en un archivo llamado *encriptación*. Este archivo importa funciones del paquete Cripto de python que le permite el acceso a funciones de encriptacion y desencriptación. Creamos funciones que mediante métodos ofrecidos por esta líbreria podamos encriptar y decriptar con las llaves publicas y privadas junto con el cálculo de la funcion SHA - 256 para el cliente y el servidor.

### Acoplado de todas las funcionalidades

Las estructura de la solución esta compuesta por dos proyectos de python, servidor y cliente. cada uno con sus respectivos archivos de encriptación, y una clase principal donde se ejecuta el proceso desde la inicialización de la conexión hasta terminar el intercambio. 

Dificultades
------------
Quiza dentro de los mayores problemas encontrados a la hora de realizar este proyecto, fue entender la documentación disponible para cada una de las librerias utilizadas en la solucion y en python. Con ello, también, que muchos de los errores que el proyecto generaba fueron frustantes en tanto no se encontraban soluciones similares en internet o de lleno parecian ser exclusivos de este proyecto. Sin embargo, en la mayor parte de estos casos, un proceso de *debug* llevado a cabo de manera correcta y el apoyo en la documentación revisada de manera exhaustiva, logro que fuera posible resolver correctamente el problema propuesto.

Además, agregamos que, de los ejemplos disponibles que se usaron como guía, la mayoria de ellos parecian ser redundantes por lo que tratar de entender su funcionamiento y tomar prestado conceptos o propuestas que fueran utiles también nos resulto complicado ya que, de lo propuesto en estos, la mayoria de las veces ninguna de nuestras elecciones fueron de utilidad, por lo que se requeria iterar de nuevo o buscar nuevas alternativas.

Conclusiones
------------
En primer lugar resaltar la facilidad con la que cuenta python para trabajar con propuestas enfocadas en la seguridad, esto ya que es un lenguaje flexible, sencillo y con un alcance muy amplio en terminos de administrar procesos criptográficos. Además, destacar que con los conocimientos correctos, realizar este proyecto resulta mucho mas sencillo de lo que aparenta ser.
