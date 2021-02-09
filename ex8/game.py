############################################################
# Imports
############################################################
import game_helper as gh
from car import Car, Direction
from board import Board

############################################################
# Class definition
############################################################
RED_CAR_SIZE = 2
RED_CAR_COLOR = 'R'
MSG_CHOOSE_CAR = 'What color car would you like to move?'
MSG_NOT_A_CAR = 'There is no car with this color'
MSG_WELCOME = 'Welcome to rush Hour game'
MSG_CHOSEN = 'Already chosen color, try again...'
EXIT = [3, 0]
COLOR_INDEX = 0
LENGTH_INDEX = 1
LOCATION_INDEX = 2
ORIENTATION_INDEX = 3


class Game:
    """
    A class representing a rush hour game.
    A game is composed of cars that are located on a square board and a user
    which tries to move them in a way that will allow the red car to get out
    through the exit
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def __check_direction(self, car, direction):
        """
        Checking that the car can move in a direction according to his
        orientation
        :param car: car to check
        :param direction: direction we want to move to
        :return: True if we can, else False
        """
        return ((direction == Direction.UP or direction == Direction.DOWN) and
                car.orientation == Direction.VERTICAL) or \
               ((direction == Direction.LEFT or direction == Direction.RIGHT)
                and car.orientation == Direction.HORIZONTAL)

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        The function runs one round of the game :
            1. gh.report board to the screen
            2. Get user's input of: what color car to move, and what direction to
                move it.
            2.a. Check the the input is valid. If not, gh.report an error message and
                return to step 2.
            2. Move car according to user's input. If movement failed (trying
                to move out of board etc.), return to step 2. 
            3. Report to the user the result of current round ()
        """

        # Asking to choose a car and a direction until the user enter valid
        # data
        while True:
            color = input(MSG_CHOOSE_CAR)
            for car in self.__board.cars:
                if car.color == color:
                    direction = gh.get_direction()
                    while not self.__check_direction(car,
                                                     direction) or \
                            direction not in Direction.ALL_DIRECTIONS:
                        direction = gh.get_direction()
                    return self.__board.move(car, direction)
            else:  # If we still return nothing, that's mean that the car
                # doesn't exist, so print a message and asking again
                gh.report(MSG_NOT_A_CAR)

    def __check_exit(self, red_car):
        """
        Checking if the red car is on (in front of actually) the exit
        :param red_car: red car
        :return: True if it's on it, else False
        """
        if red_car.orientation == Direction.VERTICAL:
            return ([red_car.location[0] + RED_CAR_SIZE,
                     red_car.location[1]] != self.__board.exit_board)
        elif red_car.orientation == Direction.HORIZONTAL:

            return [red_car.location[0],
                    red_car.location[1]] != self.__board.exit_board

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        gh.report(MSG_WELCOME)

        # Putting the red car according to the position of the exit
        location, orientation = 0, 0
        if self.__board.exit_board[0] == self.__board.size:
            location = (0, self.__board.exit_board[1])
            orientation = Direction.VERTICAL
        elif self.__board.exit_board[1] == 0:
            location = (
                self.__board.exit_board[0], self.__board.size - RED_CAR_SIZE)
            orientation = Direction.HORIZONTAL
        red_car = Car(RED_CAR_COLOR, RED_CAR_SIZE, location, orientation)
        self.__board.add_car(red_car)

        print(self.__board)  # Printing the board

        added_colors = [RED_CAR_COLOR]  # Creating a list of all cars that's
        # already on screen

        num_cars = gh.get_num_cars()  # Asking how much car the user
        # want to add

        for i in range(num_cars):
            # Create each car as wanted
            new_car = gh.get_car_input(self.__board.size)
            while new_car[0] in added_colors:
                # If we already chose this color, displaying a message and
                # asking again
                gh.report(MSG_CHOSEN)
                new_car = gh.get_car_input(self.__board.size)

            # Adding the new car to added list and adding it to the board
            added_colors.append(new_car[0])
            self.__board.add_car(
                Car(new_car[COLOR_INDEX], new_car[LENGTH_INDEX],
                    new_car[LOCATION_INDEX], new_car[ORIENTATION_INDEX]))
            # Displaying the board
            print(self.__board)

        while self.__check_exit(red_car):  # Running single turn and printing
            # the board until the victory
            self.__single_turn()
            print(self.__board)
        # Display end message
        gh.report_game_over()


############################################################
# An example usage of the game
############################################################
if __name__ == "__main__":
    board = Board([],
                  EXIT)
    game = Game(board)
    game.play()
