#!/usr/bin/python3
# Author: GMFTBY
# Time  : 2018.7.7

'''
Can use tkinter to rewrite this `run` function
'''

from game import Game, Board
# from alphazero_mcts import MCTSPlayer
from pure_mcts import MCTSPlayer
from policy_value_net import PolicyValueNet

class Human:
    def __init__(self):
        self.color = None
        self.name = "human"
    
    def set_color(self, color):
        self.color = color

    def get_action(self, board):
        # get action must use the get point function
        try:
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
    # get the training param
    # ...
    
    # best_policy = PolicyValueNet(width, height, policy_param)
    mctsplayer = MCTSPlayer(c_puct = 5, n_playout = 500)
    human = Human()
    
    # human first, red
    game.start_play(human, mctsplayer, 1, 2, 1)

if __name__ == "__main__":
    run()
