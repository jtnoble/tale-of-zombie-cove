import numpy as np
import random, os

class Room():
    def __init__(self) -> None:
        self.room_icon = "[   ]"
            
    def explore(self) -> None:
        self.room_icon = "[   ]"

class EnemyRoom(Room):
    def __init__(self) -> None:
        self.room_icon = "[ ! ]"

class LootRoom(Room):
    def __init__(self) -> None:
        self.room_icon = "[ + ]"

class BossRoom(Room):
    def __init__(self) -> None:
        self.room_icon = "[ X ]"

class Board():
    def __init__(self) -> None:
        # Create a semi-random board
        os.system('clear')
        self.rows = 5
        self.cols = 5
        self.boss_rooms = 1
        self.rooms = self.generate_rooms()
    
    def generate_rooms(self) -> list:
        rooms = np.empty((self.rows, self.cols), dtype=Room)
        for x in range(self.rows):
            for y in range(self.cols):
                rooms[x, y] = self.generate_special_type()
        # Replace one room at random with a boss room
        rng1 = random.randint(1,4)
        rng2 = random.randint(1,4)
        rooms[rng1, rng2] = BossRoom()
        return rooms
    
    def generate_special_type(self) -> Room:
        rng = random.randint(0,9)
        if rng < 5:
            return Room()
        elif 5 <= rng <= 7:
            return EnemyRoom()
        elif rng > 7:
            return LootRoom()
        
    def get_room(self, x, y) -> Room:
        return self.rooms[x,y]
    
    def show_board(self) -> None:
        for row in self.rooms:
            for col in row:
                if col is not None:
                    print(col.room_icon, end="  ")
            print("")

if __name__ == "__main__":
    print("Debug: Generate room\n")
    board = Board()
    board.show_board()
    room = board.get_room(2, 3)