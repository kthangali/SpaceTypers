from cmu_112_graphics import *
import string
from framework import *
class UserDataMode(Mode):
    #sets up mode
    def appStarted(mode):
        mode.noData = False
        mode.player = None
        mode.missedWords = None
        mode.matchedWords = None
        mode.nameEntered = False
        mode.name = ''
        mode.textBoxWidth = 200 
        mode.textBoxHeight = 150
        mode.homeButtonWidth = 50
        #image from https://t4.ftcdn.net/jpg/02/89/72/69/360_F_289726988_cF9wzIATeSAOBxCg23NqnLeaKVfXWvdy.jpg
        #used for background
        mode.background = mode.loadImage('../tp/dataBackground.jpg')
        mode.background = mode.scaleImage(mode.background, 2)

    #finds the user based on input 
    def findUser(mode, name):
        try:
            users = pickle.load( open( "players.txt", "rb" ) )
        except FileNotFoundError:
            d = dict()
            pickle.dump(d, open( "players.txt", "wb" ) )
            users = pickle.load( open( "players.txt", "rb" ) )
        if(name not in users):
            mode.noData = True
        else:
            mode.missedWords = users[name][0]
            mode.matchedWords = users[name][1]
            mode.topFiveMissed = mode.findTopFive(mode.missedWords)
            mode.topFiveMatched = mode.findTopFive(mode.matchedWords)
    
    #finds top five most frequent words in d
    def findTopFive(mode, d):
        sortedDict = dict()
        if(len(d) <= 5):
            return list(d.items())
        else: 
            #from https://tinyurl.com/y2serbgm
            #used to sort the dictionary in descending order to find 
            #most commonly missed words 
            sortedDict = sorted(d.items(), key = lambda x: x[1],
                                reverse = True)
            return list(reversed(sortedDict[0:5]))
    
    #key event handler
    def keyPressed(mode, event):
        if(mode.nameEntered): return 
        else:
            if(event.key in string.ascii_lowercase or event.key in 
                string.digits):
                mode.name += event.key 
            elif(event.key == 'Delete'):
                mode.name = mode.name[:-1]
            elif(event.key == 'Enter'):
                mode.findUser(mode.name)
                mode.nameEntered = True
    
    #mouse event handler
    def mousePressed(mode, event):
        if(mode.width // 2 + 5 <= event.x <= mode.width // 2 + 5 + mode.homeButtonWidth
           and  mode.height * 9 // 10 <= mode.height - 10):
            mode.nameEntered = False
            mode.noData = False
            mode.name = ''
            mode.app.setActiveMode(mode.app.homeScreenMode)

        elif(mode.width // 2 - 5 - mode.homeButtonWidth <= event.x <= mode.width // 2 - 5
            and mode.height * 9 // 10 <= event.y <= mode.height - 10):
            mode.name = ''
            mode.noData = False
            mode.nameEntered = False

    #draws entry box
    def drawTextBox(mode, canvas):
        w, h = mode.textBoxWidth, mode.textBoxHeight
        width, height = mode.width, mode.height
        color = 'white'
        canvas.create_rectangle(width // 2 - w // 2, height // 2 - h// 2, 
                               width // 2 + w// 2, height // 2 + h// 2,
                               width = 5, fill = color)
        canvas.create_text(width // 2, height // 2 - h - 10, 
                            text = 'Please enter a name', font = 'arial 20 bold', 
                            fill = color)
        canvas.create_text(width // 2, height // 2, text = mode.name, 
                            font = 'arial 20 bold')

    #draws back/home buttons    
    def drawHomeAndBackButtons(mode, canvas):
        canvas.create_rectangle(mode.width // 2 + 5, mode.height * 9 // 10, 
                                    mode.width // 2 + 5 + mode.homeButtonWidth, mode.height - 10,
                                    fill = 'gray')      
        cx = ((mode.width // 2 + 5) +  \
                (mode.width // 2 + 5 + mode.homeButtonWidth)) // 2

        cy = ((mode.height * 9 // 10 +  mode.height - 10)) // 2
        canvas.create_text(cx, cy, text = 'home', fill = 'black', 
                                font = 'arial 15 bold' )
        if(mode.nameEntered):
            canvas.create_rectangle(mode.width // 2 - 5 - mode.homeButtonWidth, 
                                    mode.height * 9 // 10, 
                                    mode.width // 2 - 5 , mode.height - 10,
                                    fill = 'gray')
            cx = ((mode.width // 2 - 5 - mode.homeButtonWidth) +  \
                (mode.width // 2 - 5 )) // 2

            cy = ((mode.height * 9 // 10 +  mode.height - 10)) // 2
            canvas.create_text(cx, cy, text = 'back', fill = 'black', 
                                    font = 'arial 15 bold' )
                            
    #draws mode
    def redrawAll(mode, canvas): 
        color = 'white'
        canvas.create_image(mode.width // 2, mode.height // 2, image = ImageTk.PhotoImage(mode.background))
        mode.drawHomeAndBackButtons(canvas)
        if(not mode.nameEntered):
            mode.drawTextBox(canvas)
        else:
            if(mode.noData):
                canvas.create_text(mode.width // 2, mode.height // 2, 
                                    text = 'No data for this user', 
                                    font = 'arial 25 bold', fill = color)
            else:
                canvas.create_text(mode.width // 2, mode.height // 9, 
                                    text = f"Data For {mode.name}", 
                                    font = 'arial 25 bold', fill = color)
                canvas.create_text(mode.width // 5, mode.height // 7, text = 'Frequently Missed', 
                                    font = 'arial 20 bold', fill = color)
                canvas.create_text(mode.width * 4 // 5, mode.height // 7, text = 'Frequently Matched',
                                    font = 'arial 20 bold', fill = color)
                for i in range(0,5):
                    if(i < len(mode.topFiveMissed)):
                        canvas.create_text(mode.width // 5, mode.height * (i + 1) // 5.5, 
                                            text = f'{i + 1}. {(mode.topFiveMissed[i][0])}', 
                                            font = 'arial 15 bold', fill = color)
                for i in range(0,5):
                    if(i < len(mode.topFiveMatched)):
                        canvas.create_text(mode.width * 4// 5, mode.height * (i + 1) // 5.5, 
                                            text = f'{i + 1}. {(mode.topFiveMatched[i][0])}', 
                                            font = 'arial 15 bold', fill = color)
                
                    

