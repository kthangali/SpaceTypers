from cmu_112_graphics import * 
from framework import *
#represents game state of program
class GameMode(Mode):
    #initializes/calls functions to initialize value
    def appStarted(mode):
        mode.initTime = int(time.time()) 
        mode.controlCenterHeight = 100
        
        try:
            #from wiki python https://wiki.python.org/moin/UsingPickle 
            #used for storing user data 
            mode.players = pickle.load( open( "players.txt", "rb" ) )
        except FileNotFoundError:
            d = dict()
            pickle.dump(d, open( "players.txt", "wb" ) )
            mode.players = pickle.load( open( "players.txt", "rb" ) )
        mode.player = None
        
        
        mode.entryDimensions = (mode.width * 3 // 10,
                                mode.height - mode.controlCenterHeight * 4 // 5, 
                                mode.width * 5.5 / 10,
                                mode.height - mode.controlCenterHeight // 5)
        mode.shooterChange = 2 * math.pi / 50
        initializeSuccess = False
        while not initializeSuccess:
            try:
                mode.initializeGame()
                initializeSuccess=True
            except AttributeError:
                pass
        mode.gameOver = False
        

    #initializes game state
    def initializeState(mode):
        mode.secondsClear = 0 
        mode.score = 0 
        mode.enteringText = True
        mode.wordMatched = False
        mode.paused = False
        mode.frozen = False
        mode.iceCubePresent = False
        mode.textEntered = ""
        mode.asteroidPresent = False 
        mode.asteroidWords = [] 
        mode.beamOnArc = False
        mode.beamSpeed = 15 / 2 
        mode.beamSpeedLevel = 1
        mode.beamOnShooter = True
        mode.beamSize = 5
        mode.arcInit = None
        mode.beamShot = False
        mode.ricochet = False
        mode.bigBullet = False
        mode.playerWins = False
        mode.iceCubeInit = None
        mode.streak = 0 
        mode.secondsClear = 0
        mode.aliensReachedGround = 0
        mode.toggledFrozen = False
        
    #initializes current missed and matched words 
    #incorrectly typed refers to a mistype 
    #missed completely refers to if a word floats off screen
    def initializeData(mode):
        mode.currIncorrectlyTyped = set()
        mode.currMatched = set()
        mode.currMissedCompletely = set()


    #initializes objects
    def initializeObjects(mode):
        mode.aliens = []
        mode.alienWords = set()
        mode.asteroid = None
        mode.iceCube = None
        mode.shooter = Shooter(mode.width // 2, 
                            mode.height - mode.controlCenterHeight, 
                            mode.height - mode.controlCenterHeight - 
                            mode.height // 8, 
                            mode.height // 8)
        mode.beam = Beam(mode.width // 2, mode.shooter.y - mode.beamSize, mode.beamSpeed)

    #initializes images 
    def initializeImages(mode):
        #used for background image
        url = 'https://tinyurl.com/y4aynkm8'
        mode.background = mode.loadImage(url)

        #image from https://webstockreview.net/pict/getfirst
        # used for asteroid graphics
        mode.asteroidImage = mode.loadImage('../tp/asteroid.png')
        mode.asteroidImage = mode.scaleImage(mode.asteroidImage, 1/3)

        # image from http://www.freestockphotos.biz/stockphoto/15883
        # used for alien graphics
        mode.alienImage = mode.loadImage('../tp/alienImage.png')
        mode.alienImage = mode.scaleImage(mode.alienImage, 1/5)

        #image from http://clipart-library.com/clipart/ice-cube-clip-art-3.htm
        # used for ice cube graphics
        mode.iceCubeImage = mode.loadImage('../tp/iceCubeImage.png')
        mode.iceCubeImage = mode.scaleImage(mode.iceCubeImage, 1/10)


    #initializes game, calls other initializing functions
    def initializeGame(mode):
        mode.player = Player(mode.getUserInput("Enter your name").lower()) 
        if(mode.playerInData(mode.player)):
            mode.player = mode.findPlayer(mode.player)
        
        mode.level = mode.getUserInput("Please enter a level (1-5)")
        while mode.level not in [str(x) for x in range(1,6)]:
            mode.level = mode.getUserInput("Please enter a level (1-5)")
        mode.path = f"../tp/level{mode.level}.txt"
        mode.initializeState()
        mode.initializeObjects()
        mode.initializeImages()
        mode.initializeData()


    #checks if player has played the game before
    def playerInData(mode, player):
        return player.name in mode.players.keys()
    
    #finds player if they have played before 
    #returns new player with previous state 
    def findPlayer(mode, player):
        name = player.name 
        missed, matched = mode.players[name]
        newPlayer = Player(name, missed, matched)
        return newPlayer
        
    #called by timerFired 
    def doStep(mode):
        try:
            if(mode.player == None or mode.gameOver or mode.playerWins): return 
            else:
                if(mode.secondsClear >= 60):
                    mode.playerWins = True 
                    players = pickle.load( open( "players.txt", "rb" ) )
                    players[mode.player.name] = (mode.player.missedWords, 
                                            mode.player.matchedWords)      
                    pickle.dump(players, open( "players.txt", "wb" ) )
                currTime = int(time.time())
                if((currTime  - mode.initTime) % 5 == 0 and len(mode.aliens) < 3 and
                    not mode.frozen):
                    mode.dropAlien()
                if((currTime - mode.initTime) % 40 == 0 and not mode.frozen):
                    mode.dropIceCube()
                if((currTime - mode.initTime) % 25 == 0 and not mode.asteroidPresent
                    and not mode.frozen):
                    mode.dropAsteroid()
                if(mode.asteroidPresent and not mode.frozen):
                    mode.handleAsteroids()
                if(len(mode.aliens) > 0 and not mode.frozen):
                    mode.handleAliens()
                if(mode.beamShot):
                    if(mode.beamOnArc):    
                        mode.beam.launchBeamArc(mode.shooter.angle, mode.arcInit)        
                    else:
                        mode.beam.launchBeam(mode.shooter.angle) 
                    if(mode.beamHitsAlien()):
                        mode.score += 2 
                    elif(mode.beamHitsWall() and mode.ricochet):
                        mode.beam.xspeed *= -1
                    elif(mode.beamHitsNothing()):
                        if(mode.bigBullet):
                            mode.beam = Beam(mode.shooter.x, mode.shooter.y, mode.beamSpeed, 
                            mode.beamSize * 3)
                            mode.bigBullet = False
                        else: mode.beam = Beam(mode.shooter.x, mode.shooter.y, mode.beamSpeed)
                        if(mode.ricochet): 
                            mode.ricochet = False 
                            mode.beam.speed = mode.beamSpeed 
                        mode.beamShot = False
                        mode.beamOnShooter = True
                if(mode.iceCubePresent):
                    mode.handleIceCube()
                if(mode.frozen and not mode.toggledFrozen):
                    if((currTime - mode.iceCubeInit) % 5 == 0 and 
                        currTime != mode.iceCubeInit):
                        mode.frozen = False
        except AttributeError:
            pass
             
    #calls doStep to handle timer events 
    def timerFired(mode):
        try:
            if(not mode.paused and mode.player != None
                and not mode.playerWins and not mode.gameOver):
                mode.doStep()
        except AttributeError:
            pass

    #handles key presses
    def keyPressed(mode, event):
        if(mode.player == None): return
        elif(event.key == 'Left' and not mode.beamShot and 
            mode.shooter.angle < math.pi - mode.shooterChange):
            mode.shooter.moveShooter(mode.shooterChange)
            if(not mode.beamShot):
                mode.beam.cx, mode.beam.cy = mode.shooter.x, mode.shooter.y
        elif(event.key == 'Right' and not mode.beamShot and 
                mode.shooter.angle > mode.shooterChange):
            mode.shooter.moveShooter(mode.shooterChange * -1)
            if(not mode.beamShot):
                mode.beam.cx, mode.beam.cy = mode.shooter.x, mode.shooter.y
        elif(event.key == 'Space'):
            mode.beamOnShooter = False
            mode.beamShot = True
            mode.arcInit = time.time()
        elif(event.key == 'A' and not mode.ricochet):
            mode.beamOnArc = not mode.beamOnArc
        elif(event.key == '1'):
            mode.beam.speed = 15 / 2
            mode.beamSpeed = 15 / 2
            mode.beamSpeedLevel = 1
        elif(event.key == '2'):
            mode.beam.speed = 10
            mode.beamSpeed = 10
            mode.beamSpeedLevel = 2
        elif(event.key == '3'):
            mode.beam.speed = 25 / 2
            mode.beamSpeed = 25 / 2
            mode.beamSpeedLevel = 3
        elif(event.key == 'P'): 
            mode.paused = not mode.paused
        elif(event.key == 'S' and mode.paused): 
                mode.doStep()
        elif(event.key == 'R'):
            mode.ricochet = not mode.ricochet
            mode.beamOnArc = False
            mode.beam.xspeed = 30
            mode.beam.speed = 10 
        elif(event.key == 'B'):
            mode.bigBullet = not mode.bigBullet
        elif(event.key == 'F'):
            mode.frozen = not mode.frozen
            mode.toggledFrozen = not mode.toggledFrozen
        elif(event.key == 'G'):
            mode.gameOver = True
            players = pickle.load( open( "players.txt", "rb" ) )
            players[mode.player.name] = (mode.player.missedWords, 
                                    mode.player.matchedWords)      
            pickle.dump(players, open( "players.txt", "wb" ) )
        elif(event.key == 'W'):
            mode.playerWins = True 
            players = pickle.load( open( "players.txt", "rb" ) )
            players[mode.player.name] = (mode.player.missedWords, 
                                    mode.player.matchedWords)      
            pickle.dump(players, open( "players.txt", "wb" ) )
        elif(mode.enteringText):
            if(event.key in string.ascii_lowercase or event.key == "'"):
                mode.textEntered += event.key 
            elif(event.key == 'Delete'):
                mode.textEntered = mode.textEntered[:-1]
            elif(event.key == 'Enter'):
                if(mode.textEntered in mode.alienWords):
                    mode.handleAlienMatch()
                elif(mode.textEntered in mode.asteroidWords):
                    mode.handleAsteroidMatch()
                else: 
                    mode.handleMissedWord()
                mode.textEntered = ''
    
    #handles mouse click events 
    def mousePressed(mode, event):
        x, y = event.x, event.y
        if(mode.width // 4 <= event.x <= mode.width // 2 and 
            mode.height * 2 // 3 <= event.y <= mode.height * 5 // 6
            and (mode.gameOver or mode.playerWins)):
            mode.app.setActiveMode(mode.app.reportMode)
            mode.app.reportMode.appStarted()

        elif(mode.width // 2 + 5 <= event.x <= mode.width * 3 // 4 + 5 and 
            mode.height * 4 // 6 <= event.y <=mode.height * 5 // 6 and 
            (mode.gameOver or mode.playerWins)):
            mode.app.setActiveMode(mode.app.homeScreenMode)

    #handles if user types word on alien 
    def handleAlienMatch(mode):
        targetAlien = None
        for alien in mode.aliens:
            if(alien.word == mode.textEntered):
                targetAlien = alien 
                break
        mode.alienWords.remove(mode.textEntered)
        if(mode.textEntered not in mode.currIncorrectlyTyped):
            mode.player.addMatchedWord(mode.textEntered)
            mode.currMatched.add(mode.textEntered)
        targetAlien.word = None
        targetAlien.unlocked = True 

    #handles if user types word on asteroid
    def handleAsteroidMatch(mode):
        words = []
        index = None
        for i in range(len(mode.asteroidWords)):
            if(mode.asteroidWords[i] == mode.textEntered):
                index = i
                break
        if(mode.textEntered not in mode.currIncorrectlyTyped):
            mode.player.addMatchedWord(mode.textEntered)
            mode.currMatched.add(mode.textEntered)
        mode.asteroidWords [i] = None
    
    #handles if user misses word 
    def handleMissedWord(mode):
        missedWord = mode.textEntered
        commonLetterCount =  dict() 
        for word in mode.alienWords:
            if(word != None):
                commonLetterCount[word] = 0
        for word in mode.asteroidWords:
            if(word != None):
                commonLetterCount[word] = 0
        for key in commonLetterCount: 
            commonLetterCount[key] = mode.numCommonLetters(missedWord, key)
        attemptedWord = mode.findHighestCount(commonLetterCount)
        if(attemptedWord != None):
            mode.currIncorrectlyTyped.add(attemptedWord)
            mode.player.addMissedWord(attemptedWord)

    #finds number of common letters between missedWord and key 
    def numCommonLetters(mode, missedWord, key):
        missedWord = set(missedWord)
        key = set(key)
        count = 0
        for letter in missedWord:
            if letter in key:
                count += 1
        return count

    #finds word with highest number of similar letters in d
    def findHighestCount(mode, d):
        highest = 0
        highestKey = None
        for key in d:
            if(d[key] > highest):
                highestKey = key
                highest = d[key]
        return highestKey
        
    #drops alien if timerFired calls 
    def dropAlien(mode):
            while True: 
                try:
                    if not mode.gameOver:
                        cx = random.randint(0, mode.width)
                        cy = 0 
                        word = Words.getRandomWord(mode.path)
                        if(mode.alienIsLegal(cx, cy, 10, word)):
                            mode.alienWords.add(word)
                            mode.aliens.append(Alien(cx, 0, word))
                            break
                except AttributeError:
                    pass
    
    #handles ice cube object
    def handleIceCube(mode):
        mode.iceCube.moveIceCube()
        if(mode.beamHitsIceCube()):
            mode.frozen = True
            mode.iceCube = None
            mode.iceCubePresent = False
            mode.iceCubeInit = int(time.time())
            mode.beam = Beam(mode.shooter.x, mode.shooter.y, mode.beamSpeed)
            mode.beamOnShooter = True
            mode.beamShot = False
        elif(mode.iceCubeHitsGround()):
            mode.iceCube = None
            mode.iceCubePresent = False
            
    #handles asteroid object
    def handleAsteroids(mode):
        asteroid = mode.asteroid
        asteroid.moveAsteroid()
        word1, word2, word3 = mode.asteroid.words
        if(mode.asteroidHitsGround(asteroid)):
            for word in [word1, word2, word3]:
                if(word != None and word not in mode.player.missedWords):
                    if(word not in mode.player.missedWords):
                        mode.player.addMissedWord(word)
                    mode.currMissedCompletely.add(word)
            mode.streak = 0
            mode.asteroid.words = None
            mode.asteroid = None
            mode.asteroidPresent = False 
        elif(word1 == word2 == word3 == None):
            mode.score += 10 
            mode.asteroid = None
            mode.asteroidPresent = False
            mode.clearAliens()
            mode.secondsClear += 5
            if(mode.streak % 3 == 0): 
                if(mode.beamOnShooter and not mode.beamShot):
                    mode.beam = Beam(mode.shooter.x, mode.shooter.y, mode.beamSpeed, 
                    mode.beamSize * 3)
                else:
                    mode.bigBullet = True
            elif(mode.streak % 5 == 0):
                mode.ricochet = True
                mode.beamOnArc = False
                mode.beam.xspeed = 30
                mode.beam.speed = 10
 
    #handles alien objects
    def handleAliens(mode):
        i = 0
        while(i < len(mode.aliens)):
            alien = mode.aliens[i]
            cx = alien.cx + alien.xdir 
            if(cx < 0):
                alien.cx = alien.r
                alien.xdir *= -1
            elif(cx > mode.width):
                alien.cx = mode.width - alien.r
                alien.xdir *= -1
            alien.moveAlien()

            if(mode.beamNearsAlien(alien)):
                if(mode.beam.xspeed > 0):
                    alien.cx -= random.randint(5,15)
                else:
                    alien.cx += random.randint(5,15)
                alien.cy += 5
            if(mode.alienHitsGround(alien)):
                mode.aliens.remove(alien)
                if(alien.word != None and alien.word in mode.alienWords):
                    mode.currMissedCompletely.add(alien.word)
                    mode.alienWords.remove(alien.word)
                if(alien.word not in mode.player.missedWords and alien.word != None):
                    mode.player.addMissedWord(alien.word)
                mode.aliensReachedGround += 1
                if(mode.score > 15 and not alien.unlocked):
                    mode.score -= 15
                elif(mode.score > 5 and alien.unlocked):
                    mode.score -= 5
                if(mode.aliensReachedGround >= 10): 
                    mode.gameOver = True
                    players = pickle.load( open( "players.txt", "rb" ) )
                    players[mode.player.name] = (mode.player.missedWords, 
                                            mode.player.matchedWords)      
                    pickle.dump(players, open( "players.txt", "wb" ) )
            else:
                i += 1

    #drops asteroid if timerFired calls     
    def dropAsteroid(mode):
        while True: 
            try:
                if not mode.gameOver:
                    cx = random.randint(0, mode.width)
                    cy = 0 
                    word1 = Words.getRandomWord(mode.path)
                    word2 = Words.getRandomWord(mode.path)
                    word3 = Words.getRandomWord(mode.path)
                    w = [word1, word2, word3]
                    if(mode.asteroidIsLegal(cx, cy, 40) and word1 != word2 
                        and word1 != word3 and word2 != word3 and 
                        word1 not in mode.alienWords and 
                        word2 not in mode.alienWords
                        and word3 not in mode.alienWords):
                        mode.asteroid = (Asteroid(cx, cy, w))
                        mode.asteroidPresent = True 
                        mode.asteroidWords = w
                        break
            except AttributeError:
                pass
    
    #drops ice cube if timerFired calls
    def dropIceCube(mode):
        cx = random.randint(0, mode.width) 
        if(mode.iceCubeIsLegal(cx)):
            mode.iceCube = iceCube(cx, 0)
            mode.iceCubePresent = True
    
    #ensures ice cube is within bounds of screen
    def iceCubeIsLegal(mode, cx): 
        w, h = mode.iceCubeImage.size
        return 0 <= cx - w // 2 and cx + w // 2 <= mode.width

    #clears all the aliens 
    def clearAliens(mode):
        mode.streak += 1
        mode.aliens = []
    
    #checks if beam leaves the screen
    def beamHitsNothing(mode):
        cx, cy, r = mode.beam.cx, mode.beam.cy, mode.beam.size
        if(mode.ricochet):
            return (cy - r < 0 or cy + r >= mode.width)
        else:
            return (cx - r < 0 or cx + r >= mode.width or 
                cy - r < 0 or cy + r >= mode.height)

    #handles wall bounces if beam should ricochet
    def beamHitsWall(mode):
        cx, r = mode.beam.cx, mode.beam.size
        return (cx - r <= 0 or cx + r >= mode.width)

    #checks if beam hits an alien 
    def beamHitsAlien(mode):
        if(not mode.beamShot):
            return False
        beamCx, beamCy, beamR = mode.beam.cx, mode.beam.cy, mode.beam.size
        i = 0 
        while(i < len(mode.aliens)):
            alien = mode.aliens[i]
            alienCx, alienCy = alien.cx, alien.cy
            alienW, alienH = mode.alienImage.size
            if((distance(alienCx, alienCy, beamCx, beamCy) <= alienW // 2 + beamR
                or distance(alienCx, alienCy, beamCx, beamCy) <= alienH // 2 + beamR) 
                    and alien.unlocked):
                    mode.aliens.remove(alien)
                    if(alien.word in mode.alienWords):
                        mode.alienWords.remove(alien.word)
                    if(mode.ricochet):
                        mode.beam.xspeed *= -1
                    return True
            else:
                i += 1
        return False

    #checks if beam goes near an alien 
    #alien may move away if beam nears it 
    def beamNearsAlien(mode, alien):
        beamCx, beamCy, beamR = mode.beam.cx, mode.beam.cy, mode.beam.size
        alienCx, alienCy = alien.cx, alien.cy
        alienW, alienH = mode.alienImage.size
        if(distance(alienCx, alienCy, beamCx, beamCy) <= alienW // 2 + beamR + 15
            or distance(alienCx, alienCy, beamCx, beamCy) <= alienH // 2 + beamR + 15
            and not mode.frozen):
            if(not alien.unlocked):
                probability = random.randint(1,10)
                if(probability in [1,2,3,4,5]):
                    if(mode.ricochet):
                            mode.beam.xspeed *= -1
                    return True
            elif(alien.unlocked):
                probability = random.randint(1,10)
                if(probability in [1,2]):
                    if(mode.ricochet):
                            mode.beam.xspeed *= -1
                    return True
        return False
    
    #checks if beam hits the ice cube 
    def beamHitsIceCube(mode):
        bcx, bcy, br = mode.beam.cx, mode.beam.cy, mode.beam.size
        icx, icy = mode.iceCube.cx, mode.iceCube.cy
        iceCubeW, iceCubeH = mode.iceCubeImage.size
        if(not mode.beamOnShooter):
            if(distance(bcx, bcy, icx, icy) < br + iceCubeW // 2 or 
                distance(bcx, bcy, icx, icy) < br + iceCubeH // 2 ):
                return True
        return False

    #checks if the asteroid reaches the ground 
    def asteroidHitsGround(mode, asteroid): 
        w, h = mode.asteroidImage.size
        if(asteroid.cy + h // 2 >= mode.height - mode.controlCenterHeight):
            return True
        return False
    
    #checks if the iceCube hits the ground
    def iceCubeHitsGround(mode):
        if(mode.iceCube.cy + mode.iceCube.length  
            >= mode.height - mode.controlCenterHeight):
            return True
        return False

    #checks if the asteroid is within bounds of window
    def asteroidIsLegal(mode, cx, cy, r):
        if(cx - r < 0 or cx + r > mode.width):
            return False
        return True
    
    #makes sure aliens do not overlap and are within bounds of window 
    def alienIsLegal(mode, cx, cy, r, word):
        w, h = mode.alienImage.size
        if(cx - w // 2 < 0 or cx + w // 2 > mode.width):
            return False
        for alien in mode.aliens: 
            acx = alien.cx
            acy = alien.cy 
            if((distance(acx, acy, cx, cy)  <= 2 * r) or word in mode.alienWords):
                return False
        return True

    #checks if alien hits the ground
    def alienHitsGround(mode, alien): 
        alienW, alienH = mode.alienImage.size
        if(alien.cy + alienH // 2 >= mode.height - mode.controlCenterHeight):
            return True
        return False
    
    #draws ice cube
    def drawIceCube(mode, canvas):
        if(mode.iceCubePresent and mode.iceCube != None ):
            cx = mode.iceCube.cx
            cy = mode.iceCube.cy 
            canvas.create_image(cx, cy, 
                                image = ImageTk.PhotoImage(mode.iceCubeImage))

    #draws background 
    def drawBackground(mode, canvas):
        try:
            canvas.create_image(mode.width / 2, mode.height / 2, 
                                image = ImageTk.PhotoImage(mode.background))
        except AttributeError:
            pass

    #draws asteroid 
    def drawAsteroid(mode, canvas):
        asteroid = mode.asteroid
        cx, cy, r = asteroid.cx, asteroid.cy, asteroid.r
        word1, word2, word3 = asteroid.words
        canvas.create_image(cx, cy, image = ImageTk.PhotoImage(mode.asteroidImage))
        if(word1 != None):
            canvas.create_text(cx, cy - 20, text = word1, 
                                font = 'arial 20 bold')
        if(word2 != None):
            canvas.create_text(cx, cy, text = word2, 
                                font = 'arial 20 bold')
        if(word3 != None):
            canvas.create_text(cx, cy + 20, text = word3, 
                                font = 'arial 20 bold')
    
    #draws aliens 
    def drawAliens(mode, canvas):
        for alien in mode.aliens:
            cx, cy, r, word = alien.cx, alien.cy, alien.r, alien.word
            canvas.create_image(cx , cy, image = ImageTk.PhotoImage(mode.alienImage))
            if(alien.word != None):
                canvas.create_text(cx, cy + 5, text = word, 
                                    font = 'arial 15 bold', fill = 'white')
    
    #draws shooter
    def drawShooter(mode, canvas):
        startX, startY = mode.shooter.cx, mode.shooter.cy
        shooterX, shooterY = mode.shooter.x, mode.shooter.y
        canvas.create_line(startX, startY, shooterX, 
                            shooterY, width = 20, fill = 'yellow')
    
    #draws beam
    def drawBeam(mode, canvas):
        cx, cy, r = mode.beam.cx, mode.beam.cy, mode.beam.size
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = 'white')
    
    #draws control center at bottom 
    def drawControlCenter(mode, canvas):
        canvas.create_rectangle(0, mode.height - mode.controlCenterHeight,
                                 mode.width, mode.height, fill = 'gray')
        if(mode.ricochet):
            canvas.create_text(mode.width // 12, 
                            mode.height - mode.controlCenterHeight //2, 
                            text = 'R', font = 'arial 17 bold', anchor = 'e')
        canvas.create_text(mode.width // 10, 
                        mode.height - mode.controlCenterHeight //2, 
                        text = f'Speed: {mode.beamSpeedLevel}', anchor = 'w', 
                        font = 'arial 12 bold')
        canvas.create_text(mode.width * 2 // 10 , 
                            mode.height - mode.controlCenterHeight // 2, 
                            text = f'Score: {mode.score}', anchor = 'w', 
                            font = 'arial 12 bold') 
        canvas.create_text(mode.width * 5.6 // 10, 
                            mode.height - mode.controlCenterHeight // 2,  
                            text = f'Aliens reached: {mode.aliensReachedGround}',
                            anchor = 'w', font = 'arial 12 bold')
        canvas.create_text(mode.width * 7 // 10, 
                            mode.height - mode.controlCenterHeight // 2, 
                            text = f'Seconds cleared: {mode.secondsClear}',
                            anchor = 'w', font = 'arial 12 bold')
        if(mode.beamOnArc):
            p = 'on'
        else:
            p = 'off'
        canvas.create_text(mode.width * 8.7 // 10, 
                            mode.height - mode.controlCenterHeight // 2, 
                            text = f'Parabola: {p}', anchor = 'w', 
                            font = 'arial 12 bold')
        mode.drawTextEntry(canvas, mode.width * 3 // 10,
                        mode.height - mode.controlCenterHeight * 4 // 5, 
                        mode.width * 5.5 / 10,
                        mode.height - mode.controlCenterHeight // 5, mode.textEntered)

    #draws text entry field 
    def drawTextEntry(mode, canvas, x0, y0, x1, y1, textEntry ):
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'white')
        cx = (x1 + x0) // 2
        cy = (y0 + y1) // 2
        canvas.create_text(cx, cy, text = textEntry, font = 'arial 14 bold') 

    #draws game over screen
    def drawGameOver(mode, canvas):
        canvas.create_text(mode.width // 2, mode.height // 2,
                            text = "Game Over :(", fill = 'white', 
                            font = "Arial 24 bold")
        
    def drawEndButtons(mode, canvas):
        canvas.create_rectangle(mode.width // 4, mode.height * 4 // 6, 
                                mode.width // 2, mode.height * 5 // 6, 
                                fill = 'gray' )
        canvas.create_text((mode.width // 4 + mode.width // 2) / 2,     
                            (mode.height * 4 // 6 + mode.height * 5 // 6) / 2,               
                                text = 'View report', font = 'arial 16 bold')
        canvas.create_rectangle(mode.width // 2 + 5, mode.height * 4 // 6, 
                                mode.width * 3 // 4 + 5, mode.height * 5 // 6,
                                fill = 'gray')
        canvas.create_text((mode.width // 2 + 5 + mode.width * 3 // 4 + 5) // 2, 
                            (mode.height * 4 // 6 + mode.height * 5 // 6) // 2, 
                            text = 'home', font = 'arial 16 bold', fill = 'black')
                


    #draws winning screen
    def drawWin(mode, canvas):
        canvas.create_text(mode.width // 2, mode.height // 2,
                            text = "You win!!!", fill = 'white', 
                            font = "Arial 24 bold")
        canvas.create_rectangle(mode.width // 4, mode.height * 4 // 6, 
                                mode.width // 2, mode.height * 5 // 6, 
                                fill = 'gray' )
        canvas.create_text((mode.width // 4 + mode.width // 2) / 2,     
                            (mode.height * 4 // 6 + mode.height * 5 // 6) / 2,               
                                text = 'View report', font = 'arial 16 bold')
    
    #calls necessary drawing functions 
    def redrawAll(mode, canvas):
        mode.drawBackground(canvas)
        try:
            if(mode.gameOver):
                mode.drawGameOver(canvas)
                mode.drawEndButtons(canvas)
            elif(mode.playerWins):
                mode.drawWin(canvas)
                mode.drawEndButtons(canvas)
            else:
                mode.drawShooter(canvas)
                mode.drawBeam(canvas)
                mode.drawControlCenter(canvas)
                mode.drawIceCube(canvas)
                mode.drawAliens(canvas)
                if(mode.asteroidPresent and mode.asteroid != None):
                    mode.drawAsteroid(canvas)
        except AttributeError:
            pass
            