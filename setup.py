# Initialize libraries needed for the game.
import pygame, sys, time
from pygame.locals import *
from main import *
from character import *
import self
from random import randint
import copy
from datetime import datetime

# Initialize pygame and the pygame mixer and set screen size (width, height).
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((800, 650))

class Variables():
    # Declare variables in a class so that its easier to call and cleaner.
    FPS = 30
    fpsClock = pygame.time.Clock()
    validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
    shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
    font = pygame.font.Font('font/SHPinscher-Regular.otf', 90)
    fontText = pygame.font.Font("font/slkscr.ttf", 24)
    fontSub = pygame.font.Font("font/slkscr.ttf", 16)
    pygame.display.set_caption("RPG Game")
    bgImage = pygame.image.load('images/bg.png')
    icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(icon)
    warriorImg = pygame.image.load('images/warrior.png')
    tankerImg = pygame.image.load('images/tanker.png')
    warriorEnemyImg = pygame.image.load('images/warriorEnemy.png')
    tankerEnemyImg = pygame.image.load('images/tankerEnemy.png')
    skullImg = pygame.image.load('images/skull.png')
    tickImg = pygame.image.load('images/tick.png')
    bgImage2 = pygame.image.load('images/bg2.png')
    dateTimeObj = datetime.now()
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
    # Need to change from w to a after running w once.
    gameLog = open('gameLog.txt', 'w')

class Color():
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (192, 192, 192)
    darkGray = (64, 64, 64)
    red = (255, 0, 0)
    green = (127, 255, 0)


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
        self.font = pygame.font.Font("font/slkscr.ttf", 30)
        self.image = self.font.render('Input character name: ', False, Color.white)
        self.rect = self.image.get_rect()
        self.shifted = False

    # Create a function to add captial/non-capital texts
    def AddChar(self, char):
        if char in Variables.validChars and not self.shifted:
            self.text += char
        elif char in Variables.validChars and self.shifted:
            self.text += Variables.shiftChars[Variables.validChars.index(char)]
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
    pygame.mixer.music.load('Sound/backgroundmusic.ogg')
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

        tickButton = Button()
        tickButton.assignImage(Variables.tickImg)
        tickButton.setCoords(375, 510)

        warriorButton.drawButton(Variables.warriorImg)
        tankButton.drawButton(Variables.tankerEnemyImg)
        tickButton.drawButton(Variables.tickImg)

        Dialog('Give a name for each of your players!', 100, 100)
        Dialog('Choose   units to start your adventure!', 100, 150)

        confirmation = Variables.fontSub.render("After you\'re done, press enter and click on the tick", True, Color.white)
        confirmationNext = Variables.fontSub.render("Then choose your next character!", True, Color.white)

        screen.blit(confirmation, [160, 560])
        screen.blit(confirmationNext, [230, 580])

        screen.blit(textBox.image, textBox.rect)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
            elif e.type == pygame.KEYUP:
                if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    textBox.shifted = False
            elif e.type == pygame.KEYDOWN:
                textBox.AddChar(pygame.key.name(e.key))
                if e.key == pygame.K_SPACE:
                    textBox.text += " "
                    textBox.Update()
                elif e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    textBox.shifted = True
                elif e.key == pygame.K_BACKSPACE:
                    textBox.text = textBox.text[:-1]
                    textBox.Update()
                elif e.key == pygame.K_RETURN:
                    if len(textBox.text) > 0:
                        name.append(textBox.text)
                        textBox.text = ""
                        textBox.Update()
            if e.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if tickButton.pressed(mouse):
                    running = False

def genAIPlayers(copyTeam):
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

    return aiTeam

def drawAIPlayers(button0, button1, button2, job0, job1, job2, hp0, hp1, hp2):

    if hp0 > 0:
        if job0 == "Warrior":
            button0.assignImage(Variables.warriorEnemyImg)
            button0.setCoords(690, 270)
            button0.drawButton(Variables.warriorEnemyImg)
        else:
            button0.assignImage(Variables.tankerEnemyImg)
            button0.setCoords(690, 270)
            button0.drawButton(Variables.tankerEnemyImg)
    else:
        button0.setCoords(0,0)
        screen.blit(Variables.skullImg, [690, 270])

    if hp1 > 0:
        if job1 == "Warrior":
            button1.assignImage(Variables.warriorEnemyImg)
            button1.setCoords(570, 350)
            button1.drawButton(Variables.warriorEnemyImg)
        else:
            button1.assignImage(Variables.tankerEnemyImg)
            button1.setCoords(570, 350)
            button1.drawButton(Variables.tankerEnemyImg)
    else:
        button1.setCoords(0, 0)
        screen.blit(Variables.skullImg, [570, 350])

    if hp2 > 0:
        if job2 == "Warrior":
            button2.assignImage(Variables.warriorEnemyImg)
            button2.setCoords(690, 420)
            button2.drawButton(Variables.warriorEnemyImg)
        else:
            button2.assignImage(Variables.tankerEnemyImg)
            button2.setCoords(690, 420)
            button2.drawButton(Variables.tankerEnemyImg)
    else:
        button2.setCoords(0, 0)
        screen.blit(Variables.skullImg, [690, 420])

def drawPlayers(button0, button1, button2, job0, job1, job2, hp0, hp1, hp2):
    if hp0 > 0:
        if job0 == "Warrior":
            button0.assignImage(Variables.warriorImg)
            button0.setCoords(0, 270)
            button0.drawButton(Variables.warriorImg)
        else:
            button0.assignImage(Variables.tankerImg)
            button0.setCoords(0, 270)
            button0.drawButton(Variables.tankerImg)
    else:
        button0.setCoords(0, 0)
        screen.blit(Variables.skullImg, [0, 270])

    if hp1 > 0:
        if job1 == "Warrior":
            button1.assignImage(Variables.warriorImg)
            button1.setCoords(120, 350)
            button1.drawButton(Variables.warriorImg)
        else:
            button1.assignImage(Variables.tankerImg)
            button1.setCoords(120, 350)
            button1.drawButton(Variables.tankerImg)
    else:
        button1.setCoords(0, 0)
        screen.blit(Variables.skullImg, [120, 350])

    if hp2 > 0:
        if job2 == "Warrior":
            button2.assignImage(Variables.warriorImg)
            button2.setCoords(0, 420)
            button2.drawButton(Variables.warriorImg)
        else:
            button2.assignImage(Variables.tankerImg)
            button2.setCoords(0, 420)
            button2.drawButton(Variables.tankerImg)
    else:
        button2.setCoords(0, 0)
        screen.blit(Variables.skullImg, [0, 420])

def attackFunc(turnAttacker, turnDefender):
    ranNum = randint(5, 10)
    dmg = int(turnAttacker.attack + ranNum - turnDefender.defend)
    if dmg > 0:
        turnDefender.health -= dmg
        turnAttacker.experience += dmg
        turnDefender.experience += turnDefender.defend
        Tanker.check_level_up(turnAttacker)
        Tanker.check_level_up(turnDefender)
        Tanker.check_die(turnAttacker)
        Tanker.check_die(turnDefender)
        return dmg
    elif dmg < 0:
        turnAttacker.experience += int(turnAttacker.attack + ranNum)
        turnDefender.experience += int(turnAttacker.attack + ranNum)
        Tanker.check_level_up(turnAttacker)
        Tanker.check_level_up(turnDefender)
        Tanker.check_die(turnAttacker)
        Tanker.check_die(turnDefender)
        return dmg
    else:
        return dmg

def aiAttack(aiTeam, targetTeam):
    ai_team_attack = [aiTeam[0].attack, aiTeam[1].attack, aiTeam[2].attack]
    ai_attacker = aiTeam[ai_team_attack.index(max(ai_team_attack))]
    user_team_defend = [targetTeam[0].defend, targetTeam[1].defend, targetTeam[2].defend]
    user_defender = targetTeam[user_team_defend.index(min(user_team_defend))]
    return ai_attacker, user_defender

def showPlayersAttribute(player0, player1, player2, x0, y0, x1, y1, y2):
    playerText1 = Variables.fontSub.render(str(player0), True, Color.white)
    playerText2 = Variables.fontSub.render(str(player1), True, Color.white)
    playerText3 = Variables.fontSub.render(str(player2), True, Color.white)

    screen.blit(playerText1, [x0, y0])
    screen.blit(playerText2, [x1, y1])
    screen.blit(playerText3, [x0, y2])

def showGameLog(attacker, dmg, defender, xp, x, y):
    logText = Variables.fontSub.render( "[Game Message] " + str(attacker) + " dealt " + str(dmg) + " dmg to " + str(defender) + " and gained "
    + str(xp) + " exp.", True, Color.black)

    screen.blit(logText, [x, y])

def saveGameLog(rank, attacker, dmg, defender, xp):
    Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Level {} ".format(rank) + "Unit 1: " + str(attacker) + " dealt " + str(dmg) + " dmg to " + str(defender) + " and gained "
    + str(xp) + " exp." "\n \n")

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
    while (warriorChoice + tankChoice) < 3:
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
                if warriorButton.pressed(mouse):
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
                if tankButton.pressed(mouse):
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
    Variables.gameLog.write("========================== PSB BATTLE GAME ==========================\n")
    # now lets actually render the text from the while loop before
    if warriorChoice > 0:
        # the if statement is needed because if the player chooses 3 tankers,
        # that means the warriortext will be null, which will result in a crash
        screen.blit(warriorText, [260, 320])
        screen.blit(Variables.warriorImg, [280, 350])
        Variables.gameLog.write("[" + str(Variables.dateTimeObj)+ "] " + str(warriorChoice) +  " Warriors Chosen \n")
    if tankChoice > 0:
        # the if statement is needed because if the player chooses 3 tankers,
        # that means the tankertext will be null, which will result in a crash
        screen.blit(tankerText, [433, 320])
        screen.blit(Variables.tankerEnemyImg, [443, 350])
        Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + str(tankChoice) + " Tankers Chosen \n")

    Variables.gameLog.write("\n========================== INITIALIZATION OF UNITS==========================\n")
    Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Name of unit 1: " + team[0].name + " ATK Value: " + str(team[0].attack) + " DEF Value: " + str(team[0].defend) +" Class: " + team[0].job + "\n")
    Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Name of unit 2: " + team[1].name + " ATK Value: " + str(team[1].attack) + " DEF Value: " + str(team[1].defend) + " Class: " + team[1].job + "\n")
    Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Name of unit 3: " + team[2].name + " ATK Value: " + str(team[2].attack) + " DEF Value: " + str(team[2].defend) + " Class: " + team[2].job + "\n \n")
    # Update the display again so
    # we can continue and remove the
    # elements before (not directly, we're just removing the rendered things)

    Dialog("CLICK ANYWHERE TO CONTINUE...", 100, 100)
    pygame.display.update()

    startScreen()

    # Create new frame to show player characters.
    screen.blit(Variables.bgImage, [0, 0])

    playerATKButton = [Button(), Button(), Button()]
    aiPlayerButtons = [Button(), Button(), Button()]

    user_team_hp = team[0].health + team[1].health + team[2].health
    ai_team_hp = ai[0].health + ai[1].health + ai[2].health

    Variables.gameLog.write("========================== BATTLE SEQUENCE ==========================\n")

    while user_team_hp > 0 and ai_team_hp > 0:

        firstPlayer = 0
        secondPlayer = 0
        thirdPlayer = 0
        firstAI = 0
        secondAI = 0
        thirdAI = 0

        drawPlayers(playerATKButton[0], playerATKButton[1], playerATKButton[2], team[0].job, team[1].job, team[2].job, team[0].health, team[1].health, team[2].health)

        Dialog("CLICK ON WHICH UNIT YOU WANT TO ATTACK WITH...", 80, 100)

        showPlayersAttribute(team[0].name, team[1].name, team[2].name, 20, 235, 140, 315, 390)
        showPlayersAttribute("HP: " + str(team[0].health), "HP: " + str(team[1].health), "HP: " + str(team[2].health), 20, 250, 140, 335, 405)
        showPlayersAttribute("ATK: " + str(int(team[0].attack)), "ATK: " + str(int(team[1].attack)), "ATK: " + str(int(team[2].attack)), 20, 360, 140,
                             445, 505)

        pygame.display.update()

        while (firstPlayer or secondPlayer or thirdPlayer) < 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if playerATKButton[0].pressed(mouse):
                        clickSound()
                        firstPlayer += 1
                    if playerATKButton[1].pressed(mouse):
                        clickSound()
                        secondPlayer += 1
                    if playerATKButton[2].pressed(mouse):
                        clickSound()
                        thirdPlayer += 1

        # Create new frame
        screen.blit(Variables.bgImage2, [0, 0])

        aiDefend1 = ai[0].defend
        if ai[0].health <= 0:
            aiDefend1 = 0

        aiDefend2 = ai[1].defend
        if ai[1].health <= 0:
            aiDefend2 = 0

        aiDefend3 = ai[2].defend
        if ai[2].health <= 0:
            aiDefend3 = 0

        drawAIPlayers(aiPlayerButtons[0], aiPlayerButtons[1], aiPlayerButtons[2], ai[0].job, ai[1].job, ai[2].job, ai[0].health, ai[1].health, ai[2].health)

        showPlayersAttribute(ai[0].name, ai[1].name, ai[2].name, 710, 230, 590, 315, 390)
        showPlayersAttribute("HP: " + str(ai[0].health), "HP: " + str(ai[1].health), "HP: " + str(ai[2].health),
                             710, 250, 590, 335, 405)

        showPlayersAttribute("DEF: " + str(int(aiDefend1)), "DEF: " + str(int(aiDefend2)),
                             "DEF: " + str(int(aiDefend3)), 710, 365, 590,
                             445, 510)

        Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Unit 1: " + ai[0].name + " ATK Value: " + str(
            ai[0].attack) + " HP Value: " + str(ai[0].health) + "\n")
        Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Unit 2: " + ai[1].name + " ATK Value: " + str(
            ai[1].attack) + " HP Value: " + str(ai[1].health) + "\n")
        Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Unit 3: " + ai[2].name + " ATK Value: " + str(
            ai[2].attack) + " HP Value: " + str(ai[2].health) + "\n \n")

        Dialog("CLICK ON WHICH ENEMY YOU WANT TO ATTACK...", 100, 100)

        pygame.display.update()

        while (firstAI or secondAI or thirdAI) < 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if aiPlayerButtons[0].pressed(mouse):
                        clickSound()
                        firstAI += 1
                    if aiPlayerButtons[1].pressed(mouse):
                        clickSound()
                        secondAI += 1
                    if aiPlayerButtons[2].pressed(mouse):
                        clickSound()
                        thirdAI += 1

        # Create new frame
        screen.blit(Variables.bgImage2, [0, 0])

        pygame.display.update()

        num_attacker = 0
        num_enemy = 0
        defender = 0
        attacker = 0

        while num_attacker < 1:
            if firstPlayer == 1:
                if team[0].health > 0:
                    attacker = team[0]
                    num_attacker += 1
                    firstPlayer = 0
                else:
                    break

            if secondPlayer == 1:
                if team[1].health > 0:
                    attacker = team[1]
                    num_attacker += 1
                    secondPlayer = 0
                else:
                    break

            if thirdPlayer == 1:
                if team[2].health > 0:
                    attacker = team[2]
                    num_attacker += 1
                    thirdPlayer = 0
                else:
                    break

        while num_enemy < 1:
            if firstAI == 1:
                if ai[0].health > 0:
                    defender = ai[0]
                    num_enemy += 1
                    firstAI = 0
                else:
                    break

            if secondAI == 1:
                if ai[1].health > 0:
                    defender = ai[1]
                    num_enemy += 1
                    secondAI = 0
                else:
                    break

            if thirdAI == 1:
                if ai[2].health > 0:
                    defender = ai[2]
                    num_enemy += 1
                    thirdAI = 0
                else:
                    break

        user_turn = attackFunc(attacker, defender)

        showGameLog(attacker.name, user_turn, defender.name, int(attacker.experience), 30, 570)

        saveGameLog(attacker.rank, attacker.name, user_turn, defender.name, int(attacker.experience))

        attacker, defender = aiAttack(ai, team)
        ai_turn = attackFunc(attacker, defender)

        showGameLog(attacker.name, ai_turn, defender.name, int(attacker.experience), 30, 590)

        saveGameLog(attacker.rank, attacker.name, user_turn, defender.name, int(attacker.experience))

        user_team_hp = team[0].health + team[1].health + team[2].health
        ai_team_hp = ai[0].health + ai[1].health + ai[2].health

    Variables.gameLog.write("\n========================== GAME FINISH ==========================\n")

    text = Variables.font.render("You lost. Game over.", True, Color.white)

    if user_team_hp == 0:
        text = Variables.font.render("You lost. Game over.", True, Color.white)
        Variables.gameLog.write("Game status: You lost. Game over.")
    if ai_team_hp == 0:
        text = Variables.font.render("You won. Congrats!!!", True, Color.white)
        Variables.gameLog.write("Game status: You won. Congrats!!!")

    screen.blit(Variables.bgImage, [0,0])

    Dialog("CLICK ANYWHERE TO CONTINUE...", 100, 100)

    screen.blit(text, [100, 120])

    pygame.display.update()

    startScreen()

    Variables.gameLog.close()


