import pygame
import numpy as np

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

#Dimensions of the stadium:
arena_width = 670
arena_height = 600

grid = np.zeros((arena_height+60,arena_width+60))

#Making the borders opaque:
grid[:30,:] = 1
grid[arena_height+30:,:] = 1
grid[30:arena_height+30,:30] = 1
grid[30:arena_height+30,arena_width+30:] = 1

#Making the obstacles opaque:
for obs in obstacles:
     row = obs.top + 30 #Adding the top border offset
     col = obs.left + 30 #Adding the sideways border offset
     height = obs.height
     width = obs.width
     grid[row:row+height,col:col+width] = 1