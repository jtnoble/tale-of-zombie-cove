import random

class Character():
    def __init__(self, name) -> None:
        self.name = name
        self.icon = "[ P ]"
        self.location = [0][0]
        self.max_health = random_stat(10, 20)
        self.health = self.max_health
        self.max_stamina = random_stat(10, 20)
        self.stamina = self.max_stamina
        self.armor_class = random_stat()
        self.strength = random_stat()
        self.dexterity = random_stat()
        self.intelligence = random_stat()

    # increase health points
    def heal(self) -> None:
        amt = random.randint(1,6)
        self.health += amt
        if self.health > self.max_health:
            self.health = self.max_health

    # increase stamina points
    def rest(self) -> None:
        amt = random.randint(1,6)
        self.stamina += amt
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina

    def roll(self) -> int:
        return random.randint(1, 20)
    
    def attack(self) -> int:
        return self.strength
    
    def move(self, direction) -> None:
        match direction:
            case "north":
                self.location += [0][1]
            case "east":
                self.location += [1][0]
            case "south":
                self.location -= [0][1]
            case "west":
                self.location -= [1][0]
            


class Player(Character):
    def __init__(self, name) -> None:
        super().__init__(name)

class Enemy(Character):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.armor_class = random_stat()
        self.strength = random_stat()

# Generate random stat (not needed in class)
def random_stat(MIN=1, MAX=10) -> int:
        return random.randint(MIN, MAX)
