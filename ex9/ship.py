from screen import Screen

SHIP_SIZE = 1
INITIAL_HEADING = 0
INITIAL_LIVES = 3


class Ship:

    def __init__(self, x, y, speed_x, speed_y):
        """
        The init of the Ship class

        :param x: coordinate x of the ship
        :param y: coordinate y of the ship
        :param speed_x: speed for the x coordinate
        :param speed_y: speed for the y coordinate
        """
        self.__x = x
        self.__y = y
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__heading = INITIAL_HEADING
        self.__lives = INITIAL_LIVES

    def move(self):
        """
        We use the formulas. This method move the ship
        """
        self.__x = (self.__speed_x + self.__x - Screen.SCREEN_MIN_X) % (
            Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X) + Screen.SCREEN_MIN_X
        self.__y = (self.__speed_y + self.__y - Screen.SCREEN_MIN_Y) % (
            Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y) + Screen.SCREEN_MIN_Y

    def radius(self):
        """
        :return: radius of the ship
        """
        return SHIP_SIZE

    def draw(self,screen):
        """
        Draw the ship at the given coordinates with the given heading
        """
        screen.draw_ship(self.__x,self.__y,self.__heading)

    # Getters / Setters
    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_speed_x(self, speed_x):
        self.__speed_x = speed_x

    def set_speed_y(self, speed_y):
        self.__speed_y = speed_y

    def get_speed_x(self):
        return self.__speed_x

    def get_speed_y(self):
        return self.__speed_y

    def get_lives(self):
        return self.__lives

    def get_heading(self):
        return self.__heading

    def set_heading(self, heading):
        self.__heading = heading

    def set_lives(self, lives):
        self.__lives = lives

