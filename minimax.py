def evaluate(game_state):
    black_count, white_count = game_state.count_pieces()
    return black_count - white_count


def minimax(game_state, depth, is_maximizing):
    if depth == 0 or game_state.is_game_over():
        return evaluate(game_state)  # 使用我们的评估函数

    if is_maximizing:
        best_value = float('-inf')
        for move in game_state.get_legal_moves(game_state.current_player):
            new_game_state = game_state.cloney()
            new_game_state.make_move(*move)
            new_game_state.switch_player()  # 别忘了在移动后切换玩家
            value = minimax(new_game_state, depth - 1, False)
            best_value = max(best_value, value)
        return best_value
    else:
        best_value = float('inf')
        for move in game_state.get_legal_moves(game_state.current_player):
            new_game_state = game_state.cloney()
            new_game_state.make_move(*move)
            new_game_state.switch_player()  # 别忘了在移动后切换玩家
            value = minimax(new_game_state, depth - 1, True)
            best_value = min(best_value, value)
        return best_value

def minimax_make_move(game_state):
    best_move = None
    best_value = float('-inf')
    for move in game_state.get_legal_moves(game_state.current_player):
        new_game_state = game_state.cloney()
        new_game_state.make_move(*move)
        new_game_state.switch_player()  # 别忘了在移动后切换玩家
        value = minimax(new_game_state, 8, False)  # 假设搜索深度为3
        if value > best_value:
            best_value = value
            best_move = move
    xx, yy = best_move[0], best_move[1]
    game_state.board[xx][yy] = game_state.current_player
    game_state.flip_pieces(xx, yy)
    game_state.switch_player()
    return best_move
