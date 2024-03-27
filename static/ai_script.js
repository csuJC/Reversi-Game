document.getElementById('restart-button').addEventListener('click', function() {
    window.location.href = '/ai'; // 重定向到AI对战模式的URL
});


document.addEventListener('DOMContentLoaded', function() {
    const boardElement = document.getElementById('board');
    createBoard(boardElement);
    updateBoard(); // 初始化棋盘状态
    updateLegalMoves();  // 显示初始合法落子点

    let totalTime = 0;  // 用于累计AI的总用时





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

    function updateBoard() {
        fetch('/board')
        .then(response => response.json())
        .then(data => {
            const board = data.board;
            const currentPlayer = data.currentPlayer; // 从响应中获取当前玩家
            document.getElementById('status').innerText = `当前玩家: ${currentPlayer === 'B' ? '黑色' : '白色'}`;

            const [black, white] = countPieces(board);
            document.getElementById('piece-count').innerText = `黑棋: ${black} 白棋: ${white}`;
            const boardElement = document.getElementById('board');

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
            // if (data.success) {

            updateBoard();  // 更新棋盘状态
            updateLegalMoves();  // 更新合法落子点

            fetch('/ai_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ x: x, y: y }),
            })
            .then(response => response.json())
            .then(data => {
                // if (data.success) {
                const moveTime = parseFloat(data.moveTime.toFixed(2));  // 确保是数字类型
                updateBoard();  // 更新棋盘状态
                updateLegalMoves();  // 更新合法落子点
                totalTime += moveTime;  // 累加总时间
                document.getElementById('ai-move-time').innerText = `AI本次落子用时: ${moveTime}秒`;
                document.getElementById('ai-total-time').innerText = `AI总用时: ${totalTime.toFixed(2)}秒`;
                 unlockBoard(); // AI落子后解锁棋盘，允许玩家落子
            })
            .catch((error) => {
                console.error('Error:', error);

        });


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

});



