from socket import socket, error
import hashlib  
from datetime import datetime
from time import time
import os
# Create a TCP/IP socket
sock = socket()
# Connect the socket to the port where the server is listening
server_address = ('192.168.1.58', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
"""
try:

# Send data
    message = b'This is the message.  It will be repeated.'
    print('sending {!r}'.format(message))
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))
finally:
    print('closing socket')
    sock.close()
"""
# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
print("date and time =", dt_string)	
log = open(dt_string+"-log.txt","a")
log.write("Comenzando Cliente\n")
numeroCliente = sock.recv(2048)
sock.send(bytes("Ya recibi mi numero", "utf-8"))
n = numeroCliente.decode("utf-8")
nombreArchivo = "Cliente"+str(n)+"-Prueba-xx.txt"


f = open(nombreArchivo, "wb")
print("Esperando...")

log.write("El nombre de archivo recibido es: "+nombreArchivo+"\n")
log.write("Mi numero de cliente es: "+n+"\n")
start_time = time()
paquetes = 0
while True:
    try:
        # Recibir datos del cliente.
        input_data = sock.recv(2048)
        paquetes+=1
    except error:
        print("Error de lectura.")
        break
    else:
        if input_data:
            # Compatibilidad con Python 3.
            if isinstance(input_data, bytes):
                end = input_data == bytes("Ya termine", "utf-8")
            else:
                end = input_data == "Ya termine"
            if not end:
               
                # Almacenar datos.
                f.write(input_data)

            else:
                break
        else:
            break  
print("Sali del while")
elapsed_time = time() - start_time
log.write("El tiempo de transferencia del archivo "+nombreArchivo+" al cliente "+
              n+" es: "+str(elapsed_time)+" segundos\n")    
log.write("Numero de paquetes enviados al cliente "+ n +" = "+str(paquetes)+" paquetes\n")  

   
print("El archivo se ha recibido correctamente.")
sock.send(bytes("Ya recibi", "utf-8"))
log.write("Transmision exitosa del cliente "+n+"\n")
f.close()
sizefile = os.stat(nombreArchivo).st_size
log.write("Valor total de bytes enviados al cliente "+ n +" = "+str(sizefile)+" bytes\n")  
while True:
    try:
        # Recibir datos del cliente.
        input_data = sock.recv(2048)
        
    except error:
        print("Error de lectura.")
        break
    else:
        if input_data:
            # Compatibilidad con Python 3.
            if isinstance(input_data, bytes):
                end = input_data == bytes("Ya termine", "utf-8")
            else:
                end = input_data == "Ya termine"
            if not end:
                # Almacenar datos.
                hash2 = input_data
            else:
                break
        else:
            break
hash1 = hashlib.md5()
f = open(nombreArchivo,"rb")
content = f.read(2048)
while content:
    content = f.read(2048)
    hash1.update(content)
comprobacion = hash1.digest() == hash2
print("hash recibido: "+ str(hash2))
print("hash calculado: "+ str(hash1.digest()))
print("Son iguales = " + str(comprobacion)) 
f.close()
log.close()
print('Cerrando socket')
sock.close()
