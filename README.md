# Laboratorio 2: Aplicación Servidor y protocolo HFTP

## Redes y Sistemas Distribuidos 2021

### Integrantes del grupo:

- Facundo Buc
- Agustin Silva Fiorentino
- Alejandro Claudio Spitale

### Estructuración y tomas de decisiones del servidor

El servidor esta compuesto por dos clases llamadas "Server" y "Connection", en la primera clase esta implementada todo lo referido a la conexión, aceptación y manipulación del cliente ingresante al socket, donde los pedidos son esperados 1 por 1 hasta completar todos los pedidos. En la segunda clase tenemos implementada todo lo referido a la manipulación de comandos y posibles errores de los mismos, recorriendo una queue de comandos por cada cliente hasta satisfacer dicho cliente.

### Dificultades encontradas en el proceso

Tuvimos muchas dificultades en un principio en entender la estructura general del servidor y que tenían que hacer cada función, pudimos solventarlo viendo las preguntas que los compañeros realizaron en zulip y a prueba y error, también viendo el archivo cliente y server-test, para darnos una idea de como el servidor y el cliente se comunican.

### Información sobre la realización del laboratorio

Nosotros optamos por usar la herramienta "live share" del IDE Visual Studio Code, y también discord como canal de comunicación de voz, así conseguimos realizar todo el laboratorio, es decír, debartimos todo el tiempo las decisiones a tomar entre los 3 integrantes y debatiendo diferentes ideas para la implementación del mismo. Los push fueron realizados por Facundo porque él fue quien hosteo dicha herramienta.

### Preguntas
1.¿Qué estrategias existen para poder implementar este mismo servidor pero con capacidad de atender múltiples clientes simultáneamente?Investigue y responda brevemente qué cambios serían necesario en el diseño del código.
    Las estrategias que existen para implementar el servidor con capacidad para atender múltiples clientes en simultáneo son por `Threads`,`Forks`, y `Async Server`.
    Los cambios que serían necesarios son crear por cada cliente una nueva conexión creando un nuevo thread. Se crea una nueva clase donde le pasamos el socket en donde esta la conexion del cliente con el server, para manejar cada conexion por separado dentro de un Thread.
    Para cada Thread creado es necesario llamar a la funcion start() la cual pone en marcha el Thread llamando a run (funcion definida en la nueva clase creada donde se maneja el Thread), una vez ejecutada run, podemos derivar la conexion a nuestra clase Connecction.
    Otro detalle no menos importante es que el servidor va a estar siempre escuchando, esperando una nueva conexion por ende necesitamos que dentro de nuestro While True, este la funcion listen().


2.Pruebe ejecutar el servidor en una máquina del laboratorio,mientras utiliza el cliente desde otra, hacia la ip de la máquina servidor. ¿Qué diferencia hay si se corre el servidor desde la IP “localhost”, “127.0.0.1” o la ip “0.0.0.0”?
    `127.0.0.1` es la dirección de protocolo de Internet de bucle invertido (IP) también conocida como `localhost`. La dirección se utiliza para establecer una conexión IP con la misma máquina o computadora que utiliza el usuario final.
    `0.0.0.0` significa todas las direcciones IPv4 en la máquina local. Si un host tiene dos direcciones IP, 192.168.1.1 y 10.1.2.1, y un servidor que se ejecuta en el host escuchando en 0.0.0.0, se podrá acceder a ambas IP.