# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import util, random, math
from game import *
from keyboardAgents import KeyboardAgent
from learningAgents import ReinforcementAgent
import inference
import busters
import os

class NullGraphics:
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent:
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable
        global predictN
        if predictN <= 0:
            predictN = 1
        # Iniciamos una maquina virtual de Java para Weka
        self.weka = Weka()
        self.weka.start_jvm()
        
    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)
        self.countActions = 0

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        global last_move
        global distWest
        global distEast
        global distNorth
        global distSouth

        distWest = 99999
        distEast = 99999
        distNorth = 99999
        distSouth = 99999

        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = self.countActions + 1
        last_move = KeyboardAgent.getAction(self, gameState)

        # Almacenamos en variables una serie de datos utiles
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        
        posPacman = gameState.getPacmanPosition()
        walls = gameState.getWalls()
        livingGhosts = gameState.getLivingGhosts()
        #move NORTH
        if Directions.NORTH in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0], posPacman[1] + 1
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for g in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia minima actual es menor que la almacenada, se sobreescribe
                        if self.distancer.getDistance(g, buffPacman) < distNorth:
                            distNorth = self.distancer.getDistance(g, buffPacman)
                    iterator += 1

        #move SOUTH
        if Directions.SOUTH in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0], posPacman[1] - 1
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for g in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia minima actual es menor que la almacenada, se sobreescribe
                        if self.distancer.getDistance(g, buffPacman) < distSouth:
                            distSouth = self.distancer.getDistance(g, buffPacman)
                    iterator += 1
                        
        #move EAST
        if Directions.EAST in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0] + 1, posPacman[1]
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for g in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia minima actual es menor que la almacenada, se sobreescribe
                        if self.distancer.getDistance(g, buffPacman) < distEast:
                            distEast = self.distancer.getDistance(g, buffPacman)
                    iterator += 1
                       
        #move WEST
        if Directions.WEST in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0] - 1, posPacman[1]
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for g in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia minima actual es menor que la almacenada, se sobreescribe
                        if self.distancer.getDistance(g, buffPacman) < distWest:
                            distWest = self.distancer.getDistance(g, buffPacman)
                    iterator += 1

        return last_move

    def printLineData(self, gameState):
        # En esta funcion usaremos 2 variables globales
        global predictN
        global prevState
        
        # Intentamos abrir el archivo de salida, si no existe, lo creamos usando createWekaFile()
        if(os.path.isfile("training_tutorial1.arff") == False):
            attributesList = [["distNorth","NUMERIC"],["distSouth","NUMERIC"],["distEast","NUMERIC"],["distWest","NUMERIC"], 
            ["Score","NUMERIC"],["NextScore","NUMERIC"],["NearestFood","NUMERIC"],["lastMove","{North,South,East,West,Stop}"]]
            self.createWekaFile(attributesList)

        # Necesitamos la funcion distancer para hacer calculos de distancias
        self.distancer = Distancer(gameState.data.layout, False)

        # Si hemos llegado al turno N, imprimimos en el archivo
        if self.countActions > predictN:
            # Cada vez vamos a sacar 9 elementos de la lista (8 atributos + "\n")
            counter = 9
            # Abrimos el archivo de salida
            file = open("training_tutorial1.arff", "a")
            # Obtenemos la puntuacion actual, para usarla de valor predecido
            prevState[5] = gameState.getScore()
            while(counter > 0):
                # Usamos pop para sacar uno a uno los elementos de la lista y escribirlos en el archivo de salida
                x = prevState.pop(0);
                file.write("%s" % (x))
                # Imprimimos comas entre atributos excepto entre los 2 ultimos (last_move y "\n")
                if counter > 2:
                    file.write(",")
                counter -= 1
            # Cerramos el archivo de salida
            file.close()
        # Metemos en la lista las variables de distancia
        prevState.append(distNorth)
        prevState.append(distSouth)
        prevState.append(distEast)
        prevState.append(distWest)
        # Metemos en la lista la puntuacion actual, y un placeholder para nextScore
        prevState.append(gameState.getScore())
        prevState.append(gameState.getScore()-1)
        # Metemos en la lista la distancia a la comida mas cercana, si no hay, metemos 99999 en su lugar
        if (gameState.getDistanceNearestFood() == None):
            prevState.append(99999)
        else:
            prevState.append(gameState.getDistanceNearestFood())
        # Introducimos el movimiento realizado, que se ha obtenido durante chooseAction()
        prevState.append(last_move)
        prevState.append("\n")


    def createWekaFile(self, attributesList):
        # Abrimos el archivo en modo append, para que no se sobreescriba el archivo
        file = open("training_tutorial1.arff", "a")
        # Escribimos la cabecera del archivo
        file.write("@RELATION 'training_tutorial1'\n\n")
        # Escribimos todos los atributos
        for l in attributesList:
            file.write("@ATTRIBUTE %s %s\n" % (l[0], l[1]))
        # Escribimos el indicador de que empiezan los datos
        file.write("\n@data\n")

from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):
    
    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
        
    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move
        
        
class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.EAST



class BasicAgentAA(BustersAgent):
    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState):
        print "---------------- TICK ", self.countActions, " --------------------------"
        # Dimensiones del mapa
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print "Width: ", width, " Height: ", height
        # Posicion del Pacman
        print "Pacman position: ", gameState.getPacmanPosition()
        # Acciones legales de pacman en la posicion actual
        print "Legal actions: ", gameState.getLegalPacmanActions()
        # Direccion de pacman
        print "Pacman direction: ", gameState.data.agentStates[0].getDirection()
        # Numero de fantasmas
        print "Number of ghosts: ", gameState.getNumAgents() - 1
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        print "Living ghosts: ", gameState.getLivingGhosts()
        # Posicion de los fantasmas
        print "Ghosts positions: ", gameState.getGhostPositions()
        # Direciones de los fantasmas
        print "Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Distancia de manhattan a los fantasmas
        print "Ghosts distances: ", gameState.data.ghostDistances
        # Puntos de comida restantes
        print "Pac dots: ", gameState.getNumFood()
        # Distancia de manhattan a la comida mas cercada
        print "Distance nearest pac dots: ", gameState.getDistanceNearestFood()
        # Paredes del mapa
        print "Map:  \n", gameState.getWalls()
        # Puntuacion
        print "Score: ", gameState.getScore()
        
    def chooseAction(self, gameState):

        # En esta funcion usaremos 5 variables globales, una para la accion, y 4 para las distancias
        global last_move
        global distWest
        global distEast
        global distNorth
        global distSouth
        '''
        # Incrementamos el contador de turnos
        self.countActions = self.countActions + 1
        # Se imprimen datos relevantes sobre la partida
        self.printInfo(gameState)
        # Por defecto, el movimiento a ejecutar es "Stop"
        move = Directions.STOP
        # Se inicializan las distancias a un numero muy alto
        distWest = 99999
        distEast = 99999
        distNorth = 99999
        distSouth = 99999

        # Almacenamos en variables una serie de datos relevantes
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        posPacman = gameState.getPacmanPosition()
        minDist = 99999
        walls = gameState.getWalls()
        livingGhosts = gameState.getLivingGhosts()
        #move NORTH
        if Directions.NORTH in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0], posPacman[1] + 1
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for x in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia actual es menor o igual que la previa de este movimiento, se sobreescribe
                        if self.distancer.getDistance(x, buffPacman) <= distNorth:
                            distNorth = self.distancer.getDistance(x, buffPacman)
                            # Se comprueba si la distancia es menor que la minima de todas las acciones
                            if distNorth < minDist:
                                # Se sobreescribe y se cambia el movimiento a realizar
                                minDist = distNorth
                                move = Directions.NORTH
                            # Si la distancia es igual a la minima actual, se comprueba si la casilla nueva contiene comida
                            # de ser asi, se cambia el movimiento a realizar
                            # Esto sirve para que en caso de haber 2 acciones igual de buenas, elija la que tiene comida
                            elif distNorth == minDist:
                                if gameState.hasFood(buffPacman[0],buffPacman[1]):
                                    move = Directions.NORTH
                    iterator = iterator + 1
        #move SOUTH
        if Directions.SOUTH in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0], posPacman[1] - 1
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for x in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia actual es menor o igual que la previa de este movimiento, se sobreescribe
                         if self.distancer.getDistance(x, buffPacman) <= distSouth:
                            distSouth = self.distancer.getDistance(x, buffPacman)
                            # Se comprueba si la distancia es menor que la minima de todas las acciones
                            if distSouth < minDist:
                                # Se sobreescribe y se cambia el movimiento a realizar
                                minDist = distSouth
                                move = Directions.SOUTH
                            # Si la distancia es igual a la minima actual, se comprueba si la casilla nueva contiene comida
                            # de ser asi, se cambia el movimiento a realizar
                            # Esto sirve para que en caso de haber 2 acciones igual de buenas, elija la que tiene comida
                            elif distSouth == minDist:
                                if gameState.hasFood(buffPacman[0],buffPacman[1]):
                                    move = Directions.SOUTH
                    iterator = iterator + 1
        #move EAST
        if Directions.EAST in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0] + 1, posPacman[1]
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for x in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia actual es menor o igual que la previa de este movimiento, se sobreescribe
                        if self.distancer.getDistance(x, buffPacman) <= distEast:
                            distEast = self.distancer.getDistance(x, buffPacman)
                            # Se comprueba si la distancia es menor que la minima de todas las acciones
                            if distEast < minDist:
                                # Se sobreescribe y se cambia el movimiento a realizar
                                minDist = distEast
                                move = Directions.EAST
                            # Si la distancia es igual a la minima actual, se comprueba si la casilla nueva contiene comida
                            # de ser asi, se cambia el movimiento a realizar
                            # Esto sirve para que en caso de haber 2 acciones igual de buenas, elija la que tiene comida
                            elif distEast == minDist:
                                if gameState.hasFood(buffPacman[0],buffPacman[1]):
                                    move = Directions.EAST
                    iterator = iterator + 1
        #move WEST
        if Directions.WEST in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0] - 1, posPacman[1]
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for x in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia actual es menor o igual que la previa de este movimiento, se sobreescribe
                        if self.distancer.getDistance(x, buffPacman) <= distWest:
                            distWest = self.distancer.getDistance(x, buffPacman)
                            # Se comprueba si la distancia es menor que la minima de todas las acciones
                            if distWest < minDist:
                                # Se sobreescribe y se cambia el movimiento a realizar
                                minDist = distWest
                                move = Directions.WEST
                            # Si la distancia es igual a la minima actual, se comprueba si la casilla nueva contiene comida
                            # de ser asi, se cambia el movimiento a realizar
                            # Esto sirve para que en caso de haber 2 acciones igual de buenas, elija la que tiene comida
                            elif distWest == minDist:
                                if gameState.hasFood(buffPacman[0],buffPacman[1]):
                                    move = Directions.WEST
                    iterator = iterator + 1
        # Se almacena last_move para usarla en otras funciones
        last_move = move
        return move
        '''
        # Inicializamos la lista que le pasaremos a Weka
        x = []
        # Inicializamos las variables de distancia a un numero muy alto, que significa que la accion es ilegal
        distWest = 99999
        distEast = 99999
        distNorth = 99999
        distSouth = 99999
        
        # Almacenamos en variables una serie de datos utiles
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        
        posPacman = gameState.getPacmanPosition()
        walls = gameState.getWalls()
        livingGhosts = gameState.getLivingGhosts()
        #move NORTH
        if Directions.NORTH in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0], posPacman[1] + 1
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for g in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia minima actual es menor que la almacenada, se sobreescribe
                        if self.distancer.getDistance(g, buffPacman) < distNorth:
                            distNorth = self.distancer.getDistance(g, buffPacman)
                    iterator += 1

        #move SOUTH
        if Directions.SOUTH in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0], posPacman[1] - 1
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for g in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia minima actual es menor que la almacenada, se sobreescribe
                        if self.distancer.getDistance(g, buffPacman) < distSouth:
                            distSouth = self.distancer.getDistance(g, buffPacman)
                    iterator += 1
                        
        #move EAST
        if Directions.EAST in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0] + 1, posPacman[1]
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for g in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia minima actual es menor que la almacenada, se sobreescribe
                        if self.distancer.getDistance(g, buffPacman) < distEast:
                            distEast = self.distancer.getDistance(g, buffPacman)
                    iterator += 1
                       
        #move WEST
        if Directions.WEST in legal:
            # Inicia un contador a 1 para no tener el cuenta el pacman
            iterator = 1
            # Almacena la posicion del pacman resultante de ejecutar la accion
            buffPacman = posPacman[0] - 1, posPacman[1]
            # Comprueba que la casilla objetivo no contenga un muro
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # Itera sobre los fantasmas
                for g in gameState.getGhostPositions():
                    # Comprueba que los fantasmas estan vivos
                    if livingGhosts[iterator] == True:
                        # Si la distancia minima actual es menor que la almacenada, se sobreescribe
                        if self.distancer.getDistance(g, buffPacman) < distWest:
                            distWest = self.distancer.getDistance(g, buffPacman)
                    iterator += 1

        # Metemos en la lista las variables de distancia
        x.append(distNorth)
        x.append(distSouth)
        x.append(distEast)
        x.append(distWest)
        # -------------------------- COMMENT THIS PART IF USING NoFood_NoScore --------------------------
        # Metemos en la lista la puntuacion
        x.append(gameState.getScore())
        # Metemos en la lista la distancia a la comida mas cercana, si no hay, metemos 99999 en su lugar
        if (gameState.getDistanceNearestFood() == None):
            x.append(99999)
        else:
            x.append(gameState.getDistanceNearestFood())
        # -----------------------------------------------------------------------------------------------

        # Pasamos los datos necesarios a Weka para que los clasifique
        a = self.weka.predict("./Models/Classification/Tutorial1/Samemaps/Unfiltered/LMT.model", x, "./Training/training_tutorial1_noNextScore.arff")
        
        # ------ Estas lineas sirven para evitar que el agente automatico entre en un bucle infinito ----------
        # El bug se produce cuando no se puede hacer la accion "East" y la accion "South" es mejor que "North"
        """ if (distEast == 99999 and distNorth > distSouth and a == 'North'):
            a = 'South' """
        # -----------------------------------------------------------------------------------------------------

        # ------ Estas lineas sirven para que el agente automatico de teclado no haga acciones ilegales -------
        """ if (a == 'East' and distEast == 99999):
            a = 'Stop'
        elif (a == 'West' and distWest == 99999):
            a = 'Stop'
        elif (a == 'North' and distNorth == 99999):
            a = 'Stop'
        elif (a == 'South' and distSouth == 99999):
            a = 'Stop' """
        # ------------------------------------------------------------------------------------------------------
        # Se almacena last_move para usarla en otras funciones
        last_move = a
        return a
        

    def printLineData(self, gameState):
        # En esta funcion usaremos 2 variables globales
        global predictN
        global prevState
        
        # Intentamos abrir el archivo de salida, si no existe, lo creamos usando createWekaFile()
        if(os.path.isfile("training_tutorial1.arff") == False):
            attributesList = [["distNorth","NUMERIC"],["distSouth","NUMERIC"],["distEast","NUMERIC"],["distWest","NUMERIC"], 
            ["Score","NUMERIC"],["NextScore","NUMERIC"],["NearestFood","NUMERIC"],["lastMove","{North,South,East,West,Stop}"]]
            self.createWekaFile(attributesList)

        # Si hemos llegado al turno N, imprimimos en el archivo
        if self.countActions > predictN:
            # Cada vez vamos a sacar 9 elementos de la lista (8 atributos + "\n")
            counter = 9
            # Abrimos el archivo de salida
            file = open("training_tutorial1.arff", "a")
            # Obtenemos la puntuacion actual, para usarla de valor predecido
            prevState[5] = gameState.getScore()
            while(counter > 0):
                # Usamos pop para sacar uno a uno los elementos de la lista y escribirlos en el archivo de salida
                x = prevState.pop(0);
                file.write("%s" % (x))
                # Imprimimos comas entre atributos excepto entre los 2 ultimos (last_move y "\n")
                if counter > 2:
                    file.write(",")
                counter -= 1
            # Cerramos el archivo de salida
            file.close()
        # Metemos en la lista las variables de distancia
        prevState.append(distNorth)
        prevState.append(distSouth)
        prevState.append(distEast)
        prevState.append(distWest)
        # Metemos en la lista la puntuacion actual, y un placeholder para nextScore
        prevState.append(gameState.getScore())
        prevState.append(gameState.getScore()-1)
        # Metemos en la lista la distancia a la comida mas cercana, si no hay, metemos 99999 en su lugar
        if (gameState.getDistanceNearestFood() == None):
            prevState.append(99999)
        else:
            prevState.append(gameState.getDistanceNearestFood())
        # Introducimos el movimiento realizado, que se ha obtenido durante chooseAction()
        prevState.append(last_move)
        prevState.append("\n")

    def createWekaFile(self, attributesList):
        # Abrimos el archivo en modo append, para que no se sobreescriba el archivo
        file = open("training_tutorial1.arff", "a")
        # Escribimos la cabecera del archivo
        file.write("@RELATION 'training_tutorial1'\n\n")
        # Escribimos todos los atributos
        for l in attributesList:
            file.write("@ATTRIBUTE %s %s\n" % (l[0], l[1]))
        # Escribimos el indicador de que empiezan los datos
        file.write("\n@data\n")

class ReinforcementAgent:

    def __init__( self, numTraining = 0, epsilon = 0.3, alpha = 0.3, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True, discount = 0.8 ):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable
        self.table_file = open("qtable.txt", "r+")
        self.q_table = self.readQtable()
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(discount)
        self.episodesSoFar = 0
        self.numTraining = numTraining
        self.loopCounter = 0
        
    def registerInitialState(self, gameState):
        """
            Initializes beliefs and inference modules.
            Also, it starts the episode
        """
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.startEpisode()

    def startEpisode(self):
        """
            Whenever a new episode starts, these variables are reset
        """
        self.lastState = None
        self.lastAction = None
        self.lastScore = 0

    def stopEpisode(self):
        """
            Detects when an episode has finished, and makes some adjustements
        """
        self.episodesSoFar = self.episodesSoFar + 1
        if (self.episodesSoFar >= self.numTraining and self.numTraining > 0):
            # print 'changing alpha (%.2f)and epsilon(%.2f)' % (self.alpha, self.epsilon)
            self.alpha = 0
            self.epsilon = 0
            #print 'changed alpha (%.2f)and epsilon(%.2f)' % (self.alpha, self.epsilon)
        # The epsilon value gets reduced each time a game ends. In 100 games it will be decreased by 0.5
        elif(self.epsilon > 0.05):
            #print 'actual epsilon = %.2f' % (self.epsilon)
            self.epsilon = self.epsilon - 0.005
            #print 'modified epsilon = %.2f' % (self.epsilon)


    def observationFunction(self, gameState):
        """
            Detects a change on the gameState, makes the reward calculations, and calls observeTransition()
        """
        if not self.lastState is None:
            # If the score is less than the last turn, the reward is 0
            if((gameState.getScore() - self.lastScore) <= 0): 
                reward = 0
            else:
                # If the pacman eats a ghost without eating all the food, it doesn't get rewarded
                if ((gameState.getScore() - self.lastScore) > 50 and gameState.getNumFood() > 0):
                    reward = 0
                else:
                    reward = 0.25
            # The score of the previous turn is updated
            self.lastScore = gameState.getScore()
            # We call observeTransition() to update the Q-table
            self.observeTransition(self.lastState, self.lastAction, gameState, reward)

        return gameState

    def observeTransition(self, gameState,action,nextGameState,reward):
        """
            Called by environment to inform agent that a transition has
            been observed. This will result in a call to update()
            on the same arguments
        """
        self.update(gameState,action,nextGameState,reward)

    def getAction(self, gameState):
        """
            This function is called whenever the game requests an action
        """
        posPacman = gameState.getPacmanPosition()
        state = self.getState(gameState)
        action = self.chooseAction(state, gameState)
        # This is used to fix a pacman that got stuck
        # If the pacman makes 5 reversed movements in a row, the next action will be random
        if self.epsilon == 0.0:
            if Actions.reverseDirection(action) == self.lastAction:
                self.loopCounter = self.loopCounter + 1
            else:
                self.loopCounter = 0
            if self.loopCounter >= 5:
                # print 'Unstucking'
                self.epsilon = 1.0
                action = self.chooseAction(state, gameState)
                self.epsilon = 0.0

        self.doAction(gameState, action)
        return action

    def doAction(self,state,action):
        """
            This function updates the last state and action
        """
        self.lastState = state
        self.lastAction = action


class QLearningAgent(ReinforcementAgent):
    
    def registerInitialState(self, gameState):
        ReinforcementAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
    
    def readQtable(self):
        "Read qtable from disc"
        table = self.table_file.readlines()
        q_table = []

        for i, line in enumerate(table):
            row = line.split()
            row = [float(x) for x in row]
            q_table.append(row)

        return q_table

    def writeQtable(self):
        "Write qtable to disc"
        self.table_file.seek(0)
        self.table_file.truncate()

        for line in self.q_table:
            for item in line:
                self.table_file.write(str(item)+" ")
            self.table_file.write("\n")

    def computePosition(self, state):
        """
            Translates the state into a number that can be used in the qtable
        """
        pos = state[0]*8 + state[1]*4 + state[2]*2 + state[3]
        return pos

    def getNumberAction(self, action):
        """
            Translates the action received into a number that can be used in the qtable
        """
        if action == 'North':
            action = 0
        elif action == 'East':
            action = 1
        elif action == 'South':
            action = 2
        elif action == 'West':
            action = 3
        return action

    def chooseAction(self, state, gameState):
        """
            When this function is called, it returns an action from the set of best actions based on its qvalues
        """
        legal = gameState.getLegalActions(0)
        if (len(legal) == 0):
            return None
        flip = util.flipCoin(self.epsilon)

        if flip:
            return random.choice(legal)
        
        return self.computeActionFromQValues(state, gameState)

    def computeActionFromQValues(self, state, gameState):
        """
            Returns the best action in a state
        """
        legal = gameState.getLegalActions(0)

        best_actions = []
        best_value = -99999
        for action in legal:
            value = self.getQValue(state, action)
            if value == best_value:
                best_actions.append(action)
            if value > best_value:
                best_actions = [action]
                best_value = value

        return random.choice(best_actions)

    def computeValueFromQValues(self, state, gameState):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        legalActions = gameState.getLegalActions(0)
        if len(legalActions)==0:
          return 0
        return max(self.q_table[self.computePosition(state)])

    def getQValue(self, state, action):
        """
            Returns the Qvalue of performing an action in a state
        """
        position = self.computePosition(state)
        
        action_column = self.getNumberAction(action)

        return self.q_table[position][action_column]

    def update(self, gameState, action, nextGameState, reward):
        """
            Updates the q_table according to given guidelines
        """
        state = self.getState(gameState)
        if state !=  None:
            # Calculates the position of the current state and action in the q_table
            pos = self.computePosition(state)
            action = self.getNumberAction(action)

            # Whenever the last ghost is eaten, the reward is 0.26 instead of 0.25, so we can identify the end of the game
            if(reward == 0.26):
                q_value = ((1 - self.alpha) * self.q_table[pos][action]) + (self.alpha * reward)
            else:
                nextState = self.getState(nextGameState)
                if (nextState != None):
                    nextAction = self.getNumberAction(self.chooseAction(nextState, nextGameState))
                    posNext = self.computePosition(nextState)
                    # If the state remains the same, and there is no reward, we don't edit the qvalue
                    if (state == nextState and reward == 0):
                        q_value = self.q_table[pos][action]
                    else:
                        q_value = (1 - self.alpha) * self.q_table[pos][action]
                        q_value += self.alpha * (reward + (self.discount * self.computeValueFromQValues(nextState, gameState) * self.q_table[posNext][nextAction]))

            # The Q-values table is updated
            self.q_table[pos][action] = q_value
        # We write the changes into the file
        self.writeQtable()


    def checkIfMinDist(self, minDist, distances):
        """
            Given the minimum distance, and a list of distances, generates 
            a list with binary values according to the needs of the state
        """
        result = []
        for i in distances:
            if (minDist == i):
                result.append(1)
            else:
                result.append(0)
        return result


    def final(self, state):
        """
            This function is called every time a game ends
        """
        # If the pacman doesn't eat something, the reward is 0. If it does, it gets rewarded with 0.26, since it is the last ghost
        if((state.getScore() - self.lastScore) <= 0): 
            reward = 0
        else:
            if ((state.getScore() - self.lastScore) > 50 and state.getNumFood() > 0):
                reward = 0
            else:
                reward = 0.26
        # Updates the last score to keep track of the changes
        self.lastScore = state.getScore()
        
        self.observeTransition(self.lastState, self.lastAction, state, reward)
        self.stopEpisode()

    def getState(self, gameState):
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        if len(legal) == 0:
            return None
        # By default, chooses a random movement as best
        distNorth = 99999
        distSouth = 99999
        distEast = 99999
        distWest = 99999
        minDist = 99999

        posPacman = gameState.getPacmanPosition()

        
        walls = gameState.getWalls()
        livingGhosts = gameState.getLivingGhosts()
        #move NORTH
        if Directions.NORTH in legal:
            # Starts an iterator as 1 to ignore the pacman
            iterator = 1
            # Stores in a buffer the resulting position of the pacman if it executed the given action
            buffPacman = posPacman[0], posPacman[1] + 1
            # Checks the target cell doesn't have a wall
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # If there is uneaten food, it takes priority over the ghosts
                if gameState.getDistanceNearestFood() != None:
                    # Searches for the distance to the nearest food
                    foodPos = gameState.getPositionNearestFood(buffPacman)
                    if self.distancer.getDistance(foodPos, buffPacman) < distNorth:
                        distNorth = self.distancer.getDistance(foodPos, buffPacman)
                        if distNorth < minDist:
                            minDist = distNorth
                else:
                    # Itera sobre los fantasmas
                    for x in gameState.getGhostPositions():
                        # Comprueba que los fantasmas estan vivos
                        if livingGhosts[iterator] == True:
                            # Se comprueba si la distancia es menor que la minima de todas las acciones
                            if self.distancer.getDistance(x, buffPacman) < distNorth:
                                distNorth = self.distancer.getDistance(x, buffPacman)
                                if distNorth < minDist:
                                    minDist = distNorth
                        iterator = iterator + 1
        #move SOUTH
        if Directions.SOUTH in legal:
            # Starts an iterator as 1 to ignore the pacman
            iterator = 1
            # Stores in a buffer the resulting position of the pacman if it executed the given action
            buffPacman = posPacman[0], posPacman[1] - 1
            # Checks the target cell doesn't have a wall
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # If there is uneaten food, it takes priority over the ghosts
                if gameState.getDistanceNearestFood() != None:
                    # Searches for the distance to the nearest food
                    foodPos = gameState.getPositionNearestFood(buffPacman)
                    if self.distancer.getDistance(foodPos, buffPacman) < distSouth:
                        distSouth = self.distancer.getDistance(foodPos, buffPacman)
                        if distSouth < minDist:
                            minDist = distSouth
                else:
                    # Itera sobre los fantasmas
                    for x in gameState.getGhostPositions():
                        # Comprueba que los fantasmas estan vivos
                        if livingGhosts[iterator] == True:
                            # Se comprueba si la distancia es menor que la minima de todas las acciones
                            if self.distancer.getDistance(x, buffPacman) < distSouth:
                                distSouth = self.distancer.getDistance(x, buffPacman)
                                if distSouth < minDist:
                                    # Se sobreescribe y se cambia el movimiento a realizar
                                    minDist = distSouth
                        iterator = iterator + 1
        #move EAST
        if Directions.EAST in legal:
            # Starts an iterator as 1 to ignore the pacman
            iterator = 1
            # Stores in a buffer the resulting position of the pacman if it executed the given action
            buffPacman = posPacman[0] + 1, posPacman[1]
            # Checks the target cell doesn't have a wall
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # If there is uneaten food, it takes priority over the ghosts
                if gameState.getDistanceNearestFood() != None:
                    # Searches for the distance to the nearest food
                    foodPos = gameState.getPositionNearestFood(buffPacman)
                    if self.distancer.getDistance(foodPos, buffPacman) < distEast:
                        distEast = self.distancer.getDistance(foodPos, buffPacman)
                        if distEast < minDist:
                            minDist = distEast
                else:
                    # Itera sobre los fantasmas
                    for x in gameState.getGhostPositions():
                        # Comprueba que los fantasmas estan vivos
                        if livingGhosts[iterator] == True:
                            # Se comprueba si la distancia es menor que la minima de todas las acciones
                            if self.distancer.getDistance(x, buffPacman) < distEast:
                                distEast = self.distancer.getDistance(x, buffPacman)
                                if distEast < minDist:
                                    # Se sobreescribe y se cambia el movimiento a realizar
                                    minDist = distEast
                        iterator = iterator + 1
        #move WEST
        if Directions.WEST in legal:
            # Starts an iterator as 1 to ignore the pacman
            iterator = 1
            # Stores in a buffer the resulting position of the pacman if it executed the given action
            buffPacman = posPacman[0] - 1, posPacman[1]
            # Checks the target cell doesn't have a wall
            if walls[buffPacman[0]][buffPacman[1]] == False:
                # If there is uneaten food, it takes priority over the ghosts
                if gameState.getDistanceNearestFood() != None:
                    # Searches for the distance to the nearest food
                    foodPos = gameState.getPositionNearestFood(buffPacman)
                    if self.distancer.getDistance(foodPos, buffPacman) < distWest:
                        distWest = self.distancer.getDistance(foodPos, buffPacman)
                        if distWest < minDist:
                            minDist = distWest
                else:
                    # Itera sobre los fantasmas
                    for x in gameState.getGhostPositions():
                        # Comprueba que los fantasmas estan vivos
                        if livingGhosts[iterator] == True:
                            # Se comprueba si la distancia es menor que la minima de todas las acciones
                            if self.distancer.getDistance(x, buffPacman) < distWest:
                                distWest = self.distancer.getDistance(x, buffPacman)
                                if distWest < minDist:
                                    # Se sobreescribe y se cambia el movimiento a realizar
                                    minDist = distWest
                        iterator = iterator + 1

        # Stores all the distances in a list, that will be passed to a function to create the state
        result = [distNorth, distSouth, distEast, distWest]
        state = self.checkIfMinDist(minDist, result)

        return state

