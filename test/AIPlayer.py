#!/usr/bin/python3

class RULEPlayer:
    '''
    根据走棋的棋子周围的棋子的布局情况确定是否向前发动攻击以及对应的攻击方向
    '''
    def __init__(self):
        self.color = None
        self.red_map= [[4, 4, 4, 4, 4], 
                      [4, 3, 3, 3, 3], 
                      [4, 3, 2, 2, 2],
                      [4, 3, 2, 1, 1],
                      [4, 3, 2, 1, 0]]
        self.blue_map=[[0, 1, 2, 3, 4],
                       [1, 1, 2, 3, 4],
                       [2, 2, 2, 3, 4],
                       [3, 3, 3, 3, 4],
                       [4, 4, 4, 4, 4]]

    def set_color(self, color):
        self.color = color

    def get_all_moves(self, pieces, red_lm, blue_lm):
        # get all the move
        collections = []
        if self.color == 0: lm = red_lm
        else: lm = blue_lm
        for x, y in pieces:
            for deltax, deltay in lm:
                if x + deltax < 0 or x + deltax > 4 or y + deltay < 0 or y + deltay > 4: continue
                collections.append([x, y, x + deltax, y + deltay])
        return collections

    def check_end_oppo(self, red_pieces, blue_pieces):
        # 确定我方能否全歼对方的棋子
        if self.color == 0:    # red color
            for x, y in blue_pieces:    # 存在一个蓝棋即可
                tag = False
                for ox, oy in red_pieces:
                    if ox <= x and oy <= y: 
                        tag = True
                        break 
                if not tag: return False
            return True
        else:
            for x, y in red_pieces:    # 存在一个蓝棋即可
                tag = False
                for ox, oy in blue_pieces:
                    if ox >= x and oy >= y: 
                        tag = True
                        break 
                if not tag: return False
            return True

    def rule(self, board):
        pieces = board.get_avaiable_pieces()
        red_pieces = [piece for index, piece in board.pieces.items() if index > 0]
        blue_pieces = [piece for index, piece in board.pieces.items() if index < 0]
        # must win go to dest
        if self.color == 0:
            for piece in pieces:
                if piece[0] == 3 and piece[1] == 3: return (3, 3, 4, 4)
                elif piece[0] == 4 and piece[1] == 3: return (4, 3, 4, 4)
                elif piece[0] == 3 and piece[1] == 4: return (3, 4, 4, 4)
        else:
            for piece in pieces:
                if piece[0] == 1 and piece[1] == 1: return (1, 1, 0, 0)
                elif piece[0] == 1 and piece[1] == 0: return (1, 0, 0, 0)
                elif piece[0] == 0 and piece[1] == 1: return (0, 1, 0, 0)
        # must win eat all the oppo piece
        if self.color == 0 and board.blue_number == 1:
            for i in range(-6, 0):
                tar = board.pieces.get(i, None)
                if tar: break
            for x, y in pieces:
                dx1, dy1 = x + board.red_lm[0][0], y + board.red_lm[0][1]
                dx2, dy2 = x + board.red_lm[1][0], y + board.red_lm[1][1]
                dx3, dy3 = x + board.red_lm[2][0], y + board.red_lm[2][1]
                if tar in ((dx1, dy1), (dx2, dy2), (dx3, dy3)): return (x, y, tar[0], tar[1])
        if self.color == 1 and board.red_number == 1:
            for i in range(1, 7):
                tar = board.pieces.get(i, None)
                if tar: break
            for x, y in pieces:
                dx1, dy1 = x + board.blue_lm[0][0], y + board.blue_lm[0][1]
                dx2, dy2 = x + board.blue_lm[1][0], y + board.blue_lm[1][1]
                dx3, dy3 = x + board.blue_lm[2][0], y + board.blue_lm[2][1]
                if tar in ((dx1, dy1), (dx2, dy2), (dx3, dy3)): return (x, y, tar[0], tar[1])

        # 没有必杀策略，考虑分支
        ava_move = self.get_all_moves(pieces, board.red_lm, board.blue_lm)
        # 当我方失去了全歼能力的时候，不应该吃对方的子，因为不能全歼胜利反而会增加对方棋子的灵活性，尽可能选择走法及其靠近终点的走法,这时候是非常危险的，尽快的取胜才是关键
        if not self.check_end_oppo(red_pieces, blue_pieces):
            # 不可全歼对方，不选择吃对方棋子的 move, 如果出现了多种走法都是最小的，选择走完之后比较安全的走法 !!!!!
            if self.color == 0: 
                ava_move = [(x, y, dx, dy) for x, y, dx, dy in ava_move if (dx, dy) not in blue_pieces]
                distance = [self.red_map[dx][dy] for x, y, dx, dy in ava_move]
            else:
                ava_move = [(x, y, dx, dy) for x, y, dx, dy in ava_move if (dx, dy) not in red_pieces]
                distance = [self.blue_map[dx][dy] for x, y, dx, dy in ava_move]
            left_move = []
            for index, dis in enumerate(distance):
                if dis == min(distance):
                    left_move.append(ava_move[index])
            if len(left_move) == 1: return left_move[0]
            else:
                # 选择较为安全的走子方案，统计棋局信息,考虑当我方棋子数目不多的时候避免吃掉我放弃自的15中情况考虑
                maxscore, bestmove = -2000, None
                for move in left_move:
                    score = self.just_move(move)
                    if score > maxscore: 
                        maxscore = score
                        bestmove = move
                return bestmove
        else:
            # 大多数情况的判断，这时候一般需要使用蒙特卡洛算法进行大量模拟判断
            # make the score for the mcts
            pass 

    def just_move(self, move, red_pieces, blue_pieces, red_lm, blue_lm):
        pass

    def get_action(self, board):
        # the main function for this AIPlayer
        move = self.rule(board)
        print(move)
        return move

if __name__ == "__main__":
    pass
