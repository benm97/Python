import tkinter as tk
from game import Game
from communicator import Communicator
from ai import AI
import sys
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FIRST_ROW = 172
FIRST_COLUMN = 74
COLUMN_STEP = 76
ROW_STEP = 90
MSG_TIME = 1500

RED_TOKEN_IMAGE = 'red.png'
BLUE_TOKEN_IMAGE = 'blue.png'
PLAYER_ONE_IMAGE = 'one.png'
PLAYER_TWO_IMAGE = 'two.png'
PATTERN_IMAGE = 'pattern.png'
BLUE_WIN_IMAGE = 'win_blue.png'
RED_WIN_IMAGE = 'win_red.png'
NO_WINNER_IMAGE = 'no-winner.png'
ILLEGAL_ACTION_IMAGE = 'illegal.gif'
SERVER_TITLE = "Server"
CLIENT_TITLE = "Client"
WAIT_IMAGE = 'wait.png'
WIN_SYMBOL_IMAGE = 'win-symbol.png'


class Gui():
    def __init__(self, root, port, player, ip=None, ai=None):
        self.root = root
        self.player = player
        self.game = Game()

        self.ai=ai

        self.__communicator = Communicator(root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)

        self.pattern = tk.PhotoImage(file=PATTERN_IMAGE)
        self.red = tk.PhotoImage(file=RED_TOKEN_IMAGE)
        self.blue = tk.PhotoImage(file=BLUE_TOKEN_IMAGE)
        self.player_one = tk.PhotoImage(file=PLAYER_ONE_IMAGE)
        self.player_two = tk.PhotoImage(file=PLAYER_TWO_IMAGE)
        self.blue_win = tk.PhotoImage(file=BLUE_WIN_IMAGE)
        self.red_win = tk.PhotoImage(file=RED_WIN_IMAGE)
        self.no_win = tk.PhotoImage(file=NO_WINNER_IMAGE)
        self.illegal = tk.PhotoImage(file=ILLEGAL_ACTION_IMAGE)
        self.wait = tk.PhotoImage(file=WAIT_IMAGE)
        self.win_symbol = tk.PhotoImage(file=WIN_SYMBOL_IMAGE)

        self.canvas = tk.Canvas(self.root, width=CANVAS_WIDTH,
                                height=CANVAS_HEIGHT)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.pattern)

        self.canvas.bind('<Button-1>', self.callback)
        if ip is None and self.ai:
            column=self.ai.find_legal_move(self.game,self.update)
            self.__communicator.send_message(column)


    def draw_coin(self, row, column, player):
        """
        This function draw the tokens in the board, and assigns one to each
        player
        """

        if player == 0:
            coin = self.blue
            self.player_b = self.canvas.create_image(57, 140,
                                                     image=self.player_two)
            self.player_a = self.canvas.create_image(744, 140,
                                                     image=self.player_one)
        else:
            coin = self.red
            self.canvas.delete(self.player_a)
            self.canvas.delete(self.player_b)

        self.canvas.create_image(FIRST_ROW + (column * COLUMN_STEP),
                                 FIRST_COLUMN + (row * ROW_STEP), image=coin)

    def check_winner(self):
        winner = self.game.get_winner()
        if winner == self.game.PLAYER_ONE:
            blue_win = self.canvas.create_image(379, 300, image=self.blue_win)
            self.canvas.after(1500, self.delete_msg, blue_win)
        elif winner == self.game.PLAYER_TWO:
            red_win = self.canvas.create_image(379, 300, image=self.red_win)
            self.canvas.after(1500, self.delete_msg, red_win)
        elif winner == self.game.DRAW:
            self.canvas.create_image(400, 300, image=self.no_win)
        if winner is not None and winner!=self.game.DRAW:
            self.canvas.after(1500, self.design_win)

    def design_win(self):
        direction, coord = self.game.found_winner()
        if direction == 'h':
            self.horizontal_win(coord)
        if direction == 'v':
            self.vertical_win(coord)
        if direction == 'd':
            self.diagonal_win(coord)

    def horizontal_win(self, coord):
        for i in range(coord[1], coord[1] - 4, -1):
            self.canvas.create_image(FIRST_ROW + i * COLUMN_STEP,
                                     FIRST_COLUMN + coord[0] * ROW_STEP,
                                     image=self.win_symbol)

    def vertical_win(self, coord):
        for i in range(coord[1], coord[1] - 4, -1):
            self.canvas.create_image(FIRST_ROW + coord[0] * COLUMN_STEP,
                                     FIRST_COLUMN + i * ROW_STEP,
                                     image=self.win_symbol)

    def diagonal_win(self, coord):
        for coord_tup in coord:
            self.canvas.create_image(FIRST_ROW + coord_tup[1] * COLUMN_STEP,
                                     FIRST_COLUMN + coord_tup[0] * ROW_STEP,
                                     image=self.win_symbol)

    def put_disk(self, column_coord):
        if column_coord > 134:
            column = (column_coord - 134) // COLUMN_STEP
            self.update(column)
            self.__communicator.send_message(column)
        else:
            raise Exception(self.game.ILLEGAL_MOVE)


    def delete_msg(self, illegal_image):
        self.canvas.delete(illegal_image)

    def callback(self, event):
        if self.game.get_winner() is None:
            if self.player == self.game.get_current_player():
                try:
                    self.put_disk(event.x)
                except Exception:
                    illegal_image = self.canvas.create_image(400, 300,
                                                             image=self.illegal)
                    self.canvas.after(MSG_TIME, self.delete_msg,
                                      illegal_image)
            else:
                wait_image = self.canvas.create_image(400, 300,
                                                      image=self.wait)
                self.canvas.after(MSG_TIME, self.delete_msg,
                                  wait_image)

    def update(self,column):
        row, cur_player = self.game.make_move(column)
        self.draw_coin(row, column, cur_player)
        self.check_winner()
    def __handle_message(self, msg):

        self.update(int(msg))

        if self.ai and self.game.get_winner() is None:
            column=self.ai.find_legal_move(self.game,self.update)
            self.__communicator.send_message(column)

def check_arguments(args_list):
    if len(args_list)!=3 and len(args_list)!=4:
        raise Exception
    if int(sys.argv[2])>=65535:
        raise Exception
    if args_list[1]!='human' and args_list[1]!='ai':
        raise Exception
if __name__ == '__main__':
    root = tk.Tk()

    #try:
    check_arguments(sys.argv)
    port=int(sys.argv[2])
    if sys.argv[1]=='human':
        if len(sys.argv)==3:
            Gui(root, port, Game.PLAYER_ONE)
            root.title(SERVER_TITLE)
        elif len(sys.argv)==4:
            Gui(root, port, Game.PLAYER_TWO,sys.argv[3])
            root.title(CLIENT_TITLE)
    elif sys.argv[1]=='ai':
        if len(sys.argv)==3:
            Gui(root, port, Game.PLAYER_ONE, ai=AI())
            root.title(SERVER_TITLE)
        elif len(sys.argv)==4:
            Gui(root, port, Game.PLAYER_TWO, ip=sys.argv[3],ai=AI())
            root.title(CLIENT_TITLE)
    root.mainloop()
    #except Exception:
        #print ('Illegal program arguments.')


