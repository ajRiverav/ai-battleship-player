
# coding: utf-8

# A simplified version of the game Battleship is used to train an agent using Reinforcement Learning. 
# 
# The board will consist of a single col with n rows, or squares. Only one ship is allowed and has a size of m<n squares.
# 
# The expectation is for the agent to learn to
# a) fire at intervals of m squares (because a ship has a size of m squares and one would sample the space quicker this way), and
# b) fire at squares adjacent to the previous hit. 
# 
# We believe a policy like this one will minimize the number of shots required to sink the ship.
# 
# Once this is achieved, we will move on to more, larger ships, and a bigger board. 

# Let's first develop the game engine:

import random
import numpy as np
from enum import Enum
import tensorflow as tf
import matplotlib as plt

class SHOT_RESULT(Enum):
    INVALID = 0
    HIT = 1
    MISS = 2

class GAME_STATUS(Enum):
    IN_PROGRESS = 0
    COMPLETE = 1

RewardFun = {SHOT_RESULT.MISS:-1,\
             SHOT_RESULT.HIT:1,\
             SHOT_RESULT.INVALID:-100}

def genShipCoords(shipSize, minCoord, maxCoord):
    coordinates = [0]*shipSize
    coordinates[0] = random.randint(minCoord, maxCoord)
    for i in range(1,shipSize):
        coordinates[i] = coordinates[i-1] + 1 if coordinates[i-1] < maxCoord else coordinates[i-1]-1
    return coordinates

class SimpleBattleship(object):
    
    # Only a one-row board is implemented for now
    def __init__(self, shipCoords, numBoardRows, numBoardCols):

        self.shipCoords = shipCoords
        self.numBoardRows = numBoardRows
        self.numBoardCols = numBoardCols
        self.shotsTakenSofar = []

        # the board will always have another dimension to show
        # where the crosshair is pointing at
        self.board = np.zeros(shape=[self.numBoardRows+1, self.numBoardCols])
        self.crossHairCoord = 0 # cross-hair always starts at left most pos
        self.updateCrossHairCoord(self.crossHairCoord)

    def updateCrossHairCoord(self, coord, val=1):
        # reset board
        self.board[self.numBoardRows,range(self.numBoardCols)] = 0
        # show new crosshair location
        self.board[self.numBoardRows, coord] = val

    def fireShot(self, shotCoordinate):

        # Cannot take the same shot twice
        if shotCoordinate in self.shotsTakenSofar:
            self.updateCrossHairCoord(shotCoordinate)
            return self.getState(), RewardFun[SHOT_RESULT.INVALID], GAME_STATUS.COMPLETE

        else:
            self.shotsTakenSofar.append(shotCoordinate)

            # Cannot play outside the board
            if not 0 <= shotCoordinate <= self.numBoardCols:
                # Invalid
                # update crossHair to be outside board = all zero
                self.updateCrossHairCoord(range(0,self.numBoardCols), 0)
                return self.getState(), RewardFun[SHOT_RESULT.INVALID], GAME_STATUS.COMPLETE

            elif shotCoordinate in self.shipCoords:
                # Hit
                self.updateState(shotCoordinate, 1)
                # The crosshair moves to where we fired at.
                self.updateCrossHairCoord(shotCoordinate)

                # Did we sink the ship?
                if sum(self.board[0, :]==1)==2:
                    return self.getState(), RewardFun[SHOT_RESULT.HIT], GAME_STATUS.COMPLETE
                else:
                    return self.getState(), RewardFun[SHOT_RESULT.HIT], GAME_STATUS.IN_PROGRESS

            else:
                # Miss
                self.updateState(shotCoordinate, -1)
                # The crosshair moves to where we fired at.
                self.updateCrossHairCoord(shotCoordinate)
                return self.getState(), RewardFun[SHOT_RESULT.MISS], GAME_STATUS.IN_PROGRESS

    def getState(self):
        return self.board
    
    def updateState(self,coord, val):
        self.board[0,coord] = val

# Set-up
NUM_EPISODES = 1000
BOARD_SIZE = (1,10)
SHIP_SIZE = 2

ship = genShipCoords(SHIP_SIZE, BOARD_SIZE[0], BOARD_SIZE[1])
print("SHIP LOCATION:{}".format(ship))
actionSet = (-1,1) #LEFT=-1, RIGHT= +1

# Neural Network for Q-table (aka Q-network)
tf.reset_default_graph()

#These lines establish the feed-forward part of the network used to choose actions
inputs1 = tf.placeholder(shape=[2,BOARD_SIZE[1]],dtype=tf.float32)
W = tf.Variable(tf.random_uniform([BOARD_SIZE[1],1],0,0.01)) #
Qout = tf.matmul(inputs1,W)
predict = tf.argmax(Qout,0)

#Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
nextQ = tf.placeholder(shape=[2,1],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)

init = tf.global_variables_initializer()
    
# Set learning parameters
y = .7
e = 0.1
#create lists to contain total rewards and steps per episode
jList = []
rList = []
with tf.Session() as sess:
    sess.run(init)
    for i in range(NUM_EPISODES):
        #Reset environment and get first new observation
        game = SimpleBattleship(ship, BOARD_SIZE[0], BOARD_SIZE[1])
        s = game.getState()
        crossHair = 0

        rAll = 0
        termEpisode = False
        j = 0
        #The Q-Network
        print("New Episode")
        print(game.getState())
        while j < 20: #should never need more than 10 (max number of legal moves if board size is 10
            j+=1
            #Choose an action by greedily (with e chance of random action) from the Q-network
            actionIdx,allQ = sess.run([predict,Qout],feed_dict={inputs1:s})

            if np.random.rand(1) < e:
                actionIdx = [random.randint(0,len(actionSet)-1)]
            #Get new state and reward from environment
            crossHair += actionSet[actionIdx[0]]

            s1,r, gameStatus = game.fireShot(crossHair) #0:MISS, 1:HIT, 2:INVALID
            print(str(j)+"\n")
            print(s1)

            if gameStatus == GAME_STATUS.COMPLETE:
                termEpisode = True


            #Obtain the Q' values by feeding the new state through our network
            Q1 = sess.run(Qout,feed_dict={inputs1:s1})
            #Obtain maxQ' and set our target value for chosen action.
            maxQ1 = np.max(Q1)
            targetQ = allQ
            targetQ[actionIdx[0]] = r + y*maxQ1
            #Train our network using target and predicted Q values
            _,W1 = sess.run([updateModel,W],feed_dict={inputs1:s,nextQ:targetQ})
            rAll += r

            s = s1

            if termEpisode == True:
                #Reduce chance of random action as we train the model.
                e = 1./((i/50) + 10)
                break
        jList.append(j)
        rList.append(rAll)

plt.plot(rList)

