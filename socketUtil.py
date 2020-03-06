import asyncio, socket


def socketServerStart(port):
    s = socket.socket()
    s.bind(('127.0.0.1', port))
    s.listen(5)

    print ("Socket Up and running with a connection from")
    while True:
        c, addr = s.accept()      
        rcvdData = c.recv(1024).decode()
        print(type(rcvdData))
        if rcvdData:
            print(rcvdData)
        c.close()