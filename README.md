# Tale Of Zombie Cove

A basic Text-Based adventure written in the Command Line via Python.

### How To Play

- Tale Of Zombie Cove is a command line DND-like text-based adventure game.
- You will start by inputting your name.
- You will be introduced to the game before entering the main game loop.
- To win the game, you must beat the boss, but it is recommended you bulk up before doing this.

#### Game Loop

- You are placed on a board, the key is as such
  - "[ P ]": Player
  - "[ ]": Explored Room
  - "[ - ]": Unexplored Empty Room
  - "[ + ]": Loot Room
  - "[ ! ]": Enemy Room
  - "[ X ]": Boss Room
- You are allowed the following moves
  - move: Move to a specific
    - When choosing move, you are left with a choice of direction. This will move you on the board accordingly
  - describe: Describe the current room's conditions. Purely informational/lore
  - heal: Heal your character to full. Beware, you are limited on your heals
  - item: Use an item (or just check your inventory)
- Start by moving around.
- ##### Loot Rooms
  - Upon entering this room, you will be given an item in your inventory
- ##### Enemy Rooms
  - Entering an enemy room puts you in combat immeditately (Explined in "Attack Loop" section)
- ##### Boss Room
  - Same premise as the Enemy rooms; however, defeating the boss will win you the game

#### Attack Loop

- When you enter an enemy room, you will immediately be placed into combat

- You will have the choice to either attack or use an item
  - You cannot flee combat
  - **You cannot heal regularly while being attacked**
    - You can, however, use items, such as healing potions
- Attacking
  - Attacking is pretty much automated, though in explaination it's pretty much similar to DND
  - Your player will roll 1 - 20. If your roll is higher than the armor class of your enemy, you will attack using your strength value
  - After attacking, if the enemy has not been defeated, you will be attacked the same way you attack
  - If the enemy is defeated, you will be given a chance to choose a stat to level up
  - If you are defeated, the game is over
- Items
  - Using an item does NOT give the enemy an opportunity to attack

### Installation

- Python3.10+ is REQUIRED for this application.
- Install the appropriate requirements via the requirements.txt file if present.

### Running

Use the python interpreter to run the application through the `game.py` file
Examples:

- `python game.py`
- `python3 game.py`
