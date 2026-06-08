% game.m - Main TicTacToe Game with ROS2

clear
clc

setenv('ROS_DOMAIN_ID', '7')

% Initialize board
board_state = int32(zeros(1,9));

% Print header
fprintf('================================\n');
fprintf('       TIC TAC TOE - ROS2       \n');
fprintf('================================\n\n');

fprintf('Board positions:\n');
fprintf(' 1 | 2 | 3 \n');
fprintf('---|---|---\n');
fprintf(' 4 | 5 | 6 \n');
fprintf('---|---|---\n');
fprintf(' 7 | 8 | 9 \n\n');

% Initialize ROS2
node = ros2node('game_node');
pub = ros2publisher(node, '/tictactoe/moves', 'tictactoe_msgs/TicTacToeMove');

msg = ros2message('tictactoe_msgs/TicTacToeMove');

% Game variables
players = {'X', 'O'};
player_vals = [1, 2];
turn = 1;
status = 'PLAYING';
winner = 'NONE';

% Game loop
while strcmp(status, 'PLAYING')
    cell = input(sprintf('Player %s, enter cell (1-9): ', players{turn}));
    
    if board_state(cell) ~= 0
        fprintf('Cell already taken! Try again.\n');
        continue;
    end
    
    % Update board
    board_state(cell) = int32(player_vals(turn));
    
    % Publish move
    msg.player_symbol = players{turn};
    msg.selected_cell = int32(cell);
    msg.board_state = board_state;
    msg.game_status = status;
    msg.winner = winner;
    send(pub, msg);
    
    % Display board
    print_board(board_state);
    
    % Check winner
    winner = check_winner(board_state);
    if strcmp(winner, 'X') || strcmp(winner, 'O')
        status = 'WIN';
    elseif strcmp(winner, 'DRAW')
        status = 'DRAW';
    end
    
    % Print footer
    fprintf('================================\n');
    if strcmp(status, 'WIN')
        fprintf('   GAME OVER! Winner: %s\n', winner);
        fprintf('================================\n');
    elseif strcmp(status, 'DRAW')
        fprintf('      GAME OVER! Its a Draw!\n');
        fprintf('================================\n');
    else
        fprintf('        Game in Progress...\n');
        fprintf('================================\n');
    end
    
    % Switch player
    turn = mod(turn, 2) + 1;
end

% Functions
function print_board(board_state)
    symbols = {' ', 'X', 'O'};
    fprintf('\n');
    fprintf(' %s | %s | %s \n', symbols{board_state(1)+1}, symbols{board_state(2)+1}, symbols{board_state(3)+1});
    fprintf('---|---|---\n');
    fprintf(' %s | %s | %s \n', symbols{board_state(4)+1}, symbols{board_state(5)+1}, symbols{board_state(6)+1});
    fprintf('---|---|---\n');
    fprintf(' %s | %s | %s \n', symbols{board_state(7)+1}, symbols{board_state(8)+1}, symbols{board_state(9)+1});
    fprintf('\n');
end

function result = check_winner(board_state)
    wins = [1,2,3; 4,5,6; 7,8,9; 1,4,7; 2,5,8; 3,6,9; 1,5,9; 3,5,7];
    result = 'NONE';
    for i = 1:size(wins,1)
        line = board_state(wins(i,:));
        if all(line == 1)
            result = 'X';
            return;
        elseif all(line == 2)
            result = 'O';
            return;
        end
    end
    if all(board_state ~= 0)
        result = 'DRAW';
    end
end