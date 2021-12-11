import pygame

total_num_of_players = 2
player_original = [pygame.Surface((12,30)),pygame.Surface((12,30))]

for i in range(2): player_original[i].set_colorkey((0,0,0))

#Setting the color of the players:
player_original[0].fill((255,0,0))
player_original[1].fill((0,255,0))

player_copy = [player.copy() for player in player_original]

player_rect = [i.get_rect() for i in player_copy]

#Setting the centres:
player_rect[0].center = (15,350)
player_rect[1].center = (35,350)

angle_track = [0] * total_num_of_players