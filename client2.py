import sys
import socket
import selectors
import traceback

import libclient
import libserver

sel = selectors.DefaultSelector()


def create_request(action):
    
    return dict(
        type="binary/custom-client-binary-type",
        encoding="binary",
        content=bytes(action , encoding="utf-8")
    )


def start_connection(host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)


def listening(host , port):
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((host, port))
    lsock.listen()
    print("listening on", (host, port))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


action = 'client2'
request = create_request(action)
start_connection('127.0.0.1', 1234, request)
listening('127.0.0.1', 9002)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            if message!=None:
                try:
                    message.process_events(mask)
                except Exception:
                    message.close()

        # Check for a socket being monitored to continue.
            else:
                print("received Message")
                accept_wrapper(key.fileobj)
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()