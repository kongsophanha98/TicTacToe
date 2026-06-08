% player_x.m - Player X Terminal
clear
clc
setenv('ROS_DOMAIN_ID', '7')

% Initialize ROS2
node = ros2node('player_x_node');
pub = ros2publisher(node, '/tictactoe/moves', 'tictactoe_msgs/TicTacToeMove');
sub = ros2subscriber(node, '/tictactoe/moves', 'tictactoe_msgs/TicTacToeMove');

msg = ros2message('tictactoe_msgs/TicTacToeMove');

% Initialize board
board_state = int32(zeros(1,9));

fprintf('================================\n');
fprintf('    TIC TAC TOE - Player X      \n');
fprintf('================================\n\n');
fprintf('Board positions:\n');
fprintf(' 1 | 2 | 3 \n');
fprintf('---|---|---\n');
fprintf(' 4 | 5 | 6 \n');
fprintf('---|---|---\n');
fprintf(' 7 | 8 | 9 \n\n');

status = 'PLAYING';
winner = 'NONE';

while strcmp(status, 'PLAYING')
    % Player X turn - input
    cell = input('Player X, enter cell (1-9): ');
    
    if board_state(cell) ~= 0
        fprintf('Cell already taken! Try again.\n');
        continue;
    end
    
    % Update board
    board_state(cell) = int32(1);
    
    % Publish move
    msg.player_symbol = 'X';
    msg.selected_cell = int32(cell);
    msg.board_state = board_state;
    msg.game_status = status;
    msg.winner = winner;
    send(pub, msg);
    
    % Display board
    print_board(board_state);
    
    % Check winner
    winner = check_winner(board_state);
    if strcmp(winner, 'X')
        fprintf('================================\n');
        fprintf('   GAME OVER! Player X Wins!\n');
        fprintf('================================\n');
        status = 'WIN';
        break;
    elseif strcmp(winner, 'DRAW')
        fprintf('================================\n');
        fprintf('      GAME OVER! Its a Draw!\n');
        fprintf('================================\n');
        status = 'DRAW';
        break;
    end
    
    fprintf('Waiting for Player O...\n');
    
    % Wait for Player O move
    received = false;
    while ~received
        try
            omsg = receive(sub, 30);
            if strcmp(omsg.player_symbol, 'O')
                board_state = omsg.board_state;
                fprintf('\nPlayer O played cell %d\n', omsg.selected_cell);
                print_board(board_state);
                
                winner = check_winner(board_state);
                if strcmp(winner, 'O')
                    fprintf('================================\n');
                    fprintf('   GAME OVER! Player O Wins!\n');
                    fprintf('================================\n');
                    status = 'WIN';
                end
                received = true;
            end
        catch
            fprintf('Still waiting...\n');
        end
    end
end

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