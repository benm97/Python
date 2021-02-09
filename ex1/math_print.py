######################################################################
# FILE: math_print.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex1 2017-2018
# DESCRIPTION: Create and launch some mathematical functions
#######################################################################

import math


def golden_ratio():
    # This function prints the golden ratio
    print((1 + math.sqrt(5)) / 2)


def six_square():
    # This function prints 6 power 2
    print(math.pow(6, 2))


def hypotenuse():
    # This function prints the lenght of the hypothenuse
    # of a right triangle with sides of 5 and 12
    print(math.sqrt(math.pow(5, 2) + math.pow(12, 2)))


def pi():
    # This function prints pi
    print(math.pi)


def e():
    # This function prints e (exponential 1)
    print(math.exp(1))


def squares_area():
    # This function prints aire of squares with sides from 1 to 10
    print(1 * 1, 2 * 2, 3 * 3, 4 * 4, 5 * 5, 6 * 6, 7 * 7, 8 * 8, 9 * 9, 10 * 10)


# Calling the functions
golden_ratio()
six_square()
hypotenuse()
pi()
e()
squares_area()
