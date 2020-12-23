from cmu_112_graphics import *
import math
import random
import time
import string
import pickle 

####FRAMEWORK STUFF####

#returns distance between (x1,y1) and (x2,y2)
def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

#from 15-112 course notes 
def almostEqual(d1, d2): 
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)

#class to handle list of possible words that can appear on asteroids
# words from https://www.k12reader.com/subject/vocabulary/fry-words/
# used for asteroid and alien words 
class Words(object):
    wordDict = dict()
    #reads text file containing words 
    @staticmethod
    def readFile(path): #from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
        #used for converting text file to a string
        with open(path, "rt") as f:
            return f.read()

    #returns a list of words from text file
    @staticmethod
    def getWordList(path):
        wordString = (Words.readFile(path))
        wordString.replace("'", "\'")
        wordString.replace("\x08", '\'')
        wordList = wordString.split()
        return wordList
    
    #creates dictionary using wordList
    @staticmethod 
    def getWordDict(path):
        wordList = Words.getWordList(path)
        for elem in wordList:
            elem = elem.lower()
            if(elem[0] not in Words.wordDict):
                Words.wordDict[elem[0]] = {elem}
            else:
                Words.wordDict[elem[0]].add(elem)
        return Words.wordDict
    
    #returns a random word from the word dictionary 
    @staticmethod
    def getRandomWord(path):
        Words.wordDict = dict()
        wordDict = Words.getWordDict(path)
        alpha = Words.getFirstLetters(wordDict)
        i = random.randint(0, len(alpha) - 1)
        key = alpha[i]
        wordChoices = list(wordDict[key])
        if(len(wordChoices) == 1):
            return wordChoices[0]
        i = random.randrange(0, len(wordChoices) - 1)
        return wordChoices[i]
    
    @staticmethod
    #returns string of possible first letters 
    def getFirstLetters(d):
        keys = d.keys()
        return("".join(keys))


#class to represent Player object
class Player(object):
    #sets initial/default values of player
    def __init__(self, name, missed=dict(), matched=dict()):
        self.name = name 
        self.totalAliens = 0 
        self.totalAsteroids = 0 
        self.missedWords = missed
        self.matchedWords = matched
    
    #adds a missed word to the player
    def addMissedWord(self, word):
        if(word in self.missedWords):
            self.missedWords[word] += 1
        else:
            self.missedWords[word] = 1
    
    #adds a matched word to the player
    def addMatchedWord(self, word):
        if(word in self.matchedWords):
            self.matchedWords[word] += 1
        else:
            self.matchedWords[word] = 1
    

#Class to represent asteroid object 
class Asteroid(object):
    #sets default characteristics of asteroids 
    def __init__(self, cx, cy, words):
        self.color = 'gray'
        self.words = words
        self.speed = 5
        self.r = 40
        self.cx = cx
        self.cy = cy
    #moves asteroid down by speed 
    def moveAsteroid(self):
        self.cy += self.speed

#handles alien enemies 
class Alien(object):
    #sets default characteristics of aliens 
    def __init__(self, cx, cy, word):
        self.color = "green"
        dirs = ['down', 'side to side']
        self.dir = dirs[random.randint(0,1)]
        self.isAlive = True 
        self.cx = cx
        self.cy = cy
        self.r = 10
        self.speed = random.randint(2,5)
        self.xdir = random.randint(5,8)
        self.ydir = 2
        self.startAngle = math.pi / 2
        self.word = word
        self.unlocked = False 

    #moves depending on direction
    def moveAlien(self):
        if self.dir == 'down':
            self.cy += self.speed
        elif self.dir == 'side to side':
            self.cx += self.xdir
            self.cy += self.ydir
        
    
#beam that shoots aliens 
class Beam(object):
    #sets default characteristics 
    def __init__(self, cx, cy, speed, size = 5):
        self.startX = cx
        self.startY = cy
        self.cx = cx 
        self.cy = cy 
        self.speed = speed
        self.xspeed = speed
        self.size = size
    
    #adjusts beam to fit direction of shooter
    def adjustBeam(self, newCx, newCy):
        self.cx = newCx
        self.cy = newCy

    #launches beam in linear direction of where the shooter is facing 
    def launchBeam(self, angle):
        slope = math.tan(angle)
        if(almostEqual(angle,math.pi / 2)):  
            self.cy -= self.speed
        elif(slope < 0):
            self.cx -= self.xspeed
            self.cy += slope * self.speed
        elif(slope > 0):
            self.cx += self.xspeed
            self.cy-= slope * self.speed   

    #launches beam parabolically 
    #uses physics formula to calculate x and y for parabolic arc 
    def launchBeamArc(self, angle, initTime):
        timeElapsed = time.time() - initTime
        speed = self.speed * 2
        self.cx +=  speed * timeElapsed * math.cos(angle)
        self.cy -= speed * timeElapsed * math.sin(angle) - 0.5 * (6) * (timeElapsed ** 2)

#defines ice cube object
class iceCube(object):
    #sets initial values 
    def __init__(self,cx, cy):
        self.color = "blue"
        self.dir = 5 
        self.cx = cx
        self.cy = cy
        self.length = 10

    #moves ice cube down
    def moveIceCube(self):
        self.cy += self.dir

#shooter object helps the user aim the beam 
class Shooter(object):
    #sets starter characteristics of the shooter 
    #cx and cy are where the shooter is anchored at the bottom 
    #x and y are where the shooter points 
    def __init__(self, startX, cy, startY, length):
        self.cx = startX 
        self.cy = cy
        self.x = startX 
        self.y = startY
        self.length = length
        self.angle = math.pi/2

    #moves the shooter left or right depending on angleChange 
    def moveShooter(self, angleChange): 
        cx, cy = self.cx, self.cy
        self.angle += angleChange
        if(self.angle < 0 or self.angle > math.pi ): return 
        else:
            self.x = cx + self.length * math.cos(self.angle)
            self.y = cy - self.length * math.sin(self.angle)

