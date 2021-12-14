import math
import numpy as np
from .parameter import *
from .objects import *
from .players import *

#Function to calculate euclidean distance between two points:
def euclidean_distance(pt1,pt2):
    term_1 = (pt1[0] - pt2[0]) ** 2
    term_2 = (pt1[1] - pt2[1]) ** 2
    distance = math.sqrt(term_1 + term_2)
    return distance

def angle_between_vectors(vec_1,vec_2):
    unit_vec_1 = vec_1 / np.linalg.norm(vec_1)
    unit_vec_2 = vec_2 / np.linalg.norm(vec_2)
    cos_angle = np.dot(unit_vec_1,unit_vec_2)
    angle_radians = np.arccos(cos_angle)
    return math.degrees(angle_radians)

#Function to calculate the angle between the agent's direction vector and the destination vector from the center:
def angle(target_player):
    center = player_rect[target_player]
    #Getting the angle of the agent wrt the horizontal
    player_angle = transform_angle_track(angle_track[target_player])
    destination_vec = (destination[0]-center[0],center[1]-destination[1])
    #Getting the angle of the destination vector wrt horizontal:
    destination_angle = angle_between_vectors(destination_vec,(1,0))
    rel_angle = abs(destination_angle - player_angle)
    return min(rel_angle, 360-rel_angle)
    
#Function to calculate the sensor output for the area of a rectange whose:
# Top-left point = (row_num,col_num)
# width = dim_x
# Height = dim_y
def get_sensor_output(left,top,dim_x,dim_y):
    row_num = top + 30
    col_num = left + 30
    sensor_area = grid[row_num:row_num+dim_y,col_num:col_num+dim_x].copy()
    sensor_area = sensor_area.ravel()
    sensor_output = np.sum(sensor_area)
    return sensor_output

def transform_angle_track(initial_angle):
    if initial_angle < 0:
        initial_angle += 360
    final_angle = (initial_angle + 90) % 360
    return final_angle 

def get_sensors(target_player):
    center = player_rect[target_player].center
    #Conversion of angle_track:
    rel_angle = transform_angle_track(angle_track[target_player])
    result = []
    
    if rel_angle == 0:
        #Front
        result.append(get_sensor_output(center[0]+15,center[1]-15,30,30))
        #Left
        result.append(get_sensor_output(center[0]-36,center[1]-15,30,30))
        #Right
        result.append(get_sensor_output(center[0]-15,center[1]+6,30,30))
    elif rel_angle == 90:
        result.append(get_sensor_output(center[0]-15,center[1]-45,30,30))
        result.append(get_sensor_output(center[0]-36,center[1]-15,30,30))
        result.append(get_sensor_output(center[0]+6,center[1]-15,30,30))
    elif rel_angle == 180:
        result.append(get_sensor_output(center[0]-45,center[1]-15,30,30))
        result.append(get_sensor_output(center[0]-15,center[1]+6,30,30))
        result.append(get_sensor_output(center[0]-15,center[1]-36,30,30))
    elif rel_angle == 270:
        result.append(get_sensor_output(center[0]-15,center[1]+15,30,30))
        result.append(get_sensor_output(center[0]+6,center[1]-15,30,30))
        result.append(get_sensor_output(center[0]-36,center[1]-15,30,30))
    else:
        if rel_angle > 0 and rel_angle < 90:
            result.append(get_sensor_output(center[0],center[1]-30,20,20))
            result.append(get_sensor_output(center[0]-30,center[1]-30,30,30))
            result.append(get_sensor_output(center[0],center[1],30,30))
        elif rel_angle > 90 and rel_angle < 180:
            result.append(get_sensor_output(center[0]-30,center[1]-30,30,30))
            result.append(get_sensor_output(center[0]-30,center[1],30,30))
            result.append(get_sensor_output(center[0],center[1]-30,30,30))
        elif rel_angle > 180 and rel_angle < 270:
            result.append(get_sensor_output(center[0]-30,center[1],30,30))
            result.append(get_sensor_output(center[0],center[1],30,30))
            result.append(get_sensor_output(center[0]-30,center[1]-30,30,30))
        else:
            result.append(get_sensor_output(center[0],center[1],30,30))
            result.append(get_sensor_output(center[0],center[1]-30,30,30))
            result.append(get_sensor_output(center[0]-30,center[1],30,30))

    result = [float(i)/900.0 for i in result]
    return result        
    
def get_parameters(target_player):
    distance = euclidean_distance(player_rect[target_player].center,destination)
    rel_angle = angle(target_player)
    sensor_output = get_sensors(target_player)
    param_obj = Parameters(distance,rel_angle,sensor_output)
    return param_obj