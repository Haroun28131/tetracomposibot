from robot import * 
import math
import numpy as np
import copy

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = []
    evaluations = 500 
    it_per_evaluation = 400
    trial = 0

    x_0 = 0
    y_0 = 0
    theta_0 = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.evaluations = evaluations
        self.it_per_evaluation = it_per_evaluation
        # new variables
        self.param = np.random.randint( -1, 2, size=(8, ) )
        self.ps = 0
        self.best_robot_config = None
        self.theta_0
        ###############
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - l'évaluation est ici la somme des distances parcourues par pas de temps, mais on peut en imaginer d'autres
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        
        sensors_nda = np.array(sensors)

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )
        # self.score[ self.iteration % self.it_per_evaluation ] = translation * (1 - np.abs(rotation)) * np.min(sensors_nda) * np.max(sensors_nda)
        # print(np.abs(self.log_sum_of_rotation))
        
        # self.score[ self.iteration % self.it_per_evaluation ] = (self.log_sum_of_translation) * (1 - np.abs(self.log_sum_of_rotation - self.prev_rotation))
        self.iteration = self.iteration + 1 
        current_score = self.log_sum_of_translation + (1 - np.abs(self.log_sum_of_rotation)*1.1) 

        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        if self.iteration % self.it_per_evaluation == 0:
            
            #print(f"### Current param : {np.array2string(self.param, separator=', ')}, score = {current_score}")
            if self.best_robot_config is None:
                self.best_robot_config = (current_score, self.param, self.trial)

            else:
                best_score, _, _ = self.best_robot_config

                
                if best_score < current_score:
                    self.best_robot_config = (current_score, self.param, self.trial)
            # creation du fils et mutation
            best_score, best_param, trial_found = self.best_robot_config
            mut_param = copy.deepcopy(best_param)
            """while(True):
                ind = np.random.randint(0, len(best_param))
                muter = np.random.randint( -1, 2 )
                if best_param[ind] != muter : 
                    best_param[ind] = muter
                    break"""
            i=np.random.randint(0, len(best_param))
            m=np.random.randint( -1, 2 )
            while (mut_param[i]==m):
                m=np.random.randint( -1, 2 )
            mut_param[i]=m

            print(f"the best robot found : {np.array2string(best_param, separator=', ')} with score = {best_score} found in try number {trial_found}")
            print(np.array2string(best_param, separator=', '))
            print(np.array2string(mut_param, separator=', '), "score : ", current_score)
            self.param = mut_param
            self.trial = self.trial + 1
            print ("Trying strategy no.",self.trial)
            print(i, m)
            return 0, 0, True # ask for reset     

        return translation, rotation, False
