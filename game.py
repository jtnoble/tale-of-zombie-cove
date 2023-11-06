import board_rooms, character, time, os

class Game():
    def __init__(self) -> None:
        self.location = [0][0]
        self.board = board_rooms.Board()
        self.character = character.Player(input("Input your name: "))
        self.queued_message = ""    # For showing messages at the beginning of a loop
    
    # Play handler, ONLY function calls
    def play(self) -> None:
        self.intro()
        self.game_loop()

    # Everything before the game loop
    def intro(self) -> None:
        self.clear_screen()
        print("Tale Of Zombie Cove:")
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
        self.enter_to_continue()
    
    # Main loop for movement and selection
    def game_loop(self) -> None:
        while self.character.health > 0:
            location = self.character.get_location()
            self.clear_screen()
            self.character.show_stats()
            self.board.show_board()
            self.character.inCombat = self.board.check_combat(location[0], location[1])
            if self.character.inCombat:
                self.attack_loop(self.board.rooms[location[0]][location[1]].enemy)
                continue
            loot = self.board.check_loot(location[0], location[1])
            if loot:
                item = self.character.obtain_item()
                print(f"You got a {item}")
            print(f"Choose one of the following: {self.possible_moves(self.character.inCombat)}")
            _input = input(">").lower()
            self.selection(_input, self.character.inCombat)

    # Sub loop when you are in combat
    def attack_loop(self, target) -> None:
        while target.health > 0:
            self.clear_screen()
            self.character.show_stats()
            target.show_stats()
            print(f"Choose one of the following: {self.possible_moves(self.character.inCombat)}")
            _input = input(">").lower()
            if self.selection(_input, self.character.inCombat):
                time.sleep(0.25)
                if target.health > 0:
                    print(target.attack(self.character))
                    self.enter_to_continue()
                if self.character.health <= 0 :
                    self.end_game(False)
        print(f"{self.character.name} defeated {target.name}")
        if type(target) == character.Boss:
            self.end_game(True)
        location = self.character.get_location()
        self.board.rooms[location[0]][location[1]].enemy = None
        self.character.inCombat = False
        time.sleep(1)
        # LEVEL UP
        print("Choose a stat to level up!\nstrength | health | armor")
        while True:
            if self.character.level_up(input(">")):
                break

    # Moves dependent on combat status
    def possible_moves(self, inCombat=False) -> list:
        if inCombat:
            return ["attack", "item"]
        return ["move", "describe", "heal", "item"]
    
    # Combat functions based on user input and combat status
    def selection(self, _input: str, inCombat=False) -> None:
        location = self.character.get_location()
        while True:
            if inCombat:
                enemy: character.Enemy = self.board.rooms[location[0]][location[1]].enemy
                match _input:
                    case "attack":
                        print(self.character.attack(enemy))
                        return True
                    case "item":
                        self.use_item()
                        return False
                    case _:
                        print("Invalid selection! ")
                        _input = input(">").lower()
            else:
                match _input.lower():
                    case "move":
                        self.handle_move()
                        break
                    case "describe":
                        print(self.board.rooms[location[0]][location[1]].description)
                        self.enter_to_continue()
                        break
                    case "heal":
                        self.character.heal()
                        break
                    case "item":
                        self.use_item()
                        break
                    case _:
                        print("Invalid selection!")
                        _input = input(">").lower()
    
    # Use item as a character
    def use_item(self) -> None:
        while True:
            self.clear_screen()
            self.character.show_stats()
            if len(self.character.inventory) <= 0:
                print("Inventory Empty")
                self.enter_to_continue()
                break
            items = ""
            for item in self.character.get_inventory():
                items += f"{item} | "
            print(f"Choose an item:\n{items}\nor type 'exit' to exit")
            if self.character.use_item():
                break

    # Handle calling movement functions from board_rooms and character objs
    def handle_move(self) -> None:
        _input = input("Which direction? [north, south, east, west]: ").lower()
        old_location = self.character.get_location()
        self.board.move_character(self.character, _input)
        new_location = self.character.get_location()
        self.board.rooms[old_location[0]][old_location[1]].explore()
        self.board.rooms[new_location[0]][new_location[1]].enter()
        
    # End game, for when the player has exited the game loop from having 0 HP or for beating Yharl
    def end_game(self, win) -> None:
        self.clear_screen()
        if win:
            print(f"After a long battle, {self.character.name} was triumphant.")
            time.sleep(1)
            print(f"Yharl has been taken down.")
            time.sleep(1)
            print(f"The undead horde has seemingly disintegrated after the falling of their leader.")
            time.sleep(1)
            print(f"The townsfolk nearby can march forward and bring life to the once highly established castle.")
            time.sleep(1)
            print(f"They thank you.")
            time.sleep(3)
            print(f"You return a month later, a new king has been chosen and a placard has been placed as a centerpiece to the town")
            time.sleep(1)
            print(f"You read it.")
            time.sleep(1)
            print(f'Dedicated to {self.character.name}: The brave warrior who took down Yharl.')
            time.sleep(3)
            self.enter_to_continue()
            print("THE END")
            time.sleep(5)
        else:
            print(f"It was a valiant effort; however, {self.character.name} was unable to complete their quest.")
            print("Another adventurer fallen victim to Yharl and his horde.")
            print("Game Over.")
        time.sleep(3)
        exit()

    # Press enter to continue
    def enter_to_continue(self) -> None:
        input("\n[ENTER]")

    # Clear screen (OS checking)
    def clear_screen(self):
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')

if __name__ == "__main__":
    game = Game()
    game.play()
