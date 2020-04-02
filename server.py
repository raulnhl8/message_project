import socket
from _thread import *


def threaded_client(conn, id):
    global availableClients
    global numClients
    while True:
        try:
            newData = conn.recv(1024 * 16)
            if not newData:
                break
            if startedConversation and newData:
                msg = newData.decode("utf-8")
                print("received msg: " + msg)
                availableClients[(id + 1) % 2].send(msg.encode("utf-8"))
        except:
            numClients -= 1
            availableClients[id] = None
            break
    conn.close()


server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

availableClients = list()
availableClients.append(None)
availableClients.append(None)

numClients = 0
startedConversation = False

while True:
    try:
        conn, addr = s.accept()
        print("Connected to:", addr)
        data = conn.recv(1024)
        if not data:
            break
        login = data.decode("utf-8")
        print("received login: " + login + "\n")

        availableClients[numClients] = conn

        print("started a new thread...\n")
        start_new_thread(threaded_client, (conn, numClients))
        numClients += 1
        if numClients == 2:
            print("conversation started...")
            startedConversation = True

        else:
            print("Waiting other client...")
    except socket.error as err:
        print(err)
        break
