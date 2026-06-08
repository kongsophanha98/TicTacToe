% board.m - Member 2: Board Representation and Game Flow

function board_state = init_board()
    board_state = int32(zeros(1,9));
end

function display_board(board_state)
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