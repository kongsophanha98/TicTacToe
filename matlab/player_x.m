% player_x.m - Member 2: Publisher Node
% Player X publishes moves to the TicTacToe topic

clear
clc

% Initialize ROS 2 node
node = ros2node('player_x_node');

% Create publisher
pub = ros2publisher(node, '/tictactoe/moves', 'tictactoe_msgs/TicTacToeMove');

% Create message
msg = ros2message('tictactoe_msgs/TicTacToeMove');

% Set player
msg.player_symbol = 'X';
msg.game_status = 'PLAYING';
msg.winner = 'NONE';

% Test moves
cells = [1, 5, 9];

for i = 1:length(cells)
    msg.selected_cell = int32(cells(i));
    msg.board_state(cells(i)) = int32(1);
    
    send(pub, msg);
    
    fprintf('Publishing Move...\n');
    fprintf('Player: %s\n', msg.player_symbol);
    fprintf('Cell: %d\n\n', msg.selected_cell);
    
    pause(1);
end

fprintf('Done publishing!\n');