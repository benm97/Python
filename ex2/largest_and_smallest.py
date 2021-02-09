#######################################################################
# FILE: largest_and_smallest.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex2 2017-2018
# DESCRIPTION: A function that returns
#              the largest and the smallest between 3 numbers
#######################################################################


def largest_and_smallest(number_1, number_2, number_3):
    """A function that returns largest and smallest between 3 numbers"""

    def largest(num_1, num_2, num_3):
        """A function that returns the largest between 3 numbers"""

        if num_1 >= num_2 and num_1 >= num_3:
            return num_1

        elif num_2 >= num_1 and num_2 >= num_3:
            return num_2

        elif num_3 >= num_2 and num_3 >= num_1:
            return num_3

    def smallest(num_1, num_2, num_3):
        """A function that returns the largest between 3 numbers"""

        if num_1 <= num_2 and num_1 <= num_3:
            return num_1

        elif num_2 <= num_1 and num_2 <= num_3:
            return num_2

        elif num_3 <= num_2 and num_3 <= num_1:
            return num_3

    # Return the largest and the smallest
    return largest(number_1, number_2, number_3), smallest(number_1, number_2,
                                                           number_3)
