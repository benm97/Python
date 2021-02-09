#######################################################################
# FILE: calculate_mathematical_expression.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex2 2017-2018
# DESCRIPTION: Two functions to get the result of an expression
#######################################################################


def calculate_mathematical_expression(number_1, number_2, operation):
    """The function receive two numbers and an operation and return result"""

    if operation == '+':
        return number_1 + number_2

    elif operation == '-':
        return number_1 - number_2

    elif operation == '*':
        return number_1 * number_2

    elif operation == '/' and number_2 != 0:  # Exclude division by 0
        return number_1 / number_2

    else:
        # If the third parameter doesn't correspond to an operation
        # or division by 0
        return None


def calculate_from_string(string_operation):
    """The function receive an expression in a string and return result"""

    # Getting two number and operator from the string
    term_1, operator, term_2 = string_operation.split()

    # Returning result using calculate_mathematical_expression function
    return calculate_mathematical_expression(float(term_1), float(term_2),
                                             operator)
