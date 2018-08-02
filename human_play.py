#!/usr/bin/python3
# Author: GMFTBY
# Time  : 2018.7.7

'''
Can use tkinter to rewrite this `run` function
'''

from game import Game, Board
from alphazero_mcts import MCTSPlayer
from pure_mcts import MCTSPlayer as PURE
from policy_value_net import PolicyValueNet
import time

class Human:
    def __init__(self):
        self.color = None
        self.name = "human"
    
    def set_color(self, color):
        self.color = color

    def get_action(self, board):
        # get action must use the get point function
        try:
            # get the point from outside (not the program)
            while True:
                try:
                    point = int(input("Input point (1~6): "))
                    if point <= 0 or point > 6: raise Exception()
                    break
                except KeyboardInterrupt:
                    exit(1)
                except:
                    print('Please input the right point to move !')
            
            board.get_point()     # get the point for this turn
            print(board.get_avaiable_pieces())
            move = input('Your Move: ')
            move = int(move)
        except KeyboardInterrupt:
            exit(1)
        except:
            print('Invalid Move, Please input like 4434 which means (4, 4) to (3, 4)')
            return self.get_action(board)
        return move

def run():
    # play the chess with human
    game = Game()
    
    # log, the model for training 1500 is suck, maybe the value is not prepared and need to be
    # trained more times - 2018.7.11
    best_policy = PolicyValueNet(5, 5)
    mctsplayer = MCTSPlayer(best_policy.policy_value_fn, c_puct = 5, n_playout = 10000)
    puremctsplayer = PURE(c_puct = 5, n_playout = 10000)
    human = Human()
    
    '''
    # human first, red
    win = {1: 0, 2: 0}
    for i in range(50):
        a = time.time()
        winner = game.start_play(puremctsplayer, mctsplayer, 1, 2, (i % 2 + 1), is_show=1)
        if winner == 1: win[1] += 1
        else: win[2] += 1
        # print(i, 'winner is', 'red' if winner == 1 else 'blue')
        print(i, 'blue win rate:', win[2] / (i + 1))
        print(i, 'cost:', time.time() - a, 's')
    # print('win rating ...', win[2] / 100)
    '''

    '''
    import time
    a = time.time()
    game.start_self_play(mctsplayer, is_show=1)
    print(time.time() - a)
    '''
    game.start_play(human, mctsplayer, 1, 2, 1, is_show=1)

if __name__ == "__main__":
    run()
