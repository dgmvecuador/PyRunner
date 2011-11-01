import functions
from scroller import *

#class to manage leveling
class levelManager(object):
    def __init__(self):
        #instance variables
        self.currentLevel = 1
        self.frameCount = 0
        self.framesTillNext = 0
        self.levelList = []
        self.activeLevel = None
        self.maxSpeed = 0
        self.minSpeed = 0
        self.speedInd = None
    def add(self,level): #add a level to the levels list
        self.levelList.append(level)
        level.number = len(self.levelList)-1
        if level.speed > self.maxSpeed: #maxSpeed of level assignment
            self.maxSpeed = level.speed
        if self.minSpeed == 0:
            self.minSpeed = level.speed
        if level.speed < self.minSpeed:
            self.minSpeed = level.speed
        functions.debug("maxSpeed: "+str(self.maxSpeed)+"\nminSpeed: "+str(self.minSpeed))
    def setLevel(self, levelNum): #set the level to the levelNum level in the
        #list and make it active, also set the framesTillNext to next level
        try:
            self.activeLevel = self.levelList[levelNum-1]
            self.currentLevel = levelNum
        except IndexError:
            functions.debug("no more levels, fellback to current")
        self.activeLevel.makeActive()
        self.framesTillNext = self.activeLevel.length
        functions.debug("scroller.dx:"+str(scroller.dx))
        if self.speedInd:
            if len(self.levelList) == 1:
                self.speedInd.setPercentage(100)
            else:
                self.speedInd.setPercentage(((self.activeLevel.speed-self.minSpeed)/float(self.maxSpeed-self.minSpeed))*100)
    def frame(self):#called every frame
        self.frameCount += 1
        self.framesTillNext -= 1
        if self.framesTillNext == 0:
            functions.debug("advanced to level: " + str(self.currentLevel+1))
            self.setLevel(self.currentLevel+1) #if there are no frames left
            #go to the next level
    def setIndicator(self,indicator):
        self.speedInd = indicator
    def fallback(self, time): #fallback to a level for a specified time
        if not self.currentLevel == 1:
            self.setLevel(self.currentLevel-1)
            self.framesTillNext = time

#special class which describes a level and its attributes
#can also set the level if given the appropriate objects via enableLevel'
##LEVEL IS INITIALIZED AS SO:
##    attributes is a dictionary containing keys which are the groups to set,the
##    value must be a list which contains values in order for the randomRezGroup
##    (which is the key)
##    values are as so:
##        -maxInRow
##        -minDistanceBetweenRow
##        -maxDistanceBetweenRow
##        -maxDistanceBetweenBlocks
##        -also takes a speed attribute
##        -active
class level(object):
    def __init__(self,attributes,speed,length):
        #assign instance variables
        self.attributes = attributes
        self.speed = speed
        self.number = 0 #empty variable which will store our level number
        self.length = length
        #assigned by manager
    def makeActive(self):
        for key in self.attributes: #go through keys in dictionary and assign
            #values
            values = self.attributes[key]
            key.minDistance = values[3]
            key.minRowDistance = values[1]
            key.maxRowDistance = values[2]
            key.maxInRow = values[0]
            key.active = values[4]
        scroller.dx = self.speed #set speed