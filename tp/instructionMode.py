from cmu_112_graphics import *
from framework import *
class instructionMode(Mode):
    #loads text and background image
    def appStarted(mode):
        #from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html 
        #used to read instructions text file 
        mode.instructionString = ''
        with open('../tp/instructions.txt', "rt") as f:
            mode.instructionString = f.read()
        
        #from t.ly/8bIN 
        #used for background image 
        mode.background = mode.loadImage('../tp/instructionBackground.png')
    
    #handles mouse events 
    def mousePressed(mode, event):
        if(mode.width * 7 // 8 <= event.x <= mode.width - 10 and
            mode.height * 7 // 8 <= event.y <= mode.height - 10):
            mode.app.setActiveMode(mode.app.homeScreenMode)
    
    #draws canvas
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width // 2, mode.height  // 2, 
                            image = ImageTk.PhotoImage(mode.background))
        canvas.create_text(10, 10, text = mode.instructionString, 
                            anchor = 'nw', font = 'arial 15 bold', fill = 'white')
        
        canvas.create_rectangle(mode.width * 7 // 8, mode.height * 7 // 8, 
                                    mode.width - 10, mode.height - 10,
                                    fill = 'gray')      
        cx = ((mode.width * 7 // 8) + (mode.width - 10)) // 2
        cy = ((mode.height * 7 // 8 +  mode.height - 10)) // 2
        canvas.create_text(cx, cy, text = 'home', fill = 'black', 
                                font = 'arial 15 bold' )
