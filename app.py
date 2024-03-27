from flask import Flask, jsonify, request, render_template
from reversi import ReversiGame
from mcts import mcts_make_move
from minimax import minimax_make_move
import time
app = Flask(__name__)
game = ReversiGame()


# def ai_make_move():
#     legal_moves = game.get_legal_moves(game.current_player)
#     if not legal_moves:
#         return False, "No legal moves available for AI"
#
#     import random
#     x, y = random.choice(legal_moves)
#     success, _ = game.make_move(x, y)
#     return success, "AI moved"


@app.route('/')
def welcome():
    game.reset_board()
    return render_template('welcome.html')

@app.route('/multiplayer')
def multiplayer():
    game.reset_board()
    # 确保游戏处于正确的模式
    if game.game_mode != 'multiplayer':
        game.set_game_mode('multiplayer')
    return render_template('index.html')  # 双人模式页面

@app.route('/ai')
def ai_mode():
    game.reset_board()
    # 确保游戏处于正确的模式
    if game.game_mode != 'ai':
        game.set_game_mode('ai')
    return render_template('ai.html')  # 人机模式页面
@app.route('/legal_moves', methods=['GET'])
def legal_moves():
    current_player = game.current_player
    legal_moves = game.get_legal_moves(current_player)
    return jsonify({'legalMoves': legal_moves})

@app.route('/board', methods=['GET'])
def board():
    board_state = game.get_board_state()
    current_player = game.current_player
    is_game_over = game.is_game_over()
    black_count, white_count = game.count_pieces()

    response = {
        'board': board_state,
        'currentPlayer': current_player,
        'isGameOver': is_game_over,
        'blackCount': black_count,
        'whiteCount': white_count
    }

    if is_game_over:
        winner = 'B' if black_count > white_count else 'W'
        response['winner'] = winner

    return jsonify(response)


@app.route('/move', methods=['POST'])
def move():
    data = request.json
    x, y = data['x'], data['y']
    # 首先，处理玩家落子
    success, message = game.make_move(x, y)
    if not success:
        return jsonify({'success': success, 'message': message}), 400

    response_data = {'success': True, 'gameOver': game.is_game_over()}

    # 返回游戏状态
    return jsonify(response_data)
@app.route('/ai_move', methods=['POST'])
def ai_move():
    response_data = {'success': True, 'gameOver': game.is_game_over()}
    # 如果是人机模式，并且游戏没有结束，接着让AI执行落子
    if game.game_mode == "ai" and not response_data['gameOver']:
        start_time = time.time()  # 开始计时
        ai_success, ai_message = minimax_make_move(game)  # 假设这个函数执行AI落子，并返回结果
        end_time = time.time()  # 结束计时
        move_time = end_time - start_time  # 计算AI落子所需时间
        if not ai_success:
            return jsonify({'success': ai_success,
                            'message': ai_message}), 400
        response_data['aiMove'] = True  # 可选，告诉前端AI已经落子
        response_data['gameOver'] = game.is_game_over()  # 再次检查游戏是否结束
        response_data['moveTime']=move_time

    # 返回游戏状态
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
