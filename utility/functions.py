import math
import numpy as np
from objects import *

#Function to calculate euclidean distance between two points:
def euclidean_distance(pt1,pt2):
    term_1 = (pt1[0] - pt2[0]) ** 2
    term_2 = (pt1[1] - pt2[1]) ** 2
    distance = math.sqrt(term_1 + term_2)
    return distance

#Function to calculate the angle between the velocity vector and the destination from step t-1:
def angle(current_state,prev_state,destination):
    vector_1 = (current_state[0]-prev_state[0],current_state[1]-prev_state[1])
    vector_2 = (destination[0]-prev_state[0],destination[1]-prev_state[1])
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    return angle

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

def get_sensors(player_rect,angle_track):
    #Conversion of angle_track:
    top_left = player_rect.topleft
    top_right = player_rect.topright
    center = player_rect.center

    if angle_track < 0:
        angle_track += 360
    angle_track = (angle_track + 90) % 360
    
    result = []
    
    if angle_track == 0:
        #Front
        result.append(get_sensor_output(top_left[0],top_left[1]-4,20,20))
        #Left
        result.append(get_sensor_output(top_left[0]-20,top_left[1]-20,20,20))
        #Right
        result.append(get_sensor_output(top_right[0]-20,top_right[1],20,20))
    elif angle_track == 90:
        result.append(get_sensor_output(top_left[0]-4,top_left[1]-20,20,20))
        result.append(get_sensor_output(top_left[0]-20,top_left[1],20,20))
        result.append(get_sensor_output(top_right[0]+20,top_right[1],20,20))
    elif angle_track == 180:
        result.append(get_sensor_output(top_right[0]-20,top_right[1]-4,20,20))
        result.append(get_sensor_output(top_left[0],top_left[1],20,20))
        result.append(get_sensor_output(top_right[0],top_right[1]-20,20,20))
    elif angle_track == 270:
        result.append(get_sensor_output(top_right[0]-4,top_right[1],20,20))
        result.append(get_sensor_output(top_left[0]-20,top_left[1],20,20))
        result.append(get_sensor_output(top_right[0]-20,top_right[1]-20,20,20))
    else:
        if angle_track > 0 and angle_track < 90:
            result.append(get_sensor_output(center[0],center[1]-20,20,20))
            result.append(get_sensor_output(center[0]-20,center[1]-20,20,20))
            result.append(get_sensor_output(center[0],center[1],20,20))
        elif angle_track > 180 and angle_track < 270:
            result.append(get_sensor_output(top_left[0]-4,top_left[1]-20,20,20))
            result.append(get_sensor_output(top_left[0]-20,top_left[1],20,20))
            result.append(get_sensor_output(top_right[0]+20,top_right[1],20,20))
            
    
    