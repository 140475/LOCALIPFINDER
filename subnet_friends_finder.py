import os
import socket
import netifaces
from queue import Queue
from threading import Thread
from scapy.all import srp, Ether, ARP, conf




# Get the IP address of the default gateway
gateway_ip = netifaces.gateways()['default'][netifaces.AF_INET][0]
print("_"*100+"\n")
print(f'Your gateway address is {gateway_ip}')
print("\n")

ip_range = '.'.join(gateway_ip.split('.')[:-1])



# Get the IP address of the local interface
interface_name = netifaces.gateways()['default'][netifaces.AF_INET][1]
interface_ip = netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]['addr']

# Print your IP address
print("_"*100+"\n")
print("Your IP address is:", interface_ip)
print("\n")

print("_"*100+"\n")
print("LIVE IP ADDRESSES ON YOUR SUBNET:")
print("\n")





def do_stuff(q):
    while True:
        ip=ip_range + "." + str(q.get())
        response = os.popen(f"ping  {ip} -c 1").read()
        if "1 packets received" in response:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
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


