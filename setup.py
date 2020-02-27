import pygame, sys, time
from pygame.locals import *
from main import *

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((800, 600))

class Variables():
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
  def assignImage(self, picture):
    self.rect = picture.get_rect()
  def setCoords(self, x,y):
    self.rect.topleft = x,y
  def drawButton(self, picture):
    screen.blit(picture, self.rect)
  def pressed(self,mouse):
    if self.rect.collidepoint(mouse) == True:
      return True

def Title(text, x, y):
    text = Variables.font.render(text, True, (255, 255, 255))
    screen.blit(text, (x,y))

def clickSound():
    sound = pygame.mixer.Sound('Sound/clickSound.ogg')
    sound.play()

def MenuButton(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ic, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                clickSound()
                gameLoop()
            elif action == 'load':
                clickSound()
            elif action == 'option':
                clickSound()
            elif action == "quit":
                clickSound()
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(screen, ac, (x,y, w, h))
    textSurf_1, textRect_1 = textObject(msg, Variables.fontText)
    textRect_1.center = ((x + (w/2)), (y + (h/2)))
    screen.blit(textSurf_1, textRect_1)

def bgMusic():
    bgsound = pygame.mixer.music.load('Sound/backgroundmusic.ogg')
    pygame.mixer.music.play(-1)

def Player():
    screen.blit(Variables.warriorImg, (Variables.player1X, Variables.player1Y))
    screen.blit(Variables.tankerImg, (Variables.player2X, Variables.player2Y))
    screen.blit(Variables.warriorEnemyImg, (Variables.aI1X, Variables.aI1Y))
    screen.blit(Variables.tankerEnemyImg, (Variables.aI2X, Variables.aI2Y))

def textObject(text, font):
    textSurface = font.render(text, True, Color.darkGray)
    return textSurface, textSurface.get_rect()

def Dialog(text, x, y):
    text = Variables.fontText.render(text, True, (255, 255, 255))
    screen.blit(text, (x, y))

def startScreen():
    startscreen = False
    while startscreen == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                startscreen = True

def gameLoop():
    screen.blit(Variables.bgImage, [0, 0])

    warriorButton = Button()
    warriorButton.assignImage(Variables.warriorImg)
    warriorButton.setCoords(200, 350)

    tankButton = Button()
    tankButton.assignImage(Variables.tankerEnemyImg)
    tankButton.setCoords(500, 340)

    warriorButton.drawButton(Variables.warriorImg)
    tankButton.drawButton(Variables.tankerEnemyImg)

    Dialog('Welcome to the game!', 100, 100)
    Dialog('Choose 3 units to start your adventure!', 100, 150)
    pygame.display.update()
    warriorChoice = 0
    tankChoice = 0
    while warriorChoice + tankChoice < 3:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if warriorButton.pressed(mouse) == True:
                  warriorChoice += 1
                  warriorText = Variables.fontText.render('%d Warrior' % (warriorChoice,), 1, (255, 255, 255))
                  clickSound()
                if tankButton.pressed(mouse) == True:
                  tankChoice += 1
                  tankerText = Variables.fontText.render('%d Tanker' % (tankChoice,), 1, (255, 255, 255))
                  clickSound()


    screen.blit(Variables.bgImage, [0, 0])
    Dialog("CLICK ANYWHERE TO CONTINUE...", 100, 100)
    #we need to check if the warriorchoice is more than 0 so that if the
    #user chooses 3 tanker/warrior it doesnt crash
    if (warriorChoice > 0):
        screen.blit(warriorText, [260, 320])
        screen.blit(Variables.warriorImg, [280, 350])
    if (tankChoice > 0):
        screen.blit(tankerText, [433, 320])
        screen.blit(Variables.tankerEnemyImg, [443, 350])

    pygame.display.update()
    startScreen()
