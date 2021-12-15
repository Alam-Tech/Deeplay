import pickle
import pygame
import math
import socket
import threading
from utility.parameter import *
from utility.objects import *
from utility.players import *
from utility.functions import *

port_num = 12000
server_ip = socket.gethostbyname(socket.gethostname())
server_details = (server_ip,port_num)

pygame.init()
window = pygame.display.set_mode((arena_width,arena_height))
pygame.display.set_caption("Break the maze!")

def euclidean_distance(pt1,pt2):
    term_1 = (pt1[0] - pt2[0]) ** 2
    term_2 = (pt1[1] - pt2[1]) ** 2
    distance = math.sqrt(term_1 + term_2)
    return distance

def move_up(target_player):
    #global angle_track,obstacles,destination
    temp_rect = player_rect[target_player]
    old_center = temp_rect.center
    #Modifying the angle for convenience:
    ref_angle = 90 + angle_track[target_player]
    ref_angle = (math.pi/180) * ref_angle
    #Updating the center:
    new_center = (int(old_center[0] + 10*math.cos(ref_angle)),int(old_center[1] - 10*math.sin(ref_angle)))  
    temp_rect.center = new_center
    reward = -1
    
    #Hit an obstacle:
    if temp_rect.collidelist(obstacles) > -1:
        temp_rect.center = old_center
        return reward
    
    #Hit the boundary:
    if (new_center[0] < 0 or new_center[0] > arena_width) or (new_center[1] < 0 or new_center[1] > arena_height):
        temp_rect.center = old_center
        return reward
    
    old_dist = euclidean_distance(old_center,destination)
    new_dist = euclidean_distance(new_center,destination)
    
    if(new_dist < old_dist): reward = 0.1
    else: reward = -0.2

    #Updating the current player's rect:
    player_rect[target_player] = temp_rect
    return reward

def turn(target_player,direction):
    #global angle_track,player_original
    if direction.lower() == 'r':
        if angle_track[target_player] <= 0:
              angle_track[target_player] = -1 * ((abs(angle_track[target_player]) + 15) % 360)
        else:
              angle_track[target_player] = angle_track[target_player] - 15
    elif direction.lower() == 'l':
        if angle_track[target_player] >=0:
              angle_track[target_player] = (angle_track[target_player] + 15) % 360
        else:
              angle_track[target_player] = angle_track[target_player] + 15
    
    #Applying the transformation:
    temp_image = pygame.transform.rotate(player_original[target_player],angle_track[target_player])
    old_center = player_rect[target_player].center
    temp_rect = temp_image.get_rect()
    temp_rect.center = old_center
    #Updating the rect object of the players:
    player_rect[target_player] = temp_rect
    player_copy[target_player] = temp_image
    #Calculating the reward:
    target_player_angle = angle(target_player) / 360.0
    # if target_player_angle == 0:
    #     reward = 1 / (target_player_angle + 1)
    # else: reward = 1 / target_player_angle
    return -target_player_angle
        
# Puts the obstacles on the screen
for obstacle in obstacles:
    pygame.draw.rect(window, pygame.Color('red'), obstacle)
    
def listener(conn,addr):
    reward = 0
    
    pickled_packet = conn.recv(1024)
    packet = pickle.loads(pickled_packet)
    print(f'Player {packet.player_id} connected...')
    param_obj = get_parameters(packet.player_id)
    pickled_param_obj = pickle.dumps(param_obj)
    conn.send(pickled_param_obj)
    
    print(f'[SERVER] Connected to {addr}')
    while True:
        message = conn.recv(1024)
        if message:
            packet = pickle.loads(message)
            target_player = packet.player_id
            action = packet.action
        
            if action == 0: reward = turn(target_player,'r')
            elif action == 1: reward = turn(target_player,'l')
            elif action == 2: reward = move_up(target_player)

            param_obj = get_parameters(target_player)
            param_obj.last_reward = reward
            pickled_param_obj = pickle.dumps(param_obj)
            conn.send(pickled_param_obj)

def set_server():
    global server_details
    print(f'[SERVER] listening at: {server_details}')
    server = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    server.bind(server_details)
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=listener,args=(conn,addr))
        thread.daemon = True
        thread.start()
        

running = True
server_thread = threading.Thread(target=set_server)
server_thread.daemon = True
server_thread.start()

while running:    
    window.fill((0,0,0))
    pygame.time.delay(50)
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Quitting game...')
            running = False
        
    for obstacle in obstacles:
        pygame.draw.rect(window, pygame.Color('red'), obstacle)  
        
    for i in range(total_num_of_players):
        window.blit(player_copy[i],player_rect[i])
            
    pygame.display.flip()