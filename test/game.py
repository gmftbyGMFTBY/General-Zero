#!/usr/bin/python3

import pprint, random
from AIPlayer import RULEPlayer

red_stay = [(0, 0, 3), (1, 0, 5), (2, 0, 6), (0, 1, 1), (1, 1, 4), (0, 2, 2)]
blue_stay = [(4, 4, 3), (4, 3, 1), (4, 2, 2), (3, 4, 5), (3, 3, 4), (2, 4, 6)]

class board:
    def __init__(self, red_pieces, blue_pieces, start_player=0):
        # start_player: red - 0, blue - 1
        # board:
        # 0 -- x -- 4
        # | 
        # y
        # |
        # 4
        # pieces: (x, y, index) red_index >= 1, blue_index <= -1
        self.pieces = {}
        for x, y, index in red_pieces:
            self.pieces[index] = (x, y)
        for x, y, index in blue_pieces:
            self.pieces[-index] = (x, y)
        self.turn = self.start_player = start_player
        self.red_lm = [(0, 1), (1, 0), (1, 1)]
        self.blue_lm = [(-1, 0), (0, -1), (-1, -1)]
        self.red_number = self.blue_number = 6
        self.point = -1

    def set_start(self, s):
        self.turn = self.start_player = s

    def move(self, move):
        sx, sy, dx, dy = move
        if dx < 0 or dx > 4 or dy < 0 or dy > 4: 
            raise Exception('Out of board !')

        for p_index, piece in self.pieces.items():
            if piece[0] == dx and piece[1] == dy:
                del self.pieces[p_index]
                if p_index > 0: self.red_number -= 1
                elif p_index < 0: self.blue_number -= 1
                break

        for p_index, piece in self.pieces.items():
            if sx == piece[0] and sy == piece[1]:
                index = p_index
                break
        
        self.pieces[index] = (dx, dy)
        self.turn = 1 if self.turn == 0 else 0

    def if_end(self):
        red = [piece for index, piece in self.pieces.items() if index > 0]
        blue = [piece for index, piece in self.pieces.items() if index < 0]
        if len(red) == 0: return True, 1
        elif len(blue) == 0: return True, 0
        if blue.count((0, 0)) == 1: return True, 1
        elif red.count((4, 4)) == 1: return True, 0
        return False, None

    def get_point(self, point=None):
        if point: self.point = point
        else: 
            self.point = random.randint(1, 6)
            print("Point is", self.point)

    def get_current_board():
        pass

    def get_avaiable_pieces(self):
        if self.turn == 0:
            tar = self.pieces.get(self.point, None)
            if tar: return [tar]
            else:
                coll = []
                for i in range(self.point, 7):
                    tar = self.pieces.get(i, None)
                    if tar: 
                        coll.append(tar)
                        break

                for i in range(self.point, 0, -1):
                    tar = self.pieces.get(i, None)
                    if tar:
                        coll.append(tar)
                        break
                return coll
        else:
            tar = self.pieces.get(-self.point, None)
            if tar: return [tar]
            else:
                coll = []
                for i in range(self.point, 7):
                    tar = self.pieces.get(-i, None)
                    if tar: 
                        coll.append(tar)
                        break

                for i in range(self.point, 0, -1):
                    tar = self.pieces.get(-i, None)
                    if tar:
                        coll.append(tar)
                        break
                return coll

class game:
    def __init__(self, red_pieces, blue_pieces, start_player):
        self.board = board(red_pieces, blue_pieces, start_player)

    def show(self):
        index, pieces = zip(*list(self.board.pieces.items()))
        print('   ', end='')
        for i in range(5):
            print('{0:3}'.format(i), end='')
        print('  X')
        for i in range(5):
            print(' ', i, end='')
            for j in range(5):
                try:
                    print('{0:3}'.format(index[pieces.index((j, i))]), end='')
                except:
                    print('  0', end='')
            print()
        print('  Y')

    def start_play(self, player1, player2, player1_color, player2_color, start_player=0, is_show=1):
        if start_player not in [0, 1]:
            raise Exception('start player must be the 0(red) or the 1(blue)')
        self.board.set_start(start_player)
        player1.set_color(player1_color)
        player2.set_color(player2_color)
        players = {player1_color: player1, player2_color: player2}
        if is_show: self.show()
        while True:
            if self.board.turn == 0: print('-------------------\nRed player play ...')
            else: print('-------------------\nBlue player play ...')
            self.board.get_point()
            player_in_turn = players[self.board.turn]
            move = player_in_turn.get_action(self.board)
            self.board.move(move)
            if is_show: self.show()
            end, winner = self.board.if_end()
            if end:
                if is_show: print('red win' if winner == 0 else 'blue win')
                return winner

class Human:
    def __init__(self):
        self.color = None

    def set_color(self, color):
        self.color = color

    def get_action(self, board):
        pieces = board.get_avaiable_pieces()
        while True:
            print('Legal pieces:', pieces)
            getter = input('Your move: ')
            try:
                move = [int(i) for i in getter.split(',')]
                if (move[0], move[1]) not in pieces: raise Exception()
                if len(move) != 4: raise Exception()
                if self.color == 0:
                    # red player
                    sx, sy, dx, dy = move
                    deltax, deltay = dx - sx, dy - sy
                    if board.red_lm.index((deltax, deltay)): return move
                else:
                    sx, sy, dx, dy = move
                    deltax, deltay = dx - sx, dy - sy
                    if board.blue_lm.index((deltax, deltay)): return move
                break
            except:
                print('Wrong input !')


if __name__ == "__main__":
    g = game(red_stay, blue_stay, 0)
    g.start_play(Human(), RULEPlayer(), 0, 1)