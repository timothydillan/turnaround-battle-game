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
    clock.tick(20)
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

#lets just make it here so that we can access it later (global scope)


def genAIPlayers():
    #START "AI" CREATION (ofc its possible to shorten the code and use functions instead, but lets just use this as a raw idea.)
    global aiPlayer1
    global aiPlayer2
    global aiPlayer3

    global aiPlayer1Button
    global aiPlayer2Button
    global aiPlayer3Button

    global AIplayerImg1
    global AIplayerImg2
    global AIplayerImg3

    #get a random integer to determine a character for the AI
    randoChara1 = random.randint(1, 2)
    randoChara2 = random.randint(1, 2)
    randoChara3 = random.randint(1, 2)

    #get a random integer between 10 and 99 (to make sure its 2 digits) for the AI name
    playerDigit1 = random.randint(10, 99)
    playerDigit2 = random.randint(10, 99)
    playerDigit3 = random.randint(10, 99)

    #pre-define images for each AI players
    AIplayerImg1 = warriorCharacter
    AIplayerImg2 = warriorCharacter
    AIplayerImg3 = warriorCharacter

    aiPlayer1Button = Button()
    aiPlayer2Button = Button()
    aiPlayer3Button = Button()
    #check if randomchar == 1, 1 == warrior, and 2 == tanker
    if randoChara1 == 1:
        AIplayerImg1 = warriorEnemyCharacter
        aiPlayer1Button.assignImage(AIplayerImg1)
        aiPlayer1Button.setCoords(690, 310)
    else:
        AIplayerImg1 = tankerEnemyCharacter
        aiPlayer1Button.assignImage(AIplayerImg1)
        aiPlayer1Button.setCoords(690, 310)

    if randoChara2 == 1:
        AIplayerImg2 = warriorEnemyCharacter
        aiPlayer2Button.assignImage(AIplayerImg2)
        aiPlayer2Button.setCoords(630, 360)
    else:
        AIplayerImg2 = tankerEnemyCharacter
        aiPlayer2Button.assignImage(AIplayerImg2)
        aiPlayer2Button.setCoords(630, 360)

    if randoChara3 == 1:
        AIplayerImg3 = warriorEnemyCharacter
        aiPlayer3Button.assignImage(AIplayerImg3)
        aiPlayer3Button.setCoords(690, 415)
    else:
        AIplayerImg3 = tankerEnemyCharacter
        aiPlayer3Button.assignImage(AIplayerImg3)
        aiPlayer3Button.setCoords(690, 415)

    #initialize AI player names
    #TODO: we need to make this as a global variable too for our game log
    aiPlayer1 = textFont.render('AI%d ' % (playerDigit1,), 1, (255, 255, 255))
    aiPlayer2 = textFont.render('AI%d ' % (playerDigit2,), 1, (255, 255, 255))
    aiPlayer3 = textFont.render('AI%d ' % (playerDigit3,), 1, (255, 255, 255))

    #draw button in screen
    aiPlayer1Button.drawButton(AIplayerImg1)
    aiPlayer2Button.drawButton(AIplayerImg2)
    aiPlayer3Button.drawButton(AIplayerImg3)

    screen.blit(aiPlayer1, [720, 300])
    screen.blit(aiPlayer2, [660, 350])
    screen.blit(aiPlayer3, [720, 400])

#https://stackoverflow.com/questions/419163/what-does-if-name-main-do/20158605#20158605
#only run the code if its an entry point

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
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    #initialize pygame mixer and bg song
    pygame.mixer.init()
    pygame.mixer.music.load("sound/bgmusic.ogg")
    clickSound = pygame.mixer.Sound("sound/clickSound.ogg")
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
    backgroundImage = pygame.image.load('images/bg.png')
    #Initialize warrior img
    warriorCharacter = pygame.image.load('images/warrior.png')
    #Initialize tanker img
    tankerCharacter = pygame.image.load('images/tanker.png')
    #Initialize warrior enemy img
    warriorEnemyCharacter = pygame.image.load('images/warriorEnemy.png')
    #Initialize tanker enemy img
    tankerEnemyCharacter = pygame.image.load('images/tankerEnemy.png')

    #Set character attributes
    player1HP = 100
    player2HP = 100
    player3HP = 100

    aiPlayer1HP = 100
    aiPlayer2HP = 100
    aiPlayer3HP = 100

    player1XP = 0
    player2XP = 0
    player3XP = 0

    aiPlayer1XP = 0
    aiPlayer2XP = 0
    aiPlayer3XP = 0

    player1Rank = 1
    player2Rank = 1
    player3Rank = 1

    aiPlayer1Rank = 1
    aiPlayer2Rank = 1
    aiPlayer3Rank = 1

    warriorATK = random.randint(5, 20)
    warriorDEF = random.randint(1, 10)

    tankerATK = random.randint(1, 10)
    tankerDEF = random.randint(5, 15)

    warriorATKAI = random.randint(5, 20)
    warriorDEFAI = random.randint(1, 10)

    tankerATKAI = random.randint(1, 10)
    tankerDEFAI = random.randint(5, 15)

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

    # Lets use .update instead of .flip to only update portions of the screen
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
                #should have a click sound. but its crashing, and idk how to upgrade it to python 3 > so shrug
                #clickSound.play()
                if warriorButton.pressed(mouse) == True:
                  choice = "Warrior"
                  warriorChoice += 1
                  warriorText = textFont.render('%d Warrior' % (warriorChoice,), 1, (255, 255, 255))
                if tankButton.pressed(mouse) == True:
                  choice = "Tank"
                  tankChoice += 1
                  tankerText = textFont.render('%d Tanker' % (tankChoice,), 1, (255, 255, 255))

    #lets draw a counter so that the user can see how many units that they chose
    screen.blit(warriorText, [280, 320])
    screen.blit(tankerText, [443, 320])

    #continue the process
    animateText("CLICK ANYWHERE TO CONTINUE...", textFont, screen, 270, 500, white)

    pygame.display.update()

    #ask for user input
    startScreen = False
    while startScreen == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                startScreen = True

    screen.blit(backgroundImage, [0,0])
    #check user choices, and draw characters based on conditions

    player1 = Button()
    player2 = Button()
    player3 = Button()

    playerImg1 = warriorCharacter
    playerImg2 = warriorCharacter
    playerImg3 = warriorCharacter

    if warriorChoice == 2 and tankChoice == 1:
        playerImg1 = warriorCharacter
        playerImg2 = tankerCharacter
        playerImg3 = warriorCharacter
        player1.assignImage(playerImg1)
        player1.setCoords(0, 310)
        player2.assignImage(playerImg2)
        player2.setCoords(60, 360)
        player3.assignImage(playerImg3)
        player3.setCoords(0, 415)
    elif warriorChoice == 1 and tankChoice == 2:
        playerImg1 = warriorCharacter
        playerImg2 = tankerCharacter
        playerImg3 = tankerCharacter
        player1.assignImage(playerImg1)
        player1.setCoords(0, 310)
        player2.assignImage(playerImg2)
        player2.setCoords(60, 360)
        player3.assignImage(playerImg3)
        player3.setCoords(0, 415)

    player1.drawButton(playerImg1)
    player2.drawButton(playerImg2)
    player3.drawButton(playerImg3)

    genAIPlayers()

    animateText("CLICK ON THE UNIT YOU WANT TO ATTACK WITH...", textFont, screen, 205, 100, white)

    firstPlayer = 0
    secondPlayer = 0
    thirdPlayer = 0
    while (firstPlayer or secondPlayer or thirdPlayer) < 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                #should have a click sound. but its crashing, and idk how to upgrade it to python 3 > so shrug
                #clickSound.play()
                if player1.pressed(mouse) == True:
                  firstPlayer += 1
                if player2.pressed(mouse) == True:
                  secondPlayer += 1
                if player3.pressed(mouse) == True:
                  thirdPlayer += 1

    unitText = textFont.render('You are attacking with: ', 1, (255, 255, 255))

    '''if firstPlayer == 1:
        unitText1 = pygame.Surface((unitText.get_width() + player1Name.get_width(), unitText.get_height()), pygame.SRCALPHA)
    elif secondPlayer == 1:
        unitText2 = pygame.Surface((unitText.get_width() + player2Name.get_width(), unitText.get_height()), pygame.SRCALPHA)
    elif thirdPlayer == 1:
        unitText3 = pygame.Surface((unitText.get_width() + player3Name.get_width(), unitText.get_height()), pygame.SRCALPHA)
    '''

    animateText("CLICK ANYWHERE TO CONTINUE...", textFont, screen, 270, 500, white)

    pygame.display.update()

    #ask for user input
    startScreenAgain = False
    while startScreenAgain == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                startScreenAgain = True

    screen.blit(backgroundImage, [0,0])

    #draw button in screen
    aiPlayer1Button.drawButton(AIplayerImg1)
    aiPlayer2Button.drawButton(AIplayerImg2)
    aiPlayer3Button.drawButton(AIplayerImg3)

    player1.drawButton(playerImg1)
    player2.drawButton(playerImg2)
    player3.drawButton(playerImg3)

    screen.blit(aiPlayer1, [720, 300])
    screen.blit(aiPlayer2, [660, 350])
    screen.blit(aiPlayer3, [720, 400])

    animateText("CLICK ON WHICH ENEMY YOU WANT TO STRIKE...", textFont, screen, 205, 100, white)

    firstAI = 0
    secondAI = 0
    thirdAI = 0
    while (firstAI or secondAI or thirdAI) < 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                #should have a click sound. but its crashing, and idk how to upgrade it to python 3 > so shrug
                #clickSound.play()
                if aiPlayer1Button.pressed(mouse) == True:
                  firstAI += 1
                if aiPlayer2Button.pressed(mouse) == True:
                  secondAI += 1
                if aiPlayer3Button.pressed(mouse) == True:
                  thirdAI += 1

    attackText = textFont.render('You are attacking: ', 1, (255, 255, 255))
    if firstAI == 1:
        attackText1 = pygame.Surface((attackText.get_width() + aiPlayer1.get_width(), attackText.get_height()), pygame.SRCALPHA)
    elif secondAI == 1:
        attackText2 = pygame.Surface((attackText.get_width() + aiPlayer2.get_width(), attackText.get_height()), pygame.SRCALPHA)
    elif thirdAI == 1:
        attackText3 = pygame.Surface((attackText.get_width() + aiPlayer3.get_width(), attackText.get_height()), pygame.SRCALPHA)

    animateText("CLICK ANYWHERE TO CONTINUE...", textFont, screen, 270, 500, white)

    pygame.display.update()

    #ask for user input
    startScreenAgain1 = False
    while startScreenAgain1 == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                startScreenAgain1 = True

    screen.blit(backgroundImage, [0,0])

    Damage = 0
    extraXP = 0.0
    if (firstPlayer == 1 and firstAI == 1) and (AIplayerImg1 == warriorEnemyCharacter):
    	Damage = warriorATK - warriorDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer1HP -= Damage
            player1XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player1XP = (player1XP * extraXP) + player1XP
    elif (firstPlayer == 1 and firstAI == 1) and (AIplayerImg1 == tankerEnemyCharacter):
    	Damage = warriorATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer1HP -= Damage
            player1XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player1XP = (player1XP * extraXP) + player1XP
    elif (firstPlayer == 1 and secondAI == 1) and (AIplayerImg2 == warriorEnemyCharacter):
    	Damage = warriorATK - warriorDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer2HP -= Damage
            player1XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player1XP = (player1XP * extraXP) + player1XP
    elif (firstPlayer == 1 and secondAI == 1) and (AIplayerImg2 == tankerEnemyCharacter):
    	Damage = warriorATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer2HP -= Damage
            player1XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player1XP = (player1XP * extraXP) + player1XP
    elif (firstPlayer == 1 and thirdAI == 1) and (AIplayerImg3 == warriorEnemyCharacter):
    	Damage = warriorATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer3HP -= Damage
            player1XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player1XP = (player1XP * extraXP) + player1XP
    elif (firstPlayer == 1 and thirdAI == 1) and (AIplayerImg3 == tankerEnemyCharacter):
    	Damage = warriorATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer3HP -= Damage
            player1XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player1XP = (player1XP * extraXP) + player1XP

    if (secondPlayer == 1 and firstAI == 1) and (AIplayerImg1 == warriorEnemyCharacter):
    	Damage = tankerATK - warriorDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer1HP -= Damage
            player2XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player2XP = (player2XP * extraXP) + player2XP
    elif (secondPlayer == 1 and firstAI == 1) and (AIplayerImg1 == tankerEnemyCharacter):
    	Damage = tankerATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer1HP -= Damage
            player2XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player2XP = (player2XP * extraXP) + player2XP
    elif (secondPlayer == 1 and secondAI == 1) and (AIplayerImg2 == warriorEnemyCharacter):
    	Damage = tankerATK - warriorDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer2HP -= Damage
            player2XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player2XP = (player2XP * extraXP) + player2XP
    elif (secondPlayer == 1 and secondAI == 1) and (AIplayerImg2 == tankerEnemyCharacter):
    	Damage = tankerATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer2HP -= Damage
            player2XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player2XP = (player2XP * extraXP) + player2XP
    elif (secondPlayer == 1 and thirdAI == 1) and (AIplayerImg3 == warriorEnemyCharacter):
    	Damage = tankerATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer3HP -= Damage
            player2XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player2XP = (player2XP * extraXP) + player2XP
    elif (secondPlayer == 1 and thirdAI == 1) and (AIplayerImg3 == tankerEnemyCharacter):
    	Damage = tankerATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer3HP -= Damage
            player2XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player2XP = (player2XP * extraXP) + player2XP

    if (thirdPlayer == 1 and firstAI == 1) and (AIplayerImg1 == warriorEnemyCharacter) and (playerImg3 == warriorCharacter):
    	Damage = warriorATK - warriorDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer1HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and firstAI == 1) and (AIplayerImg1 == tankerEnemyCharacter) and (playerImg3 == warriorCharacter):
    	Damage = warriorATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer1HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and firstAI == 1) and (AIplayerImg1 == warriorEnemyCharacter) and (playerImg3 == tankerCharacter):
    	Damage = tankerATK - warriorDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer1HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and firstAI == 1) and (AIplayerImg1 == tankerEnemyCharacter) and (playerImg3 == tankerCharacter):
    	Damage = tankerATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer1HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and secondAI == 1) and (AIplayerImg2 == warriorEnemyCharacter) and (playerImg3 == warriorCharacter):
    	Damage = warriorATK - warriorDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer2HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and secondAI == 1) and (AIplayerImg2 == tankerEnemyCharacter) and (playerImg3 == warriorCharacter):
    	Damage = warriorATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer2HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and secondAI == 1) and (AIplayerImg2 == warriorEnemyCharacter) and (playerImg3 == tankerCharacter):
    	Damage = tankerATK - warriorDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer2HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and secondAI == 1) and (AIplayerImg2 == tankerEnemyCharacter) and (playerImg3 == tankerCharacter):
    	Damage = tankerATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer2HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and thirdAI == 1) and (AIplayerImg3 == warriorEnemyCharacter) and (playerImg3 == warriorCharacter):
    	Damage = warriorATK - warriorDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer3HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and thirdAI == 1) and (AIplayerImg3 == tankerEnemyCharacter) and (playerImg3 == warriorCharacter):
    	Damage = warriorATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer3HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and thirdAI == 1) and (AIplayerImg3 == warriorEnemyCharacter) and (playerImg3 == tankerCharacter):
    	Damage = tankerATK - warriorDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer3HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP
    elif (thirdPlayer == 1 and thirdAI == 1) and (AIplayerImg3 == tankerEnemyCharacter) and (playerImg3 == tankerCharacter):
    	Damage = tankerATK - tankerDEFAI + random.randint(-5, 10)
        if(Damage > 0):
            aiPlayer3HP -= Damage
            player3XP += Damage
            if(Damage > 10):
                extraXP = 0.2
                player3XP = (player3XP * extraXP) + player3XP

    if (player1XP == 100):
        player1Rank += 1
        player1XP = 0
    elif (player2XP == 100):
        player2Rank += 1
        player2XP = 0
    elif (player3XP == 100):
        player3Rank += 1
        player3XP = 0
    '''
    Debugging purposes:
    
    print(firstPlayer)
    print(secondPlayer)
    print(thirdPlayer)
    print(firstAI)
    print(secondAI)
    print(thirdAI)
    print("AI Player1 HP: ",aiPlayer1HP)
    print("AI Player2 HP: ",aiPlayer2HP)
    print("AI Player3 HP: ",aiPlayer3HP)
    print (Damage)
    '''

    '''TODO:
    1. Prompt users to assign names for each unit they choose and store the names

    5. follow other instructions in the assignment guideline
    '''
