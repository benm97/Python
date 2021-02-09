#######################################################################
# FILE: ex3.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex4 2017-2018
# DESCRIPTION: Some list functions
#######################################################################


EMPTY_STRING = ""  # An empty string
INCREASE = 1  # A variable to increase
MIN_PRIME_NUMBER = 2  # The smallest prime number


def create_list():
    """
    Function that's asking from user to type string
    until he type just enter and return all the entries as a list
    @return: return the entered list
    """

    entered_list = []  # Creating an empty list
    string_from_user = input()  # Ask from the user the first entry

    while string_from_user:  # While the precedent entry is not empty
        entered_list.append(string_from_user)  # Adding it to the list
        string_from_user = input()  # Asking for the next entry
    # When he type an empty string we get out from the loop
    return entered_list  # And return the list


def concat_list(str_list):
    """
    Function that's get a list of string and return a string
    with all the elements of the list
    @param str_list: A list of string to concatenate
    @return: The concatenated string
    """

    concatenated_string = EMPTY_STRING  # Creating an empty string

    for i in str_list:  # For each element in the list
        concatenated_string += i  # Adding this element to the string

    return concatenated_string  # Returning the string


def average(num_list):
    """
    Function that's get a list of numbers and return their average
    @param num_list: list of numbers we want averaging
    @return: the average as float
    """

    if num_list:  # If the list not empty

        list_sum = 0  # Creating a variable for the sum

        for i in num_list:  # For each number in num_list
            list_sum += i  # We adding this number to the the sum
        # Divide by number of elements to get the average
        return list_sum / len(num_list)
    else:  # If the list is empty
        return None


def cyclic(lst1, lst2):
    """
    Function that's get two list and return true
     if one is a cyclic permutation of the other
    @param lst1: first list
    @param lst2: second list
    @return: True if it's a cyclic permutation else false
    """

    k = len(lst1)  # Putting the length of the first list in k to use it easily

    if not lst1 and not lst2:  # If the two lists are empty return true

        return True

    elif len(lst2) == k:  # If they have the same length we compare them:

        # We need to check if lst1 is a permutation of lst2
        # for every permutation index m between 0 and k. Over k we come back
        # to an already checked permutation (because we're using 'modulo k')
        for m in range(k):

            # Creating a tester that will stay true
            # while there is no difference between lst1 and the m-permuted lst2
            tester = True

            for i in range(k):  # For each index of lst1

                # We calculating the m-permuted index,
                # where this member supposed to being in lst2
                permuted_index = (i + m) % k

                if lst1[i] != lst2[permuted_index]:  # If a member doesn't
                    # correspond we do not have the good m so
                    # we put the tester to false

                    tester = False

            if tester:  # If we tested every element and the tester still true
                # then lst2 is a m-permutation of lst1

                return True

        else:  # If after we test all the m, we didn't return anything
            # then any m correspond and lst1 and lst2 aren't permutation

            return False

    else:  # If they not empty and doesn't have the same length return false

        return False


def histogram(n, num_list):
    """
    A function that's for a n and a list of number return the histogram until n
    @param n: Size of the wanted histogram
    @param num_list: list of numbers
    @return: the histogram as a list
    """

    histogram_list = []  # Creating an empty list for the histogram

    for i in range(n):  # For each number from 1 to n

        occurrences = 0  # We initialise the counter

        for j in num_list:  # And we checking every number in num_list

            if j == i:  # When the checked number appear in the list
                occurrences += INCREASE  # We adding 1 to the counter

        histogram_list.append(occurrences)  # We checked every occurrence
        # of one number so we add the occurrence number at the end of the list
    return histogram_list


def prime_factors(n):
    """
    A function to decompose a natural n to a product of prime number.
     For each potential divisor, we'll divide n by it as many time as possible.
     Then we'll try the next number. We get prime number only, if a non-prime
     number was a divisor of the original n, he's divisor (inferior to him)
     already divide the original n so he can't be a divisor of n
    @param n: the number to decompose
    @return: the prime factors a s a list
    """
    factor_list = []  # Creating an empty list

    for prime_divisor in range(MIN_PRIME_NUMBER, n + 1):  # For every potential
        # prime divisor, so superior to 2 and inferior or equal to n

        while n % prime_divisor == 0:  # If it's a divisor
            factor_list.append(prime_divisor)  # Adding it to the list
            n /= prime_divisor  # Dividing by it

    return factor_list


def cartesian(lst1, lst2):
    """
    A function that's return all the combination lst1 members
    with lst2 members (cartesian multiplication)
    @param lst1: First list
    @param lst2: Second list
    @return: List of tuples
    """

    cartesian_list = []  # Creating an empty list
    for lst1_member in lst1:  # For each element of lst1
        for lst2_member in lst2:  # For each element of lst2
            cartesian_list.append((lst1_member, lst2_member))  # We adding this
            # combination to the list as tuple

    return cartesian_list


def pairs(n, num_list):
    """
    A function to get couple of numbers from a list,
     with the sum for each couple is n
    @param n: Sum of couple are supposed to equal n
    @param num_list:the list to take numbers
    @return:list of couples
    """
    couple_list = []  # Creating a empty list to put founded couples

    # For each two numbers in num_list
    for num1 in num_list:
        for num2 in num_list:
            # If they are different, there sum equal to n,
            # and they note already are in couple_list
            if num1 != num2 \
                    and num1 + num2 == n \
                    and not ((num1, num2) in couple_list) \
                    and not ((num2, num1) in couple_list):
                couple_list.append((num1, num2))  # Add this couple to the list

    return couple_list


