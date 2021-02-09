#########################################################################
# FILE: quadratic_equation.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex2 2017-2018
# DESCRIPTION: Function that checks if the temperature
#              get over a fixed limit in 2 between 3 days
#########################################################################


def is_it_summer_yet(temp_limit, day1_temp, day2_temp, day3_temp):
    """Function that checks if the temperature
    get over a fixed limit in 2 between 3 days"""

    def is_it_superior(temp):
        """Checking if one temp get over the limit"""

        if temp > temp_limit:
            return True
        else:
            return False

    # Days_of_sun is variable that counts days
    # were the temperature get over the limit
    days_of_sun = 0

    # For each day, if temperature get over the limit,
    # we increment 1 to the counter
    if is_it_superior(day1_temp):
        days_of_sun += 1
    if is_it_superior(day2_temp):
        days_of_sun += 1
    if is_it_superior(day3_temp):
        days_of_sun += 1

    if days_of_sun >= 2:  # If we get over the limit 2 or 3 times return true
        return True
    else:  # If we get over the limit 0 or 1 time return false
        return False
