import socket
import time
import pickle
import threading
import sys
from player_2_model import Brain 

sys.path.append('..')
from utility.parameter import *

host_ip = socket.gethostbyname(socket.gethostname())
port_num = 12000
host_details = (host_ip,port_num)

#Creating the brain of the player:
player_brain = Brain(6,3,0.9)

player = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
player_id = 1
player.connect(host_details)

def listener():
    print(f'Player {player_id} acive!')
    while True:
        pickled_params = player.recv(1024)
        if pickled_params:
            params = pickle.loads(pickled_params)
            param_tuple = (params.distance,params.angle,-params.angle,*params.sensors)
            prev_reward = params.last_reward
            action = player_brain.update(prev_reward,param_tuple)
            trigger = ActionTrigger(player_id,action)
            pickled_trigger = pickle.dumps(trigger)
            player.send(pickled_trigger)
            time.sleep(0.01)

thread = threading.Thread(target=listener)
thread.start()

#Sending the inital actionTrigger:
dummy = ActionTrigger(player_id,-1)
pickled_dummy = pickle.dumps(dummy)
player.send(pickled_dummy)