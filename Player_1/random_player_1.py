import socket
import random
import time
import pickle
import threading

import sys 
sys.path.append('..')

from utility.parameter import *

player_id = 0
port_number = 12000
host_ip = socket.gethostbyname(socket.gethostname())
host_details = (host_ip,port_number)

def listener():
    while True:
        pickled_params = player.recv(1024)
        if pickled_params:
            params = pickle.loads(pickled_params)

player = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
player.connect(host_details)
print(f'Player is connected.')

thread = threading.Thread(target=listener)
thread.start()

while True:
    action = random.randint(0, 2)
    packet = ActionTrigger(player_id,action)
    pickled_packet = pickle.dumps(packet)
    player.send(pickled_packet) 
    time.sleep(0.01)