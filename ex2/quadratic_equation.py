#########################################################################
# FILE: quadratic_equation.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex2 2017-2018
# DESCRIPTION: Functions that returns solution of quadratic equation
#########################################################################

import math


def quadratic_equation(a, b, c):
    """A function that returns solution of quadratic equation"""

    delta = (b * b) - (4 * a * c)  # Calculate discriminant

    if delta > 0:  # Positive discriminant, two solutions
        x1 = (-b - math.sqrt(delta)) / (2 * a)
        x2 = (-b + math.sqrt(delta)) / (2 * a)
        return x1, x2

    elif delta == 0:  # Discriminant 0, one solution
        x = (-b) / (2 * a)
        return x, None
    else:  # Negative discriminant, no solution
        return None, None


def quadratic_equation_user_input():
    """A function that receive a polynom in a string and return solutions """

    coefficients = input(
        'Insert coefficients a, b, and c:')  # Asking coefficients
    a, b, c = coefficients.split()  # Get them from the string
    # Sending them to quadratic_equation function as float
    x1, x2 = quadratic_equation(float(a), float(b), float(c))

    if x1 is None and x2 is None:  # If the function return no solution
        print('The equation has no solutions')
    elif x2 is None:  # If the function return one solution
        print('The equation has 1 solution: ' + str(x1))
    elif x1 is not None and x2 is not None: # If the function return 2 solution
        print('The equation has 2 solutions: ' + str(x1) + ' and ' + str(x2))
