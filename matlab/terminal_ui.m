% terminal_ui.m - Member 3: Terminal UI Layout

function terminal_ui()
    fprintf('================================\n');
    fprintf('       TIC TAC TOE - ROS2       \n');
    fprintf('================================\n\n');
end

function print_board(board_state)
    symbols = {' ', 'X', 'O'};
    fprintf('  1 | 2 | 3  \n');
    fprintf(' -----------\n');
    fprintf('  %s | %s | %s  \n', symbols{board_state(1)+1}, symbols{board_state(2)+1}, symbols{board_state(3)+1});
    fprintf(' -----------\n');
    fprintf('  4 | 5 | 6  \n');
    fprintf(' -----------\n');
    fprintf('  %s | %s | %s  \n', symbols{board_state(4)+1}, symbols{board_state(5)+1}, symbols{board_state(6)+1});
    fprintf(' -----------\n');
    fprintf('  7 | 8 | 9  \n');
    fprintf(' -----------\n');
    fprintf('  %s | %s | %s  \n', symbols{board_state(7)+1}, symbols{board_state(8)+1}, symbols{board_state(9)+1});
    fprintf(' -----------\n\n');
end

function print_status(player, cell, status, winner)
    fprintf('Player: %s\n', player);
    fprintf('Selected Cell: %d\n', cell);
    fprintf('Game Status: %s\n', status);
    if ~strcmp(winner, 'NONE')
        fprintf('Winner: %s\n', winner);
    end
    fprintf('\n');
end

function print_footer(status, winner)
    fprintf('================================\n');
    if strcmp(status, 'WIN')
        fprintf('   GAME OVER! Winner: %s\n', winner);
    elseif strcmp(status, 'DRAW')
        fprintf('      GAME OVER! Its a Draw!\n');
    else