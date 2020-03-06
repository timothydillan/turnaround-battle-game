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
    gameLog = open('gameLog.txt', 'w')

class Color():
    # Declare colors in a class so that we dont have to put in three numbers everytime.
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
    # character choosing.
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # Get mouse position
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        # Change button color when hovering
        pygame.draw.rect(screen, ic, (x, y, w, h))
        # Check if a button is clicked and if there is no action running
        if click[0] == 1 and action != None:
            if action == "play":
                # If the new game button is clicked, run game loop
                clickSound()
                gameLoop()
            elif action == 'load':
                # If the load game button is clicked, load text file from saved game and continue game
                clickSound()
            elif action == "quit":
                # If the quit game button is clicked, quit the game.
                clickSound()
                pygame.quit()
                sys.exit()
    else:
        # Change button color when mouse not hovering
        pygame.draw.rect(screen, ac, (x, y, w, h))
    textSurf, textRect = textObject(msg, Variables.fontText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    #Display text unto button
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
    #Render the text that we're going to use later in a darkgray color
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
    # This boolean is needed to declare a pre-condition statement that will
    # Make the while loop run.
    running = True
    # This boolean is needed to draw the tick button after
    # the user clicks enter
    returned = False
    while running:
        #Create a new frame
        screen.blit(Variables.bgImage, [0, 0])
        #Declare buttons
        # It's same as the one below, but we need this to be here so that when we update the display
        # It doesn't remove the button
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

        # Only draw the tick button when user clicks on enter
        if returned:
            tickButton.drawButton(Variables.tickImg)

        Dialog('Give a name for each of your players!', 100, 100)
        Dialog('Choose   units to start your adventure!', 100, 150)

        # Tell the user what to do so that it won't be confusing for them to input names.
        confirmation = Variables.fontSub.render("After you\'re done, press enter and click on the tick", True, Color.white)
        confirmationNext = Variables.fontSub.render("Then choose your next character!", True, Color.white)

        # Display the instructions
        screen.blit(confirmation, [160, 560])
        screen.blit(confirmationNext, [230, 580])

        # Display the text that the user is going to input
        screen.blit(textBox.image, textBox.rect)

        # Update the display so that it actually shows all the things we rendered before.
        pygame.display.update()

        # Loop through the all the possible pygame events
        for e in pygame.event.get():
            # If the user quits, quit the game.
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            # If the shift key is released, do not set shifted as true.
            elif e.type == KEYUP:
                if e.key in [K_RSHIFT, K_LSHIFT]:
                    textBox.shifted = False
            # If a key is pressed
            elif e.type == KEYDOWN:
                # Add a character
                textBox.AddChar(pygame.key.name(e.key))
                # If the user press space, add a empty text and update the textbox.
                if e.key == K_SPACE:
                    textBox.text += " "
                    textBox.Update()
                # If the user holds shift, set shifted as true and set capitalize keys
                elif e.key in [K_RSHIFT, K_LSHIFT]:
                    textBox.shifted = True
                # If the user presses backspace, delete a character
                elif e.key == K_BACKSPACE:
                    textBox.text = textBox.text[:-1]
                    textBox.Update()
                # If the user presses return,
                elif e.key == K_RETURN:
                    # And if the text size was more than 0
                    if len(textBox.text) > 0:
                        # Append the current text
                        name.append(textBox.text)
                        # Set returned to true (for the tick button)
                        returned = True
                        # Then reset the text
                        textBox.text = ""
                        # Then update the textbox
                        textBox.Update()
            # If the user clicks
            elif e.type == MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse = pygame.mouse.get_pos()
                # And if the mouse pressed the tickButton
                if tickButton.pressed(mouse):
                    # Set running to false.
                    running = False

def genAIPlayers(copyTeam):
    aiTeam = copy.deepcopy(copyTeam)

    for aiPlayer in aiTeam:
        aiPlayer.name = 'AI' + str(randint(00, 100))
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
    # A function to draw the AI enemies.
    if hp0 > 0:
        # Check if the first AI player has a hp more than 0.
        # If its true, assign the buttons an image based on their jobs/class.
        if job0 == "Warrior":
            button0.assignImage(Variables.warriorEnemyImg)
            button0.setCoords(690, 270)
            button0.drawButton(Variables.warriorEnemyImg)
        else:
            button0.assignImage(Variables.tankerEnemyImg)
            button0.setCoords(690, 270)
            button0.drawButton(Variables.tankerEnemyImg)
    else:
        # If the hp is less than or is zero
        # Place the button in a place that the user cant click on (because there is no way to remove the button)
        button0.setCoords(-100,-100)
        # And add a skull image instead to show that the player is dead.
        screen.blit(Variables.skullImg, [690, 270])

    if hp1 > 0:
        # Check if the second AI player has a hp more than 0.
        if job1 == "Warrior":
            button1.assignImage(Variables.warriorEnemyImg)
            button1.setCoords(570, 350)
            button1.drawButton(Variables.warriorEnemyImg)
        else:
            button1.assignImage(Variables.tankerEnemyImg)
            button1.setCoords(570, 350)
            button1.drawButton(Variables.tankerEnemyImg)
    else:
        button1.setCoords(-100, -100)
        screen.blit(Variables.skullImg, [570, 350])

    if hp2 > 0:
        # Check if the third AI player has a hp more than 0.
        if job2 == "Warrior":
            button2.assignImage(Variables.warriorEnemyImg)
            button2.setCoords(690, 420)
            button2.drawButton(Variables.warriorEnemyImg)
        else:
            button2.assignImage(Variables.tankerEnemyImg)
            button2.setCoords(690, 420)
            button2.drawButton(Variables.tankerEnemyImg)
    else:
        button2.setCoords(-100, -100)
        screen.blit(Variables.skullImg, [690, 420])

def drawPlayers(button0, button1, button2, job0, job1, job2, hp0, hp1, hp2):
    # A function to draw players.
    if hp0 > 0:
        # Check if the first player has a hp more than 0.
        # If its true, assign the buttons an image based on their jobs/class.
        if job0 == "Warrior":
            button0.assignImage(Variables.warriorImg)
            button0.setCoords(0, 270)
            button0.drawButton(Variables.warriorImg)
        else:
            button0.assignImage(Variables.tankerImg)
            button0.setCoords(0, 270)
            button0.drawButton(Variables.tankerImg)
    else:
        # If the hp is less than or is zero
        # Place the button in a place that the user cant click on (because there is no way to remove the button)
        button0.setCoords(-100, -100)
        # And add a skull image instead to show that the player is dead.
        screen.blit(Variables.skullImg, [0, 270])

    if hp1 > 0:
        # Check if the second player has a hp more than 0.
        # If its true, assign the buttons an image based on their jobs/class.
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
        # Check if the third player has a hp more than 0.
        # If its true, assign the buttons an image based on their jobs/class.
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
        turnAttacker.health -= int(dmg * 0.2)
        turnDefender.health -= dmg
        turnAttacker.experience += dmg
        turnDefender.experience += turnDefender.defend
        Tanker.check_level_up(turnAttacker)
        Tanker.check_level_up(turnDefender)
        Tanker.check_die(turnAttacker)
        Tanker.check_die(turnDefender)
        return dmg
    elif dmg < 0:
        turnAttacker.health -= int(abs(dmg * 0.5))
        turnAttacker.experience += int(abs(turnAttacker.attack + ranNum))
        turnDefender.experience += int(abs(turnAttacker.attack + ranNum))
        Tanker.check_level_up(turnAttacker)
        Tanker.check_level_up(turnDefender)
        Tanker.check_die(turnAttacker)
        Tanker.check_die(turnDefender)
        return dmg
    else:
        return dmg

def aiAttack(aiTeam, targetTeam):
    # A function to create the AI Logic.
    # Retrieve all the atk value of the units in the AI team and put them into a list
    aiTeamAttack = [aiTeam[0].attack, aiTeam[1].attack, aiTeam[2].attack]
    # Then, based on the list before, get the index of the AI with the highest attack value.
    aiAttacker = aiTeam[aiTeamAttack.index(max(aiTeamAttack))]
    # Then, retrieve all the def value of the units in the player team and put them into a list
    userTeamDefend = [targetTeam[0].defend, targetTeam[1].defend, targetTeam[2].defend]
    # and, based on the defend list before, get the index of the player with the lowest defend value.
    userDefender = targetTeam[userTeamDefend.index(min(userTeamDefend))]
    # then return the index number.
    return aiAttacker, userDefender


def showPlayersAttribute(player0, player1, player2, x0, y0, x1, y1, y2):
    # A function to show attributes of a unit.
    # Only has 3 texts to be rendered since there are only three units.
    playerText1 = Variables.fontSub.render(str(player0), True, Color.white)
    playerText2 = Variables.fontSub.render(str(player1), True, Color.white)
    playerText3 = Variables.fontSub.render(str(player2), True, Color.white)
    # Then display the texts based on the argument coordinates.
    screen.blit(playerText1, [x0, y0])
    screen.blit(playerText2, [x1, y1])
    screen.blit(playerText3, [x0, y2])

def showGameLog(attacker, dmg, defender, xp, x, y):
    # A function to render the game log inside the gamelog box.
    logText = Variables.fontSub.render( "[Game Message] " + str(attacker) + " dealt " + str(dmg) + " dmg to " + str(defender) + " and now has a total of "
    + str(xp) + " exp.", True, Color.black)
    # Then display the texts based on the argument coordinates.
    screen.blit(logText, [x, y])

def saveGameLog(rank, attacker, dmg, defender, xp):
    #A function to write the game log events to the file.
    Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Level {} ".format(rank) + "Unit 1: " + str(attacker) + " dealt " + str(dmg) + " dmg to " + str(defender) + " and now has a total of "
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

    # Show a welcoming Text
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
        # a for loop that loops through all the possible pygame event
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
                    # show num of warriors player has in team
                    warriorText = Variables.fontText.render('%d Warrior' % (warriorChoice,), 1, (255, 255, 255))
                    team.append(Warrior.create(self))
                    # make a click sound so the user knows that they've clicked on the button
                    clickSound()
                    # ask user to input name
                    TextBox()
                # now check if the tankbutton is pressed by the mouse
                elif tankButton.pressed(mouse):
                    # add tankChoice by 1 to make sure that the loop stops if the units reaches 3.
                    tankChoice += 1
                    # show num of tanker player has in team
                    tankerText = Variables.fontText.render('%d Tanker' % (tankChoice,), 1, (255, 255, 255))
                    # create tanker instance, add in to player team
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

    # Header of the text file gamelog.
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

    # Write what units the players chosen into the text file.
    Variables.gameLog.write("\n========================== INITIALIZATION OF UNITS==========================\n")
    Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Name of unit 1: " + team[0].name + " ATK Value: " + str(team[0].attack) + " DEF Value: " + str(team[0].defend) +" Class: " + team[0].job + "\n")
    Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Name of unit 2: " + team[1].name + " ATK Value: " + str(team[1].attack) + " DEF Value: " + str(team[1].defend) + " Class: " + team[1].job + "\n")
    Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "Name of unit 3: " + team[2].name + " ATK Value: " + str(team[2].attack) + " DEF Value: " + str(team[2].defend) + " Class: " + team[2].job + "\n \n")

    Dialog("CLICK ANYWHERE TO CONTINUE...", 100, 100)

    # Update the display again so
    # we can continue and remove the
    # elements before (not directly, we're just removing the rendered things)
    pygame.display.update()

    startScreen()

    # Create new frame to show player characters.
    screen.blit(Variables.bgImage, [0, 0])
    # Declare Player Buttons and AI buttons (for the Battle)
    playerATKButton = [Button(), Button(), Button()]
    aiPlayerButtons = [Button(), Button(), Button()]

    # These two variables is needed for the while loop.
    userTeamHP = team[0].health + team[1].health + team[2].health
    aiTeamHP = ai[0].health + ai[1].health + ai[2].health

    # Write a battle sequence header to the gamelog to indicate that the battle is starting.
    Variables.gameLog.write("========================== BATTLE SEQUENCE ==========================\n")

    # Check if all the players and all the AI has more than 0 hp.
    while userTeamHP > 0 and aiTeamHP > 0:
        # Declare an initial value of 0 for attacker and defender
        # since we dont have an attacker or a defender yet.
        attacker = 0
        defender = 0

        # Render the players that the user has chosen
        drawPlayers(playerATKButton[0], playerATKButton[1], playerATKButton[2], team[0].job, team[1].job, team[2].job, team[0].health, team[1].health, team[2].health)

        Dialog("CLICK ON WHICH UNIT YOU WANT TO ATTACK WITH...", 80, 100)

        # Show all the players unit and their attributes.
        showPlayersAttribute(team[0].name, team[1].name, team[2].name, 20, 235, 140, 315, 390)
        showPlayersAttribute("HP: " + str(int(team[0].health)), "HP: " + str(int(team[1].health)), "HP: " + str(int(team[2].health)), 20, 250, 140, 335, 405)
        showPlayersAttribute("ATK: " + str(int(team[0].attack)), "ATK: " + str(int(team[1].attack)), "ATK: " + str(int(team[2].attack)), 20, 360, 140,
                             445, 505)

        # Always update the attributes to the file every time the loop iterates.
        Variables.gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "Player 1: " + team[0].name + " ATK Value: " + str(
                team[0].attack) + " HP Value: " + str(int(team[0].health)) + "\n")
        Variables.gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "Player 2: " + team[1].name + " ATK Value: " + str(
                team[1].attack) + " HP Value: " + str(int(team[1].health)) + "\n")
        Variables.gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "Player 3: " + team[2].name + " ATK Value: " + str(
                team[2].attack) + " HP Value: " + str(int(team[2].health)) + "\n \n")

        # Update the display so that the things we rendered actually renders to the screen.
        pygame.display.update()

        # While the attacker is still empty
        while attacker == 0:
            # loop through all the possible pygame events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # If there is a mouse click
                elif event.type == MOUSEBUTTONDOWN:
                    # Then get the mouse position.
                    mouse = pygame.mouse.get_pos()
                    if playerATKButton[0].pressed(mouse):
                        # If the first player is chosen and the mouse pos is in the
                        # first player button, then make a clickSound
                        clickSound()
                        # we check if the first player is not dead
                        if team[0].health > 0:
                            # If true, then the attacker will be the first player
                            attacker = team[0]
                        else:
                            # If false, break the loop and continue to the next statement
                            break
                    elif playerATKButton[1].pressed(mouse):
                        # If the second player is chosen and the mouse pos is in the
                        # second player button, then make a clickSound
                        clickSound()
                        # we check if the second player is not dead
                        if team[1].health > 0:
                            # If true, then the attacker will be the second player
                            attacker = team[1]
                        else:
                            # If false, break the loop and continue to the next statement
                            break
                    elif playerATKButton[2].pressed(mouse):
                        # If the second player is chosen and the mouse pos is in the
                        # second player button, then make a clickSound
                        clickSound()
                        if team[2].health > 0:
                            # If true, then the attacker will be the third player
                            attacker = team[2]
                        else:
                            # If false, break the loop and continue to the next statement
                            break

        # Create new frame
        screen.blit(Variables.bgImage2, [0, 0])

        # This is needed for GUI purposes
        # If we dont use this, then the defend value will show 100000 instead.
        # Read more on character.py
        aiDefend1 = ai[0].defend
        if ai[0].health <= 0:
            aiDefend1 = 0

        aiDefend2 = ai[1].defend
        if ai[1].health <= 0:
            aiDefend2 = 0

        aiDefend3 = ai[2].defend
        if ai[2].health <= 0:
            aiDefend3 = 0

        # Draw the AI players so that the user can choose which AI does the user wants to attack
        drawAIPlayers(aiPlayerButtons[0], aiPlayerButtons[1], aiPlayerButtons[2], ai[0].job, ai[1].job, ai[2].job, ai[0].health, ai[1].health, ai[2].health)

        # Show the AI attributes
        showPlayersAttribute(ai[0].name, ai[1].name, ai[2].name, 710, 230, 590, 315, 390)
        showPlayersAttribute("HP: " + str(int(ai[0].health)), "HP: " + str(int(ai[1].health)), "HP: " + str(int(ai[2].health)),
                             710, 250, 590, 335, 405)

        showPlayersAttribute("DEF: " + str(int(aiDefend1)), "DEF: " + str(int(aiDefend2)),
                             "DEF: " + str(int(aiDefend3)), 710, 365, 590,
                             445, 510)

        # Always update the attributes to the file everytime the loop iterates.
        Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "AI Unit 1: " + ai[0].name + " DEF Value: " + str(
            ai[0].defend) + " HP Value: " + str(int(ai[0].health)) + "\n")
        Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "AI Unit 2: " + ai[1].name + " DEF Value: " + str(
            ai[1].defend) + " HP Value: " + str(int(ai[1].health)) + "\n")
        Variables.gameLog.write("[" + str(Variables.dateTimeObj) + "] " + "AI Unit 3: " + ai[2].name + " DEF Value: " + str(
            ai[2].defend) + " HP Value: " + str(int(ai[2].health)) + "\n \n")

        # Show a loading text so that the user doesn't think that the game is broken/froze
        loadingText = Variables.fontSub.render("Waiting for a move.......", True, Color.black)
        # Display the loading text
        screen.blit(loadingText, [30, 570])

        Dialog("CLICK ON WHICH ENEMY YOU WANT TO ATTACK...", 100, 100)

        # Update the display
        pygame.display.update()
        # While the defender/enemy is empty
        while defender == 0:
            # Loop through all the possible pygame events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # If the user clicks on the screen
                elif event.type == MOUSEBUTTONDOWN:
                    # Then get the mouse position
                    mouse = pygame.mouse.get_pos()
                    # and check if the user clicks on the first ai
                    if aiPlayerButtons[0].pressed(mouse):
                        # make a click sound if true
                        clickSound()
                        # and check if the first AI's health is more than 0
                        if ai[0].health > 0:
                            # If true, then the defender/enemy will be the first ai
                            defender = ai[0]
                        else:
                            # If false, break the loop and continue to the next statement
                            break
                    # check if the user clicks on the second ai
                    elif aiPlayerButtons[1].pressed(mouse):
                        # make a click sound if true
                        clickSound()
                        # check if the second AI's health is more than 0
                        if ai[1].health > 0:
                            # If true, then the defender/enemy will be the second ai
                            defender = ai[1]
                        else:
                            # If false, break the loop and continue to the next statement
                            break
                    # check if the user clicks on the third ai
                    elif aiPlayerButtons[2].pressed(mouse):
                        # make a click sound if true
                        clickSound()
                        # check if the third AI's health is more than 0
                        if ai[2].health > 0:
                            # If true, then the defender/enemy will be the third ai
                            defender = ai[2]
                        else:
                            # If false, break the loop and continue to the next statement
                            break

        # Create new frame
        screen.blit(Variables.bgImage2, [0, 0])
        # Update the display
        pygame.display.update()

        #Declare a user turn, in which the player will attack the AI
        userTurn = attackFunc(attacker, defender)

        # Show and save the game log when the user attacks.
        showGameLog(attacker.name, userTurn, defender.name, int(attacker.experience), 30, 570)

        saveGameLog(attacker.rank, attacker.name, userTurn, defender.name, int(attacker.experience))

        # After the user attacks, change the attacker to AIs and defender to Players.
        attacker, defender = aiAttack(ai, team)
        # Then the AI will attack here.
        aiTurn = attackFunc(attacker, defender)

        # Show and save the game log when the AI attacks.
        showGameLog(attacker.name, aiTurn, defender.name, int(attacker.experience), 30, 590)

        saveGameLog(attacker.rank, attacker.name, aiTurn, defender.name, int(attacker.experience))

        # Always get the latest Team hps.
        userTeamHP = team[0].health + team[1].health + team[2].health
        aiTeamHP = ai[0].health + ai[1].health + ai[2].health

    # If one of the team loses, write to the file that the game has finished.
    Variables.gameLog.write("\n========================== GAME FINISH ==========================\n")

    if userTeamHP == 0:
        # If the player team loses all their health, write, you lost.
        text = Variables.font.render("You lost. Game over.", True, Color.white)
        Variables.gameLog.write("Game status: You lost. Game over.")
    else:
        # If not, then say, you won!
        text = Variables.font.render("You won. Congrats!!!", True, Color.white)
        Variables.gameLog.write("Game status: You won. Congrats!!!")

    # Create a new frame
    screen.blit(Variables.bgImage, [0,0])

    Dialog("CLICK ANYWHERE TO CONTINUE...", 100, 100)

    # Display the winning/losing text
    screen.blit(text, [100, 120])

    # Update the display
    pygame.display.update()

    startScreen()
    
    Variables.gameLog.close()