INCREASE = 1
ONE_SEQUENCE = '1111'
ZERO_SEQUENCE = '0000'


class Game:
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    ILLEGAL_MOVE = 'Illegal move.'

    def __init__(self):
        self.board = []
        self.move_count = 0
        for i in range(6):
            line = []
            for j in range(7):
                line.append(None)
            self.board.append(line)

    def __repr__(self):
        board_string = ''
        for line in self.board:
            board_string += str(line)
            board_string += '\n'
        return board_string


    def inverted_board(self):
        """
        For a matrix, return the inverted matrix (line 1 became last line,...)
        :param matrix: the matrix to invert
        :return: inverted matrix
        """
        invert_board = []
        for line_index in range(len(self.board) - 1, -1,
                                -1):  # For each number
            # (descending) from the max index line
            # of the matrix (len-1) to 0 (included)

            invert_board.append(self.board[line_index])  #
        return invert_board

    def find_bottom(self, column):
        if column > 6:
            raise Exception(self.ILLEGAL_MOVE)
        for row in range(6):
            if self.board[row][column] == self.PLAYER_ONE or self.board[row][
                column] == self.PLAYER_TWO:
                return row - 1
        return 5

    def check(self, lst, max_sequence):

        for (i, string) in enumerate(lst):
            count_zero = 0
            count_one = 0
            for (j, char) in enumerate(string):
                if char == 0:
                    count_zero += INCREASE
                    count_one = 0
                    if count_zero == max_sequence:
                        return ((i, j), 0)
                elif char == 1:
                    count_one += INCREASE
                    count_zero = 0
                    if count_one == max_sequence:
                        return ((i, j), 1)
                else:
                    count_zero = 0
                    count_one = 0

    def check_tup(self, tup_lst, board, max_sequence):

        for lst in tup_lst:
            count_one = []
            count_zero = []

            for tup in lst:
                if board[tup[0]][tup[1]] == 1:
                    count_zero = []
                    count_one.append(tup)
                    if len(count_one) == max_sequence:
                        return (count_one, self.PLAYER_TWO)
                elif board[tup[0]][tup[1]] == 0:
                    count_one = []
                    count_zero.append(tup)
                    if len(count_zero) == max_sequence:
                        return (count_zero, self.PLAYER_ONE)
                else:
                    count_one = []
                    count_zero = []
        return None

    def vertical_check(self,max_sequence=4):
        lst = []
        width = len(self.board[0])
        height = len(self.board)
        for column in range(width):
            column_lst = []
            for line in range(height):
                column_lst.append(self.board[line][column])
            lst.append(column_lst)
        return self.check(lst,max_sequence)  # TODO

    def horizontal_check(self,max_sequence=4):
        lst = []
        width = len(self.board[0])
        height = len(self.board)
        for line in range(height):
            line_lst = []
            for column in range(width):
                line_lst.append(self.board[line][column])
            lst.append(line_lst)
        return self.check(lst,max_sequence)

    def diagonal_check(self, board,max_sequence=4):
        lst_coords = []
        width = len(board[0])
        height = len(board)
        for line in range(height):
            lst_tup = []
            i = line
            j = 0
            while i < height and j < width:
                lst_tup.append((i, j))
                j += INCREASE
                i += INCREASE
            lst_coords.append(lst_tup)
        for column in range(1, width):
            lst_tup = []
            i = 0
            j = column
            while i < height and j < width:
                lst_tup.append((i, j))
                j += INCREASE
                i += INCREASE
            lst_coords.append(lst_tup)

        return self.check_tup(lst_coords, board,max_sequence)

    def inverted_diagonal_check(self,max_sequence=4):
        checked = self.diagonal_check(self.inverted_board(),max_sequence)

        if checked is not None:
            new_coord_lst = []
            for coord_tup in list(checked[0]):
                new_coord_lst.append((5 - coord_tup[0], coord_tup[1]))
            new_tuple = (new_coord_lst, checked[1])

            return new_tuple

    def found_winner(self):
        check_vertical = self.vertical_check()
        if check_vertical is not None:
            return ('v', check_vertical[0])
        check_horizontal = self.horizontal_check()
        if check_horizontal is not None:
            return ('h', check_horizontal[0])
        check_diag = self.diagonal_check(self.board)
        if check_diag is not None:
            return ('d', check_diag[0])
        check_invert_diag = self.inverted_diagonal_check()
        if check_invert_diag is not None:
            return ('d', check_invert_diag[0])

    def make_move(self, column):
        row = self.find_bottom(column)
        if row < 0 or self.get_winner() is not None:
            raise Exception(self.ILLEGAL_MOVE)
        current_player = self.get_current_player()
        self.board[row][column] = current_player
        self.move_count += INCREASE
        return (row, current_player)

    def get_current_player(self):
        return self.move_count % 2

    def get_player_at(self, row, col):
        return self.board[row][col]

    def get_winner(self):
        check_list = [self.diagonal_check(self.board),
                      self.inverted_diagonal_check(),
                      self.horizontal_check(),
                      self.vertical_check()]
        for checked in check_list:
            if checked is not None:
                return checked[1]
        if self.move_count >= 42:
            return self.DRAW
