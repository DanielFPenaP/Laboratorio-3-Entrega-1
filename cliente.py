import threading
import hashlib
from socket import socket, error
from datetime import datetime
from time import time
import os

def connectToServer():
    sock = socket()
    server_address = ('172.31.200.83', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    return sock


def helloProtocol(socket, log):
    clientId = socket.recv(2048)
    socket.send(bytes("Ya recibi mi numero", "utf-8"))
    clientId = clientId.decode("utf-8")
    fileName = "Cliente"+ str(clientId) +"-.mp4"
    log.write("El nombre de archivo recibido es: "+fileName+"\n")
    log.write("Mi numero de cliente es: " + clientId + "\n")
    return [fileName, clientId]


def getHashFromFile(fileName):
    hash = hashlib.md5()
    file = open(fileName, "rb")
    content = file.read(2048)
    while content:
        content = file.read(2048)
        hash.update(content)
    return hash.digest()


def checkHash(socket, fileName):
    input_data = socket.recv(2048)
    if input_data:
        if isinstance(input_data, bytes):
            end = input_data == bytes("Ya termine", "utf-8")
        else:
            end = input_data == "Ya termine"
        if not end:
            hash = input_data
            calculateHash = getHashFromFile(fileName)
            comprobacion = hash == calculateHash
            print("hash recibido: "+ str(hash))
            print("hash calculado: "+ str(calculateHash))
            print("Son iguales = " + str(comprobacion)) 


def saveFileFromServer(fileName, socket , clientId, log):
    file = open(fileName, "wb")
    print("Esperando...")
    start_time = time()
    paquetes = 0
    goodEnd = False
    while True:
        paquetes += 1
        bytes_read = socket.recv(2048)
        if not bytes_read:
            break
        end = bytes_read[len(bytes_read) - 10:len(bytes_read)] == bytes("Ya termine", "utf-8")
        if not end:
            file.write(bytes_read)
        else:
            file.write(bytes_read[0:len(bytes_read) - 10])
            goodEnd = True
            break

    if(goodEnd):     
        elapsed_time = time() - start_time
        log.write("El tiempo de transferencia del archivo "+fileName+" al cliente "+
                clientId + " es: " + str(elapsed_time) + " segundos\n")    
        log.write("Numero de paquetes enviados al cliente "+ clientId +" = " + str(paquetes) + " paquetes\n") 
        file.close()
        print("El archivo se ha recibido correctamente.")
        socket.send(bytes("Ya recibi", "utf-8"))
        log.write("Transmision exitosa del cliente "+ clientId +"\n")
    else:
        print("Error en la transmicion")
        log.write("Error en transmision del cliente "+ clientId +"\n")


def threadedC(id):
    print('inicio cliente')
    socket = connectToServer()
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    print("date and time =", dt_string)	
    log = open(dt_string+"-log.txt","a")
    log.write("Comenzando Cliente\n")
    fileName, clientId = helloProtocol(socket, log)
    saveFileFromServer(fileName, socket, clientId, log)
    sizefile = os.stat(fileName).st_size
    log.write("Valor total de bytes enviados al cliente "+  clientId +" = "+str(sizefile)+" bytes\n")
    log.close()
    checkHash(socket, fileName)
    print('Cerrando socket')
    socket.close()


def Main():
    print('Ingrese el numero de clientes a crear')
    clientNumber = int(input())
    # print (clientNumber)
    thread_list = []
    for j in range(clientNumber):
        print(j)
        thread = threading.Thread(target = threadedC, args = (j,))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()
    print("Se termino de recivir la informacion de todos los clientes")

if __name__ == '__main__': 
    Main() 