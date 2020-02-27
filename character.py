from random import randint
from setup import *
class warrior:
    def __init__(self, name, health, attack, defend, experience, rank):
        self.name = variables.fontText.render(name, True, (255, 255, 255))
        self.health = health
        self.attack = attack
        self.defend = defend
        self.experience = experience
        self.rank = rank
    def attribute(self):
        string = "Health" + str(self.health) + "Attack" + str(self.attack)
        return string
    def is_dead(self):
        return self.health <= 0
        
class tanker:
    def __init__(self, name, health, attack, defend, experience, rank):
        self.name = variables.fontText.render(name, True, (255, 255, 255))
        self.health = health
        self.attack = attack
        self.defend = defend
        self.experience = experience
        self.rank = rank
    def attribute(self):
        string = "Health" + str(self.health) + "Attack" + str(self.attack)
        return string
    def is_dead(self):
        return self.health <= 0   

war = ('Rich', 100, randint(5, 20), randint(1, 10), 0, 1 )
tan = ('Tom', 100, randint(1, 10), randint(5, 15), 0, 1)
print(war)
print(type(war))
print(tan)