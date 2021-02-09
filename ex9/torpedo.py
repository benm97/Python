from screen import Screen
import math

TORPEDO_SIZE = 4


class Torpedo:
    SPEED_FACTOR = 2

    def __init__(self, x, y, speed_x, speed_y, heading):
        """
        The init of the Torpedo class
        :param x: coordinate x of a torpedo
        :param y: coordinate y of a torpedo
        :param speed_x: speed for the x coordinate
        :param speed_y: speed for the y coordinate
        :param heading: direction in degree
        """
        self.__x = x
        self.__y = y
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__heading = heading
        self.__life_time = 0

    def draw(self, screen):
        """
        Draw the given torpedo on the specified (x,y) coordinates with
        the given heading
        :param screen: screen object to draw on
        :return:
        """

        screen.draw_torpedo(self, self.__x, self.__y, self.__heading)

    def move(self):
        """
        We use the formulas. This method move a torpedo
        """
        self.__x = (self.__speed_x + self.__x - Screen.SCREEN_MIN_X) % (
            Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X) + Screen.SCREEN_MIN_X
        self.__y = (self.__speed_y + self.__y - Screen.SCREEN_MIN_Y) % (
            Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y) + Screen.SCREEN_MIN_Y

    def __radius(self):
        """
        :return: radius of the torpedo
        """
        return TORPEDO_SIZE

    def get_intersection(self, asteroid):
        """
        :param asteroid: an asteroid
        :return: True if a torpedo hit an asteroid, False otherwise
        """
        distance = math.sqrt(
            (asteroid.get_x() - self.__x) ** 2 + (
                asteroid.get_y() - self.__y) ** 2)
        return distance <= self.__radius() + asteroid.radius()

    # Getters / Setters
    def get_speed_x(self):
        return self.__speed_x

    def get_speed_y(self):
        return self.__speed_y

    def get_life_time(self):
        return self.__life_time

    def set_life_time(self, new_life_time):
        self.__life_time = new_life_time
