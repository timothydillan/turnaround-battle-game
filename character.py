from random import randint

from pylint.checkers import variables
import self
from setup import *


class Warrior:
    def __init__(self, name, health, attack, defend, experience, rank):
        self.name = name
        self.health = health
        self.attack = attack
        self.defend = defend
        self.experience = experience
        self.rank = rank
        self.job = "Warrior"
    def attribute(self):
        string = "Health" + str(self.health) + "Attack" + str(self.attack)
        return string
    def is_dead(self):
        return self.health <= 0
    def create(self):
        warrior_char = Warrior("Alice", 100, randint(10, 20),
                            randint(5, 10), 0, 1,)
        return warrior_char


class Tanker:
    def __init__(self, name, health, attack, defend, experience, rank):
        self.name = name
        self.health = health
        self.attack = attack
        self.defend = defend
        self.experience = experience
        self.rank = rank
        self.job = "Tanker"
    def attribute(self):
        string = "Health" + str(self.health) + "Attack" + str(self.attack)
        return string
    def is_dead(self):
        return self.health <= 0

    def create(self):
        tanker_char = Tanker("Bob", 100, randint(5, 10),
                            randint(10, 20), 0, 1,)
        return tanker_char


