import random

class Player:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.inventory = []

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        return self.health

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
        return self.health

    def add_item(self, item):
        self.inventory.append(item)


class Game:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def random_event(self):
        for player in self.players:
            if random.choice([True, False]):
                damage = random.randint(5, 20)
                player.take_damage(damage)
                print(f'{player.name} took {damage} damage! Health now: {player.health}')
            else:
                heal_amount = random.randint(5, 20)
                player.heal(heal_amount)
                print(f'{player.name} healed {heal_amount}! Health now: {player.health}')