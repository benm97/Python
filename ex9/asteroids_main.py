from screen import Screen
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import math

DEFAULT_ASTEROIDS_NUM = 3
TURN_LEFT = 7
TURN_RIGHT = -7
MAX_ASTEROID = 3
MEDIUM_ASTEROID = 2
SMALL_ASTEROID = 1
MIN_PTS = 20
MEDIUM_PTS = 50
MAX_PTS = 100
MAX_LIFE_TIME = 200
INCREASE = 1
MAX_TORPEDO = 15
INITIAL_SHIP_X = 0
INITIAL_SHIP_Y = 0
INITIAL_SHIP_SPEED_X = 0
INITIAL_SHIP_SPEED_Y = 0
WARNING_TITLE = "Warning!"
WARNING_MESSAGE = "You lose a life"
VICTORY_TITLE = 'Victory'
VICTORY_MESSAGE = "You win bro/sis' ;)"
DEFEAT_TITLE = 'Defeat'
DEFEAT_MESSAGE = "You lose :("
QUIT_TITLE = 'Bye'
QUIT_MESSAGE = "So sad! See you soon"


class GameRunner:
    def __init__(self, asteroids_amnt):
        """
        The init of the Game Runner class

        :param asteroids_amnt: the number of asteroid we want in the game
        """

        # Init the attribute
        self._screen = Screen()
        self.ship = Ship(INITIAL_SHIP_X, INITIAL_SHIP_Y,
                         INITIAL_SHIP_SPEED_X, INITIAL_SHIP_SPEED_Y)
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        self.asteroids_list = []
        self.torpedos_list = []
        self.score = 0

        # Creating the wanted amount of asteroid
        self.create_asteroids(asteroids_amnt)

    def create_asteroids(self, asteroids_amnt):
        """
        This method create the asteroids, and check that they are in a
        different position that the ship
        :param asteroids_amnt: number of asteroid we want in the game
        """

        for i in range(asteroids_amnt):
            new_asteroid = Asteroid()

            # Generate a new asteroid until it's on an available place
            while new_asteroid.get_x() == self.ship.get_x() \
                    and new_asteroid.get_y() == self.ship.get_y():
                new_asteroid = Asteroid()

            # Adding the new asteroid
            self._screen.register_asteroid(new_asteroid, MAX_ASTEROID)
            self.asteroids_list.append(new_asteroid)

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def is_collision(self, asteroid):
        """
        If there is collision between the given asteroid and the ship,
        this method remove the asteroid from the game,
        remove life from the user and show him warning message
        :param asteroid: asteroid to check
        :return:
        """

        if asteroid.has_intersection(self.ship):
            self._screen.show_message(WARNING_TITLE, WARNING_MESSAGE)
            self._screen.remove_life()
            self.ship.set_lives(self.ship.get_lives() - 1)
            self._screen.unregister_asteroid(asteroid)
            self.asteroids_list.remove(asteroid)

    def update_score(self, size):
        """
        Updating the score for size of destroyed asteroid
        :param size: destroyed asteroid
        :return:
        """
        if size == MAX_ASTEROID:
            self.score += MIN_PTS
        elif size == MEDIUM_ASTEROID:
            self.score += MEDIUM_PTS
        elif size == SMALL_ASTEROID:
            self.score += MAX_PTS

        self._screen.set_score(self.score)

    def split_asteroid(self, asteroid, torpedo, correction):
        """
        This function create a new smaller asteroid
        :param asteroid: destroyed asteroid
        :param torpedo: torpedo that destroyed it
        :param correction: the direction correction (1 or -1)
        :return:
        """

        # Create the new asteroid (it will be at a random place)
        new_asteroid = Asteroid(asteroid.get_size() - 1)

        # Putting his speed ad location as wanted
        new_asteroid.set_x(asteroid.get_x())
        new_asteroid.set_y(asteroid.get_y())
        new_asteroid.set_speed_x(((torpedo.get_speed_x() +
                                   asteroid.get_speed_x()) /
                                  math.sqrt((asteroid.get_speed_x()) ** 2 +
                                            (asteroid.get_speed_y()) ** 2)) *
                                 correction)
        new_asteroid.set_speed_y(((torpedo.get_speed_y() +
                                   asteroid.get_speed_y()) /
                                  math.sqrt((asteroid.get_speed_x()) ** 2 +
                                            (asteroid.get_speed_y()) ** 2)) *
                                 correction)

        # Registering it
        self._screen.register_asteroid(new_asteroid, new_asteroid.get_size())
        self.asteroids_list.append(new_asteroid)

    def is_hit(self):
        """
        If there was a collision between a torpedo and an asteroid, this
        method update the score of the user, split the asteroid who was hit in
        2 smaller and remove the torpedo
        """
        torpedo_to_remove = []
        asteroid_to_remove = []

        # For each torpedo checking each asteroid
        for torpedo in self.torpedos_list:
            for asteroid in self.asteroids_list:

                # If there is a collision with an existent asteroid
                if torpedo.get_intersection(asteroid) and \
                                asteroid not in asteroid_to_remove and \
                                torpedo not in torpedo_to_remove:
                    self.update_score(asteroid.get_size())
                    asteroid_to_remove.append(asteroid)
                    torpedo_to_remove.append(torpedo)

                    # If the size of the asteroid not 1
                    if asteroid.get_size() == MAX_ASTEROID or \
                                    asteroid.get_size() == MEDIUM_ASTEROID:
                        # Create 2 smaller in opposite speed
                        self.split_asteroid(asteroid, torpedo, 1)
                        self.split_asteroid(asteroid, torpedo, -1)

        # Remove from the screen torpedo and asteroids founded
        for torpedo_removed in torpedo_to_remove:
            self.torpedos_list.remove(torpedo_removed)
            self._screen.unregister_torpedo(torpedo_removed)
        for asteroid_removed in asteroid_to_remove:
            self.asteroids_list.remove(asteroid_removed)
            self._screen.unregister_asteroid(asteroid_removed)

    def user_action(self):
        """
        This function does different actions depending on the request of the
        user
        """
        if self._screen.is_left_pressed():
            self.ship.set_heading(self.ship.get_heading() + TURN_LEFT)
        if self._screen.is_right_pressed():
            self.ship.set_heading(self.ship.get_heading() + TURN_RIGHT)
        if self._screen.is_up_pressed():
            self.ship.set_speed_x(self.ship.get_speed_x() + math.cos(
                math.radians(self.ship.get_heading())))
            self.ship.set_speed_y(self.ship.get_speed_y() + math.sin(
                math.radians(self.ship.get_heading())))
        if self._screen.is_space_pressed():
            # Launching a torpedo
            if len(self.torpedos_list) < MAX_TORPEDO:
                torpedo_speed_x = self.ship.get_speed_x() + \
                                  Torpedo.SPEED_FACTOR * \
                                  math.cos(math.radians(
                                      self.ship.get_heading()))
                torpedo_speed_y = self.ship.get_speed_y() + \
                                  Torpedo.SPEED_FACTOR * \
                                  math.sin(math.radians(
                                      self.ship.get_heading()))
                # Create the new torpedo
                torpedo = Torpedo(self.ship.get_x(), self.ship.get_y(),
                                  torpedo_speed_x, torpedo_speed_y,
                                  self.ship.get_heading())
                self._screen.register_torpedo(torpedo)
                self.torpedos_list.append(torpedo)

    def check_end(self):
        """
        This method is to end the game, it check if the ship has no more life,
        if the user want to exit or if there is no more asteroids
        """
        if not len(self.asteroids_list):
            self._screen.show_message(VICTORY_TITLE, VICTORY_MESSAGE)
            self._screen.end_game()
            sys.exit()
        elif not self.ship.get_lives():
            self._screen.show_message(DEFEAT_TITLE, DEFEAT_MESSAGE)
            self._screen.end_game()
            sys.exit()
        elif self._screen.should_end():
            self._screen.show_message(QUIT_TITLE, QUIT_MESSAGE)
            self._screen.end_game()
            sys.exit()

    def _game_loop(self):
        """
        This method check all the game : move the objects, check if the game
        over, check if the user want to do some action ..
        """

        # At each loop we check that the game not supposed to end, moving the
        # ship/asteroids/torpedo, checking if the user pressed a key, drawing
        # the ship/asteroids/torpedos, delete over timed torpedo and updating
        # there life time, checking collisions between ship/asteroid
        # or torpedo/asteroid

        self.check_end()
        self.ship.move()
        self.user_action()
        self.ship.draw(self._screen)
        for asteroid in self.asteroids_list:
            asteroid.move()
            asteroid.draw(self._screen)
            self.is_collision(asteroid)
        for torpedo in self.torpedos_list:
            torpedo.move()
            torpedo.draw(self._screen)
            torpedo.set_life_time(torpedo.get_life_time() + INCREASE)
            if torpedo.get_life_time() == MAX_LIFE_TIME:
                self.torpedos_list.remove(torpedo)
                self._screen.unregister_torpedo(torpedo)

        self.is_hit()


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
