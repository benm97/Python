import sys
import os.path
import crossword

NUMBER_OF_ARGUMENTS = 4
DEPTH_DIRECTION = 'a'
LENGTH_DIRECTION = 'b'
WIDTH_DIRECTION = 'c'
MATRIX_SEPARATOR = '***'
LIST_DIRECTION = [DEPTH_DIRECTION, LENGTH_DIRECTION, WIDTH_DIRECTION]
WORDS_ARGUMENT_INDEX = 1
MATRIX_ARGUMENT_INDEX = 2
OUTPUT_ARGUMENT_INDEX = 3
DIRECTIONS_ARGUMENT_INDEX = 4


def to_length(matrix_3d):
    length_matrix_3d = []
    for j in range(len(matrix_3d[0])):
        matrix_2d = []
        for i in range(len(matrix_3d)):
            matrix_2d.append(matrix_3d[i][j])
        length_matrix_3d.append(matrix_2d)
    return length_matrix_3d


def to_width(matrix_3d):
    width_matrix_3d = []
    for k in range(len(matrix_3d[0][0])):
        matrix_2d = []
        for i in range(len(matrix_3d)):
            matrix_line = []
            for j in range(len(matrix_3d[0])):
                matrix_line.append(matrix_3d[i][j][k])
            matrix_2d.append(matrix_line)
        width_matrix_3d.append(matrix_2d)
    return width_matrix_3d


def direction_choice_3d(matrix_3d, direction):
    if direction == DEPTH_DIRECTION:
        return matrix_3d
    elif direction == LENGTH_DIRECTION:
        return to_length(matrix_3d)
    elif direction == WIDTH_DIRECTION:
        return to_width(matrix_3d)


def cross_word_3d(word_file, matrix_file, output_file, directions):
    word_list = [word_line.strip().lower() for word_line in word_file]
    matrix_3d = []
    temp_matrix_2d = []
    for line in matrix_file:
        line = line.strip().lower()
        if line != MATRIX_SEPARATOR:
            temp_matrix_2d.append(list(map(str, line.split(','))))
        else:
            matrix_3d.append(temp_matrix_2d)
            temp_matrix_2d = []
    matrix_3d.append(temp_matrix_2d)

    checked_directions = []
    results_count = dict()
    width = len(temp_matrix_2d[0][0])
    height = len(temp_matrix_2d[0])
    for direction in directions:
        if direction not in checked_directions:
            checked_directions.append(direction)
            ordered_matrix = direction_choice_3d(matrix_3d, direction)
            for matrix_2d in ordered_matrix:
                for direction_2d in crossword.LIST_DIRECTION:
                    strings_list = crossword.direction_choice(matrix_2d,
                                                              direction_2d)
                    results_count = crossword.update_dictionary(word_list,
                                                                strings_list,
                                                                max(width,
                                                                    height)
                                                                ,
                                                                results_count)

    crossword.write_in_order(results_count, output_file)


if __name__ == "__main__":

    if len(sys.argv) == NUMBER_OF_ARGUMENTS + 1:
        if not os.path.isfile(sys.argv[WORDS_ARGUMENT_INDEX]):
            print("ERROR: Word file" + sys.argv[WORDS_ARGUMENT_INDEX]
                  + "does not exist.")
        elif not os.path.isfile(sys.argv[MATRIX_ARGUMENT_INDEX]):
            print("ERROR: Matrix file" + sys.argv[MATRIX_ARGUMENT_INDEX]
                  + "does not exist.")
        elif not crossword.check_directions(
                sys.argv[DIRECTIONS_ARGUMENT_INDEX],
                LIST_DIRECTION):
            print("ERROR: invalid directions.")
        else:
            cross_word_3d(open(sys.argv[WORDS_ARGUMENT_INDEX], 'r'),
                          open(sys.argv[MATRIX_ARGUMENT_INDEX], 'r'),
                          open(sys.argv[OUTPUT_ARGUMENT_INDEX], 'w'),
                          sys.argv[DIRECTIONS_ARGUMENT_INDEX])
    else:
        print("ERROR: invalid number of parameters."
              " Please enter word_file matrix_file output_file directions.")
