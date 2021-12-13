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

#Function to calculate the angle between the agent's direction vector and the destination vector from the center:
def angle(target_player):
    player_angle = transform_angle_track(angle_track[target_player])
    rel_angle = player_angle - destination_angle
    if rel_angle <= 0 :
        return abs(rel_angle)
    else: return min(rel_angle,360-rel_angle)
    
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
    #Need to fix the function and get rid of the problem of the dynamic change
    #of topleft and topright points
    #Conversion of angle_track:
    top_left = player_rect[target_player].topleft
    top_right = player_rect[target_player].topright
    center = player_rect[target_player].center
    rel_angle = transform_angle_track(angle_track[target_player])
    result = []
    
    if rel_angle == 0:
        #Front
        result.append(get_sensor_output(top_left[0],top_left[1]-4,20,20))
        #Left
        result.append(get_sensor_output(top_left[0]-20,top_left[1]-20,20,20))
        #Right
        result.append(get_sensor_output(top_right[0]-20,top_right[1],20,20))
    elif rel_angle == 90:
        result.append(get_sensor_output(top_left[0]-4,top_left[1]-20,20,20))
        result.append(get_sensor_output(top_left[0]-20,top_left[1],20,20))
        result.append(get_sensor_output(top_right[0]+20,top_right[1],20,20))
    elif rel_angle == 180:
        result.append(get_sensor_output(top_right[0]-20,top_right[1]-4,20,20))
        result.append(get_sensor_output(top_left[0],top_left[1],20,20))
        result.append(get_sensor_output(top_right[0],top_right[1]-20,20,20))
    elif rel_angle == 270:
        result.append(get_sensor_output(top_right[0]-4,top_right[1],20,20))
        result.append(get_sensor_output(top_left[0]-20,top_left[1],20,20))
        result.append(get_sensor_output(top_right[0]-20,top_right[1]-20,20,20))
    else:
        if rel_angle > 0 and rel_angle < 90:
            result.append(get_sensor_output(center[0],center[1]-20,20,20))
            result.append(get_sensor_output(center[0]-20,center[1]-20,20,20))
            result.append(get_sensor_output(center[0],center[1],20,20))
        elif rel_angle > 90 and rel_angle < 180:
            result.append(get_sensor_output(center[0]-20,center[1]-20,20,20))
            result.append(get_sensor_output(center[0]-20,center[1],20,20))
            result.append(get_sensor_output(center[0],center[1]-20,20,20))
        elif rel_angle > 180 and rel_angle < 270:
            result.append(get_sensor_output(center[0]-20,center[1],20,20))
            result.append(get_sensor_output(center[0],center[1],20,20))
            result.append(get_sensor_output(center[0]-20,center[1]-20,20,20))
        else:
            result.append(get_sensor_output(center[0],center[1],20,20))
            result.append(get_sensor_output(center[0],center[1]-20,20,20))
            result.append(get_sensor_output(center[0]-20,center[1],20,20))

    result = [float(i)/400.0 for i in result]
    return result        
    
def get_parameters(target_player):
    distance = euclidean_distance(player_rect[target_player].center,destination)
    rel_angle = angle(target_player)
    sensor_output = get_sensors(target_player)
    param_obj = Parameters(distance,rel_angle,sensor_output)
    return param_obj