import threading
import socket
#Connection Data
HOST = '127.0.0.1'
PORT = 55555

#Запуск сервера

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

#List For Clients and Their Nicknames

clients = []

nicknames = []

# Brodcast Methode/Function To send  Messages to all connected Clients

def broadcast(message):
    for client in clients:
        client.send(message)


#This Function will Handle Messages From Clients
def handle(client):
    while True:
        try:
            #Brodcasting Messages
            message = client.rcv(1024)
            broadcast(message)
        except:
            #Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left !'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

#Receiving / Listening Function
def receive():
    while True:
        #Accept Connection
        client , address = server.accept()
        print("Connected with {}".format(str(address)))

        #Request and Store Nicknames
        client.send('Nick'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        #Print and Broadcast Nickname
        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined !".encode('ascii'))
        client.send('Connected to server !.'.encode('ascii'))

        # Strat handling thread for Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("Server is listening")
receive()