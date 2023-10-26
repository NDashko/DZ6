import socket
import threading
#Client2
#Nickname input

nickname = input("Chose your nickname ")

#Connecting to the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


#Listening to server and Sending Nickname

def receive():
    while True:
        try:
            # Receive Message From Server
            # if Nick Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'Nick':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            #Close Connection when Error
            print("An error occured")
            client.close()
            break



# Sending message To the server

def write():
    while True:
        message = '{} : {}'.format(nickname , input(""))
        client.send(message.encode('ascii'))



#Starting Threads for Listening And Writing

receive_thread = threading.Thread(target=receive())
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()