#######################################################################
# FILE: hangman.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex4 2017-2018
# DESCRIPTION: Hangman
#######################################################################
import hangman_helper

EMPTY_STRING = ""
INCREASE = 1
LENGTH_ONE_LETTER = 1
CHAR_A = 97
HIDDEN_LETTER_SYMBOL = '_'
ALPHABET_SIZE = 26
COMMAND_INDEX = 0
VALUE_INDEX = 1


def letter_to_index(letter):
    """
    Return the index of the given letter in an alphabet list.
    """
    return ord(letter.lower()) - CHAR_A


def index_to_letter(index):
    """
    Return the letter corresponding to the given index.
    """
    return chr(index + CHAR_A)


def update_word_pattern(word, pattern, letter):
    """
    A function to update the pattern with a letter
    :param word: the word to guess
    :param pattern: actual pattern
    :param letter: the letter to update the pattern with
    :return: updated pattern
    """
    new_pattern = EMPTY_STRING

    for tested_letter_index in range(len(word)):  # For each index in the word

        if pattern[tested_letter_index] != HIDDEN_LETTER_SYMBOL:  # If we've
            # already put a letter
            new_pattern += pattern[tested_letter_index]  # Copy it
            # to the new pattern

        elif word[tested_letter_index] == letter:  # If we have
            # the tested letter
            new_pattern += letter  # Add it to the new pattern

        else:  # If we do not found the good letter
            new_pattern += HIDDEN_LETTER_SYMBOL  # Putting a _ in the
            #  new pattern

    return new_pattern


def run_single_game(words_list):
    """
    Running the game
    :param words_list: list of words
    """

    # Initialising
    word = hangman_helper.get_random_word(words_list)  # Getting a word
    errors_list = []
    error_count = 0
    pattern = HIDDEN_LETTER_SYMBOL * len(word)  # Creating default pattern
    message = hangman_helper.DEFAULT_MSG

    while len(errors_list) < hangman_helper.MAX_ERRORS and pattern != word:
        # While the user has not reach maximum number of error
        # and he did not found the word

        # Displaying state
        hangman_helper.display_state(pattern, error_count,
                                     errors_list, message, ask_play=False)
        user_input = hangman_helper.get_input()  # Getting the input

        if user_input[COMMAND_INDEX] == hangman_helper.LETTER:  # If the input
            #  is a guess
            letter = user_input[VALUE_INDEX]  # Get the letter

            # Testing the letter
            if len(letter) != LENGTH_ONE_LETTER or not letter.islower():  # If
                # there is more than a letter or it's uppercase
                message = hangman_helper.NON_VALID_MSG
                continue

            elif letter in errors_list or letter in pattern:  # If we already
                # choose this letter
                message = hangman_helper.ALREADY_CHOSEN_MSG + letter

            elif letter in word:  # If he guess a good letter
                pattern = update_word_pattern(word, pattern, letter)
                # Updating the pattern with it
                message = hangman_helper.DEFAULT_MSG

            else:  # His letter not in the word
                errors_list.append(letter)  # Adding it to errors list
                error_count += INCREASE  # Count an error
                message = hangman_helper.DEFAULT_MSG

        # Giving a hint
        elif user_input[COMMAND_INDEX] == hangman_helper.HINT:  # If he want
            # a hint
            # Updating words list to keep only that's correspond
            words_list = filter_words_list(words_list, pattern, errors_list)

            # Choosing letters
            hint_letter = choose_letter(words_list, pattern)

            # Updating the message (it will display with the display_state
            #  at the beginning of the while)
            message = hangman_helper.HINT_MSG + hint_letter

    # If he win
    if pattern == word:  # If he found the entire word
        message = hangman_helper.WIN_MSG

    # If he loose
    else:  # If he reach the limit
        message = hangman_helper.LOSS_MSG + word

    # Displaying state and asking if he want to play again
    hangman_helper.display_state(pattern, error_count,
                                 errors_list, message, ask_play=True)


def correspond(word, pattern, wrong_guess_lst):
    """
    A function to check if a word correspond to
    the pattern and to the wrong guess list"
    :param word: tested word
    :param pattern: tested pattern
    :param wrong_guess_lst: wrong list
    :return: true if it's corresponding, else false
    """

    # Creating an empty pattern
    tested_word_pattern = HIDDEN_LETTER_SYMBOL * len(word)

    # For each revealed letter in the pattern,
    #  I'm updating my new pattern with this letter and the tested word
    if len(word) == len(pattern):  # Checking they have the same size
        for letter in pattern:
            if letter != HIDDEN_LETTER_SYMBOL:  # If this is a revealed letter
                tested_word_pattern = update_word_pattern(word,
                                                          tested_word_pattern,
                                                          letter)
                # Updating the pattern with this letter
    # Now if the word correspond, my updated pattern should be equal
    #  to the original pattern

    # Checking that any letter from this word is the wrong list
    flag = True  # We suppose there is no
    for wrong_letter in wrong_guess_lst:  # For every letter of the wrong list
        if wrong_letter in word:  # If it's in the word, even one time
            flag = False  # It's not corresponding

    if tested_word_pattern == pattern and flag:
        return True

    else:
        return False


def filter_words_list(words, pattern, wrong_guess_lst):
    """A function to filter list of words to keep only words whose
     correspond to the pattern and to the wrong guess list"
    :param words: tested words list
    :param pattern: tested pattern
    :param wrong_guess_lst: wrong list
    :return: filtered list"""

    words_list = []
    for word in words:  # For each word in words list
        if correspond(word, pattern, wrong_guess_lst):  # If it's corresponding
            words_list.append(word)  # Adding it to the list

    return words_list


def choose_letter(words, pattern):
    """
    A function that return the most occurred letter in a list of words,
     that's not already in the pattern
    :param words: list of words
    :param pattern: pattern
    :return: most occurred letter
    """
    occurrence = [0] * ALPHABET_SIZE  # Creating a list of 26 counters,
    # one for each letter

    for word in words:  # For each word
        for letter in word:  # And each letter in it
            if letter not in pattern:  # If the letter is not in the pattern
                occurrence[letter_to_index(letter)] += INCREASE  # We increase
                # the counter of this letter

    return index_to_letter(occurrence.index(max(occurrence)))  # Return most
    # occurred letter


def main():
    """
    Launching the game until the user click on no more
    :return:
    """
    # Launching the first game
    words_list = hangman_helper.load_words()  # Loading words
    run_single_game(words_list)  # Running the game with those words
    input_from_user = hangman_helper.get_input()

    # Playing again
    while input_from_user[COMMAND_INDEX] == hangman_helper.PLAY_AGAIN \
            and input_from_user[VALUE_INDEX]:  # While the input is play
        # again choice and it's true
        run_single_game(words_list)  # Running the game
        input_from_user = hangman_helper.get_input()


if __name__ == "__main__":
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()
