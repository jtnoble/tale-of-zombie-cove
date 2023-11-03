import board_rooms, character, time, os

class Game():
    def __init__(self) -> None:
        self.location = [0][0]
        self.board = board_rooms.Board()
        self.character = character.Character(input("Input your name: "))
    
    def play(self) -> None:
        self.intro()
        self.game_loop()

    def intro(self) -> None:
        clear_screen()
        print("Zombie Cove:")
        time.sleep(1)
        print("Another castle once ruled by a monarchy of heroes gone to ruin.")
        print("It is known well not to tread lightly around these parts")
        print("The undead horde of past residents haunt the grounds, making for an impossible journey")
        print(f"You, {self.character.name}, are tasked with slaying the Boss Zombie: Yharl")
        print("May you survive, you shall be granted all wishes, but death is an outcome much more likely.\n")
        time.sleep(1)
        print("\nGuide:")
        print("[   ]: Explored Room")
        print("[ - ]: Unexplored Room")
        print("[ ! ]: Enemy Room")
        print("[ + ]: Loot Room")
        print("[ X ]: Boss Room")
        time.sleep(1)
        input("Press ENTER to continue...")
    
    def game_loop(self) -> None:
        while self.character.health > 0:
            self.board.show_board()
            self.character.inCombat = self.board.check_combat(self.character.location_x, self.character.location_y)
            print(f"Choose one of the following: {self.possible_moves(self.character.inCombat)}")
            _input = input(">").lower()
            self.selection(_input, self.character.inCombat)

    def attack_loop(self, target) -> None:
        while target.health > 0:
            clear_screen()
            print(f"{self.character.name} Health: {self.character.health}")
            print(f"Enemy: Health: {self.character.health}")
            print(f"Choose one of the following: {self.possible_moves(self.character.inCombat)}")
            _input = input(">").lower()
            self.selection(_input, self.character.inCombat)
            target.attack(self.character)

    def possible_moves(self, inCombat=False) -> list:
        if inCombat:
            return ["attack", "item"]
        return ["move", "describe", "heal", "rest", "item"]
    
    def selection(self, _input: str, inCombat=False) -> None:
        location = self.character.get_location()
        if inCombat:
            match _input:
                case "attack":
                    print(self.character.attack(self.board.rooms[location[0]][location[1]].enemy))
                case "item":
                    pass
        else:
            match _input.lower():
                case "move":
                    self.handle_move()
                case "describe":
                    print(self.board.rooms[location[0]][location[1]].description)
                    #get current room and explore
                case "heal":
                    self.character.heal()
                case "rest":
                    self.character.rest()
    
    def handle_move(self) -> None:
        _input = input("Which direction? [north, south, east, west]: ").lower()
        old_location = self.character.get_location()
        self.board.move_character(self.character, _input)
        new_location = self.character.get_location()
        self.board.rooms[old_location[0]][old_location[1]].explore()
        self.board.rooms[new_location[0]][new_location[1]].enter()
        

def clear_screen():
    os.system("clear")
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    game = Game()
    game.play()
