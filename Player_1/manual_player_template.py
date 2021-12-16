import socket
import pickle
import sys 
from pynput import keyboard

sys.path.append('..')
from utility.parameter import *

player_id = 0
port_number = 12000
host_ip = socket.gethostbyname(socket.gethostname())
host_details = (host_ip,port_number)

player = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
player.connect(host_details)
print(f'Player {player_id} is connected.')

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        action = -1
        if key == key.up:
            action = 1
        elif key == key.right:
            action = 2
        elif key == key.left:
            action = 0
        trigger = ActionTrigger(player_id,action)
        pickled_trigger = pickle.dumps(trigger)
        player.send(pickled_trigger)

def on_release(key):
    # print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    

print('Press the escape key to exit the remote controller!')

with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()
print('Thank you! -Team Deeplay')