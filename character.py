# Initialize libraries needed for the class.
# All things taken from the internet are put in referenceList.txt

from random import randint
import self
from setup import *

# Declare a warrior class for the units.
class Warrior:
    # Initialize attributes of a Warrior
    def __init__(self, name, health, attack, defend, experience, rank):
        self.name = name
        self.health = health
        self.attack = attack
        self.defend = defend
        self.experience = experience
        self.rank = rank
        self.job = "Warrior"

    def create(self):
        # A function to create a warrior with predefined values. We'll change it later on setup.py.
        warriorChar = Warrior("Alice", 100, randint(10, 20), randint(5, 10), 0, 1,)
        return warriorChar

    def checkLevelUp(self):
        # A function that automatically levels up the current unit, and resets the xp if xp is 100.
        if self.experience > 99:
            self.rank += 1
            self.attack = round(self.attack * 1.05, 2)
            self.defend = round(self.defend * 1.05, 2)
            self.experience = 0

    def checkDie(self):
        # A function that checks if a player is dead.
        if self.health <= 0:
            # if the player has a hp below or is 0
            # then set all attributes to 0, except for defend.
            # We set defend to a large value, so that the AI does not attack a dead player.
            self.health = 0
            self.attack = 0
            self.defend = 1000000
            self.experience = 0

# Delcare a Tanker class for the units.
class Tanker:
    # Initialize attributes of a Warrior
    def __init__(self, name, health, attack, defend, experience, rank):
        self.name = name
        self.health = health
        self.attack = attack
        self.defend = defend
        self.experience = experience
        self.rank = rank
        self.job = "Tanker"
    def create(self):
        # A function to create a warrior with predefined values. We'll change it later on setup.py.
        tankerChar = Tanker("Bob", 100, randint(5, 10), randint(10, 20), 0, 1,)
        return tankerChar

    def checkLevelUp(self):
        # A function that automatically levels up the current unit, and resets the xp if xp is 100.
        if self.experience > 99:
            self.rank += 1
            self.attack = round(self.attack * 1.05, 2)
            self.defend = round(self.defend * 1.05, 2)
            self.experience = 0

    def checkDie(self):
        # A function that checks if a player is dead.
        if self.health <= 0:
            # if the player has a hp below or is 0
            # then set all attributes to 0, except for defend.
            # We set defend to a large value, so that the AI does not attack a dead player.
            self.health = 0
            self.attack = 0
            self.defend = 1000000
            self.experience = 0
