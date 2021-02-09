import random
import math
from screen import Screen

MIN_SPEED = 1
MAX_SPEED = 3
MAX_ASTEROID = 3
SIZE_COEFFICIENT = 10
NORMATIVE_FACTOR = 5


class Asteroid:
    def __init__(self, size=MAX_ASTEROID):
        """
        The init of the Asteroid class
        """
        self.__x = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
        self.__y = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
        self.__speed_x = random.randint(MIN_SPEED, MAX_SPEED)
        self.__speed_y = random.randint(MIN_SPEED, MAX_SPEED)
        self.__size = size

    def radius(self):
        """
        :return: radius of an asteroid
        """
        return self.__size * SIZE_COEFFICIENT - NORMATIVE_FACTOR

    def move(self):
        """
        We use the formulas. This method move an asteroid
        """
        self.__x = ((self.__speed_x + self.__x - Screen.SCREEN_MIN_X) % (
            Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X)) + Screen.SCREEN_MIN_X
        self.__y = ((self.__speed_y + self.__y - Screen.SCREEN_MIN_Y) % (
            Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y)) + Screen.SCREEN_MIN_Y

    def has_intersection(self, ship):
        """
        :param ship: the ship
        :return: True if the ship hit the asteroid, False otherwise
        """
        distance = math.sqrt(
            (ship.get_x() - self.__x) ** 2 + (ship.get_y() - self.__y) ** 2)
        return distance <= self.radius() + ship.radius()

    def draw(self, screen):
        """
        Draw the given asteroid on the specified (x,y) coordinates
        """
        screen.draw_asteroid(self, self.__x, self.__y)

    # Getters / Setters
    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def get_size(self):
        return self.__size

    def set_speed_x(self, speed_x):
        self.__speed_x = speed_x

    def set_speed_y(self, speed_y):
        self.__speed_y = speed_y

    def get_speed_x(self):
        return self.__speed_x

    def get_speed_y(self):
        return self.__speed_y
