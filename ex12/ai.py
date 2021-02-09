import random
import copy
NO_MOVE_MSG='No possible AI moves.'
class AI:

    def make_adversary_move(self,g, column):
        row = g.find_bottom(column)
        current_player = abs(g.get_current_player()-1)
        g.board[row][column] = current_player

    def get_winner_3(self,g):
        check_list_diag = [g.diagonal_check(g.board,max_sequence=3),
                      g.inverted_diagonal_check(max_sequence=3)]

        for checked in check_list_diag:
            if checked is not None:
                return checked[0][0]
        check_h = g.horizontal_check(max_sequence=3)
        if check_h is not None:
            return check_h[0]
        check_v = g.vertical_check(max_sequence=3)
        if check_v is not None:
            return (check_v[0][1],check_v[0][0])

    def optimal_col(self,g,available_col):
        for i in available_col:
            test_game_win=copy.deepcopy(g)
            test_game_win.make_move(i)
            if test_game_win.get_winner() is not None:
                print('a')
                return i
        for j in available_col:
            test_game_lose=copy.deepcopy(g)
            self.make_adversary_move(test_game_lose,j)
            if test_game_lose.get_winner() is not None:
                print('b')
                return j

    def optimal_col_second(self,original_g,available_col):
        g=copy.deepcopy(original_g)
        winner_3=self.get_winner_3(g)
        while winner_3 is not None:
            g.board[winner_3[0]][winner_3[1]]=None
            print(g)
            winner_3=self.get_winner_3(g)
            print(winner_3)

        for j in available_col:
            test_game_lose=copy.deepcopy(g)
            self.make_adversary_move(test_game_lose,j)
            if self.get_winner_3(test_game_lose) is not None:

                print('c')
                return j
        for i in available_col:
            test_game_win=copy.deepcopy(g)
            test_game_win.make_move(i)
            if self.get_winner_3(test_game_win) is not None:
                print('d')
                return i


    def find_legal_move(self, g, func, timeout=None):
        available_columns=[]
        for i in range(7):
            if g.find_bottom(i)>=0:
                available_columns.append(i)
        if not available_columns:
            raise Exception(NO_MOVE_MSG)
        else:
            potential_col=self.optimal_col(g,available_columns)
            potential_col_3=self.optimal_col_second(g,available_columns)
            if potential_col is not None:
                choosed_column=potential_col
            elif g.board[5][3] is None:
                choosed_column=3
            elif potential_col_3 is not None:
                choosed_column=potential_col_3
            else:
                print('random')
                choosed_column=random.choice(available_columns)
            func(choosed_column)
            return choosed_column