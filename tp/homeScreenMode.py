from cmu_112_graphics import *

#class for home screen mode
class HomeScreenMode(Mode):
    #loads background image
    def appStarted(mode):
        #image from https://tinyurl.com/y5nmlfhh
        #used for background
        #I used Canva to scale the photo and add the title 
        mode.image = mode.loadImage('../tp/homeScreenBackground.png')

    #detects button presses 
    def mousePressed(mode, event):
        #code for button presses was taken from piazza post @3791
        #I changed the dimensions/bounds/color of the button to make it fit my
        #layout better
        cx, cy = mode.width/2, mode.height/2
        if ((cx-150 <= event.x <= cx-5) and
            (cy-50 <= event.y <= cy+50)):
            mode.app.setActiveMode(mode.app.gameMode)
            if(mode.app.gameMode.gameOver or mode.app.gameMode.playerWins):
                mode.app.gameMode.appStarted()
        elif(cx - 50 <= event.x <= cx + 95 and
                cy - 50 <= event.y <= cy + 50): 
                mode.app.setActiveMode(mode.app.instructionMode)
        elif(cx + 100 <= event.x <= cx + 245 and
            cy - 50 <= event.y <= cy + 50):
            mode.app.setActiveMode(mode.app.userDataMode)

    #draws screen
    def redrawAll(mode, canvas): 
        canvas.create_image(mode.width / 2, mode.height / 2, 
                            image = ImageTk.PhotoImage(mode.image))
        cx, cy = mode.width/2, mode.height/2
        canvas.create_rectangle(cx-200, cy-50, cx - 55, cy+50, fill='gray')
        canvas.create_text(cx - 127, cy, text='Play game!')
        canvas.create_rectangle(cx - 50, cy-50, cx + 95, cy+50, fill='gray')
        canvas.create_text(cx + 22.5, cy, text='Instructions')
        canvas.create_rectangle(cx + 100, cy-50, cx + 245, cy+50, fill='gray')
        canvas.create_text(cx + 172.5, cy, text='User Data')