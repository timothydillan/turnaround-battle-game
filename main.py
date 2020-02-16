#initialize apis
import pygame, os, sys, time, random
from pygame.locals import *

class Button():
#Class for creating and maintaining unique buttons for a number of different
#purposes.
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

def animateText(text, font, surface, x, y, color):
#Function for printing text. The first block of code acts as a word wrap creator
#in the event that the string is too long to fit in the window. The animated portion
#is simply the act of adding each additional charcter after a tick in the FPS clock.
  if len(text) > 49:
    textLine1 = text[:49]
    textLine2 = text[48:]
  else:
    textLine1 = text
    textLine2 = ""
  i = 0
  for letter in textLine1:
    realLine1 = textLine1[:i]
    textobj1 = font.render(realLine1,1,color)
    textrect1 = textobj1.get_rect()
    textrect1.topleft = (x,y)
    surface.blit(textobj1,textrect1)
    pygame.display.update()
    clock.tick(15)
    i += 1
  j = 0
  for letter in textLine2:
    realLine2 = textLine2[:j]
    textobj2 = font.render(textLine2,1,color)
    textrect2 = textobj2.get_rect()
    textrect2.topleft = (x,y+10)
    surface.blit(textobj2,textrect2)
    pygame.display.update()
    j += 1

if __name__ == '__main__':
    #initialize the screen size
    width = 800
    height = 600
    fps = 60

    #initialize colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)

    #initialize pygame
    pygame.mixer.pre_init(44100, -16, 1, 1024)
    pygame.init()
    #initialize pygame mixer and bg song
    pygame.mixer.init()
    pygame.mixer.music.load("bgmusic.ogg")

    #PLAY BACKGROUND MUSIC
    pygame.mixer.music.play(-1)

    textFont = pygame.font.SysFont("smallfont", 18)
    titleFont = pygame.font.SysFont("flappybirdy", 108)

    #initialize screen size (w, h)
    screen = pygame.display.set_mode((width, height))
    #title of game
    pygame.display.set_caption("PSB Battle Game")

    clock  = pygame.time.Clock()
    #Initialize background img
    backgroundImage = pygame.image.load('bg.png')
    #Initialize start img
    startImage = pygame.image.load('startgame.png')
    #Initialize warrior img
    warriorCharacter = pygame.image.load('warrior.png')
    #Initialize tanker img
    tankerCharacter = pygame.image.load('tanker.png')
    #Initialize warrior enemy img
    warriorEnemyCharacter = pygame.image.load('warriorEnemy.png')
    #Initialize tanker enemy img
    tankerEnemyCharacter = pygame.image.load('tankerEnemy.png')

    #Set character attributes
    warriorATK = random.randint(5, 20)
    warriorDEF = random.randint(1, 10)

    tankerATK = random.randint(1, 10)
    tankerDEF = random.randint(5, 15)

    #bg image
    screen.blit(backgroundImage,[0,0])

    #game start image and text
    #screen.blit(startImage, [310,100])
    animateText("PSB Battle Game ", titleFont, screen, 180, 100, white)
    animateText("CLICK ANYWHERE TO START...", textFont, screen, 275, 500, white)

    #players
    screen.blit(warriorCharacter, [0, 320])
    screen.blit(tankerCharacter, [40, 360])
    screen.blit(warriorCharacter, [0, 400])

    #ai enemy
    screen.blit(tankerEnemyCharacter, [690, 320])
    screen.blit(warriorEnemyCharacter, [650, 360])
    screen.blit(warriorEnemyCharacter, [690, 400])

    pygame.display.update()

    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                start = True

    #display image as button and assign cords
    warriorButton = Button()
    warriorButton.assignImage(warriorCharacter)
    warriorButton.setCoords(280, 347)

    tankButton = Button()
    tankButton.assignImage(tankerEnemyCharacter)
    tankButton.setCoords(430, 340)
    #draw background again and draw the buttons
    screen.blit(backgroundImage, [0,0])
    warriorButton.drawButton(warriorCharacter)
    tankButton.drawButton(tankerEnemyCharacter)

    #update display
    animateText("CHOOSE YOUR UNIT...", textFont, screen, 315, 100, white)

    #start the choosing of unit process
    warriorChoice = 0
    tankChoice = 0

    while warriorChoice + tankChoice < 3:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                #pygame.mixer.Sound.play(clickSound)
                if warriorButton.pressed(mouse) == True:
                  choice = "Warrior"
                  playerImgList = warriorCharacter
                  warriorChoice += 1
                  warriorText = textFont.render('%d Warrior' % (warriorChoice,), 1, (255, 255, 255))
                if tankButton.pressed(mouse) == True:
                  choice = "Tank"
                  playerImgList = tankerEnemyCharacter
                  tankChoice += 1
                  tankerText = textFont.render('%d Tanker' % (tankChoice,), 1, (255, 255, 255))

    #lets draw a counter so that the user can see how many units that they chose
    screen.blit(warriorText, [280, 320])
    screen.blit(tankerText, [443, 320])

    #continue the process
    animateText("CLICK ANYWHERE TO CONTINUE...", textFont, screen, 270, 500, white)
    startscreen = False
    while startscreen == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                startscreen = True

    '''TODO:
    1. Prompt users to assign names for each unit they choose and store the names
    2. Create AI Players (choose a random value from 3 arrays) and assign names to them using the
    format AI_ _ the two placeholders should be a 2-digit random value from 0-99
    3. Warriors should have an attack value from a range of 5 - 20 and defend value between 1 - 10 use randint
    4. Tanker should have an attack value from a range of 1 - 10 and defend value between 5 - 15 use randint
    5. follow other instructions in the assignment guideline
    '''
