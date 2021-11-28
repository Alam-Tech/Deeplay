import socket
# import random
# import time
import pickle
import player_1_model

port_number = 12000
host_ip = socket.gethostbyname(socket.gethostname())
host_details = (host_ip,port_number)

player = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
player.connect(host_details)

model = player_1_model.Brain(5,2,0.9)

while True:
    message = player.recv(1024)
    if message:
        parameters = pickle.loads(message)
        input_tuple = tuple(parameters.distance,parameters.angle,*parameters.sensors)
        prev_reward = parameters.last_reward
        action = model.update(prev_reward,input_tuple)
        player.send(str(action).encode('utf-8'))

# thread = thread
# while True:
#     action = str(random.randint(0, 1))
#     player.send(action.encode('utf-8')) 
#     time.sleep(0.1)