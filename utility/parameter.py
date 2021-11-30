class Parameters:
    last_reward = 0
    
    def __init__(self,distance,angle,sensors):
        self.distance = distance
        self.angle = angle
        self.sensors = sensors

class ActionTrigger:
    
    def __init__(self,player_id,action):
        self.player_id = player_id
        self.action = action