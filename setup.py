# Initialize libraries needed for the game.
import pygame, sys, time
from pygame.locals import *
from main import *
from character import *
import self
from random import randint
import copy

# Initialize pygame and the pygame mixer and set screen size (width, height).
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((800, 600))
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'


class Variables():
    # Declare variables in a class so that its easier to call and cleaner.
    FPS = 30
    fpsClock = pygame.time.Clock()
    font = pygame.font.Font('font/SHPinscher-Regular.otf', 90)
    fontText = pygame.font.Font("font/slkscr.ttf", 24)
    pygame.display.set_caption("RPG Game")
    bgImage = pygame.image.load('images/bg.png')
    icon = pygame.image.load("images/icon.png")
    startGame = pygame.image.load('images/startgame.png')
    pygame.display.set_icon(icon)
    warriorImg = pygame.image.load('images/warrior.png')
    tankerImg = pygame.image.load('images/tanker.png')
    warriorEnemyImg = pygame.image.load('images/warriorEnemy.png')
    tankerEnemyImg = pygame.image.load('images/tankerEnemy.png')
    buttonImg = pygame.image.load('images/button.png')
    player1X = 150
    player1Y = 385
    player2X = 50
    player2Y = 375
    aI1X = 550
    aI1Y = 385
    aI2X = 650
    aI2Y = 375
    textX = 150
    textY = 75


class Color():
    black = (0, 0, 0)
    white = (255, 255, 255)
    Gray = (192, 192, 192)
    darkGray = (64, 64, 64)


class Button():
    # Class for creating and maintaining unique buttons for a number of different purposes
    def assignImage(self, picture):
        # function for handling the assignment of an image to each individual button object
        self.rect = picture.get_rect()

    def setCoords(self, x, y):
        # Function for handling the assignment of coordinates for each individual button
        # object
        self.rect.topleft = x, y

    def drawButton(self, picture):
        # Function for handling drawing the actual button on the screen
        screen.blit(picture, self.rect)

    def pressed(self, mouse):
        # Function for determining whether or not a mouse click is inside a button object
        if self.rect.collidepoint(mouse) == True:
            return True


class TextBox(pygame.sprite.Sprite):
    #A "TextBox" class so that we're able to input things unto the screen.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.font = pygame.font.Font(None, 30)
        self.image = self.font.render('Input character name: ', False, Color.white)
        self.rect = self.image.get_rect()
        self.shifted = False

    # Create a function to add captial/non-capital texts
    def AddChar(self, char):
        if char in validChars and not self.shifted:
            self.text += char
        elif char in validChars and self.shifted:
            self.text += shiftChars[validChars.index(char)]
        self.Update()
    # The actual update function so that we can use this while adding characters
    def Update(self):
        old_rect_pos = self.rect.center
        self.image = self.font.render(self.text, False, Color.white)
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_pos


def Title(text, x, y):
    # A function used for creating a title text.
    text = Variables.font.render(text, True, (255, 255, 255))
    screen.blit(text, (x, y))


def clickSound():
    # A function used to play a sound that we define.
    sound = pygame.mixer.Sound('Sound/clickSound.ogg')
    sound.play()


def MenuButton(msg, x, y, w, h, ic, ac, action=None):
    # Similar to the button class, this function also creates a button,
    # but this is mainly for the menu buttons, and the other button is mainly for
    # character choosing etc
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # Get mouse position
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        # Change button color when hovering
        pygame.draw.rect(screen, ic, (x, y, w, h))
        # Check if a button is clicked and there is no action running
        if click[0] == 1 and action != None:
            if action == "play":
                # if the new game button is clicked, run game loop
                clickSound()
                gameLoop()
            elif action == 'load':
                # if the load game button is clicked, load text file from saved game and continue game
                clickSound()
            elif action == "quit":
                # if the quit game button is clicked, quit the game.
                clickSound()
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(screen, ac, (x, y, w, h))
    textSurf, textRect = textObject(msg, Variables.fontText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


def bgMusic():
    # A function used to play a song that we define.
    bgsound = pygame.mixer.music.load('Sound/backgroundmusic.ogg')
    # Loop the music.
    pygame.mixer.music.play(-1)


def Player():
    # Show players on the main menu (UI Purposes)
    screen.blit(Variables.warriorImg, (Variables.player1X, Variables.player1Y))
    screen.blit(Variables.tankerImg, (Variables.player2X, Variables.player2Y))
    screen.blit(Variables.warriorEnemyImg, (Variables.aI1X, Variables.aI1Y))
    screen.blit(Variables.tankerEnemyImg, (Variables.aI2X, Variables.aI2Y))


def textObject(text, font):
    #actually render the text that we're going to use later in a darkgray color
    textSurface = font.render(text, True, Color.darkGray)
    return textSurface, textSurface.get_rect()


def Dialog(text, x, y):
    # This function renders a text.
    text = Variables.fontText.render(text, True, (255, 255, 255))
    screen.blit(text, (x, y))


textBox = TextBox()
textBox.rect.center = [400, 500]
name = []

def startScreen():
    # This function is used for the "click on anywhere" part of the game
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Check if the user clicks anywhere and set the boolean to true
                start = True


def TextBox():
    running = True
    while running:
        screen.blit(Variables.bgImage, [0, 0])
        warriorButton = Button()
        warriorButton.assignImage(Variables.warriorImg)
        warriorButton.setCoords(200, 350)

        tankButton = Button()
        tankButton.assignImage(Variables.tankerEnemyImg)
        tankButton.setCoords(500, 340)
        warriorButton.drawButton(Variables.warriorImg)
        tankButton.drawButton(Variables.tankerEnemyImg)

        Dialog('Give a name for each of your players!', 100, 100)
        Dialog('Choose   units to start your adventure!', 100, 150)

        screen.blit(textBox.image, textBox.rect)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYUP:
                if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    textBox.shifted = False
            if e.type == pygame.KEYDOWN:
                textBox.AddChar(pygame.key.name(e.key))
                if e.key == pygame.K_SPACE:
                    textBox.text += " "
                    textBox.Update()
                if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    textBox.shifted = True
                if e.key == pygame.K_BACKSPACE:
                    textBox.text = textBox.text[:-1]
                    textBox.Update()
                if e.key == pygame.K_RETURN:
                    if len(textBox.text) > 0:
                        name.append(textBox.text)
                        textBox.text = ""
                        textBox.Update()
                        running = False


# joes ver (but i added the global cuz we need to access it out of the scope)
def genAIPlayers(copyTeam):
    global aiTeamList
    aiTeam = copy.deepcopy(copyTeam)

    for aiPlayer in aiTeam:
        aiPlayer.name = 'AI' + str(randint(10, 100))
        aiPlayer.job = randint(0, 1)
        if aiPlayer.job == 0:
            aiPlayer.job = "Warrior"
            aiPlayer.attack = randint(10, 20)
            aiPlayer.defend = randint(5, 10)
        else:
            aiPlayer.job = "Tanker"
            aiPlayer.attack = randint(5, 10)
            aiPlayer.defend = randint(10, 20)

    aiTeamList = aiTeam

    return aiTeam


def aiPlayersButton():
    global aiPlayerButton1, aiPlayerButton2, aiPlayerButton3
    aiPlayerButton1 = Button()
    aiPlayerButton2 = Button()
    aiPlayerButton3 = Button()

    if aiTeamList[0].job == "Warrior":
        aiPlayerButton1.assignImage(Variables.warriorImg)
    else:
        aiPlayerButton1.assignImage(Variables.tankerImg)

    if aiTeamList[1].job == "Warrior":
        aiPlayerButton2.assignImage(Variables.warriorImg)
    else:
        aiPlayerButton2.assignImage(Variables.tankerImg)

    if aiTeamList[2].job == "Warrior":
        aiPlayerButton3.assignImage(Variables.warriorImg)
    else:
        aiPlayerButton3.assignImage(Variables.tankerImg)

def drawPlayers(x0, y0, x1, y1, y2, job0, job1, job2):
    if (job0 == "Warrior"):
        screen.blit(Variables.warriorImg, [x0, y0])
    else:
        screen.blit(Variables.tankerImg, [x0, y0])

    if (job1 == "Warrior"):
        screen.blit(Variables.warriorImg, [x1, y1])
    else:
        screen.blit(Variables.tankerImg, [x1, y1])

    if (job2 == "Warrior"):
        screen.blit(Variables.warriorImg, [x0, y2])
    else:
        screen.blit(Variables.tankerImg, [x0, y2])


def drawAIPlayers(job0, job1, job2):
    if (job0 == "Warrior"):
        aiPlayerButton1.drawButton(Variables.warriorImg)
    else:
        aiPlayerButton1.drawButton(Variables.tankerImg)

    if (job1 == "Warrior"):
        aiPlayerButton2.drawButton(Variables.warriorImg)
    else:
        aiPlayerButton2.drawButton(Variables.tankerImg)

    if (job2 == "Warrior"):
        aiPlayerButton3.drawButton(Variables.warriorImg)
    else:
        aiPlayerButton3.drawButton(Variables.tankerImg)


def gameLoop():
    # Start game by creating a new frame (by loading a bg image)
    screen.blit(Variables.bgImage, [0, 0])

    # Declare units as buttons so that users can pick them.
    warriorButton = Button()
    warriorButton.assignImage(Variables.warriorImg)
    warriorButton.setCoords(200, 350)

    tankButton = Button()
    tankButton.assignImage(Variables.tankerEnemyImg)
    tankButton.setCoords(500, 340)

    # Draw the buttons declared before.
    warriorButton.drawButton(Variables.warriorImg)
    tankButton.drawButton(Variables.tankerEnemyImg)

    # Show some welcoming Text
    Dialog('Welcome to the game!', 100, 100)
    Dialog('Choose   units to start your adventure!', 100, 150)

    # Start choosing process
    # Declare variables needed in the choosing process
    warriorChoice = 0
    tankChoice = 0
    team = []
    # while warriorchoice + tankchoice is less than 3, we create
    while warriorChoice + tankChoice < 3:
        option = 3 - (warriorChoice + tankChoice)
        Dialog('          {}                             '.format(option), 100, 150)
        pygame.display.update()
        # a nested loop (for loop) that loops through the possible pygame event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Check if the mouse is clicking
            elif event.type == MOUSEBUTTONDOWN:
                # Now get the position of the mouse
                mouse = pygame.mouse.get_pos()
                # and check if the warriorbutton is pressed by the mouse
                if warriorButton.pressed(mouse) == True:
                    # add warriorChoice by 1 to make sure that the loop stops if the units reaches 3.
                    warriorChoice += 1
                    # Declare a text that contains a value of how many warriors the player has in his/her team,
                    # so that he/she knows how many unit does he/she have
                    warriorText = Variables.fontText.render('%d Warrior' % (warriorChoice,), 1, (255, 255, 255))
                    team.append(Warrior.create(self))
                    # make a click sound so the user knows that they've clicked on the button
                    clickSound()
                    # ask user to input name
                    TextBox()
                # now check if the tankbutton is pressed by the mouse
                if tankButton.pressed(mouse) == True:
                    # add tankChoice by 1 to make sure that the loop stops if the units reaches 3.
                    tankChoice += 1
                    # Declare a text that contains a value of how many tanker the player has in his/her team,
                    # so that he/she knows how many unit does he/she have
                    tankerText = Variables.fontText.render('%d Tanker' % (tankChoice,), 1, (255, 255, 255))
                    team.append(Tanker.create(self))
                    # make a click sound so the user knows that they've clicked on the button
                    clickSound()
                    # ask user to input name
                    TextBox()

    # assign the default names into the name received
    team[0].name = name[0]
    team[1].name = name[1]
    team[2].name = name[2]
    # generate ai players here
    ai = genAIPlayers(team)
    # after the loop ends, create a new frame
    screen.blit(Variables.bgImage, [0, 0])

    # now lets actually render the text from the while loop before
    if (warriorChoice > 0):
        # the if statement is needed because if the player chooses 3 tankers,
        # that means the warriortext will be null, which will result in a crash
        screen.blit(warriorText, [260, 320])
        screen.blit(Variables.warriorImg, [280, 350])
    if (tankChoice > 0):
        # the if statement is needed because if the player chooses 3 tankers,
        # that means the tankertext will be null, which will result in a crash
        screen.blit(tankerText, [433, 320])
        screen.blit(Variables.tankerEnemyImg, [443, 350])
    # Update the display again so
    # we can continue and remove the
    # elements before (not directly, we're just removing the rendered things)
    Dialog("CLICK ANYWHERE TO CONTINUE...", 100, 100)

    pygame.display.update()

    startScreen()
    # Create new frame to show player characters.
    screen.blit(Variables.bgImage, [0, 0])

    playerATKButton = [Button(), Button(), Button()]
    aiPlayersButton()
    drawPlayers(0, 290, 70, 350, 405, team[0].job, team[1].job, team[2].job)
    drawAIPlayers(ai[0].job, ai[1].job, ai[2].job)

    playerATKButton[0].assignImage(Variables.buttonImg)
    playerATKButton[1].assignImage(Variables.buttonImg)
    playerATKButton[2].assignImage(Variables.buttonImg)

    playerATKButton[0].setCoords(20, 290)
    playerATKButton[1].setCoords(90, 350)
    playerATKButton[2].setCoords(20, 405)

    playerATKButton[0].drawButton(Variables.buttonImg)
    playerATKButton[1].drawButton(Variables.buttonImg)
    playerATKButton[2].drawButton(Variables.buttonImg)

    firstPlayer = 0
    secondPlayer = 0
    thirdPlayer = 0

    while firstPlayer or secondPlayer or thirdPlayer < 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                clickSound()
                if playerATKButton[0].pressed(mouse) == True:
                    firstPlayer += 1
                if playerATKButton[1].pressed(mouse) == True:
                    secondPlayer += 1
                if playerATKButton[2].pressed(mouse) == True:
                    thirdPlayer += 1

    pygame.display.update()

    # Create new frame
    screen.blit(Variables.bgImage, [0, 0])

    # TODO: generate ai players and draw ai buttons
    # TODO: tell user to choose which enemy to attack same like the one above
    drawAIPlayers(ai[0].job, ai[1].job, ai[2].job)

    Dialog("CLICK ON WHICH ENEMY YOU WANT TO ATTACK...", 100, 100)

    firstAI = 0
    secondAI = 0
    thirdAI = 0
    while firstAI or secondAI or thirdAI < 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                clickSound()
                if aiPlayerButton1.pressed(mouse) == True:
                    firstAI += 1
                if aiPlayerButton2.pressed(mouse) == True:
                    secondAI += 1
                if aiPlayerButton3.pressed(mouse) == True:
                    thirdAI += 1

    pygame.display.update()

    screen.blit(Variables.bgImage, [0, 0])

    # update display
    # create new frame
    # start attack function