from reversi import ReversiGame
import random
import copy
import math

class TreeNode:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move  # 表示到达当前节点的落子动作
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_actions = game_state.get_legal_moves(game_state.current_player)
    def is_leaf(self):
        return len(self.children) == 0
    def select_child(self):
        # UCT选择公式
        c = math.sqrt(2)
        return max(self.children, key=lambda child: child.wins / child.visits + c * math.sqrt(math.log(self.visits) / child.visits))
    def expand(self, move, game_state):
        # 扩展新的子节点
        child = TreeNode(game_state=game_state, parent=self, move=move)
        self.untried_actions.remove(move)
        self.children.append(child)
        return child
    def backpropagate(self, result):
        # 反向传播结果
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)
    def get_best_move(self):
        # 根据访问次数选择最佳动作
        return max(self.children, key=lambda child: child.visits).move

def mcts_make_move(game_state):
    root = TreeNode(game_state=game_state.cloney())
    i=0
    for _ in range(600):  # 设定模拟次数
        print(i)
        i=i+1
        node = root
        state_clone = game_state.cloney()

        # 选择 - 一直到达未完全探索的节点
        while not node.is_leaf():
            if node.untried_actions:  # 如果还有未尝试的动作，跳出选择循环
                break
            node = node.select_child()
            state_clone.make_move(*node.move)

        # 扩展 - 如果可能，随机选择一个未尝试的动作扩展新节点
        if node.untried_actions:
            move = random.choice(node.untried_actions)
            state_clone.make_move(*move)
            node = node.expand(move, state_clone.cloney())

        # 模拟 - 从当前节点随机玩到游戏结束
        while not state_clone.is_game_over():
            possible_moves = state_clone.get_legal_moves(state_clone.current_player)
            move = random.choice(possible_moves)
            state_clone.make_move(*move)

        # 反向传播 - 根据游戏结果更新节点信息
        # 假设AI玩家颜色存储在ai_player变量中 ('B' 或 'W')
        ai_player = state_clone.current_player  # 或者 'W'，根据你的设定
        if ai_player == 'B':
            result = 1 if state_clone.count_pieces()[0] > state_clone.count_pieces()[1] else 0  # 黑棋胜利
        else:
            result = 1 if state_clone.count_pieces()[1] > state_clone.count_pieces()[0] else 0  # 白棋胜利
        node.backpropagate(result)

    best_move = root.get_best_move()
    xx,yy=best_move[0], best_move[1]
    game_state.board[xx][yy] = game_state.current_player
    game_state.flip_pieces(xx, yy)
    game_state.switch_player()
    print('sucessfullt find the best move')
    print(xx+1,yy+1)
    return True

