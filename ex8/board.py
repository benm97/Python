############################################################
# Imports
############################################################
import game_helper as gh
from car import Direction

############################################################
# Constants
############################################################
MSG_SUCCESS = 'A car was added successfully!'
MSG_FAIL = 'Error! Car not added'
MSG_NOT_AVAILABLE = 'Destination not available'
EDGE_SHIFT = 1
DEFAULT_SIZE = 6
AVAILABLE_SYMBOL = '_'
EXIT_SYMBOL = 'E'
RED_CAR_SYMBOL = 'R'

############################################################
# Class definition
############################################################


class Board:
    """
    A class representing a rush hour board.
    """

    def __init__(self, cars, exit_board, size=DEFAULT_SIZE):
        """
        Initialize a new Board object.
        :param cars: A list (@or dictionary) of cars. @can be empty
        :param size: Size of board (Default size is 6). 
        """
        self.cars = cars
        self.exit_board = exit_board
        self.size = size

    def __is_in(self, location):
        """
        Telling if a location actually in the table game
        :param location: location to check
        :return: True if is in, False else
        """
        return (0 <= location[0] <= self.size - EDGE_SHIFT and 0 <= location[
            1] <= self.size - EDGE_SHIFT)

    def add_car(self, car):
        """
        Add a single car to the board.
        :param car: A car object
        :return: True if a car was successfully added, or False otherwise.
        """

        # Checking if all the locations that the new car want to take are
        # available
        available = True
        for location in car.list_location():
            if not self.__is_empty(location):
                available = False
            if not self.__is_in(location):
                available = False
        if available:
            self.cars.append(car)  # Adding the car
            if car.color != RED_CAR_SYMBOL:  # Do not display the message if
                # it's the red car
                gh.report(MSG_SUCCESS)
        else:
            gh.report(MSG_FAIL)
        return available

    def __is_empty(self, location):
        """
        Check if a given location on the board is free.
        :param location: x and y coordinations of location to be check
        :return: True if location is free, False otherwise
        """
        # Checking if any car is on the location
        for car in self.cars:
            if location in car.list_location():
                return False
        return True

    def move(self, car, direction):
        """
        Move a car in the given direction.
        :param car: A Car object to be moved.
        :param direction: A Direction object representing desired direction
            to move car.
        :return: True if movement was possible and car was moved, False otherwise.
        """
        location = car.location
        # For the given direction, checking that the place that the car
        # will take after moving is on the board and is empty
        if direction == Direction.UP:
            # To move up, we need to check the place at the top of the car
            if self.__is_empty(
                    (location[0] - EDGE_SHIFT, location[1])) and self.__is_in(
                    (location[0] - EDGE_SHIFT, location[1])):
                car.location = (location[0] - EDGE_SHIFT, location[1])
                return True
            else:
                gh.report(MSG_NOT_AVAILABLE)
                return False
        elif direction == Direction.DOWN:
            # To move down, we need to check the place at the bottom of the car
            if self.__is_empty(
                    (location[0] + car.length, location[1])) and self.__is_in(
                    (location[0] + car.length, location[1])):
                car.location = (location[0] + EDGE_SHIFT, location[1])
                return True
            else:
                gh.report(MSG_NOT_AVAILABLE)
                return False
        elif direction == Direction.LEFT:
            # To move left, we need to check the place at the left of the car
            if self.__is_empty(
                    (location[0], location[1] - EDGE_SHIFT)) and self.__is_in(
                    (location[0], location[1] - EDGE_SHIFT)):
                car.location = (location[0], location[1] - EDGE_SHIFT)
                return True
            else:
                gh.report(MSG_NOT_AVAILABLE)
                return False
        elif direction == Direction.RIGHT:
            # To move right, we need to check the place at the right of the car
            if self.__is_empty(
                    (location[0], location[1] + car.length)) and self.__is_in(
                    (location[0], location[1] + car.length)):
                car.location = (location[0], location[1] + EDGE_SHIFT)
                return True
            else:
                gh.report(MSG_NOT_AVAILABLE)
                return False

    def __empty_board(self):
        """
        Creating the empty pattern of the board, according to the given size
        :return: the pattern as a list of list
        """
        # Creating it as a list of list
        table = []
        for i in range(self.size + EDGE_SHIFT):
            line = []
            for j in range(self.size + EDGE_SHIFT):
                if i == self.size:
                    line.append(str(j - EDGE_SHIFT))
                elif j == 0:
                    line.append(str(i))
                else:
                    line.append(AVAILABLE_SYMBOL)
            table.append(line)

        table[self.size][0] = AVAILABLE_SYMBOL

        # Putting the exit symbol
        if self.exit_board[0] == self.size:
            table[self.exit_board[0]][
                self.exit_board[1] + EDGE_SHIFT] = EXIT_SYMBOL
        elif self.exit_board[1] == 0:
            table[self.exit_board[0]][self.exit_board[1]] = EXIT_SYMBOL

        return table

    def __repr__(self):
        """
        :return: Return a string representation of the board.
        """
        table = self.__empty_board()  # Get the empty board

        # Adding each car to the pattern
        for car in self.cars:
            for location in car.list_location():
                table[location[0]][location[1] + EDGE_SHIFT] = car.color
        # Convert it to a string
        string = ''
        for line in table:
            string += str(line) + '\n'
        return string
