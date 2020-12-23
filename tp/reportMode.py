from GameMode import * 
from cmu_112_graphics import *
from framework import *
#class for the report that is generated at the end of a game 
class ReportMode(Mode):
    #sets initial state
    def appStarted(mode):
        mode.incorrect = mode.app.gameMode.currIncorrectlyTyped
        mode.missedCompletely = mode.app.gameMode.currMissedCompletely
        mode.matched = mode.app.gameMode.currMatched
        mode.practiceWords = list(mode.incorrect.union(mode.missedCompletely))
        mode.textEntryWidth = 200
        mode.textEntryHeight = 150
        mode.currIndex = 0
        mode.currentWord = None
        if(len(mode.practiceWords) > 0):
            mode.currentWord = mode.practiceWords[0]
        mode.textEntered = ''
        mode.complete = False
        #image from https://i.pinimg.com/originals/b4/2b/ad/b42badff8069acf080b4b57857670e8c.jpg
        #used for background
        mode.backgroundImage = mode.loadImage('../tp/reportBackground.jpg')
        mode.backgroundImage = mode.scaleImage(mode.backgroundImage, 0.3)
    
    #changes the word to the next one if the user types it correctly 
    #sets complete to true if there are no more words to type 
    def changeWord(mode):
        if(mode.currIndex >= len(mode.practiceWords) - 1):
            mode.complete = True
        else:
            mode.currIndex += 1
            mode.currentWord = mode.practiceWords[mode.currIndex]

    #handles key events
    def keyPressed(mode, event):
        if(event.key in string.ascii_lowercase or event.key == "'"):
            mode.textEntered += event.key 
        elif(event.key == 'Delete'):
            mode.textEntered = mode.textEntered[:-1]
    
    #returns true if the user has correctly typed the word
    def checkMatch(mode):
        return mode.textEntered == mode.currentWord
    
    #handles timer events
    def timerFired(mode):
        matched = mode.checkMatch()
        if(matched): 
            mode.changeWord()
            mode.textEntered = ''
    
    #handles mouse clicks/button presses
    def mousePressed(mode, event):
        if(mode.width * 7 // 8 <= event.x <= mode.width - 10 and
            mode.height * 7 // 8 <= event.y <= mode.height - 10):
            mode.app.setActiveMode(mode.app.homeScreenMode)
            mode.complete = False
    
    #draws textbox that displays the word 
    def drawTextDisplay(mode, canvas, word):
        x0 = mode.width // 2 - mode.textEntryWidth // 2
        x1 = mode.width // 2 + mode.textEntryWidth // 2
        y0 = mode.height * 3 // 5 - mode.textEntryHeight // 2
        y1 = mode.height * 3 // 5 + mode.textEntryHeight // 2
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'white', outline = 'black',
                                width = 5)
        cx = (x1 + x0) // 2
        cy = (y0 + y1) // 2
        canvas.create_text(cx - mode.textEntryWidth // 2 - 5, 
                            cy, text = 'word:', anchor = 'e', fill = 'white', 
                            font = 'arial 13 bold')
        canvas.create_text(cx, cy - 5, text = word, font = 'arial 20 bold')

    #draws text entry field
    def drawTextEntry(mode, canvas, textEntered):
        x0 = mode.width // 2 - mode.textEntryWidth // 2
        x1 = mode.width // 2 + mode.textEntryWidth // 2
        y0 = mode.height * 4 // 5 + 5 - mode.textEntryHeight // 2
        y1 = mode.height * 4 // 5 + 5 + mode.textEntryHeight // 2
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'white', outline = 'black', 
                                width = 5)
        cx = (x1 + x0) // 2
        cy = (y0 + y1) // 2
        canvas.create_text(cx - mode.textEntryWidth // 2 - 5, cy, 
                            text = 'Enter word here:', fill = 'white', anchor = 'e', 
                            font = 'arial 13 bold')
        canvas.create_text(cx, cy, text = textEntered, font = 'arial 20 bold')
    
    #draws complete screen if the user has typed all the words
    def drawComplete(mode, canvas):
        canvas.create_text(mode.width // 2, mode.height * 7 // 10, 
                        text = "Complete!", fill = 'white', font = 'arial 20 bold')
    
    #draws canvas
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width // 2, mode.height // 2, 
                            image = ImageTk.PhotoImage(mode.backgroundImage) )
        canvas.create_text(mode.width // 2, mode.height // 10, 
                            text = f'You typed {len(mode.matched)} word(s) correctly', 
                            fill = 'white',font = 'arial 16 bold')
        canvas.create_text(mode.width // 2, mode.height  // 5, 
                            text = f'You typed {len(mode.incorrect)} word(s) incorrectly', 
                            fill = 'white', font = 'arial 16 bold')
        canvas.create_text(mode.width // 2 , mode.height * 3 // 10, 
                        text = f'You missed {(len(mode.missedCompletely))} words',
                        fill = 'white', font = 'arial 16 bold')
        if(mode.currentWord == None):
            canvas.create_text(mode.width // 2, mode.height * 2 // 5, 
                            text = 'You missed no words, good job :)', 
                            fill = 'white', font = 'arial 16 bold')
        else:
            canvas.create_text(mode.width // 2, mode.height * 2 // 5, 
                                text = 'Practice the missed/incorrect words below', 
                                fill = 'white', font = 'arial 16 bold')
            if(not mode.complete):
                mode.drawTextDisplay(canvas, mode.currentWord)
                mode.drawTextEntry(canvas, mode.textEntered)
            else:
                mode.drawComplete(canvas)   
        canvas.create_rectangle(mode.width * 7 // 8, mode.height * 7 // 8, 
                                    mode.width - 10, mode.height - 10,
                                    fill = 'gray')      
        cx = ((mode.width * 7 // 8) + (mode.width - 10)) // 2
        cy = ((mode.height * 7 // 8 +  mode.height - 10)) // 2
        canvas.create_text(cx, cy, text = 'home', fill = 'black', 
                                font = 'arial 15 bold' )

                    
                

        
