import pickle
import pygame
import math
import socket
import threading
import parameter

port_num = 12000
server_ip = socket.gethostbyname(socket.gethostname())
server_details = (server_ip,port_num)

pygame.init()
window = pygame.display.set_mode((640,600))
pygame.display.set_caption("Break the maze!")

player_original = [pygame.Surface((12,30)),pygame.Surface((12,30))]

#Setting the color of the players:
for i in range(2): player_original[i].set_colorkey((0,0,0))
player_original[0].fill((255,0,0))
player_original[1].fill((0,255,0))

player_copy = [player.copy() for player in player_original]

player_rect = [i.get_rect() for i in player_copy]
player_rect[0].center = (15,350)
player_rect[1].center = (35,350)

angle_track = 0
destination = (615,25)

clock = pygame.time.Clock()

obstacles = (
     pygame.Rect(0, 0, 50, 300),
     pygame.Rect(0, 400, 50, 200),
     pygame.Rect(100, 0, 50, 200),
     pygame.Rect(100, 250, 50, 200),
     pygame.Rect(100, 500, 50, 100),
     pygame.Rect(150, 100, 50, 30),
     pygame.Rect(200, 100, 30, 230),
     pygame.Rect(150, 300, 50, 30),
     pygame.Rect(200,0,110,50),
     pygame.Rect(280,50,30,100),
     pygame.Rect(280,200,110,250),
     pygame.Rect(200,380,30,170),
     pygame.Rect(230,500,160,50), 
     pygame.Rect(360,550,30,50),
     pygame.Rect(360,50,30,100),
     pygame.Rect(390,50,50,30),
     pygame.Rect(440,50,50,300),
     pygame.Rect(390,320,50,30),
     pygame.Rect(440,400,50,200),
     pygame.Rect(540,0,50,200),
     pygame.Rect(540,250,50,200),
     pygame.Rect(540,500,50,100)
)

def euclidean_distance(pt1,pt2):
    term_1 = (pt1[0] - pt2[0]) ** 2
    term_2 = (pt1[1] - pt2[1]) ** 2
    distance = math.sqrt(term_1 + term_2)
    return distance

def move_up(current_rect):
    global angle_track,obstacles,destination
    old_center = current_rect.center
    ref_angle = 90 + angle_track
    ref_angle = (math.pi/180) * ref_angle
    
    new_center = (old_center[0] + 10*math.cos(ref_angle),old_center[1] - 10*math.sin(ref_angle))  
    current_rect.center = new_center
    reward = -1
    
    #Hit an obstacle:
    if current_rect.collidelist(obstacles) > -1:
        return old_center,reward
    #Hit the boundary:
    if (new_center[0] < 0 or new_center[0] > 600) or (new_center[1] < 0 or new_center[1] > 600):
        return old_center,reward
    
    old_dist = euclidean_distance(old_center,destination)
    new_dist = euclidean_distance(new_center,destination)
    if(new_dist < old_dist): reward = 0.1
    else: reward = -0.2
    
    return new_center,reward

def turn(player_id,direction):
    global angle_track,player_original
    if direction.lower() == 'r':
        if angle_track <= 0:
              angle_track = -1 * ((abs(angle_track) + 15) % 360)
        else:
              angle_track = angle_track - 15
    elif direction.lower() == 'l':
        if angle_track >=0:
              angle_track = (angle_track + 15) % 360
        else:
              angle_track = angle_track + 15
    
    temp_image = pygame.transform.rotate(player_original[player_id],angle_track)
    old_center = player_rect[player_id].center
    temp_rect = temp_image.get_rect()
    temp_rect.center = old_center
    return (temp_image,temp_rect)
        
# Puts the obstacles on the screen
for obstacle in obstacles:
    pygame.draw.rect(window, pygame.Color('red'), obstacle)
    
def listener(conn,addr):
    global player_rect,player_copy
    # A function to get the current parameter object filled with all instances except the 'last_reward'
    # set the parametr object's last_reward instance as zero
    # Pickle the parameter object and send it via TCP connection.
    print(f'[SERVER] Connected to {addr}')
    while True:
        message = conn.recv(1024)
        if message:
            packet = pickle.loads(message)
            target_player = packet.player_id
            action = packet.action
            # print(f'Recieved packet from id: {target_player}')
            if action == 0: player_copy[target_player],player_rect[target_player] = turn(target_player,'r')
            elif action == 1: player_copy[target_player],player_rect[target_player] = turn(target_player,'l')
            #elif action == 2: player_rect[target_player].center,reward = move_up(player_rect[target_player])
            player_rect[target_player].center,reward = move_up(player_rect[target_player])
            #Get the parameter object from the function
            #set the last_reward of the parameter object.

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
        
    for i in range(2):
        window.blit(player_copy[i],player_rect[i])
            
    pygame.display.flip()
    