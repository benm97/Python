#######################################################################
# FILE: ex7.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex7 2017-2018
# DESCRIPTION: Some recursive functions
#######################################################################
FIRST_POSITIVE = 1
DECREASE = -1
SMALLER_DIVISOR = 1
SMALLER_PRIME = 2
INCREASE = 1
MIN_DISKS = 2
BINARY_FIRST = '0'
BINARY_SECOND = '1'


def print_to_n(n):
    """
    Print all numbers from 1 to n
    :param n: stop to n
    :return: nothing
    """
    if n >= FIRST_POSITIVE:  # It will stop when n will go under 1
        print_to_n(n + DECREASE)
        print(n)


def print_reversed(n):
    """
    Print all numbers from n to 1
    :param n: start with n
    :return: nothing
    """
    if n >= FIRST_POSITIVE:  # It will stop when n will go under 1
        print(n)  # Print before calling again
        print_reversed(n + DECREASE)


def has_divisor_smaller_than(n, i):
    """
    Saying if n has divisor smaller than i
    :param n: number to check divisors
    :param i: max number to check
    :return: True if there are divisors smaller than i, False else
    """
    if i == SMALLER_DIVISOR:  # base case
        return False

    else:
        if n % i != 0:  # If i is not a divisor
            return has_divisor_smaller_than(n,
                                            i + DECREASE)  # Calling again the
            # function with i-1

        else:  # If i is a divisor we finished
            return True


def is_prime(n):
    """
    Checking if a number n is prime
    :param n: number to check
    :return: True if is prime, else False
    """
    if n >= SMALLER_PRIME:
        # Return True if n has a divisor smaller than itself, else false
        return not has_divisor_smaller_than(n, int(n ** 0.5))
    else:  # If n under 2, it can't be prime
        return False


def divisors_from(n, i, divisors_list):
    """
    Giving a list of all divisors of n bigger than (or equal to) i
    :param n: number to check
    :param i: minimal potential divisor to check
    :param divisors_list: the list of founded divisors
    :return: list of divisors
    """
    if i == n:  # Base case
        divisors_list.append(i)  # Adding the number itself
        return divisors_list
    else:
        if n % i == 0:  # If i is a divisor adding it to the list
            divisors_list.append(i)
        return divisors_from(n, i + INCREASE,
                             divisors_list)  # Calling again for i+1


def divisors(n):
    """
    Giving all the divisors of a number n
    :param n: number to check
    :return: list of divisors
    """
    if n == 0:
        return []
    else:
        return divisors_from(abs(n), SMALLER_DIVISOR, [])  # Return a list of
        # all divisors bigger than (or equal to) n


def factorial(n):
    """
    Get n factorial
    :param n: the number
    :return: factorial of n
    """
    if n == 0:  # Base case
        return FIRST_POSITIVE
    else:
        return n * factorial(n + DECREASE)  # Calling the function for n-1,
        # multiplied by n


def exp_n_x(n, x):
    """
    Giving exponential sum of x
    :param n: number of terms of the sum
    :param x: exponent
    :return: exponential sum of x (an approximation of e^x)
    """
    if n == 0:  # Base case
        return 1
    else:
        # Compute the actual term (beginning by the end) and calling again the
        # function with n-1 to get the others terms
        return (pow(x, n)) / (factorial(n)) + exp_n_x(n + DECREASE, x)


def play_hanoi(hanoi, n, src, dest, temp):
    """
    The function plays (and win) an hanoi game
    :param hanoi: graphical game as an object
    :param n: number of disk
    :param src: the source rod
    :param dest: destination rod
    :param temp: the rod used to transfer
    :return: nothing
    """
    if n <= 0:
        pass
    else:
        if n == MIN_DISKS:  # Base case
            hanoi.move(src, temp)
            hanoi.move(src, dest)
            hanoi.move(temp, dest)
        else:
            # Calling recursively the function with n-1
            play_hanoi(hanoi, n + DECREASE, src, temp, dest)
            hanoi.move(src, dest)
            play_hanoi(hanoi, n + DECREASE, temp, dest, src)


def print_binary_sequences_with_prefix(prefix, n):
    """
    Print all sequences of size n of 0 and 1 beginning by the prefix
    :param prefix: the beginning of all sequences
    :param n: size of the sequences (including the prefix)
    :return: Nothing
    """
    if len(prefix) == n:  # Base case, when the prefix is big as n
        print(prefix)
    else:
        # Calling again the function with prefix increased by 0
        print_binary_sequences_with_prefix(prefix + BINARY_FIRST, n)
        # Calling again the function with prefix increased by 0
        print_binary_sequences_with_prefix(prefix + BINARY_SECOND, n)


def print_binary_sequences(n):
    """
    Print all sequences of size n of 0 and 1
    :param n: size of sequence
    :return: nothing
    """
    # Print all sequences of size n with an empty prefix
    print_binary_sequences_with_prefix('', n)


def print_sequences_with_prefix(char_list, prefix, n):
    """
    Print all sequences of size n of characters from char_list beginning by
    the prefix
    :param char_list: the characters to compose the sequences
    :param prefix: the beginning of all sequences
    :param n: size of sequences
    :return: nothing
    """
    if len(prefix) == n:  # Base case, when the prefix is big as n
        print(prefix)
    else:
        # For each character, calling again the function with prefix increased,
        # by the char
        for char in char_list:
            print_sequences_with_prefix(char_list, prefix + char, n)


def print_sequences(char_list, n):
    """
    Print all sequences of size n of characters from char_list
    :param char_list: the characters to compose the sequences
    :param n: size of sequences
    :return: nothing
    """
    # Print all sequences of size n with an empty prefix
    print_sequences_with_prefix(char_list, '', n)


def print_no_repetition_sequences_with_prefix(char_list, prefix, n):
    """
    Print all sequences of size n of characters from char_list beginning by
    the prefix, without repetition
    :param char_list: the characters to compose the sequences
    :param prefix: the beginning of all sequences
    :param n: size of sequences
    :return: nothing
    """
    if len(prefix) == n:  # Base case, when the prefix is big as n
        print(prefix)
    else:
        # For each character, calling again the function with prefix increased
        # by the char
        for char in char_list:
            # Checking that's the char not already in the sequence to avoid
            # repetitions
            if char not in prefix:
                print_no_repetition_sequences_with_prefix(char_list,
                                                          prefix + char, n)


def print_no_repetition_sequences(char_list, n):
    """
    Print all sequences of size n of characters from char_list,
    without repetition
    :param char_list: the characters to compose the sequences
    :param n: size of sequences
    :return: nothing
    """
    # Print all sequences of size n with an empty prefix
    print_no_repetition_sequences_with_prefix(char_list, '', n)


def no_repetition_sequences_with_prefix_list(char_list, prefix, n,
                                             strings_list):
    """
    Return a list of all sequences of size n of characters from char_list
    beginning by the prefix, without repetition
    :param char_list: the characters to compose the sequences
    :param prefix: the beginning of all sequences
    :param n: size of sequences
    :param strings_list: list of founded sequences
    :return: the list of sequences
    """
    if len(prefix) == n:  # Base case, when the prefix is big as n
        strings_list.append(prefix)
    else:
        # For each character, calling again the function with prefix increased
        # by the char
        for char in char_list:
            # Checking that's the char not already in the sequence to avoid
            # repetitions
            #if char not in prefix:
                no_repetition_sequences_with_prefix_list(char_list,
                                                         prefix + char, n,
                                                         strings_list)
    return strings_list


def no_repetition_sequences_list(char_list, n):
    """
    Return a list of all sequences of size n of characters from char_list
    without repetition
    :param char_list: the characters to compose the sequences
    :param n: size of sequences
    :return: the list of sequences
    """
    # Return a list of all sequences of size n with an empty prefix
    return no_repetition_sequences_with_prefix_list(char_list, '', n, [])

print(no_repetition_sequences_list(['a','b','c'],2))