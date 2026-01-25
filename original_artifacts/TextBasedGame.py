"""
Jason Fuller
Project 2
"""

ROOMS = {'Space Room':
         {'item': 'Blue Stone', 'South': 'Reality Room', 'East': 'Avengers Campus'},
         'Avengers Campus':
         {'item': '', 'South': 'Power Room', 'East': 'Mind Room', 'West': 'Space Room'},
         'Mind Room':
         {'item': 'Yellow Stone', 'South': 'Time Room', 'West': 'Avengers Campus'},
         'Reality Room':
         {'item': 'Red Stone', 'North': 'Space Room', 'South': 'Soul Room', 'East': 'Power Room'},
         'Power Room':
         {'item': 'Purple Stone', 'North': 'Avengers Campus', 'East': 'Time Room', 'West': 'Reality Room'},
         'Time Room':
         {'item': 'Green Stone', 'North': 'Mind Room', 'South': 'Avengers Compound', 'West': 'Power Room'},
         'Soul Room':
         {'item': 'Orange Stone', 'North': 'Reality Room'},
         'Avengers Compound':
         {'item': 'Villain', 'North': 'Time Room'}}

ITEMS = {v for v in {v['item'] for k, v in ROOMS.items() if v} if v != '' and v != 'Villain'}
DIRECTIONS = ['North', 'South', 'East', 'West']
NAVIGATE_COMMAND = 'go '
VALID_MOVE_COMMANDS = [NAVIGATE_COMMAND + direction for direction in DIRECTIONS]
ITEM_COMMAND = 'get '
VALID_ITEM_COMMANDS = [ITEM_COMMAND + stone for stone in ITEMS]
INVALID_DIRECTION = "Invalid direction. Direction need to be one of: " + str(DIRECTIONS)
INVALID_COMMAND = "Invalid command."
UNKNOWN_COMMAND = "Unhandled command."
CANNOT_GO_THAT_WAY = "You bumped into a wall."
INVALID_ITEM = "Invalid item."
ITEM_NOT_FOUND = "Item not found."
GAME_OVER = "Thanks for playing."
VILLAIN_ROOM_NAME = "Villain"
INPUT_PROMPT = "Enter your command:"
ALREADY_HAVE_ITEM = "You already have this item."


def get_new_state(current_room: str, user_input: str):
    """
    Given a current_room in rooms and a user_input, return a tuple (next_room, err_msg) with
    next_room -- where you are after
    err_msg -- message to print, if any, empty, GAME_OVER, INVALID_DIRECTION, or CANNOT_GO_THAT_WAY
    """
    next_room = current_room
    err_msg = ''

    if user_input in DIRECTIONS:
        if user_input in ROOMS[current_room]:
            next_room = ROOMS[current_room][user_input]
        else:
            err_msg = CANNOT_GO_THAT_WAY
    else:
        err_msg = INVALID_DIRECTION

    return next_room, err_msg


def get_new_item(current_room: str, user_item: str):
    """
    Given a current_room in rooms and a user_item from player input, return a tuple (new_item, err_msg) with
    new_item -- where you are after
    err_msg -- message to print, if any, empty, ITEM_NOT_FOUND, INVALID_ITEM
    """
    new_item = user_item
    err_msg = ''

    if user_item in ITEMS:
        if user_item in ROOMS[current_room]['item']:
            new_item = ROOMS[current_room]['item']
        else:
            err_msg = ITEM_NOT_FOUND
    else:
        err_msg = INVALID_ITEM

    return new_item, err_msg


def handle_villain(inventory: list):
    """
    Villain room found. Determine win/loss and output to player.
    """

    if len(inventory) == len(ITEMS):  # Check if the player has all the stones.
        print('You have found Thanos! Since you have all the stones, you WIN!')
    else:
        print("You have found Thanos! You do not have all the stones. You have been eliminated!!")


def show_status(current_room: str, inventory: list):
    """
    Given a current_room, output the status so the player knows where they are.
    """
    print('You are in the {}'.format(current_room))
    print('User inventory: ' + str(inventory))
    if ROOMS[current_room]['item'] != '':
        if ROOMS[current_room]['item'] not in inventory:
            print('You see the {}'.format(ROOMS[current_room]['item']))
    print('-' * 30)


def show_instructions():
    """
    This function outputs the game intro, rules, and commands.
    """
    print('Avengers Stone Collector Game')
    print('')
    print('Collect 6 stones before finding Thanos to win the game, or be eliminated.')
    print('Valid move commands: ' + str(VALID_MOVE_COMMANDS))
    print('Valid item commands: ' + str(VALID_ITEM_COMMANDS))


def main(start_room: str):
    """
    Given a start_room, loop indefinitely until the player enters EXIT_COMMAND.
    """
    game_over_sentinel = False
    current_room = start_room
    player_inventory = []

    while not game_over_sentinel:
        show_status(current_room, player_inventory)  # Show player current status.
        user_input = input(INPUT_PROMPT)  # Prompt for input.

        if user_input in VALID_MOVE_COMMANDS:  # Check for a valid move command by checking VALID_MOVE_COMMANDS.
            if user_input[0:len(NAVIGATE_COMMAND)] == NAVIGATE_COMMAND:  # Check player input for move command.
                result = get_new_state(current_room, user_input[len(NAVIGATE_COMMAND):])  # Get return of get_new_state.
                if result[1] == "":  # Check for errors.
                    current_room = result[0]  # Set the current room to the move result.

                    if ROOMS[current_room]['item'] == VILLAIN_ROOM_NAME:  # Check if the new room is the villain room.
                        handle_villain(player_inventory)  # Handle the villain room.
                        game_over_sentinel = True  # Set to GAME_OVER_SENTINEL so the game loop ends.
                else:
                    print(result[1])  # Output move result error message.
            else:
                print(UNKNOWN_COMMAND)  # Output unknown command error message.
        elif user_input in VALID_ITEM_COMMANDS:  # Check for a valid item command by checking VALID_ITEM_COMMANDS
            if user_input[0:len(ITEM_COMMAND)] == ITEM_COMMAND:  # Check player input for item command.
                if user_input[len(ITEM_COMMAND):] in player_inventory:  # Check if the player already has item.
                    print(ALREADY_HAVE_ITEM)  # Output that the player already has this item.
                else:
                    result = get_new_item(current_room, user_input[len(ITEM_COMMAND):])  # Get return of get_new_item.
                    if result[1] == "":  # Check for errors.
                        player_inventory += [result[0]]  # Add item to player inventory.
                    else:
                        print(result[1])  # Output error collecting item.
            else:
                print(UNKNOWN_COMMAND)  # Output unknown command error message.
        else:
            print(INVALID_COMMAND)  # Output invalid command error message.


"""
This is the primary code block after data and functions.
"""
show_instructions()  # Run the function to output the game header which includes instructions.
main('Avengers Campus')  # Start the gameplay loop by passing the starting room.
print(GAME_OVER)  # Output game over message.
