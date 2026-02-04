from robot import * 



nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "subsomption_test"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        


        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\t\tsensors to wall  =",sensor_to_wall)
                print ("\t\tsensors to robot =",sensor_to_robot)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)
        #Premier robot a pour Stratégie Subsomption
        if self.robot_id == 0 or self.robot_id == 3 :
            import random
            if (sensor_to_robot[sensor_front] < 1 or sensor_to_robot[sensor_front_left] < 1 or sensor_to_robot[sensor_front_right] < 1) and (sensor_team[sensor_front] != 'n/a' or sensor_team[sensor_front_left] != 'n/a' or sensor_team[sensor_front_right] != 'n/a')  and (sensor_team[sensor_front] != self.team_name or sensor_team[sensor_front_left] != self.team_name or sensor_team[sensor_front_right] != self.team_name) :
                translation = 0.5 
                rotation = sensor_to_wall[sensor_front] - sensor_to_wall[sensor_rear] - sensor_to_robot[sensor_front_left] + sensor_to_robot[sensor_front_right] - sensor_to_robot[sensor_left] + sensor_to_robot[sensor_right] 
            
            # elif (sensor_to_robot[sensor_front] < 1 or sensor_to_robot[sensor_front_left] < 1 or sensor_to_robot[sensor_front_right] < 1) : 
            #     translation = 0.5
            #     rotation = ((sensor_to_robot[sensor_right] + sensor_to_robot[sensor_front_right]) - (sensor_to_robot[sensor_left] + sensor_to_robot[sensor_front_left]))
            
            elif sensor_to_robot[sensor_rear] < 0.3 and sensor_team[sensor_rear] != self.team_name: 
                translation = 0 
                rotation = 0
            
            elif sensor_to_wall[sensor_front] < 0.8 or sensor_to_wall[sensor_front_left] < 0.8 or sensor_to_wall[sensor_front_right] < 0.8 :
                translation = 0.5
                rotation = sensor_to_wall[sensor_front] - sensor_to_wall[sensor_rear] + sensor_to_wall[sensor_front_left] - sensor_to_wall[sensor_front_right] + sensor_to_wall[sensor_left] - sensor_to_wall[sensor_right] + (random.random()-0.5)*1.   
                
            else : 
                translation = sensors[sensor_front]
                rotation = (random.random()-0.5)*1.
        elif self.robot_id == 2 :
            translation = 0
            rotation = 0
        
        self.iteration = self.iteration + 1        
        return translation, rotation, False
