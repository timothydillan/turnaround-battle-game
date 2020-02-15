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

def drawText(text, font, surface, x, y, color):
#Simple function for drawing text onto the screen. Function contains expression
#for word wrap.
  if len(text) > 49:
    textLine1 = text[:48]
    textLine2 = text[48:]
  else:
    textLine1 = text
    textLine2 = ""

  textobj1 = font.render(textLine1,1,color)
  textrect1 = textobj1.get_rect()
  textrect1.topleft = (x,y)
  surface.blit(textobj1,textrect1)
  pygame.display.update()

  textobj2 = font.render(textLine2,1,color)
  textrect2 = textobj2.get_rect()
  textrect2.topleft = (x,y+10)
  surface.blit(textobj2,textrect2)
  pygame.display.update()

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
    textlist = ['evan gay', 'evan sangat gay', 'evan kok gay sih?']
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
    pygame.init()
    #initialize pygame mixer and bg song
    pygame.mixer.init()
    pygame.mixer.music.load("bgmusic.ogg")
    #PLAY BACKGROUND MUSIC LETS GO BOYS
    pygame.mixer.music.play(-1)

    font = pygame.font.SysFont("smallfont", 18)

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
    #display main screen
    #bg image
    screen.blit(backgroundImage,[0,0])

    #game start image and text
    screen.blit(startImage, [310,100])
    animateText("CLICK ANYWHERE TO START...", font, screen, 275, 500, white)

    #players
    screen.blit(warriorCharacter, [0, 230])
    screen.blit(tankerCharacter, [10, 370])
    screen.blit(warriorCharacter, [0, 380])

    #ai enemy
    screen.blit(warriorEnemyCharacter, [630, 230])
    screen.blit(tankerEnemyCharacter, [630, 370])
    screen.blit(warriorEnemyCharacter, [630, 380])

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
    warriorButton.setCoords(250, 300)

    tankButton = Button()
    tankButton.assignImage(tankerEnemyCharacter)
    tankButton.setCoords(400, 340)
    #draw background again and draw the buttons
    screen.blit(backgroundImage, [0,0])
    warriorButton.drawButton(warriorCharacter)
    tankButton.drawButton(tankerEnemyCharacter)

    #update display
    animateText("CHOOSE YOUR UNIT...", font, screen, 300, 100, white)

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
                if warriorButton.pressed(mouse) == True:
                  choice = "Warrior"
                  playerImgList = warriorCharacter
                  warriorChoice += 1
                  warriorText = font.render('%d Warrior' % (warriorChoice,), 1, (255, 255, 255))
                if tankButton.pressed(mouse) == True:
                  choice = "Tank"
                  playerImgList = tankerEnemyCharacter
                  tankChoice += 1
                  tankerText = font.render('%d Tanker' % (tankChoice,), 1, (255, 255, 255))

    #lets draw a counter so that the user can see how many units that they chose
    screen.blit(warriorText, [247, 300])
    screen.blit(tankerText, [450, 325])
    pygame.display.update()

    #continue the process
    animateText("CLICK ANYWHERE TO CONTINUE...", font, screen, 270, 500, white)
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
