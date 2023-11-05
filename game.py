import board_rooms, character, time, os

class Game():
    def __init__(self) -> None:
        self.location = [0][0]
        self.board = board_rooms.Board()
        self.character = character.Character(input("Input your name: "))
        self.queued_message = ""    # For showing messages at the beginning of a loop
    
    # Play handler, ONLY function calls
    def play(self) -> None:
        self.intro()
        self.game_loop()
        self.end_game()

    # Everything before the game loop
    def intro(self) -> None:
        self.clear_screen()
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
    
    # Main loop for movement and selection
    def game_loop(self) -> None:
        while self.character.health > 0:
            self.clear_screen()
            self.board.show_board()
            self.character.inCombat = self.board.check_combat(self.character.location_x, self.character.location_y)
            if self.character.inCombat:
                self.attack_loop(self.board.rooms[self.character.location_x][self.character.location_y].enemy)
                continue
            print(f"Choose one of the following: {self.possible_moves(self.character.inCombat)}")
            _input = input(">").lower()
            self.selection(_input, self.character.inCombat)

    # Sub loop when you are in combat
    def attack_loop(self, target) -> None:
        while target.health > 0:
            self.clear_screen()
            print(f"{self.character.name} Health: {self.character.health}")
            print(f"{target.name} Health: {target.health}")
            print(f"Choose one of the following: {self.possible_moves(self.character.inCombat)}")
            _input = input(">").lower()
            self.selection(_input, self.character.inCombat)
            time.sleep(1)
            if target.health > 0:
                print(target.attack(self.character))
                time.sleep(1)
            if self.character.health <= 0 :
                self.end_game()
        print(f"{self.character.name} defeated {target.name}")      
        time.sleep(2)

    # Moves dependent on combat status
    def possible_moves(self, inCombat=False) -> list:
        if inCombat:
            return ["attack", "item"]
        return ["move", "describe", "heal", "rest", "item"]
    
    # Combat functions based on user input and combat status
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
                case "heal":
                    self.character.heal()
                case "rest":
                    self.character.rest()
    
    # Handle calling movement functions from board_rooms and character objs
    def handle_move(self) -> None:
        _input = input("Which direction? [north, south, east, west]: ").lower()
        old_location = self.character.get_location()
        self.board.move_character(self.character, _input)
        new_location = self.character.get_location()
        self.board.rooms[old_location[0]][old_location[1]].explore()
        self.board.rooms[new_location[0]][new_location[1]].enter()
        
    # End game, for when the player has exited the game loop from having 0 HP
    def end_game(self) -> None:
        print(f"It was a valiant effort; however, {self.character.name} was unable to complete their quest.")
        print("Another adventurer fallen victim to Yharl and his horde.")
        print("Game Over.")
        time.sleep(2)
        exit()

    # Clear screen (OS checking)
    def clear_screen(self):
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')

if __name__ == "__main__":
    game = Game()
    game.play()
