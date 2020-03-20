# Initialize libraries needed for the game.
# All things taken from the internet are put in referenceList.txt

from pygame.locals import *
from setup import *
from sounds import bgMusic
from gui import Title, Player

def __main__():
    # Play the background music
    bgMusic()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                run = False
        # Create a new frame
        screen.blit(Variables.bgImage, [0, 0])
        # Create main menu buttons
        menuButton("New Game", 325, 400, 150, 30, Color.white, Color.gray, 'play')
        menuButton("Load Game", 325, 450, 150, 30, Color.white, Color.gray, 'load')
        menuButton("Credits", 325, 500, 150, 30, Color.white, Color.gray, 'credits')
        menuButton("Quit", 325, 550, 150, 30,  Color.white, Color.gray, 'quit')
        # Render PSB Battle Game as the title
        Title('First Fantasia', Variables.textX, Variables.textY)
        # Draw players for the main menu (UI Purposes)
        Player()
        # Update the screen so that we can see everything we rendered before.
        pygame.display.update()

# https://stackoverflow.com/questions/419163/what-does-if-name-main-do/20158605#20158605
# only run the code if its the entry point to the program
if __name__ == '__main__':
    __main__()
