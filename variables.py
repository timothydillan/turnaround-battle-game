import pygame
from datetime import datetime

pygame.init()

class Variables:
    # Declare variables in a class so that its easier to call and cleaner.
    validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
    shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
    font = pygame.font.Font('font/SHPinscher-Regular.otf', 110)
    subTitleFont = pygame.font.Font('font/SHPinscher-Regular.otf', 90)
    fontText = pygame.font.Font("font/slkscr.ttf", 24)
    fontSub = pygame.font.Font("font/slkscr.ttf", 16)
    pygame.display.set_caption("First Fantasia")
    bgImage = pygame.image.load('images/bg.png')
    icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(icon)
    warriorImg = pygame.image.load('images/warrior.png')
    tankerImg = pygame.image.load('images/tanker.png')
    tankerOppositeImgPlayer = pygame.image.load('images/tanker2.png')
    warriorEnemyImg = pygame.image.load('images/warriorEnemy.png')
    tankerEnemyImg = pygame.image.load('images/tankerEnemy.png')
    skullImg = pygame.image.load('images/skull.png')
    tickImg = pygame.image.load('images/tick.png')
    bgImage2 = pygame.image.load('images/bg2.png')
    saveImg = pygame.image.load('images/save.png')
    dateTimeObj = datetime.now()
    isLoaded = False
    player1X = 150
    player1Y = 385
    player2X = 50
    player2Y = 375
    aI1X = 550
    aI1Y = 385
    aI2X = 650
    aI2Y = 375
    textX = 130
    textY = 90

class Color:
    # Declare colors in a class so that we don't have to put in three numbers every time.
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (192, 192, 192)
    darkGray = (64, 64, 64)
    red = (255, 0, 0)
    green = (127, 255, 0)