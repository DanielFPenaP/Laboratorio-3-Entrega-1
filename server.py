 
from _thread import *
import hashlib
import threading 
import socket
import sys
from datetime import datetime
from time import time
import os
"""
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Bind the socket to the port
server_address = ('192.168.1.58', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(25)
# Menu de opciones
print('Seleccione el archivo a utilizar')
print('1. Archivo de 100MB')
print('2. Archivo de 250MB')
opcionA = input()
if opcionA == '1':
    print('Ustede selecciono la opcion 1')
elif opcionA == '2':
    print('Ustede selecciono la opcion 2')
else:
    print('Opcion invalida')
print('A cuantos usuarios desea transmitir el archivo')
opcionU = int(input())
print('Usted seleciono '+str(opcionU)+' usuarios')
cont = 0
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    if(cont<=opcionU):
        print('Enviando a ', client_address)
        cont += 1
    try:
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
"""
# print_lock = threading.Lock()
def threaded(c,opcionA,count,log): 
    """
    while True: 
  
        # data received from client 
        data = c.recv(16) 
        if not data: 
            print('Transferencia exitosa') 
            # lock released on exit 
            print_lock.release() 
            break
  
        # reverse the given string from client 
        data = data[::-1] 
  
        # send back reversed string to client 
        c.send(data) 
  
    # connection closed 
    c.close() 
    """
    if opcionA == "1":
        nombreArchivo = "100 MB.mp4"
    elif opcionA == "2":
        nombreArchivo = "250 MB.mp4"
    else:
        nombreArchivo = "prueba.txt"
    print("Enviando archivo "+nombreArchivo+" al cliente "+str(count+1))
    hash1 = hashlib.md5()
    start_time = time()
    paquetes = 0
    while True:   
        f = open(nombreArchivo, "rb")
        content = f.read(2048)
        while content:
            # Enviar contenido. 
            c.send(content)
            paquetes += 1
            content = f.read(2048)
            hash1.update(content)       
        break
        
        """
        # Se utiliza el caracter de código 1 para indicar
        # al cliente que ya se ha enviado todo el contenido.
        try:
            print("sin compatibilidad")
            print('Terminando transaccion') 
            # lock released on exit 
            c.send("Ya termine")
            print_lock.release() 
        except TypeError:
            print('Terminando transaccion') 
            # lock released on exit 
            
            # Compatibilidad con Python 3.
            c.send(bytes("Ya termine", "utf-8"))
            print_lock.release() 
        """
    c.send(bytes("Ya termine", "utf-8"))
    print("Voy a recibir la confirmacion")
    cliente = c.recv(2048)
    elapsed_time = time() - start_time
    if cliente == bytes("Ya recibi", "utf-8"):
        log.write("Tranferencia Exitosa hacia el cliente "+ str(count+1)+"\n")
    else:
        log.write("Tranferencia No Exitosa hacia el cliente "+ str(count+1)+"\n")
    log.write("El tiempo de transferencia del archivo "+nombreArchivo+" al cliente"+
              str(count+1)+" es: "+str(elapsed_time)+" segundos\n")
    log.write("Numero de paquetes enviados al cliente "+ str(count+1) +" = "+str(paquetes)+" paquetes\n")
    sizefile = os.stat(nombreArchivo).st_size
    log.write("Valor total de bytes enviados al cliente "+ str(count+1) +" = "+str(sizefile)+" bytes\n")
    print("el cliente "+str(count+1) +"ha mandado: "+ str(cliente))
    c.send(hash1.digest())
    # Cerrar conexión y archivo.
    c.close()
    f.close()
    print("El archivo ha sido enviado correctamente al usuario "+str(count+1))
    # print_lock.release() 
    
def Main(): 
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    print("date and time =", dt_string)	
    log = open(str(dt_string)+"-log.txt","a")
    log.write("Comenzando servidor\n")
    
    host = "192.168.1.58" 
    port = 10000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("socket binded to port", port) 
   
    
   # Menu de opciones
    print('Seleccione el archivo a utilizar')
    print('1. Archivo de 100MB')
    print('2. Archivo de 250MB')
    opcionA = input()
    log.write("Nombre del archivo Enviado: ")
    if opcionA == '1':
        print('Ustede selecciono la opcion 1')
        log.write("100MB.mp4\n")
    elif opcionA == '2':
        print('Ustede selecciono la opcion 2')
        log.write("250MB.mp4\n")
    else:
        print('Opcion de prueba')
        log.write("prueba.txt\n")
    print('A cuantos usuarios desea transmitir el archivo')
    opcionU = int(input())
    print('Usted seleciono '+str(opcionU)+' usuarios')
    # put the socket into listening mode 
    s.listen(25) 
    print("socket is listening") 
    count = 0
    lista = []
    # a forever loop until client wants to exit 
    for i in range(opcionU):
        c, addr = s.accept()
        lista.append(c)
        count+=1
        print('Connected to :', addr[0], ':', addr[1]) 
        log.write("Cliente "+str(count)+":\n")
        log.write("Se ha conectado el cliente "+str(addr[0])+" al puerto "+str(addr[1])+"\n")
        c.send(bytes(str(count),"utf-8"))
        comprobacion = c.recv(2048)
        if comprobacion == bytes("Ya recibi mi numero", "utf-8"):
            print("el cliente recibio su numero")
        else:
            print("Error recibiendo comprobacion")
    #while True:   
        # lock acquired by client 
        # print_lock.acquire() 
        # c, addr = s.accept()
        # print('Connected to :', addr[0], ':', addr[1]) 

        # Start a new thread and return its identifier 
        # count += 1
    for j in range(len(lista)):
        start_new_thread(threaded, (lista[j],opcionA,j,log)) 
    while True:
        noApagar = 1
    print("y me cerre")
    # s.close() 

  
  
if __name__ == '__main__': 
    Main() 