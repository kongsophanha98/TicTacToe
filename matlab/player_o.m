% player_o.m - Member 3: Subscriber Node
% Player O subscribes and receives moves from the TicTacToe topic

clear
clc

setenv('ROS_DOMAIN_ID', '7')

% Initialize ROS 2 node
node = ros2node('player_o_node');

% Create subscriber
sub = ros2subscriber(node, '/tictactoe/moves', 'tictactoe_msgs/TicTacToeMove');

fprintf('Waiting for messages...\n\n');

% Receive 3 messages
for i = 1:3
    msg = receive(sub, 30);
    
    fprintf('Message Received!\n');
    fprintf('Player: %s\n', msg.player_symbol);
    fprintf('Cell: %d\n', msg.selected_cell);
    fprintf('Game Status: %s\n\n', msg.game_status);
end

fprintf('Done receiving!\n');