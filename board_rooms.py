import numpy as np
import random, os
from character import Character, CHAR_ICON, Enemy, Boss, Player

# Global variables for access by other classes
ROWS = 4
COLS = 4
BOSS = 1

# Basic empty room class, to fill the board
class Room():
    def __init__(self) -> None:
        self.room_icon = "[ - ]"
        self.description = self.create_description()
        self.item = False
        self.enemy = None
        self.boss = None
    
    def explore(self) -> None:
        self.room_icon = "[   ]"
    
    def create_description(self) -> str:
        with open("room_descriptions.txt", "r") as f:
            lines = f.readlines()
        return random.choice(lines).replace("\n","")
    
    def enter(self) -> None:
        self.room_icon = CHAR_ICON

# Room subclass, contains an enemy
class EnemyRoom(Room):
    def __init__(self) -> None:
        super().__init__()
        self.room_icon = "[ ! ]"
        self.enemy = Enemy()

# Room subclass, contains loot
class LootRoom(Room):
    def __init__(self) -> None:
        super().__init__()
        self.room_icon = "[ + ]"
        self.item = True

# Room subclass, contains Yharl, the Boss
class BossRoom(Room):
    def __init__(self) -> None:
        super().__init__()
        self.room_icon = "[ X ]"
        self.description = "A large cavern holding Yharl"
        self.enemy = Boss()
        self.boss = Boss()

# Main board for game, created from rows and columns
class Board():
    def __init__(self) -> None:
        # Create a semi-random board
        self.clear_screen()
        self.rows = ROWS
        self.cols = COLS
        self.boss_rooms = 1
        self.rooms = self.generate_rooms()

    # Generate rooms in a grid using numpy
    # Ensure one boss room and clear the player spawn to elimate immediate loot or combat
    def generate_rooms(self) -> list:
        rooms = np.empty((self.rows, self.cols), dtype=Room)
        for x in range(self.rows):
            for y in range(self.cols):
                rooms[x, y] = self.generate_special_type()
        # Replace first room with empty room for player
        rooms[0,0] = Room()
        rooms[0,0].room_icon = CHAR_ICON
        # Replace one room at random with a boss room
        rng1 = random.randint(1,ROWS-1)
        rng2 = random.randint(1,COLS-1)
        rooms[rng1, rng2] = BossRoom()
        return rooms
    
    # Random chance for a special or normal room
    # Roughly 60% for Normal rooms, 20% for Enemies, and 20% for loot
    def generate_special_type(self) -> Room:
        rng = random.randint(0,9)
        if rng < 5:
            return Room()
        elif 5 <= rng <= 7:
            return EnemyRoom()
        elif rng > 7:
            return LootRoom()
    
    # Getter for rooms
    def get_room(self, x, y) -> Room:
        return self.rooms[x,y]
    
    # Getter for room description
    def describe_room(self, x, y) -> str:
        return self.rooms[x, y].description
    
    # Print the board in a grid to the screen
    def show_board(self) -> None:
        for row in self.rooms:
            for col in row:
                if col is not None:
                    print(col.room_icon, end="  ")
            print("")
    
    # Handle calling the character obj's movement
    def move_character(self, character: Character, direction: str) -> None:
        character.move(direction)
    
    # Return bool based on if the room has an enemy or boss in it
    def check_combat(self, x, y) -> bool:
        if self.rooms[x][y].enemy or self.rooms[x][y].boss:
            return True
        return False
    
    # Return item if item is in the room
    def check_loot(self, x, y) -> dict:
        if self.rooms[x][y].item:
            item = self.rooms[x][y].item
            self.rooms[x][y].item = None
            return item
        return None

    # Clear screen (OS checking)
    def clear_screen(self):
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')

if __name__ == "__main__":
    print("Debug: Generate room\n")
    board = Board()
    board.show_board()
    room = board.get_room(2, 3)