from framework import * 
from UserDataMode import * 
from GameMode import *
from cmu_112_graphics import * 
from homeScreenMode import *
from reportMode import *
from instructionMode import *
#handles different modes of game
#framework/instructions for modal app from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
class MyModalApp(ModalApp):
    def appStarted(app):
        app.homeScreenMode = HomeScreenMode()
        app.gameMode = GameMode()  
        app.instructionMode = instructionMode()    
        app.userDataMode = UserDataMode()
        app.reportMode = ReportMode()     
        app.setActiveMode(app.homeScreenMode) 

app = MyModalApp(width = 800, height = 600)
