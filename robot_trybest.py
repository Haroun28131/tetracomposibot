from robot import * 
import math
import numpy as np

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
        theta_0=np.random.uniform(0.0, 360.0)
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = 0
        self.evaluations = evaluations
        self.it_per_evaluation = it_per_evaluation
        # new variables
        #self.param = [-1,  0,  1,  1,  0,  0,  0,  0] #randomsearch
        #self.param = [ 1,  1, -1,  1,  1,  1, -1, -1] #Randomsearch2
        #self.param = [ 1,  0,  1,  0, -1,  1,  0,  0] #GeneticNoAddedWeight
        self.param = [-1, -1, -1, -1,  0,  0,  0, -1]
        self.score = 0
        self.best_robot_config = None
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
                    #print ("\tparameters           =",self.param)
                    #print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                    #print ("\tdistance from origin =",math.sqrt((self.x-self.x_0)**2+(self.y-self.y_0)**2))

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )
        print(self.log_sum_of_translation)
        print("->",translation)
        print("score ",self.log_sum_of_translation + (1 - np.abs(self.log_sum_of_rotation)))
        print("oldscore ",self.log_sum_of_translation * (1 - np.abs(self.log_sum_of_rotation)))
        print("weightedscore ",self.log_sum_of_translation * 10*(1 - np.abs(self.log_sum_of_rotation)))

        self.iteration = self.iteration + 1  

        """# toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        if self.iteration % self.it_per_evaluation == 0:
            current_score = self.log_sum_of_translation * (1 - np.abs(self.log_sum_of_rotation)) 
            if self.best_robot_config is None:
                self.best_robot_config = (current_score, self.param, self.trial)
            else:
                best_score, _, _ = self.best_robot_config
                if best_score < current_score:
                    self.best_robot_config = (current_score, self.param, self.trial)
            best_score, best_param, trial_found = self.best_robot_config
            print(f"the best robot found : {np.array2string(best_param, separator=', ')} with score = {best_score} found in try number {trial_found}")
            self.param = np.random.randint( -1, 2, size=(18, ) )
            self.trial = self.trial + 1
            print ("Trying strategy no.",self.trial)
            return 0, 0, True # ask for reset    """ 

        return translation, rotation, False
