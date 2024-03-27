import copy
class ReversiGame:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.reset_board()
        self.current_player = 'B'
        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.game_mode = "multiplayer"  # 默认为双人模式

    def cloney(self):
        # 创建一个新的ReversiGame实例
        cloned_game = ReversiGame()
        # 使用深拷贝复制棋盘状态，确保新旧棋盘互不影响
        cloned_game.board = copy.deepcopy(self.board)
        # 复制当前玩家
        cloned_game.current_player = self.current_player
        # 如果有其他需要复制的属性，也应该在这里处理
        # 例如游戏模式
        cloned_game.game_mode = self.game_mode
        # 返回新创建的游戏状态副本
        return cloned_game

    def set_game_mode(self, mode):
        self.game_mode = mode

    def reset_board(self):
        # 重置整个棋盘为None
        self.board = [[None for _ in range(8)] for _ in range(8)]
        # 放置初始的四个棋子
        self.board[3][3], self.board[4][4] = 'W', 'W'  # 白棋的初始位置
        self.board[3][4], self.board[4][3] = 'B', 'B'  # 黑棋的初始位置

    def switch_player(self):
        self.current_player = 'W' if self.current_player == 'B' else 'B'

    def make_move(self, x, y):
        if self.board[x][y] is not None or not self.can_flip(x, y):
            return False, "Player Invalid move"

        self.board[x][y] = self.current_player
        self.flip_pieces(x, y)
        self.switch_player()
        return True, "Move successful"

    def can_flip(self, x, y):
        # Check if placing a piece at (x, y) can flip any opponent's pieces
        for dx, dy in self.directions:
            if self.check_direction(x, y, dx, dy):
                return True
        return False

    def check_direction(self, x, y, dx, dy):
        # Check a single direction for opponent's pieces that can be flipped
        x += dx
        y += dy
        has_opponent_piece = False
        while 0 <= x < 8 and 0 <= y < 8:
            if self.board[x][y] == None:
                return False
            if self.board[x][y] == self.current_player:
                return has_opponent_piece
            has_opponent_piece = True
            x += dx
            y += dy
        return False

    def flip_pieces(self, x, y):
        # Flip opponent's pieces
        for dx, dy in self.directions:
            if self.check_direction(x, y, dx, dy):
                self.flip_direction(x, y, dx, dy)

    def flip_direction(self, x, y, dx, dy):
        # Flip pieces in a single direction
        x += dx
        y += dy
        while self.board[x][y] != self.current_player:
            self.board[x][y] = self.current_player
            x += dx
            y += dy

    def get_board_state(self):
        # 转换棋盘状态为前端所需的格式
        state = []
        for row in self.board:
            state_row = []
            for cell in row:
                if cell is None:
                    state_row.append(None)
                else:
                    state_row.append(cell)
            state.append(state_row)
        return state

    def count_pieces(self):
        # 计算黑白棋各自的数量
        black, white = 0, 0
        for row in self.board:
            for cell in row:
                if cell == 'B':
                    black += 1
                elif cell == 'W':
                    white += 1
        return black, white

    def has_legal_move(self, player):
        # 检查是否有合法棋步可下
        for x in range(8):
            for y in range(8):
                if self.is_valid_move(x, y, player, check_only=True):
                    return True
        return False

    def is_game_over(self):
        # 检查棋盘是否已满
        is_full = all(cell is not None for row in self.board for cell in row)
        if is_full:
            return True

        # 检查是否还有合法的落子位置
        has_legal_move_for_black = self.has_legal_move('B')
        has_legal_move_for_white = self.has_legal_move('W')
        if not has_legal_move_for_black and not has_legal_move_for_white:
            return True

        return False

    def is_valid_move(self, x, y, player, check_only=False):
        if self.board[x][y] is not None:
            return False  # 确保目标位置为空

        return self.can_flip(x, y)  # 使用can_flip检查是否可以翻转棋子

    def get_legal_moves(self, player):
        legal_moves = []
        for x in range(8):
            for y in range(8):
                if self.board[x][y] is None and self.is_valid_move(x, y, player):
                    legal_moves.append((x, y))
        return legal_moves

