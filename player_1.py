import socket
import random
import time

port_number = 12000
host_ip = socket.gethostbyname(socket.gethostname())
host_details = (host_ip,port_number)

player = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
player.connect(host_details)

while True:
    action = str(random.randint(0, 1))
    player.send(action.encode('utf-8')) 
    time.sleep(0.1)