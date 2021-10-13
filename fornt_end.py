import pygame
import math

pygame.init()
window = pygame.display.set_mode((600,600))
pygame.display.set_caption("Helloo!")

width = 40
height = 60
x = int(250 - (width / 2))
y = int(250 - (height / 2))
velocity = 5

image_orig = pygame.Surface((12,30))
image_orig.set_colorkey((0,0,0))  
image_orig.fill((255,0,0))
image = image_orig.copy()
rect = image.get_rect()
rect.center = (400,100)
clock = pygame.time.Clock()
angle_track = 0

fences = (
     pygame.Rect(50, 0, 50, 300),
     pygame.Rect(50, 400, 50, 200),
     pygame.Rect(150, 0, 50, 200),
     pygame.Rect(150, 250, 50, 200),
     pygame.Rect(150, 500, 50, 100),
     pygame.Rect(200, 100, 50, 50),
     pygame.Rect(250, 100, 30, 250),
     pygame.Rect(200, 300, 50, 50)
)

sample_obs = pygame.Rect(400,400,100,100)

def move_up(current_rect):
    global angle_track
    old_center = current_rect.center
    ref_angle = 90 + angle_track
    ref_angle = (math.pi/180) * ref_angle
    
    new_center = (old_center[0] + 5*math.cos(ref_angle),old_center[1] - 5*math.sin(ref_angle))  
    current_rect.center = new_center
    if current_rect.colliderect(sample_obs) or current_rect.collidelist(fences) > -1:
        return old_center
    return new_center

def turn(direction):
    global angle_track,image_orig
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
    
    temp_image = pygame.transform.rotate(image_orig,angle_track)
    old_center = rect.center
    temp_rect = temp_image.get_rect()
    temp_rect.center = old_center
    return (temp_image,temp_rect)
        
        
# Puts the fences on the screen
for fence in fences:
    pygame.draw.rect(window, pygame.Color('red'), fence)

initialised = False
running = True

while running:    
    # clock.tick(30)
    window.fill((0,0,0))
    pygame.time.delay(50)
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Quitting game...')
            running = False
      
    for fence in fences:
        pygame.draw.rect(window, pygame.Color('red'), fence)  
    pygame.draw.rect(window,pygame.Color('red'),sample_obs)
    key_pressed = pygame.key.get_pressed()
      
    if key_pressed[pygame.K_UP]:
        #   old_center = rect.center
        #   ref_angle = 90 + angle_track
        #   ref_angle = (math.pi/180) * ref_angle
        #   # print(f'ref angle: {ref_angle}')
          
        #   rect.center = (old_center[0] + 5*math.cos(ref_angle),old_center[1] - 5*math.sin(ref_angle))  
        #   if rect.colliderect(sample_obs) or rect.collidelist(fences) > -1:
        #       rect.center = old_center
        rect.center = move_up(rect)
          # print(f'x update : {5 * math.cos(ref_angle)}')
          # print(f'y update : {5 * math.sin(ref_angle)}')
          # print(f'Center at {rect.center}')         
      
    if key_pressed[pygame.K_RIGHT]:
        # old_image = image_orig
        # if angle_track <= 0:
        #       angle_track = -1 * ((abs(angle_track) + 15) % 360)
        # else:
        #       angle_track = angle_track - 15         
        # # print(f'Angle : {-angle_track}')
        # image = pygame.transform.rotate(image_orig,angle_track)
        # old_center = rect.center
        # temp_rect = image.get_rect()
        # temp_rect.center = old_center
        # if not temp_rect.colliderect(sample_obs) and temp_rect.collidelist(fences) == -1:
        image,rect = turn('r')
        
    if key_pressed[pygame.K_LEFT]:
        # if angle_track >=0:
        #       angle_track = (angle_track + 15) % 360
        # else:
        #       angle_track = angle_track + 15
        # # print(f'Angle : {-angle_track}')
        # image = pygame.transform.rotate(image_orig,angle_track)
        # old_center = rect.center
        # temp_rect = image.get_rect()
        # temp_rect.center = old_center
        # if not temp_rect.colliderect(sample_obs) and temp_rect.collidelist(fences) == -1:
        image,rect = turn('l')
        
    window.blit(image,rect)
    
    pygame.display.flip()