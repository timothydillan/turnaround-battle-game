import pygame
from variables import Variables, Color

pygame.init()
screen = pygame.display.set_mode((800, 650))

class Button:
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
    # A "TextBox" class so that we're able to input things unto the screen.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.font = pygame.font.Font("font/slkscr.ttf", 30)
        self.image = self.font.render('Input character name: ', False, Color.white)
        self.rect = self.image.get_rect()
        self.shifted = False

    # Create a function to add capital/non-capital texts
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

def Dialog(text, x, y):
    # This function renders a text.
    text = Variables.fontText.render(text, True, (255, 255, 255))
    screen.blit(text, (x, y))

def Player():
    # Show players on the main menu (UI Purposes)
    screen.blit(Variables.warriorImg, (Variables.player1X, Variables.player1Y))
    screen.blit(Variables.tankerImg, (Variables.player2X, Variables.player2Y))
    screen.blit(Variables.warriorEnemyImg, (Variables.aI1X, Variables.aI1Y))
    screen.blit(Variables.tankerEnemyImg, (Variables.aI2X, Variables.aI2Y))

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
        button0.assignImage(Variables.tankerEnemyImg)
        button0.setCoords(-100, -100)
        button0.drawButton(Variables.tankerEnemyImg)
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
        button1.assignImage(Variables.tankerEnemyImg)
        button1.setCoords(-100, -100)
        button1.drawButton(Variables.tankerEnemyImg)
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
        button2.assignImage(Variables.tankerEnemyImg)
        button2.setCoords(-100, -100)
        button2.drawButton(Variables.tankerEnemyImg)
        screen.blit(Variables.skullImg, [0, 420])

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
        button0.assignImage(Variables.tankerEnemyImg)
        button0.setCoords(-100, -100)
        button0.drawButton(Variables.tankerEnemyImg)
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
        button1.assignImage(Variables.tankerEnemyImg)
        button1.setCoords(-100, -100)
        button1.drawButton(Variables.tankerEnemyImg)
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
        button2.assignImage(Variables.tankerEnemyImg)
        button2.setCoords(-100, -100)
        button2.drawButton(Variables.tankerEnemyImg)
        screen.blit(Variables.skullImg, [690, 420])


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

    if dmg > 0:
        # We check if the damage done is more than 0.
        # If true, then let the damage be whatever the value is.
        dmg = dmg
    else:
        # If not set damage to 0 (to prevent from gamelog showing negative values.
        dmg = 0

    logText = Variables.fontSub.render("[Game Message] " + str(attacker) + " dealt " + str(dmg) + " dmg to " + str(
        defender) + " and now has a total of "
                                       + str(xp) + " exp.", True, Color.black)
    # Then display the texts based on the argument coordinates.
    screen.blit(logText, [x, y])

def saveGameLog(log, rank, attacker, dmg, defender, xp, time):
    # A function to write the game log events to the file.
    log.write("[" + str(time) + "] " + "Level {} ".format(rank) + "Unit 1: " + str(
        attacker) + " dealt " + str(dmg) + " dmg to " + str(defender) + " and now has a total of "
              + str(xp) + " exp." "\n \n")