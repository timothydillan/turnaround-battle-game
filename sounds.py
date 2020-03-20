import pygame

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.mixer.init()

def clickSound():
    # A function used to play a sound that we define.
    # In this case, we're playing a click sound.
    sound = pygame.mixer.Sound('sound/clickSound.ogg')
    sound.play()

def saveSound():
    # A function used to play a sound that we define.
    # In this case, we're playing a sound requested by one of our group members.
    # Evan.
    sound = pygame.mixer.Sound('sound/evan.ogg')
    sound.play()

def bgMusic():
    # A function used to play a song that we define.
    pygame.mixer.music.load('sound/backgroundmusic.ogg')
    # Loop the music.
    pygame.mixer.music.play(-1)