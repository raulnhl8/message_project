import select
import socket
import threading


bufferLock = threading.Lock()
inputBuffer = list()


def runThread(threadName):
    global inputBuffer

    while True:
        try:
            inputMsg = input()
            bufferLock.acquire()
            inputBuffer.insert(0, inputMsg)
            bufferLock.release()
        except EOFError:
            print(EOFError)
            break


HOST = "localhost"
PORT = 5555  # The same port as used by the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.setblocking(False)

lgn = input("What is your name? ")

client.send(lgn.encode("utf-8"))

t1 = threading.Thread(target = runThread, args=("nomeThread", ))
t1.start()

print("say hi! :D")

while True:
    bufferLock.acquire()
    if len(inputBuffer) > 0:
        inputMsg = inputBuffer.pop()
        inputMsg = lgn + ": " + inputMsg
        client.send(inputMsg.encode("utf-8"))
    bufferLock.release()

    ready = select.select([client], [], [], 0.3)
    if ready[0]:
        data = client.recv(1024 * 16)
        print(data.decode("utf-8"))

