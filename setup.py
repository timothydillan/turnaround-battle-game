# Initialize libraries needed for the game.
# All things taken from the internet are put in referenceList.txt

import pygame, sys
from pygame.locals import *
import shelve
import self
from main import *
from character import *
from datetime import datetime
from variables import Variables, Color
from gui import Button, TextBox, Title, Dialog, drawPlayers, drawAIPlayers, showGameLog, saveGameLog, showPlayersAttribute
from sounds import clickSound, saveSound
from logic import genAIPlayers, attackFunc, aiAttack

# Initialize screen and screen size (width, height).
screen = pygame.display.set_mode((800, 650))


def startScreen():
    # This function is used for the "click on anywhere" part of the game
    start = False
    while not start:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Check if the user clicks anywhere and set the boolean to true
                start = True


def menuButton(msg, x, y, w, h, ic, ac, action=None):
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
        if click[0] == 1 and action is not None:
            if action == 'play':
                # If the new game button is clicked, run game loop
                clickSound()
                gameLoop()
            elif action == 'load':
                # If the load game button is clicked load text file from saved game and set is Loaded to true
                clickSound()
                # Play click sound
                if not Variables.isLoaded:
                    # If isLoaded is false, load the saved file
                    loadFile = shelve.open('firstFantasia')
                    # Check if playerteam is inside the load file
                    if 'playerTeam' in loadFile:
                        # then set is loaded to true, this bool will be used in line 653 to
                        # actually load the game
                        Variables.isLoaded = True
                        gameLoop()
            elif action == 'credits':
                clickSound()
                # If the quit game button is clicked, quit the game.
                credits()
            elif action == 'quit':
                # If the quit game button is clicked, quit the game.
                clickSound()
                pygame.quit()
                sys.exit()
    else:
        # Change button color when mouse not hovering
        pygame.draw.rect(screen, ac, (x, y, w, h))
    textSurf, textRect = textObject(msg, Variables.fontText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    # Display text unto button
    screen.blit(textSurf, textRect)


def textObject(text, font):
    # Render the text that we're going to use later in a dark gray color
    textSurface = font.render(text, True, Color.darkGray)
    return textSurface, textSurface.get_rect()


textBox = TextBox()

# Text box coordinates in the screen
textBox.rect.center = [400, 500]

# Name list to store the names we are going to input later
name = []


def TextBox():
    # This boolean is needed to declare a pre-condition statement that will
    # Make the while loop run.
    running = True
    # This boolean is needed to draw the tick button after
    # the user clicks enter
    returned = False
    while running:
        # Create a new frame
        screen.blit(Variables.bgImage, [0, 0])
        # Declare buttons
        # It's same as the one below, but we need this to be here so that when we update the display
        # It doesn't remove the button
        warriorButton = Button()
        warriorButton.assignImage(Variables.warriorImg)
        warriorButton.setCoords(200, 350)

        tankButton = Button()
        tankButton.assignImage(Variables.tankerOppositeImgPlayer)
        tankButton.setCoords(500, 340)

        tickButton = Button()
        tickButton.assignImage(Variables.tickImg)
        tickButton.setCoords(375, 510)

        warriorButton.drawButton(Variables.warriorImg)
        tankButton.drawButton(Variables.tankerOppositeImgPlayer)

        # Only draw the tick button when user clicks on enter
        if returned:
            tickButton.drawButton(Variables.tickImg)

        Dialog('Give a name for each of your players!', 100, 100)
        Dialog('Choose   units to start your adventure!', 100, 150)

        # Tell the user what to do so that it won't be confusing for them to input names.
        confirmation = Variables.fontSub.render("After you\'re done, press enter and click on the tick", True,
                                                Color.white)
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
                    # Set running to false to stop the loop.
                    running = False

def credits():

    screen.blit(Variables.bgImage, [0, 0])

    Title('First Fantasia', 130, 50)
    Dialog("Edbert Russel - Game Log", 200, 200)
    Dialog("Evan Reginald Wijaya - Save/Load Game", 110, 240)
    Dialog("Wong Chun Ting - Battle Logic & Characters", 90, 280)
    Dialog("Nguyen Tien Vu - Main Menu & Sorting", 120, 320)
    Dialog("Nguyen Trung Hieu - Create Units", 150, 360)
    Dialog("Timothy Dillan Tandjung - GUI Porting", 120, 400)
    Dialog("PSB Academy - Introduction to Programming", 100, 440)

    confirmation = Variables.fontSub.render("Click anywhere to go back...", True, Color.white)

    # Display the instructions
    screen.blit(confirmation, [255, 560])

    pygame.display.update()

    startScreen()

def gameLoop():
    # Create a variable called gameLog to create a file named gameLog.txt that stores every event in the game.
    gameLog = open('gameLog.txt', 'w')

    if not Variables.isLoaded:
        # Start game by creating a new frame (by loading a bg image)
        screen.blit(Variables.bgImage, [0, 0])

        # Declare units as buttons so that users can pick them.
        warriorButton = Button()
        warriorButton.assignImage(Variables.warriorImg)
        warriorButton.setCoords(200, 350)

        tankButton = Button()
        tankButton.assignImage(Variables.tankerOppositeImgPlayer)
        tankButton.setCoords(500, 340)

        # Draw the buttons declared before.
        warriorButton.drawButton(Variables.warriorImg)
        tankButton.drawButton(Variables.tankerOppositeImgPlayer)

        # Show a welcoming Text
        Dialog('Welcome to the game!', 100, 100)
        Dialog('Choose   units to start your adventure!', 100, 150)

        # Start choosing process
        # Declare variables needed in the choosing process
        warriorChoice = 0
        tankChoice = 0

        # Player team list to store the characters that the user chose
        playerTeam = []

        # while warriorChoice + tankChoice is less than 3, we create a while loop
        # to let the user pick what character that they want
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
                    # and check if the warrior button is pressed by the mouse
                    if warriorButton.pressed(mouse):
                        # add warriorChoice by 1 to make sure that the loop stops if the units reaches 3.
                        warriorChoice += 1
                        # show num of warriors player has in team
                        warriorText = Variables.fontText.render('%d Warrior' % (warriorChoice,), 1, (255, 255, 255))
                        playerTeam.append(Warrior.create(self))
                        # make a click sound so the user knows that they've clicked on the button
                        clickSound()
                        # ask user to input name
                        TextBox()
                    # now check if the tank button is pressed by the mouse
                    elif tankButton.pressed(mouse):
                        # add tankChoice by 1 to make sure that the loop stops if the units reaches 3.
                        tankChoice += 1
                        # show num of tanker player has in team
                        tankerText = Variables.fontText.render('%d Tanker' % (tankChoice,), 1, (255, 255, 255))
                        # create tanker instance, add in to player team
                        playerTeam.append(Tanker.create(self))
                        # make a click sound so the user knows that they've clicked on the button
                        clickSound()
                        # ask user to input name
                        TextBox()

        # assign the default names into the name received
        playerTeam[0].name = name[0]
        playerTeam[1].name = name[1]
        playerTeam[2].name = name[2]

        # generate ai players here
        aiTeam = genAIPlayers(playerTeam)

        # after the loop ends, create a new frame
        screen.blit(Variables.bgImage, [0, 0])

        # Header of the text file gamelog.
        gameLog.write("========================== PSB BATTLE GAME ==========================\n")

        # now lets actually render the text from the while loop before
        if warriorChoice > 0:
            # the if statement is needed because if the player chooses 3 tankers,
            # that means the warriortext will be null, which will result in a crash
            screen.blit(warriorText, [260, 320])
            screen.blit(Variables.warriorImg, [280, 350])
            gameLog.write(
                "[" + str(Variables.dateTimeObj) + "] " + str(warriorChoice) + " Warriors Chosen \n")

        if tankChoice > 0:
            # the if statement is needed because if the player chooses 3 tankers,
            # that means the tankertext will be null, which will result in a crash
            screen.blit(tankerText, [433, 320])
            screen.blit(Variables.tankerOppositeImgPlayer, [443, 350])
            gameLog.write("[" + str(Variables.dateTimeObj) + "] " + str(tankChoice) + " Tankers Chosen \n")

        # Write what units the players chosen into the text file.
        gameLog.write("\n========================== INITIALIZATION OF UNITS==========================\n")
        gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "Name of unit 1: " + playerTeam[0].name + " ATK Value: " + str(
                playerTeam[0].attack) + " DEF Value: " + str(playerTeam[0].defend) + " Class: " + playerTeam[
                0].job + "\n")
        gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "Name of unit 2: " + playerTeam[1].name + " ATK Value: " + str(
                playerTeam[1].attack) + " DEF Value: " + str(playerTeam[1].defend) + " Class: " + playerTeam[
                1].job + "\n")
        gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "Name of unit 3: " + playerTeam[2].name + " ATK Value: " + str(
                playerTeam[2].attack) + " DEF Value: " + str(playerTeam[2].defend) + " Class: " + playerTeam[
                2].job + "\n \n")

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

    # Declare save button
    saveButton = Button()
    saveButton.assignImage(Variables.saveImg)
    saveButton.setCoords(15, 20)

    if Variables.isLoaded:
        # If isLoaded is true
        loadFile = shelve.open("firstFantasia")
        # Load the file
        playerTeam = loadFile['playerTeam']
        # Set team to be the value in the file saved
        aiTeam = loadFile['aiTeam']
        # Set ai to be the value in the file saved
        Variables.isLoaded = False
        # Then set is loaded to false so if the user wants to load it again
        # they can.

    # These two variables is needed for the while loop.
    userTeamHP = playerTeam[0].health + playerTeam[1].health + playerTeam[2].health
    aiTeamHP = aiTeam[0].health + aiTeam[1].health + aiTeam[2].health

    # Write a battle sequence header to the gamelog to indicate that the battle is starting.
    gameLog.write("========================== BATTLE SEQUENCE ==========================\n")

    # Check if all the players and all the AI has more than 0 hp.
    while userTeamHP > 0 and aiTeamHP > 0:
        # Declare an initial value of 0 for attacker and defender
        # since we dont have an attacker or a defender yet.
        attacker = 0
        defender = 0

        # Render the players that the user has chosen
        drawPlayers(playerATKButton[0], playerATKButton[1], playerATKButton[2], playerTeam[0].job, playerTeam[1].job,
                    playerTeam[2].job,
                    playerTeam[0].health, playerTeam[1].health, playerTeam[2].health)

        # Draw the AI players so that the user can choose which AI does the user wants to attack
        drawAIPlayers(aiPlayerButtons[0], aiPlayerButtons[1], aiPlayerButtons[2], aiTeam[0].job, aiTeam[1].job,
                      aiTeam[2].job,
                      aiTeam[0].health, aiTeam[1].health, aiTeam[2].health)

        # This is needed for GUI purposes
        # If we don't use this, then the defend value will show 100000 instead.
        # Read more on character.py
        aiDefend1 = aiTeam[0].defend
        if aiTeam[0].health <= 0:
            aiDefend1 = 0

        aiDefend2 = aiTeam[1].defend
        if aiTeam[1].health <= 0:
            aiDefend2 = 0

        aiDefend3 = aiTeam[2].defend
        if aiTeam[2].health <= 0:
            aiDefend3 = 0

        Dialog("CLICK ON WHICH UNIT YOU WANT TO ATTACK WITH...", 80, 100)

        # Show all the players unit and their attributes.
        showPlayersAttribute(playerTeam[0].name, playerTeam[1].name, playerTeam[2].name, 20, 235, 140, 315, 390)
        showPlayersAttribute("HP: " + str(int(playerTeam[0].health)), "HP: " + str(int(playerTeam[1].health)),
                             "HP: " + str(int(playerTeam[2].health)), 20, 250, 140, 335, 405)
        showPlayersAttribute("ATK: " + str(int(playerTeam[0].attack)), "ATK: " + str(int(playerTeam[1].attack)),
                             "ATK: " + str(int(playerTeam[2].attack)), 20, 360, 140, 445, 505)

        showPlayersAttribute(aiTeam[0].name, aiTeam[1].name, aiTeam[2].name, 710, 230, 590, 315, 390)
        showPlayersAttribute("HP: " + str(int(aiTeam[0].health)), "HP: " + str(int(aiTeam[1].health)),
                             "HP: " + str(int(aiTeam[2].health)), 710, 250, 590, 335, 405)
        showPlayersAttribute("DEF: " + str(int(aiDefend1)), "DEF: " + str(int(aiDefend2)),
                             "DEF: " + str(int(aiDefend3)), 710, 365, 590, 445, 510)

        # Always update the attributes to the file every time the loop iterates.
        gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "Player 1: " + playerTeam[0].name + " ATK Value: " + str(
                playerTeam[0].attack) + " HP Value: " + str(int(playerTeam[0].health)) + "\n")
        gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "Player 2: " + playerTeam[1].name + " ATK Value: " + str(
                playerTeam[1].attack) + " HP Value: " + str(int(playerTeam[1].health)) + "\n")
        gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "Player 3: " + playerTeam[2].name + " ATK Value: " + str(
                playerTeam[2].attack) + " HP Value: " + str(int(playerTeam[2].health)) + "\n \n")

        saveButton.drawButton(Variables.saveImg)

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
                        if playerTeam[0].health > 0:
                            # If true, then the attacker will be the first player
                            attacker = playerTeam[0]
                        else:
                            # If false, break the loop and continue to the next statement
                            break
                    elif playerATKButton[1].pressed(mouse):
                        # If the second player is chosen and the mouse pos is in the
                        # second player button, then make a clickSound
                        clickSound()
                        # we check if the second player is not dead
                        if playerTeam[1].health > 0:
                            # If true, then the attacker will be the second player
                            attacker = playerTeam[1]
                        else:
                            # If false, break the loop and continue to the next statement
                            break
                    elif playerATKButton[2].pressed(mouse):
                        # If the second player is chosen and the mouse pos is in the
                        # second player button, then make a clickSound
                        clickSound()
                        if playerTeam[2].health > 0:
                            # If true, then the attacker will be the third player
                            attacker = playerTeam[2]
                        else:
                            # If false, break the loop and continue to the next statement
                            break
                    # if save button is pressed
                    elif saveButton.pressed(mouse):
                        # Play save sound if true
                        saveSound()
                        # Create a file called firstFantasia to save our values
                        saveFile = shelve.open('firstFantasia')
                        # Declare playerTeam as a variable inside the file, and set it to the value of the player team right now
                        saveFile['playerTeam'] = playerTeam
                        # Declare aiTeam as a variable inside the file, and set it to the value of the player ai team right now
                        saveFile['aiTeam'] = aiTeam
                        # Close the file after saving.
                        saveFile.close()

        # Create new frame
        screen.blit(Variables.bgImage2, [0, 0])

        # Draw the AI players so that the user can choose which AI does the user wants to attack
        drawPlayers(playerATKButton[0], playerATKButton[1], playerATKButton[2], playerTeam[0].job, playerTeam[1].job,
                    playerTeam[2].job,
                    playerTeam[0].health, playerTeam[1].health, playerTeam[2].health)
        drawAIPlayers(aiPlayerButtons[0], aiPlayerButtons[1], aiPlayerButtons[2], aiTeam[0].job, aiTeam[1].job,
                      aiTeam[2].job,
                      aiTeam[0].health, aiTeam[1].health, aiTeam[2].health)

        # Show all the players unit and their attributes.
        showPlayersAttribute(playerTeam[0].name, playerTeam[1].name, playerTeam[2].name, 20, 235, 140, 315, 390)
        showPlayersAttribute("HP: " + str(int(playerTeam[0].health)), "HP: " + str(int(playerTeam[1].health)),
                             "HP: " + str(int(playerTeam[2].health)), 20, 250, 140, 335, 405)
        showPlayersAttribute("ATK: " + str(int(playerTeam[0].attack)), "ATK: " + str(int(playerTeam[1].attack)),
                             "ATK: " + str(int(playerTeam[2].attack)), 20, 360, 140, 445, 505)

        showPlayersAttribute(aiTeam[0].name, aiTeam[1].name, aiTeam[2].name, 710, 230, 590, 315, 390)
        showPlayersAttribute("HP: " + str(int(aiTeam[0].health)), "HP: " + str(int(aiTeam[1].health)),
                             "HP: " + str(int(aiTeam[2].health)), 710, 250, 590, 335, 405)
        showPlayersAttribute("DEF: " + str(int(aiDefend1)), "DEF: " + str(int(aiDefend2)),
                             "DEF: " + str(int(aiDefend3)), 710, 365, 590, 445, 510)

        # Always update the attributes to the file everytime the loop iterates.
        gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "AI Unit 1: " + aiTeam[0].name + " DEF Value: " + str(
                aiDefend1) + " HP Value: " + str(int(aiTeam[0].health)) + "\n")
        gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "AI Unit 2: " + aiTeam[1].name + " DEF Value: " + str(
                aiDefend2) + " HP Value: " + str(int(aiTeam[1].health)) + "\n")
        gameLog.write(
            "[" + str(Variables.dateTimeObj) + "] " + "AI Unit 3: " + aiTeam[2].name + " DEF Value: " + str(
                aiDefend3) + " HP Value: " + str(int(aiTeam[2].health)) + "\n \n")

        # Show a loading text so that the user doesn't think that the game is broken/froze
        loadingText = Variables.fontSub.render("Waiting for a move.......", True, Color.black)

        # Display the loading text
        screen.blit(loadingText, [30, 570])

        saveButton.drawButton(Variables.saveImg)

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
                        if aiTeam[0].health > 0:
                            # If true, then the defender/enemy will be the first ai
                            defender = aiTeam[0]
                        else:
                            # If false, break the loop and continue to the next statement
                            break
                    # check if the user clicks on the second aiTeam
                    elif aiPlayerButtons[1].pressed(mouse):
                        # make a click sound if true
                        clickSound()
                        # check if the second AI's health is more than 0
                        if aiTeam[1].health > 0:
                            # If true, then the defender/enemy will be the second ai
                            defender = aiTeam[1]
                        else:
                            # If false, break the loop and continue to the next statement
                            break
                    # check if the user clicks on the third ai
                    elif aiPlayerButtons[2].pressed(mouse):
                        # make a click sound if true
                        clickSound()
                        # check if the third AI's health is more than 0
                        if aiTeam[2].health > 0:
                            # If true, then the defender/enemy will be the third ai
                            defender = aiTeam[2]
                        else:
                            # If false, break the loop and continue to the next statement
                            break
                    # if save button is pressed
                    elif saveButton.pressed(mouse):
                        # Play save sound if true
                        saveSound()
                        # Create a file called firstFantasia to save our values
                        saveFile = shelve.open('firstFantasia')
                        # Declare playerTeam as a variable inside the file, and set it to the value of the player team right now
                        saveFile['playerTeam'] = playerTeam
                        # Declare aiTeam as a variable inside the file, and set it to the value of the player aiTeam team right now
                        saveFile['aiTeam'] = aiTeam
                        # Close the file after saving.
                        saveFile.close()

        # Create new frame
        screen.blit(Variables.bgImage2, [0, 0])

        # Update the display
        pygame.display.update()

        # Declare a user turn, in which the player will attack the AI
        userTurn = attackFunc(attacker, defender)

        # Show and save the game log when the user attacks.
        showGameLog(attacker.name, userTurn, defender.name, int(attacker.experience), 25, 570)
        saveGameLog(gameLog, attacker.rank, attacker.name, userTurn, defender.name, int(attacker.experience),
                    Variables.dateTimeObj)

        # After the user attacks, change the attacker to AIs and defender to Players.
        attacker, defender = aiAttack(aiTeam, playerTeam)

        # Then the AI will attack here.
        aiTurn = attackFunc(attacker, defender)

        # Show and save the game log when the AI attacks.
        showGameLog(attacker.name, aiTurn, defender.name, int(attacker.experience), 25, 590)
        saveGameLog(gameLog, attacker.rank, attacker.name, aiTurn, defender.name, int(attacker.experience),
                    Variables.dateTimeObj)

        # Always get the latest Team hps.
        userTeamHP = playerTeam[0].health + playerTeam[1].health + playerTeam[2].health
        aiTeamHP = aiTeam[0].health + aiTeam[1].health + aiTeam[2].health

        # Always get the latest timestamp
        Variables.dateTimeObj = datetime.now()

    # If one of the team loses, write to the file that the game has finished.
    gameLog.write("\n========================== GAME FINISH ==========================\n")

    if userTeamHP == 0:
        # If the player team loses all their health, write, you lost.
        text = Variables.subTitleFont.render("You lost. Game over.", True, Color.white)
        gameLog.write("Game status: You lost. Game over.")
    else:
        # If not, then say, you won!
        text = Variables.subTitleFont.render("You won. Congrats!!!", True, Color.white)
        gameLog.write("Game status: You won. Congrats!!!")

    # Create a new frame
    screen.blit(Variables.bgImage, [0, 0])

    Dialog("CLICK ANYWHERE TO CONTINUE...", 100, 100)

    # Display the winning/losing text
    screen.blit(text, [100, 120])

    # Update the display
    pygame.display.update()

    startScreen()

    # Close the gamelog file.
    gameLog.close()
