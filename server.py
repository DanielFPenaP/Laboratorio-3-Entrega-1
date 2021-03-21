import threading
import hashlib
import socket
from datetime import datetime
from time import sleep, time
import os

# print_lock = threading.Lock()
def threaded(connection, fileName, hash, clientId, log): 
    
    print("Enviando archivo "+fileName+" al cliente "+str(clientId))
    start_time = time()
    paquetes = 0
    while True:   
        file = open(fileName, "rb")
        content = file.read(2048)
        while content:
            connection.send(content)
            paquetes += 1
            content = file.read(2048)      
        break
    print(paquetes)
    connection.send(bytes("Ya termine", "utf-8"))
    # connection.send()
    print("Voy a recibir la confirmacion")
    cliente = connection.recv(2048)
    elapsed_time = time() - start_time
    if cliente == bytes("Ya recibi", "utf-8"):
        print("Confimacion exitosa para cliente " + str(clientId))
        log.write("Tranferencia Exitosa hacia el cliente "+ str(clientId)+"\n")
    else:
        print("Confimacion exitosa para cliente " + str(clientId))
        log.write("Tranferencia No Exitosa hacia el cliente "+ str(clientId)+"\n")
    log.write("El tiempo de transferencia del archivo "+fileName+" al cliente"+
              str(clientId)+" es: "+str(elapsed_time)+" segundos\n")
    log.write("Numero de paquetes enviados al cliente "+ str(clientId) +" = "+str(paquetes)+" paquetes\n")
    sizefile = os.stat(fileName).st_size
    log.write("Valor total de bytes enviados al cliente "+ str(clientId) +" = "+str(sizefile)+" bytes\n")
    print("El cliente "+str(clientId) +" ha mandado: "+ str(cliente))
    connection.send(hash)
    # Cerrar conexión y archivo.
    connection.close()
    file.close()
    print("El archivo ha sido enviado correctamente al usuario "+str(clientId))
    # print_lock.release()

def getHashFromFile(fileName):
    hash = hashlib.md5()
    file = open(fileName, "rb")
    content = file.read(2048)
    while content:
        content = file.read(2048)
        hash.update(content)
    return hash.digest()

    
def getFileName(value):
    if value == "1":
        fileName = "infra/100 MB.mp4"
    elif value == "2":
        fileName = "infra/250 MB.mp4"
    else:
        fileName = "prueba.txt"
    return fileName

    
def Main(): 
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    print("date and time =", dt_string)	
    log = open(str(dt_string)+"-Server-log.txt","a")
    log.write("Comenzando servidor\n")
    host = "172.31.200.83" 
    port = 10000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((host, port)) 
    print("socket binded to port", port) 
   
    
   # Menu de opciones
    print('Seleccione el archivo a utilizar')
    print('1. Archivo de 100MB')
    print('2. Archivo de 250MB')
    opcionA = input()
    log.write("Nombre del archivo Enviado: ")
    consoleMsg = ('Usted selecciono la opcion ' + opcionA) if opcionA == '1' or opcionA == '2' else 'Opcion de prueba'
    print(consoleMsg)
    fielName = getFileName(opcionA)
    log.write(fielName+"\n")
    hash = getHashFromFile(fielName)
    print('A cuantos usuarios desea transmitir el archivo')
    opcionU = int(input())
    print('Usted seleciono '+str(opcionU)+' usuarios')
    # put the socket into listening mode 
    server.listen(25) 
    print("Socket is listening") 
    clientId = 0
    lista = []
    # a forever loop until client wants to exit 
    for i in range(opcionU):
        conecction, addr = server.accept()
        lista.append(conecction)
        clientId+=1
        print('Connected to :', addr[0], ':', addr[1]) 
        log.write("Cliente "+str(clientId)+":\n")
        log.write("Se ha conectado el cliente "+str(addr[0])+" al puerto "+str(addr[1])+"\n")
        conecction.send(bytes(str(clientId),"utf-8"))
        comprobacion = conecction.recv(2048)
        if comprobacion == bytes("Ya recibi mi numero", "utf-8"):
            print("El cliente recibio su numero")
        else:
            print("Error recibiendo comprobacion")

    thread_list = []

    for j in range(len(lista)):
        thread = threading.Thread(target = threaded, args = (lista[j], fielName, hash, j+1, log))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()
    print("Se termino de enviar la informacion a todos los clientes")


  
  
if __name__ == '__main__': 
    Main() 
