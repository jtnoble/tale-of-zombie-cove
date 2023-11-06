import random, board_rooms

CHAR_ICON = "[ P ]"
MAX_STR = 20
MAX_AC = 18

# Information to store for character entities in the game
class Character():
    def __init__(self, name) -> None:
        self.name = name
        if len(name) == 0:
            self.name = "Steve"
        self.icon = CHAR_ICON
        self.location_x = 0
        self.location_y = 0
        self.inCombat = False
        self.inventory = []
        self.max_health = random_stat(10, 20)
        self.health = self.max_health
        self.max_stamina = random_stat(10, 20)
        self.stamina = self.max_stamina
        self.armor_class = random_stat()
        self.strength = random_stat()
        self.dexterity = random_stat()
        self.intelligence = random_stat()

    # Print off stats
    def show_stats(self) -> None:
        print(f"{self.name} | HP: {self.health}/{self.max_health} | AC: {self.armor_class} | Str: {self.strength} ")
    
    # Random roll chance for attacking
    def roll(self) -> int:
        return random.randint(1, 20)
    
    # Attacking, based on your roll versus an enemy's armor class
    def attack(self, target) -> str:
        d = self.roll()
        print(f"{self.name} rolled a {d}.")
        if d == 20:
            target.take_damage(self.strength * 2)
            if target.health < 0:
                self.inCombat = False
            return f"CRITICAL: {self.name} hit {target.name} for {str(self.strength * 2)}"
        elif d >= target.armor_class:
            target.take_damage(self.strength)
            if target.health < 0:
                self.inCombat = False
            return f"{self.name} hit {target.name} for {self.strength}"
        else:
            return f"{self.name} missed!"

    # Taking damage by subtracting health
    def take_damage(self, amount) -> None:
        self.health -= amount
    
    # Move character based on str input
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
    
    # Check if move is within the bounds of the board
    def check_move(self, direction, incrememnt) -> bool:
        val = direction + incrememnt
        rows = board_rooms.ROWS
        cols = board_rooms.COLS
        if val < 0 or val > rows or val < 0 or val > cols:
            return False
        return True
    
    # Friendly readable getter for inventory
    def get_inventory(self) -> list:
        items = []
        for item in self.inventory:
            items.append(list(item)[0])
        return items
    
    # Getter for character location
    def get_location(self) -> list:
        return[self.location_x, self.location_y]
            
# Character subclass: For the player
class Player(Character):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.armor_class = random_stat(8,13)
        self.strength = random_stat(4, 10)
        self.heals_left = 3
    
    # Print off stats (overload to include heals)
    def show_stats(self) -> None:
        print(f"{self.name} | HP: {self.health}/{self.max_health} | AC: {self.armor_class} | Str: {self.strength} | Heals: {self.heals_left}/3")

    # Add item to inventory
    def obtain_item(self) -> str:
        if self.strength >= MAX_STR and self.armor_class >= MAX_AC:
            item = self.possible_items()[0]
        else:
            item = random.choice(self.possible_items())
        self.inventory.append(item)
        return list(item.keys())[0]

    # Possible items to get from pickups
    def possible_items(self) -> list:
        h_potion = {"health_potion": self.heal_potion}
        whetstone = {"whetstone": self.strength_levelup}
        armor = {"armor_plate": self.armor_increase}
        return [h_potion, whetstone, armor]
    
    # increase health points
    def heal(self, potion=False, amt=random.randint(3,6)) -> None:
        if potion:
            if self.health == self.max_health:
                self.inventory.append(self.possible_items()[0])
                print("Already at full health!")
                return None
            self.health += amt
            if self.health > self.max_health:
                self.health = self.max_health
            print("Healed for " + str(amt))
        elif self.heals_left > 0:
            if self.health == self.max_health:
                print("Already at full health!")
                input("[ENTER]")
                return None
            self.health = self.max_health
            self.heals_left -= 1
            print("Healed to full health")
            input("[ENTER]")
        else:
            print("No more heals left!")
            input("[ENTER]")
    def heal_potion(self) -> None:
        self.heal(True)
    
    # increase strength
    def strength_levelup(self, amt=random.randint(1,3)) -> bool:
        if self.strength >= MAX_STR:
            print("Strength already at max!")
            self.inventory.append(self.possible_items()[1])
            return False
        if self.strength + amt > MAX_STR:
            self.strength = MAX_STR
            print("Strength maxed out!")
            return True
        self.strength += amt
        print(f"Strength increased by {amt}")
        return True
        
    
    # increase armor class
    def armor_increase(self, amt=random.randint(1,3)) -> bool:
        if self.armor_class >= MAX_AC:
            print("Armor Class already maxed out!")
            self.inventory.append(self.possible_items()[2])
            return False
        if self.armor_class + amt > MAX_AC:
            print("Armor Class maxed out!")
            return True
        self.armor_class += amt
        print(f"Armor Class increased by {amt}")
        return True
    
    # Use an item
    def use_item(self) -> bool:
        _input = input(">").lower()
        keys = []
        for item in self.inventory:
            keys.append(item.keys())
        if _input in self.get_inventory():
            items_list = self.possible_items()
            for i in items_list:
                if i.get(_input):
                    i.get(_input)()
                    self.inventory.pop(self.inventory.index(i))
                    input("[ENTER]")
                    return True
        elif _input == "exit":
            return True
        return False
      
    # Level character up 
    def level_up(self, stat) -> bool:
        match stat:
            case "strength":
                if not self.strength_levelup(amt=1):
                    return False
                input("[ENTER]")
            case "health":
                self.max_health += 1
                print("Increased max health by 1.")
                input("[ENTER]")
            case "armor":
                if not self.armor_increase(amt=1):
                    return False
                input("[ENTER]")
            case _:
                return False
        return True

# Character subclass: For enemies to be given slightly modified stats
class Enemy(Character):
    def __init__(self, name="Zombie") -> None:
        super().__init__(name)
        self.armor_class = random_stat(3,12)
        self.strength = random_stat(1,5)

# Character subclass: For boss enemy to have specific armor class, strength and health
class Boss(Character):
    def __init__(self, name="Yharl") -> None:
        super().__init__(name)
        self.max_health = 50
        self.health = self.max_health
        self.armor_class = 14
        self.strength = 8

# Generate random stat (not needed in class)
def random_stat(MIN=1, MAX=10) -> int:
        return random.randint(MIN, MAX)

if __name__ == "__main__":
    print("Please run the `game.py` file instead of this file.")