#!/usr/bin/python
# Author: GMFTBY
# Time  : 2018.7.3

import numpy as np
from collections import deque

class Board:
    def __init__(self):
        self.width = self.height = 5
        self.point = -1

    def init_board(self, start_player, red_pieces, blue_pieces):
        self.red_pieces = red_pieces
        self.blue_pieces = blue_pieces
        self.current_player = self.first = start_player         # start player is a string red or blue
        self.states = deque(maxlen=10)    # each player save 5 step in the game

    def get_point(self, point):
        self.point = point

    def get_current_state(self):
        pass

    def do_move(self):
        pass

    def if_win(self):
        # check win or the wrong pass