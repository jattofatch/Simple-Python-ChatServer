import time
import socket
import threading
from queue import Queue

NUMBER_OF_THREADS = 3
JOB_NUMBER = [1,2,3]
queue = Queue()
connections =[]
addresses = []


# creates the socket at the desired port
def create_socket():
    try:
        global host
        global port
        global s
        s = socket.socket()

    except socket.error as e:
        print("there was an error creating the socket : " + str(e))


# binds the port to the socket
def bind_socket():
    try:
        host = ''
        port = 9996
        print("Binding socket to port " + str(port))
        s.bind((host,port))
        s.listen(5)
    except socket.error as e:
        print("there was an error dawg : " + str(e))


# accepts incoming requests to join
def socket_accept():
    conn, address = s.accept()
    s.setblocking(1)
    connections.append(conn)
    addresses.append(address)

    ##start_chat(conn)
    ##conn.close()
    ##s.close()


# creates the threads and points them to the job they should do
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# work that each thread should do
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            socket_accept()
            print("connection succesful")
        if x == 2:
            write_to_conn()
        if x ==3:
            read_from_conn()
        queue.task_done()


def write_to_conn():
    while True:
        data = input()
        conn = connections[0]
        if conn is not None:
            if data == "quit":
                conn.send(str.encode(data))
                quit()
            if len(data)>0:
                conn.send(str.encode(data))

        else:
            print("no connection")


def read_from_conn():
    while True:
        if len(connections)>0:
            conn = connections[0]
            if conn is not None:
                response = str(conn.recv(1024),"utf-8")
                print(response)
        else:
            time.sleep(1.5)
            read_from_conn()



# creates queue for something
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()





















