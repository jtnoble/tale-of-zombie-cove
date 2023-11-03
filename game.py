import board_rooms, character, time, os

class Game():
    def __init__(self) -> None:
        self.location = [0][0]
        self.board = board_rooms.Board()
        self.character = character.Character(input("Input your name: "))
    
    def play(self) -> None:
        self.intro()

    def intro(self) -> None:
        os.system('clear')
        print("Zombie Cove:")
        time.sleep(1)
        print("Another castle once ruled by a monarchy of heroes gone to ruin.")
        print("It is known well not to tread lightly around these parts")
        print("The undead horde of past residents haunt the grounds, making for an impossible journey")
        print(f"You, {self.character.name}, are tasked with slaying the Boss Zombie: Yharl")
        print("May you survive, you shall be granted all wishes, but death is an outcome much more likely.\n")
        time.sleep(1)
        input("Press ENTER to continue...")
    
    def game_loop(self) -> None:
        while self.character.health > 0:
            self.board.show_board()

    def selection(self, _input: str) -> None:
        match _input.lower():
            case "move":
                _input = input("Which direction? [north, south, east, west]: ").lower()
                


if __name__ == "__main__":
    game = Game()
    game.play()
