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
        self.param = np.random.randint( -1, 2, size=(18, ) )
        self.score = np.empty( shape=(self.it_per_evaluation, ) )
        self.best_robot_config = None
        self.prev_trans, self.prev_rotation = 0.0, self.theta_0
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
        translation = np.tanh ( self.param[0] + self.param[1:9] @  sensors_nda )
        rotation = np.tanh ( self.param[9] + self.param[10:] @  sensors_nda )
        # self.score[ self.iteration % self.it_per_evaluation ] = translation * (1 - np.abs(rotation)) * np.min(sensors_nda) * np.max(sensors_nda)
        # print(np.abs(self.log_sum_of_rotation))
        self.score[ self.iteration % self.it_per_evaluation ] = (self.log_sum_of_translation-self.prev_trans) * (1 - np.abs(self.log_sum_of_rotation - self.prev_rotation))
        
        # self.score[ self.iteration % self.it_per_evaluation ] = (self.log_sum_of_translation) * (1 - np.abs(self.log_sum_of_rotation - self.prev_rotation))
        self.iteration = self.iteration + 1 

        self.prev_trans, self.prev_rotation = self.log_sum_of_translation, self.log_sum_of_rotation


        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        if self.iteration % self.it_per_evaluation == 0:
            current_score = np.sum( self.score )
            if self.best_robot_config is None:
                self.best_robot_config = (current_score, self.param, self.trial)

            else:
                best_score, _, _ = self.best_robot_config

                
                if best_score < current_score:
                    self.best_robot_config = (current_score, self.param, self.trial)
            # creation du fils et mutation
            best_score, best_param, trial_found = self.best_robot_config
            best_param = copy.deepcopy(best_param)
            while(True):
                ind = np.random.randint(0, len(best_param))
                muter = np.random.randint( -1, 2 )
                if best_param[ind] != muter : 
                    best_param[ind] = muter
                    break
            print(f"the best robot found : {np.array2string(best_param, separator=', ')} with score = {best_score} found in try number {trial_found}")
            self.param = best_param
            self.trial = self.trial + 1
            print ("Trying strategy no.",self.trial)
            print(ind, muter)
            return 0, 0, True # ask for reset     

        return translation, rotation, False
