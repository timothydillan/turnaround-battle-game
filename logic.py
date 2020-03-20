import copy
from character import *
from random import randint

def genAIPlayers(copyTeam):
    # A function to generate AI players.
    # Deep copy the User team to create another object, instead of referencing it to
    # the user team itself.
    aiTeam = copy.deepcopy(copyTeam)
    # Make a nested loop that loops through all the players in the AI team.
    for aiPlayer in aiTeam:
        # Randomize their names and jobs so that it isn't the same as the user team.
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

def attackFunc(turnAttacker, turnDefender):
    # A function for the damage calculation which is used later at the battle sequence.
    ranNum = randint(5, 10)
    # Create a random number from 5-10 for a additional damage.
    # And do the damage calculation here.
    dmg = int(turnAttacker.attack + ranNum - turnDefender.defend)
    if dmg > 0:
        # There is a problem if we don't check if dmg is > 0
        # The dmg can be less than 0 and can decrease/increase the opponents HP
        # So we only deal damage if the dmg is more than 0.
        turnDefender.health -= dmg
        # A new game logic, here after the attacker deals dmg,
        # the defender actually also inflicts a small amount of dmg to the attacker.
        turnAttacker.health -= int(dmg * 0.2)
        # Add the attacker xp based on the damage inflicted
        turnAttacker.experience += dmg
        # And add the defender/enemy xp based on the defend value.
        turnDefender.experience += turnDefender.defend
        # Check if the user can level up/ is dead
        Tanker.checkLevelUp(turnAttacker)
        Tanker.checkLevelUp(turnDefender)
        Tanker.checkDie(turnAttacker)
        Tanker.checkDie(turnDefender)
        return dmg
    elif dmg < 0:
        # If the damage inflicted is less than 0
        # Actually penalty the player or basically, like in pokemon
        # the move confused deals dmg to the user itself (but a small amount).
        turnAttacker.health -= int(abs(dmg * 0.5))
        # Add both the attacker and defender xp by the attack value of the attacker
        # and add a random number to amplify the number.
        turnAttacker.experience += int(abs(turnAttacker.attack + ranNum))
        turnDefender.experience += int(abs(turnAttacker.attack + ranNum))
        # Check if the user can level up/ is dead
        Tanker.checkLevelUp(turnAttacker)
        Tanker.checkLevelUp(turnDefender)
        Tanker.checkDie(turnAttacker)
        Tanker.checkDie(turnDefender)
        return dmg
    else:
        return dmg

def aiAttack(aiTeam, targetTeam):
    # A function to create the AI Logic.
    # Get the AI unit that has the highest attack point using getattr and put them into a list
    # then find the unit that has the highest atk point and match it to the list, then get the number
    aiAttacker = [char for char in aiTeam if char.attack == max([getattr(char, 'attack') for char in aiTeam])]
    # Get the users unit that has lowest defence point and use getattr and put them into a list like the attack one
    userDefender = [char for char in targetTeam if char.defend == min([getattr(char, 'defend') for char in targetTeam])]
    # and return the index number.
    return aiAttacker[0], userDefender[0]