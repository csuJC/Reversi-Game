document.addEventListener('DOMContentLoaded', function () {
    const boardElement = document.getElementById('board');
    createBoard(boardElement);
    updateBoard();
    updateLegalMoves();  // 显示初始合法落子点

    function createBoard(board) {
        board.innerHTML = ''; // 清空棋盘
        for (let i = 0; i < 64; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.index = i;
            cell.addEventListener('click', () => makeMove(Math.floor(i / 8), i % 8));
            board.appendChild(cell);
        }
    }

    function makeMove(x, y) {

        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ x: x, y: y }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateBoard();  // 更新棋盘状态
                updateLegalMoves();  // 更新合法落子点
            } else {
                alert(data.message);  // 落子非法时的提示
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function countPieces(board) {
        let black = 0, white = 0;
        board.forEach(row => {
            row.forEach(cell => {
                if (cell === 'B') black++;
                if (cell === 'W') white++;
            });
        });
        return [black, white];
    }

    function updateLegalMoves() {
        fetch('/legal_moves')
        .then(response => response.json())
        .then(data => {
            const legalMoves = data.legalMoves;
            const cells = document.querySelectorAll('.cell');
            cells.forEach((cell, index) => {
                const x = Math.floor(index / 8);
                const y = index % 8;
                // 移除旧的小灰点
                cell.classList.remove('legal-move');
                // 如果是合法落子点，添加小灰点
                if (legalMoves.some(move => move[0] === x && move[1] === y)) {
                    cell.classList.add('legal-move');
                }
            });
        })
        .catch(error => console.error('Error updating legal moves:', error));
    }

// 你可能需要在游戏的关键时刻调用updateLegalMoves函数，比如游戏开始、玩家落子后等


    function updateBoard() {
        fetch('/board')
        .then(response => response.json())
        .then(data => {
            const board = data.board;
            const currentPlayer = data.currentPlayer; // 从响应中获取当前玩家
            document.getElementById('status').innerText = `当前玩家: ${currentPlayer === 'B' ? '黑色' : '白色'}`;

            const [black, white] = countPieces(board);
            document.getElementById('piece-count').innerText = `黑棋: ${black} 白棋: ${white}`;

            for (let i = 0; i < 64; i++) {
                const cell = boardElement.children[i];
                const x = Math.floor(i / 8);
                const y = i % 8;
                cell.innerHTML = ''; // 清空当前格子
                if (board[x][y]) {
                    const piece = document.createElement('div');
                    piece.className = 'piece';
                    piece.style.backgroundColor = board[x][y] === 'B' ? 'black' : 'white';
                    cell.appendChild(piece);
                }
            }
            // 在updateBoard函数中添加处理游戏结束的逻辑
            if (data.isGameOver) {
                const message = `游戏结束，${data.winner === 'B' ? '黑棋胜' : '白棋胜'}。黑棋: ${data.blackCount}, 白棋: ${data.whiteCount}`;
                alert(message);
                // 可以在这里禁用棋盘，阻止玩家继续落子
            }

        })
        .catch(error => console.error('Error updating board:', error));
    }
});
