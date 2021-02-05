"""
This module contains the scyscrapers game and checks whether the board has a winning combination.

Github link: https://github.com/oliuba/lab0_skyscrapers
"""


def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("check.txt")
    ['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    with open(path) as board:
        board_lines = [line.strip() for line in board]
    return board_lines


def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    for index in range(1, pivot):
        if int(input_line[index]) > int(input_line[pivot]):
            return False
    return True


def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', \
    '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', \
    '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', \
    '*41532*', '*2*1***'])
    False
    """
    for line in board:
        if '?' in line:
            return False
    return True


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', \
        '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', \
        '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', \
        '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board:
        line = line[1:-1]
        only_numbers =  line.replace('*', '')
        if len(only_numbers) != len(set(only_numbers)):
            return False
    return True


def check_horizontal_visibility(board: list) -> bool:
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*', \
        '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*', \
        '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*', \
        '*41532*', '*2*1***'])
    False
    """
    for line in board:
        left_hint = line[0]
        right_hint = line[-1]
        if left_hint.isdigit():
            seen_buildings = 0
            for pivot in range(1, len(line) - 1):
                if left_to_right_check(line, pivot):
                    seen_buildings += 1
            if int(left_hint) != seen_buildings:
                return False
        if right_hint.isdigit():
            seen_buildings = 0
            for pivot in range(1, len(line) - 1):
                if left_to_right_check(line[::-1], pivot):
                    seen_buildings += 1
            if int(right_hint) != seen_buildings:
                return False
    return True


def check_columns(board: list) -> bool:
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height)
    and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    vertical_lines = ['' for _ in range(len(board))]
    for ind, _ in enumerate(board):
        vertical = ''
        for line in board:
            vertical += line[ind]
        vertical_lines[ind] = vertical
    return check_horizontal_visibility(vertical_lines)


def check_skyscrapers(input_path: str) -> bool:
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """
    board = read_input(input_path)
    return check_not_finished_board(board) and check_uniqueness_in_rows(board) and \
        check_horizontal_visibility(board) and check_columns(board)


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
