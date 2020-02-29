#Initialize libraries needed for the game.
import pygame, sys, time
from pygame.locals import *
from main import *

#Initialize pygame and the pygame mixer and set screen size (width, height).
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((800, 600))
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

class Variables():
    #Declare variables in a class so that its easier to call and cleaner.
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
    white =(255, 255, 255)
    Gray = (192, 192, 192)
    darkGray = (64, 64, 64)

class Button():
  #Class for creating and maintaining unique buttons for a number of different purposes
  def assignImage(self, picture):
  #function for handling the assignment of an image to each individual button object
    self.rect = picture.get_rect()
  def setCoords(self, x,y):
  #Function for handling the assignment of coordinates for each individual button
  #object
    self.rect.topleft = x,y
  def drawButton(self, picture):
  #Function for handling drawing the actual button on the screen
    screen.blit(picture, self.rect)
  def pressed(self,mouse):
  #Function for determining whether or not a mouse click is inside a button object
    if self.rect.collidepoint(mouse) == True:
      return True

class TextBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.font = pygame.font.Font(None, 30)
        self.image = self.font.render('Input character name: ', False, Color.white)
        self.rect = self.image.get_rect()

    def AddChar(self, char):
        global shiftDown
        if char in validChars and not shiftDown:
            self.text += char
        elif char in validChars and shiftDown:
            self.text += shiftChars[validChars.index(char)]
        self.Update()

    def Update(self):
        old_rect_pos = self.rect.center
        self.image = self.font.render(self.text, False, Color.white)
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_pos

def Title(text, x, y):
    #A function used for creating a title text.
    text = Variables.font.render(text, True, (255, 255, 255))
    screen.blit(text, (x,y))

def clickSound():
    #A function used to play a sound that we define.
    sound = pygame.mixer.Sound('Sound/clickSound.ogg')
    sound.play()

def MenuButton(msg, x, y, w, h, ic, ac, action=None):
    #Similar to the button class, this function also creates a button,
    #but this is mainly for the menu buttons, and the other button is mainly for
    #character choosing etc
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #Get mouse position
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        #Change button color when hovering
        pygame.draw.rect(screen, ic, (x, y, w, h))
        #Check if a button is clicked and there is no action running
        if click[0] == 1 and action != None:
            if action == "play":
                #if the new game button is clicked, run game loop
                clickSound()
                gameLoop()
            elif action == 'load':
                #if the load game button is clicked, load text file from saved game and continue game
                clickSound()
            elif action == "quit":
                #if the quit game button is clicked, quit the game.
                clickSound()
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(screen, ac, (x,y, w, h))
    textSurf, textRect = textObject(msg, Variables.fontText)
    textRect.center = ((x + (w/2)), (y + (h/2)))
    screen.blit(textSurf, textRect)

def bgMusic():
    #A function used to play a song that we define.
    bgsound = pygame.mixer.music.load('Sound/backgroundmusic.ogg')
    #Loop the music.
    pygame.mixer.music.play(-1)

def Player():
    #Show players on the main menu (UI Purposes)
    screen.blit(Variables.warriorImg, (Variables.player1X, Variables.player1Y))
    screen.blit(Variables.tankerImg, (Variables.player2X, Variables.player2Y))
    screen.blit(Variables.warriorEnemyImg, (Variables.aI1X, Variables.aI1Y))
    screen.blit(Variables.tankerEnemyImg, (Variables.aI2X, Variables.aI2Y))

def textObject(text, font):
    textSurface = font.render(text, True, Color.darkGray)
    return textSurface, textSurface.get_rect()

def Dialog(text, x, y):
    #This function renders a text.
    text = Variables.fontText.render(text, True, (255, 255, 255))
    screen.blit(text, (x, y))

textBox = TextBox()
shiftDown = False
textBox.rect.center = [400, 500]
name = []

def startScreen():
    #This function is used for the "click on anywhere" part of the game
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                #Check if the user clicks anywhere and set the boolean to true
                start = True


def TextBox(font):
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

        Dialog('Choose 3 units to start your adventure!', 100, 100)
        Dialog('AND Give a name for each of your players!', 100, 150)
        
        screen.blit(textBox.image, textBox.rect)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYUP:
                if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = False
            if e.type == pygame.KEYDOWN:
                textBox.AddChar(pygame.key.name(e.key))
                if e.key == pygame.K_SPACE:
                    textBox.text += " "
                    textBox.Update()
                if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = True
                if e.key == pygame.K_BACKSPACE:
                    textBox.text = textBox.text[:-1]
                    textBox.Update()
                if e.key == pygame.K_RETURN:
                    if len(textBox.text) > 0:
                        name.append(textBox.text)
                        textBox.text = ""
                        textBox.Update()
                        running = False

def gameLoop():
    #Start game by creating a new frame (by loading a bg image)
    screen.blit(Variables.bgImage, [0, 0])

    '''#Create button
    AttackButton = Button()
    AttackButton.assignImage(Variables.buttonImg)
    AttackButton.setCoords(200, 300) #coords depends
    AttackButton.drawButton(Variables.buttonImg)
    Dialog('ATTACK', 300, 200) #coords depends'''

    #Declare units as buttons so that users can pick them.
    warriorButton = Button()
    warriorButton.assignImage(Variables.warriorImg)
    warriorButton.setCoords(200, 350)

    tankButton = Button()
    tankButton.assignImage(Variables.tankerEnemyImg)
    tankButton.setCoords(500, 340)

    #Draw the buttons declared before.
    warriorButton.drawButton(Variables.warriorImg)
    tankButton.drawButton(Variables.tankerEnemyImg)

    #Show some welcoming Tex
    Dialog('Welcome to the game!', 100, 100)
    Dialog('Choose 3 units to start your adventure!', 100, 150)

    #Update the display so that it can continue to the new frame.
    pygame.display.update()

    #Start choosing process
    #Declare variables needed in the choosing process
    warriorChoice = 0
    tankChoice = 0
    #while warriorchoice + tankchoice is less than 3, we create
    while warriorChoice + tankChoice < 3:
        #a nested loop (for loop) that loops through the possible pygame event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #Check if the mouse is clicking
            elif event.type == MOUSEBUTTONDOWN:
                #Now get the position of the mouse
                mouse = pygame.mouse.get_pos()
                #and check if the warriorbutton is pressed by the mouse
                if warriorButton.pressed(mouse) == True:
                  #add warriorChoice by 1 to make sure that the loop stops if the units reaches 3.
                  warriorChoice += 1
                  #Declare a text that contains a value of how many warriors the player has in his/her team,
                  #so that he/she knows how many unit does he/she have
                  warriorText = Variables.fontText.render('%d Warrior' % (warriorChoice,), 1, (255, 255, 255))
                  #make a click sound so the user knows that they've clicked on the button
                  clickSound()
                  #ask user to input name
                  TextBox(pygame.font.Font(None, 30))
                #now check if the tankbutton is pressed by the mouse
                if tankButton.pressed(mouse) == True:
                  #add tankChoice by 1 to make sure that the loop stops if the units reaches 3.
                  tankChoice += 1
                  #Declare a text that contains a value of how many tanker the player has in his/her team,
                  #so that he/she knows how many unit does he/she have
                  tankerText = Variables.fontText.render('%d Tanker' % (tankChoice,), 1, (255, 255, 255))
                  #make a click sound so the user knows that they've clicked on the button
                  clickSound()
                  # ask user to input name
                  TextBox(pygame.font.Font(None, 30))
    #after the loop ends, create a new frame
    screen.blit(Variables.bgImage, [0, 0])
    Dialog("CLICK ANYWHERE TO CONTINUE...", 100, 100)
    #now lets actually render the text from the while loop before
    if (warriorChoice > 0):
        #the if statement is needed because if the player chooses 3 tankers,
        #that means the warriortext will be null, which will result in a crash
        screen.blit(warriorText, [260, 320])
        screen.blit(Variables.warriorImg, [280, 350])
    if (tankChoice > 0):
        #the if statement is needed because if the player chooses 3 tankers,
        #that means the tankertext will be null, which will result in a crash
        screen.blit(tankerText, [433, 320])
        screen.blit(Variables.tankerEnemyImg, [443, 350])
    #Update the display again so
    #we can continue and remove the
    #elements before (not directly, we're just removing the rendered things)
    pygame.display.update()
    startScreen()


