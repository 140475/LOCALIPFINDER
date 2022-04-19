import os
import socket
from queue import Queue
from threading import Thread



def do_stuff(q):
    while True:
        ip=(f"192.168.0.{q.get()}")
        response = os.popen(f"ping  {ip} -c 1").read()
        if "1 packets received" in response:
            try:
                hostname = socket.gethostbyaddr(ip)
                print(" {}ONLINE".format( hostname))
            except socket.error:
                hostname = "No HOST NAME "
                print(" {}{} ONLINE".format( hostname,ip))
        q.task_done()



q = Queue(maxsize=0)
num_threads = 100


for i in range(num_threads):
    worker = Thread(target=do_stuff, args=(q,))
    worker.setDaemon(True)
    worker.start()



for x in range(1,256):
    q.put(x)




q.join()

# Check to see if the queue is empty. if it is print 'Done!'
if q.qsize() == 0:
    print('Done!')


