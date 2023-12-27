#!/bin/python
import random
import copy

# Game randomly choose the first player and assigngs character X or 0
# This is Milestone Project 1 for Udemy's
# "The Complete Python Bootcamp From Zero to Hero in Python"


def first_move():
    # Function to randomly select player who will make a first move
    first_mover = random.randrange(1, 3)
    print(f"First move should be made by Player {first_mover}", first_mover)
    return first_mover


def player_flip(player: int) -> int:
    # Function takes accepts int var:first_mover and flips it between value 1
    #  and 2 on each call
    if player == 1:
        globals()["who_moves"] = 2
    else:
        globals()["who_moves"] = 1
    globals()["game_msg"] = ""
    globals()["next_move"] = True
    return who_moves


def print_line():
    print(
        """
===================================================================================
          """
    )


def info():
    # Function to print information about how you should select where to place your symbol
    print(
        """
===================================================================================
The index map keys that user can select to place X or O are looking like this:
-------
1|2|3
4|5|6
7|8|9
-------
Player1 plays with: X
Player2 plays with: 0
===================================================================================
          """
    )


game_on: bool = False  # set if game should proceed or not

board = {
    0: "   |   |   ",
    1: "___|___|___",
    2: "   |   |   ",
    3: "___|___|___",
    4: "   |   |   ",
    5: "   |   |   ",
}


def player_symbol(player: int):
    # Function returns player symbol
    symbols = {1: "X", 2: "0"}
    return symbols[player]


def validate_userinput():
    # Ask user for input and validate that it is number from 1 to 9
    position = "WRONG"
    allowed_range = range(0, 10)
    while position.isdigit() is False:
        position = input(
            """ Please select field position(should be a number from 1 to 9, or press 'q' to quit game): """
        )
        if position.isdigit() is False:
            if position == "q":
                print_line()
                print("You pressed 'q', exiting game...")
                exit()
            else:
                print("What you've entered is not a number or letter 'q' !")
        elif int(position) not in allowed_range:
            userinput = position
            position = "STILL WRONG"
            print(
                f"Your number should be in range of 1 to 9, you've entered {userinput} ", userinput
            )
    return int(position)


def row_switcher(position: int):
    # Function to select correct row to update, based on position passed into it
    row_to_update = {}
    if position >= 1 and position <= 3:
        row_to_update[1] = board[1]
    elif position >= 4 and position <= 6:
        row_to_update[3] = board[3]
    elif position >= 7 and position <= 9:
        row_to_update[5] = board[5]
    return row_to_update


def check_occupied(row_element: list):
    if row_element not in ["X", "0"]:
        return True
    else:
        return False


def position_update(row: list, position: int, symbol: list):
    # Updates position in the list var:row according to int var:position passed into
    # returns the new row with var:symbol set in var:position according to tic tac toe board map
    first_cell = [1, 4, 7]
    second_cell = [2, 5, 8]
    third_cell = [3, 6, 9]
    updated_row = copy.deepcopy(row)
    if position in first_cell:
        # we are checking index - 1/5/9 because all "real" game symbols in first_cell (first column really)
        # have index 1, _x_|__|__ example of how "row" variable value looks like inside, so x here have index of 1.
        if check_occupied(updated_row[1]):
            updated_row[1] = symbol
            globals()["next_move"] = True
        else:
            globals()["game_msg"] = "Position is occupied, check another one"
            globals()["next_move"] = False
            # print(f'Position is occupied, check another one')
    elif position in second_cell:
        # we are checking index - 1/5/9 because all "real" game symbols in first_cell (first column really)
        # have index 1, _x_|__|__ example of how "row" variable value looks like inside, so x here have index of 1.
        if check_occupied(updated_row[5]):
            updated_row[5] = symbol
            globals()["next_move"] = True
        else:
            globals()["game_msg"] = "Position is occupied, check another one"
            globals()["next_move"] = False
    elif position in third_cell:
        # we are checking index - 1 because all "real" game symbols in first_cell (first column really)
        # have index 1, _x_|__|__ example of how "row" variable value looks like inside, so x here have index of 1.
        if check_occupied(updated_row[9]):
            updated_row[9] = symbol
            globals()["next_move"] = True
        else:
            globals()["game_msg"] = "Position is occupied, check another one"
            globals()["next_move"] = False
    else:
        globals()["game_msg"] = "Incorrect position"
        print("Incorrect position")
    return updated_row


def row_update(position: int, symbol: list):
    # Function to update row of the filed with a user input position and user's symbol (X/0)
    for key, value in row_switcher(position).items():
        row_to_update = key
        row = value
    row_intolist = [item for item in row]
    row_new = "".join(position_update(row_intolist, position, symbol))
    board[row_to_update] = row_new
    print("New row:", row_new)
    return


def check_win():
    check_matrix = []  # keep list of lists or matrix of the board
    row_with_symbol = [1, 3, 5]
    for key in row_with_symbol:
        arr_row = []

        # Copy row that we are checking, substitute all empty positions where we are potentially can place X or 0 symbols with "Z",
        # so later in step with .translate() it will not be substituted with None, and we will preserve correct empty positions index.
        row_copy_list = list(copy.deepcopy(board[key]))
        index_with_symbol = [1, 5, 9]

        for index in index_with_symbol:
            if row_copy_list[index] == "_":
                row_copy_list[index] = "Z"
            elif row_copy_list[index] == " ":
                row_copy_list[index] = "Z"

        row_copy_str = "".join(row_copy_list)
        arr_row.extend(
            row_copy_str.translate({ord(i): None for i in "_| "})
        )  # removes pretty chars from list

        if len(arr_row) != 0:
            check_matrix.append(arr_row)
        arr_row = []
    check_horizontal_win(check_matrix, player_symbol(who_moves))
    check_vertical_win(check_matrix, player_symbol(who_moves))
    check_diagonal_win(check_matrix, player_symbol(who_moves))


def check_horizontal_win(
    check_matrix, symbol: list
):  # called inside check_win() function
    # for i in range(len(check_matrix[0])):
    for i in range(len(check_matrix[0])):
        try:
            if list(check_matrix[i]).count(symbol) == 3:
                print(symbol, "Won")
                show_gamefield(board, who_moves)
                globals()["game_on"] = False
        except IndexError:
            continue


def check_vertical_win(
    check_matrix, symbol: list
):  # called inside check_win() function
    for col in range(3):
        try:
            column_chars = [check_matrix[row][col] for row in range(3)]
            if column_chars.count(symbol) == 3:
                print(symbol, "Won")
                show_gamefield(board, who_moves)
                globals()["game_on"] = False
        except IndexError:
            continue


def check_diagonal_win(
    check_matrix, symbol: list
):  # called inside check_win() function
    __diagonal_chars = []
    __reverse_diagonal_chars = []
    for diagonal in range(len(check_matrix)):
        __diagonal_chars.append(check_matrix[diagonal][diagonal])
        __reverse_diagonal_chars.append(
            check_matrix[diagonal][len(check_matrix) - 1 - diagonal]
        )
        if __diagonal_chars.count(symbol) == 3:
            print(symbol, "Won")
            show_gamefield(board, who_moves)
            globals()["game_on"] = False
        elif __reverse_diagonal_chars.count(symbol) == 3:
            print(symbol, "Won")
            show_gamefield(board, who_moves)
            globals()["game_on"] = False


def check_line(board: dict):
    return board.values()


def show_gamefield(board: dict, who_moves: int):
    # Function to show current gameboard
    # print(f'Game message:', globals()["game_msg"] )
    if game_msg != "":
        print(game_msg)
    print("Current situation is:")
    print("======================")
    for key, value in board.items():
        print(value)
    print("Player that moves now is:", who_moves)
    print("======================")


def next_move_check():
    if next_move is True:
        return True
    else:
        return False


game_on = True
who_moves = first_move()
next_move = True
game_msg = ""


if __name__ == "__main__":
    while game_on:
        info()
        # os.system('clear')
        show_gamefield(board, who_moves)
        row_update(validate_userinput(), player_symbol(who_moves))
        check_win()
        if next_move_check():
            player_flip(who_moves)
