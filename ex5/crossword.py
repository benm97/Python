#######################################################################
# FILE: crossword.py
# WRITERS: Rubens Valensi, rubensval, Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex5 2017-2018
# DESCRIPTION: Write in the output file all the word (from a list)
#              in a given matrix, in given directions
#######################################################################

import sys  # Used to get the arguments
import os.path  # Used to check files existence

EMPTY_STRING = ""
UP = 'u'
DOWN = 'd'
RIGHT = 'r'
LEFT = 'l'
GO_UP_RIGHT = 'w'
GO_UP_LEFT = 'x'
GO_DOWN_RIGHT = 'y'
GO_DOWN_LEFT = 'z'
LIST_DIRECTION = [UP, DOWN, RIGHT, LEFT,
                  GO_UP_RIGHT, GO_UP_LEFT, GO_DOWN_RIGHT, GO_DOWN_LEFT]
INCREASE = 1
NUMBER_OF_ARGUMENTS = 4
WORD_COUNT_SEPARATOR = ','
WORD_SEPARATOR = '\n'
WORDS_ARGUMENT_INDEX = 1
MATRIX_ARGUMENT_INDEX = 2
OUTPUT_ARGUMENT_INDEX = 3
DIRECTIONS_ARGUMENT_INDEX = 4


def invert(strings_list):
    """
    For a given list of strings, return the list of inverted strings
    :param strings_list: the list with strings to invert
    :return: list of inverted strings
    """
    inverted_list = []
    for string_letters in strings_list:
        inverted_list.append(string_letters[::-1])
    return inverted_list


def invert_matrix(matrix):
    """
    For a matrix, return the inverted matrix (line 1 became last line,...)
    :param matrix: the matrix to invert
    :return: inverted matrix
    """
    inverted_matrix = []
    for line_index in range(len(matrix) - 1, -1, -1):  # For each number
        # (descending) from the max index line
        # of the matrix (len-1) to 0 (included)

        # So beginning by the last line...
        inverted_matrix.append(matrix[line_index])  # Adding each line to
        # a new matrix
    return inverted_matrix


def up_down(matrix, direction):
    """
    
    :param matrix:
    :param direction:
    :return:
    """
    lst_strings = []
    width = len(matrix[0])
    height = len(matrix)
    for column in range(width):
        column_string = EMPTY_STRING
        for line in range(height):
            column_string += matrix[line][column]
        lst_strings.append(column_string)
    if direction == DOWN:
        return lst_strings
    elif direction == UP:
        return invert(lst_strings)


def right_left(matrix, direction):
    lst_strings = []
    width = len(matrix[0])
    height = len(matrix)
    for line in range(height):
        line_string = EMPTY_STRING
        for column in range(width):
            line_string += matrix[line][column]
        lst_strings.append(line_string)
    if direction == RIGHT:
        return lst_strings
    elif direction == LEFT:
        return invert(lst_strings)


def diagonals(matrix, direction):
    lst_strings = []
    width = len(matrix[0])
    height = len(matrix)
    for line in range(height):
        diagonal_string = EMPTY_STRING
        i = line
        j = 0
        while i < height and j < width:
            diagonal_string += matrix[i][j]
            j += INCREASE
            i += INCREASE
        lst_strings.append(diagonal_string)
    for column in range(1, width):
        diagonal_string = EMPTY_STRING
        i = 0
        j = column
        while i < height and j < width:
            diagonal_string += matrix[i][j]
            j += INCREASE
            i += INCREASE
        lst_strings.append(diagonal_string)
    if direction == GO_DOWN_RIGHT:
        return lst_strings
    elif direction == GO_UP_LEFT:
        return invert(lst_strings)


def symmetrical_diagonals(matrix, direction):
    if direction == GO_UP_RIGHT:
        return diagonals(invert_matrix(matrix), GO_DOWN_RIGHT)
    elif direction == GO_DOWN_LEFT:
        return invert(diagonals(invert_matrix(matrix), GO_DOWN_RIGHT))


def check_directions(string_direction, list_direction):
    invalid_directions = [letter for letter in string_direction if letter
                          not in list_direction]
    if not invalid_directions:
        return True
    else:
        return False


def direction_choice(matrix, direction):
    if direction == UP or direction == DOWN:
        return up_down(matrix, direction)
    elif direction == LEFT or direction == RIGHT:
        return right_left(matrix, direction)
    elif direction == GO_UP_LEFT or direction == GO_DOWN_RIGHT:
        return diagonals(matrix, direction)
    elif direction == GO_UP_RIGHT or direction == GO_DOWN_LEFT:
        return symmetrical_diagonals(matrix, direction)


def counting(word, string):
    counter = 0
    for i in range(len(string)):
        if word in string[i:len(word) + i]:
            counter += INCREASE
    return counter


def update_dictionary(word_list, lst_strings, max_size, results_count):
    for word in word_list:
        if len(word) <= max_size:
            for string in lst_strings:
                if len(word) <= len(string):
                    if string.count(word) != 0:
                        if word not in results_count:
                            results_count[word] = counting(word, string)
                        else:
                            results_count[word] += counting(word, string)
    return results_count


def write_in_order(dictionary_count, output_file):
    keys = sorted(dictionary_count.keys())
    for key in keys:
        to_write = key + WORD_COUNT_SEPARATOR + str(dictionary_count[key]) \
                   + WORD_SEPARATOR
        output_file.write(to_write)


def cross_word(word_file, matrix_file, output_file, directions):
    matrix = []
    for line in matrix_file:
        line = line.strip().lower()
        matrix.append(list(map(str, line.split(','))))
    word_list = [word_line.strip().lower() for word_line in word_file]

    width = len(matrix[0])
    height = len(matrix)

    results_count = dict()
    checked_directions = []
    for direction in directions:
        if direction not in checked_directions:
            checked_directions.append(direction)
            strings_list = direction_choice(matrix, direction)
            results_count = update_dictionary(word_list, strings_list,
                                              max(width, height),
                                              results_count)
    write_in_order(results_count, output_file)


if __name__ == "__main__":

    if len(sys.argv) == NUMBER_OF_ARGUMENTS + 1:
        if not os.path.isfile(sys.argv[WORDS_ARGUMENT_INDEX]):
            print("ERROR: Word file" + sys.argv[WORDS_ARGUMENT_INDEX]
                  + "does not exist.")
        elif not os.path.isfile(sys.argv[MATRIX_ARGUMENT_INDEX]):
            print("ERROR: Matrix file" + sys.argv[MATRIX_ARGUMENT_INDEX]
                  + "does not exist.")
        elif not check_directions(sys.argv[DIRECTIONS_ARGUMENT_INDEX],
                                  LIST_DIRECTION):
            print("ERROR: invalid directions.")
        else:
            cross_word(open(sys.argv[WORDS_ARGUMENT_INDEX], 'r'),
                       open(sys.argv[MATRIX_ARGUMENT_INDEX], 'r'),
                       open(sys.argv[OUTPUT_ARGUMENT_INDEX], 'w'),
                       sys.argv[DIRECTIONS_ARGUMENT_INDEX])
    else:
        print("ERROR: invalid number of parameters."
              " Please enter word_file matrix_file output_file directions.")

