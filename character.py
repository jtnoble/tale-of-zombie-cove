import random, board_rooms

CHAR_ICON = "[ P ]"
class Character():
    def __init__(self, name) -> None:
        self.name = name
        self.icon = CHAR_ICON
        self.location_x = 0
        self.location_y = 0
        self.inCombat = False
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
    
    def attack(self, target) -> str:
        d = self.roll()
        if d >= target.armor_class:
            target.take_damage(self.strength)
            if target.health < 0:
                self.inCombat = False
            return f"{self.name} hit {target.name} for {self.strength}"
        else:
            return f"{self.name} missed!"

    def take_damage(self, amount) -> int:
        self.health -= amount
    
    def move(self, direction) -> None:
        match direction:
            case "east":
                if self.check_move(self.location_y, 1):
                    self.location_y += 1
            case "south":
                if self.check_move(self.location_x, 1):
                    self.location_x += 1
            case "west":
                if self.check_move(self.location_y, -1):
                    self.location_y -= 1
            case "north":
                if self.check_move(self.location_x, -1):
                    self.location_x -= 1
            case _:
                print("Invalid Movement")
    
    def check_move(self, direction, incrememnt) -> bool:
        val = direction + incrememnt
        rows = board_rooms.ROWS
        cols = board_rooms.COLS
        if val < 0 or val > rows or val < 0 or val > cols:
            return False
        return True

    def get_location(self) -> list:
        return[self.location_x, self.location_y]
            


class Player(Character):
    def __init__(self, name) -> None:
        super().__init__(name)

class Enemy(Character):
    def __init__(self, name="Zombie") -> None:
        super().__init__(name)
        self.armor_class = random_stat()
        self.strength = random_stat()

class Boss(Character):
    def __init__(self, name="Yharl") -> None:
        super().__init__(name)
        self.health = 30
        self.armor_class = 8
        self.strength = 8

# Generate random stat (not needed in class)
def random_stat(MIN=1, MAX=10) -> int:
        return random.randint(MIN, MAX)
