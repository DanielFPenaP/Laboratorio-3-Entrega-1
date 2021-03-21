## Aplicaciones servidor y cliente

### Servidor

Se implementó una aplicación servidor en Python que permite transmitir dos archivos de video (uno de aproximadamente 103 MB y otro de cerca de 265 MB) usando el protocolo TCP. La aplicación envía un hash junto con el archivo para que el cliente pueda comprobar la integridad del mismo. Junto con la implementación del servidor se creó un archivo de log para guardar el registro de las transferencias realizadas.

### Cliente

Se desarrollo una aplicacion cliente en Python que permite recibir un archivo utilizando el protocolo TCP. Junto con la implementación del cliente se creó un archivo de log para guardar el registro de la transferencia recibida.
