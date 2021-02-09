import ex6_helper
import math
import copy
import sys

INCREASE = 1
MEAN_COEF = -1 / 8
BLACK = 0
WHITE = 255
MINIMAL_THRESHOLD = 0
MAXIMAL_THRESHOLD = 256
FILTER_SIZE = 9
NUMBER_OF_NEIGHBORS = 9
ITSELF_NEIGHBOR_INDEX = 4
DOWNSAMPLE_GAP = 3
ROW_INDEX = 0
COLUMN_INDEX = 1
LAST_MEMBER_INDEX = -1
MAX_DOUBLE_LINE_ANGLE = math.pi / 2
MAX_ANGLE = 180
LIMIT_ANGLE = 90
IMAGE_ARGUMENT = 1
OUTPUT_ARGUMENT = 2
DIAGONAL_ARGUMENT = 3
NUMBER_OF_ARGUMENTS = 4


def otsu(image):
    """
    Finding the best threshold value for an image
    :param image: image to work on
    :return: optimal threshold value
    """

    # Initialising
    max_intra_variance, optimal_threshold = 0, 0

    # Running on every potential threshold, compute the intra-variance for
    # it and keeping the one with the max one
    for threshold in range(MINIMAL_THRESHOLD, MAXIMAL_THRESHOLD):
        black, white, sum_black, sum_white, mean_black, mean_white = 0, 0, 0, \
                                                                     0, 0, 0
        # For each pixel
        for row in range(len(image)):
            for column in range(len(image[0])):

                # Under the threshold, it's black
                if image[row][column] < threshold:
                    black += INCREASE
                    sum_black += image[row][column]
                # Over the threshold, it's black
                else:
                    white += INCREASE
                    sum_white += image[row][column]
        # Compute means
        if black != 0:
            mean_black = sum_black / black
        if white != 0:
            mean_white = sum_white / white

        # Compute intra-variance
        intra_variance = black * white * (mean_black - mean_white) ** 2

        # If it superior to the precedent max
        if intra_variance > max_intra_variance:
            # Saving intra_variance and threshold
            max_intra_variance = intra_variance
            optimal_threshold = threshold
    return optimal_threshold


def threshold_filter(image):
    """
    Transform a grey scale image to black and white, with the optimal threshold
    :param image: image to work on
    :return: black and with image
    """

    new_image = []
    optimal_threshold = otsu(image)  # Obtain the best threshold for this image

    # For each pixel
    for row in range(len(image)):
        new_row = []
        for column in range(len(image[0])):

            if image[row][column] < optimal_threshold:  # Under the threshold
                new_row.append(BLACK)  # Replace by black in the new image
            else:  # Over the threshold
                new_row.append(WHITE)  # Replace by white in the new image
        new_image.append(new_row)
    return new_image


def get_pixel_neighbors(matrix, row, column):
    """
    Function to get all the neighbors of a pixel in a given matrix
    :param matrix: the matrix (image) from it we want to extract neighbors
    :param row: row index of the pixel
    :param column: column index of the pixel
    :return: a list of the neighbors (including the pixel itself)
    """

    width = len(matrix[0])
    height = len(matrix)
    neighbors_list = []

    for i in range(-1, 2):  # For the row of our pixel,
        # the one before and the one after
        for j in range(-1, 2):  # For the column of our pixel,
            # the one before and the one after

            if height > row + i >= 0 and width > column + j >= 0:  # If we are
                # on an existent pixel
                neighbors_list.append(matrix[row + i][column + j])
            else:  # If we are out of the image
                neighbors_list.append(matrix[row][column])  # Adding the
                # pixel itself
    return neighbors_list


def matrix_to_list(matrix):
    """
    A function to transform a list of list to a linear list, row after row
    :param matrix: the list of list
    :return: linear list
    """

    linear_list = []
    for row in matrix:
        for letter in row:
            linear_list.append(letter)
    return linear_list


def apply_filter(image, filter):
    """
    Applying a 3*3 matrix filter to an image
    :param image: image to apply filter on it
    :param filter: 3*3 matrix
    :return: modified image
    """

    filter_list = matrix_to_list(filter)  # Getting the list of the pixel
    # from the filter
    new_image = []

    # For each pixel of the image
    for row in range(len(image)):
        new_row = []
        for column in range(len(image[0])):
            new_pixel = 0
            neighbors_list = get_pixel_neighbors(image, row, column)  # Getting
            #  his neighbors

            for neighbor_index in range(0, FILTER_SIZE):  # For each neighbor
                # Adding his 'contribution' to the new pixel ( multiplied by
                # the corresponding pixel on the filter)
                new_pixel += filter_list[neighbor_index] * neighbors_list[
                    neighbor_index]

            new_pixel = math.floor(math.fabs(new_pixel))  # Keeping entire part
            # only

            # If the new pixel over 255 adding 255 at his place
            if new_pixel <= WHITE:
                new_row.append(new_pixel)
            else:
                new_row.append(WHITE)
        new_image.append(new_row)
    return new_image


def detect_edges(image):
    """
    Returns an image with edges in white
    :param image: image to work on
    :return: modified image
    """
    new_image = []

    # For each pixel of the image
    for row in range(len(image)):
        new_row = []
        for column in range(len(image[0])):
            neighbors_list = get_pixel_neighbors(image, row, column)  # Get the
            #  list of neighbors of this pixel
            neighbors_sum = 0
            # Adding all neighbors excluding the pixel itself
            for neighbor_index in range(NUMBER_OF_NEIGHBORS):
                if neighbor_index != ITSELF_NEIGHBOR_INDEX:
                    neighbors_sum += neighbors_list[neighbor_index]
            # Creating a new pixel equal to the pixel minus
            # the mean of neighbors
            new_pixel = math.floor(
                math.fabs(image[row][column] - neighbors_sum / 8))
            new_row.append(new_pixel)
        new_image.append(new_row)
    return new_image


def downsample_by_3(image):
    """
    Dividing the diagonal size of an image by 3
    :param image: image to reduce
    :return: reduced image
    """
    new_image = []

    for row in range(1, len(image), DOWNSAMPLE_GAP):  # For one row between 3
        new_row = []
        for column in range(1, len(image[0]), DOWNSAMPLE_GAP):  # For one
            # column between 3
            neighbors_list = get_pixel_neighbors(image, row, column)  # Getting
            #  neighbors
            neighbors_sum = 0
            # Adding a new pixel equal to rhe mean of the 9 neighbors
            for neighbor_index in range(NUMBER_OF_NEIGHBORS):
                neighbors_sum += neighbors_list[neighbor_index]
            new_pixel = math.floor(neighbors_sum / NUMBER_OF_NEIGHBORS)
            new_row.append(new_pixel)
        new_image.append(new_row)
    return new_image


def get_diagonal_size(matrix):
    """
    Get the diagonal size of a matrix
    :param matrix: the matrix
    :return: diagonal size
    """
    # Compute it with Pythagoras theorem
    return math.sqrt(len(matrix) ** 2 + len(matrix[0]) ** 2)


def downsample(image, max_diagonal_size):
    """
    Reducing an image under a given diagonal size
    :param image: imagee to reduce
    :param max_diagonal_size: max wanted diagonal
    :return: 
    """
    diagonal_size = get_diagonal_size(image)
    new_image = copy.deepcopy(image)
    # Reduce by 3 until we get under the wanted diagonal sizz
    while diagonal_size > max_diagonal_size:
        new_image = downsample_by_3(new_image)
        diagonal_size = get_diagonal_size(new_image)

    return new_image


def get_distance(row1, column1, row2, column2):
    """
    Getting the distance between 2 points
    :param row1: first point row
    :param column1: first point column
    :param row2: second point row
    :param column2: second point column
    :return: distance
    """
    return math.sqrt((row1 - row2) ** 2 + (column1 - column2) ** 2)


def rating_line(image, angle, distance, top):
    """
    For a given line, giving the rate of this line
    :param image: image to work on
    :param angle: angle of the tested line
    :param distance: distance of the line
    :param top: true or false
    :return: the rate (the size of each blank line in the line power 2)
    """

    # Getting the pixels of the line
    line = ex6_helper.pixels_on_line(image, angle, distance, top)

    blank_line = []
    line_rate = 0

    # Getting the first blank pixel in blank_line (to be able to compare in
    # any cases after that)
    for i in range(len(line)):
        if image[line[i][ROW_INDEX]][line[i][COLUMN_INDEX]] == WHITE:
            blank_line.append(line[i])
            break

    # For each white pixel
    for index_line in range(len(line)):
        if image[line[index_line][ROW_INDEX]][
            line[index_line][COLUMN_INDEX]] == WHITE:
            # If it's close in off to the last blank pixel
            if get_distance(
                    blank_line[LAST_MEMBER_INDEX][ROW_INDEX],
                    blank_line[LAST_MEMBER_INDEX][COLUMN_INDEX],
                    line[index_line][ROW_INDEX],
                    line[index_line][COLUMN_INDEX]) <= 2:
                # Adding it to the list
                blank_line.append(line[index_line])
            else:  # But if the distance is too big, that's mean we ended a 
                # blank line

                # So, adding the rate of the actual blank segment to line_rate
                line_rate += (get_distance(blank_line[0][ROW_INDEX],
                                           blank_line[0][COLUMN_INDEX],
                                           blank_line[len(blank_line) - 1][
                                               ROW_INDEX],
                                           blank_line[len(blank_line) - 1][
                                               COLUMN_INDEX])) ** 2
                blank_line = []
                # Adding the actual pixel for the next segment
                blank_line.append(line[index_line])

    if blank_line:  # If something still in blank_line

        # Adding it's rate to line_rate
        line_rate += (get_distance(blank_line[0][ROW_INDEX],
                                   blank_line[0][COLUMN_INDEX],
                                   blank_line[len(blank_line) - 1][ROW_INDEX],
                                   blank_line[len(blank_line) - 1][
                                       COLUMN_INDEX])) ** 2

    return line_rate


def rating_angle(image, angle):
    """
    Running on all the line of an angle and getting the angle rate
    :param image: image to work on
    :param angle: angle to test
    :return: rating of the angle
    """
    angle_rate = 0
    for distance in range(int(get_diagonal_size(image))):  # For each distance 
        # under diagonal size
        angle_rate += rating_line(image, angle, distance, top=True)

        # For some angle, a second line corresponds
        if 0 < angle < MAX_DOUBLE_LINE_ANGLE:
            angle_rate += rating_line(image, angle, distance, top=False)

    return angle_rate


def get_angle(image):
    """
    Getting the dominant angle of an image
    :param image: the image
    :return: dominant angle
    """
    image=threshold_filter(image)
    dominant_angle_rate = 0
    dominant_angle = 0
    # For each angle
    for angle in range(0, MAX_ANGLE):
        angle_rate = rating_angle(image, math.radians(angle))  # Get the
        # rate of the angle

        # Keeping only the highest
        if angle_rate > dominant_angle_rate:
            dominant_angle_rate = angle_rate
            dominant_angle = angle
    #print(dominant_angle)
    return dominant_angle


def rotate(image, angle):
    """
    Rotate image in a given angle
    :param image: the image
    :param angle: angle to rotate
    :return: rotated image
    """

    # Computing the size of the new image (under -90 or over 90 height and
    # width inverted)
    if angle >= -LIMIT_ANGLE and angle <= LIMIT_ANGLE:
        new_image_width = int(
            math.cos(math.radians(math.fabs(angle))) * len(
                image[0]) + math.sin(
                math.radians(math.fabs(angle))) * len(image))
        new_image_height = int(
            math.sin(math.radians(math.fabs(angle))) * len(
                image[0]) + math.cos(
                math.radians(math.fabs(angle))) * len(image))
    else:
        new_image_width = int(
            math.cos(math.radians(math.fabs(angle) - LIMIT_ANGLE)) * len(
                image) + math.sin(
                math.radians(math.fabs(angle) - LIMIT_ANGLE)) * len(image[0]))
        new_image_height = int(
            math.sin(math.radians(math.fabs(angle) - LIMIT_ANGLE)) * len(
                image) + math.cos(
                math.radians(math.fabs(angle) - LIMIT_ANGLE)) * len(image[0]))

    new_image = []
    # For each pixel of the new image
    for row in range(new_image_height):
        new_row = []
        for column in range(new_image_width):

            # Putting the center to (0,0)
            x = column - new_image_width / 2
            y = row - new_image_height / 2

            # Getting the position of the correspinding pixel in the original
            # image
            original_column = int(
                x * math.cos(math.radians(angle)) + y * math.sin(
                    math.radians(angle)) + len(image[0]) / 2)
            original_row = int(
                -x * math.sin(math.radians(angle)) + y * math.cos(
                    math.radians(angle)) + len(image) / 2)

            # If the originals row column actually inside of the original image
            if original_row < len(image) and original_row >= 0 and \
                            original_column < len(image[0]) \
                    and original_column >= 0:

                # Copying it
                new_row.append(image[original_row][original_column])
            else:  # If we are not in the limit of the original
                new_row.append(0)
        new_image.append(new_row)  # Adding a black pixel
    return new_image


def make_correction(image, max_diagonal):
    """
    Detects the dominant angle of an image and rotate it in the opposite angle
    :param image: image to correct
    :param max_diagonal: diagonal used to work on the image
    :return: corrected image
    """
    new_image = threshold_filter(detect_edges(
        threshold_filter(downsample(image, float(max_diagonal)))))
    dominant_angle = get_angle(new_image)
    return rotate(image, -dominant_angle)

image3=ex6_helper.load_image('lines001_thresh_downsampled.jpg')
print(get_angle(image3))

# Getting the parameters from the console
if __name__ == '__main__':
    if len(sys.argv) != NUMBER_OF_ARGUMENTS:
        print(
            "Wrong number of parameters. The correct usage is: "
            "ex6.py <image_source> <output> <max_diagonal>")
    else:
        # Saving corrected image
        ex6_helper.save(
            make_correction(ex6_helper.load_image(sys.argv[IMAGE_ARGUMENT]),
                            sys.argv[DIAGONAL_ARGUMENT]),
            sys.argv[OUTPUT_ARGUMENT])
