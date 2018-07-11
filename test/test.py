import sys
sys.path.append('..')
from game import Board
from pprint import pprint

b = Board()
b.init_board()
pprint(b.map)
