import socket
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()

s = socket.socket()
host = "169.254.7.32"
port = 9996

s.connect((host,port))
print("connection done")


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            read_from_conn()
        if x == 2:
            write_to_conn()


def read_from_conn():
    while True:
        data = str(s.recv(1024), "utf-8")
        if len(data) > 0:
            if data == "quit":
                s.close()
                quit()
            print(data[:])


def write_to_conn():
    while True:
        server_response = input()

        s.send(str.encode(server_response))
        if server_response == "quit":
            s.close()
            quit()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()