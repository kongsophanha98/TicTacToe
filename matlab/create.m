% Step 1: Create the folder structure
cd 'C:\Users\U-ser\Documents\MATLAB'
genDir = fullfile(pwd,'ros2CustomMessages');
packagePath = fullfile(genDir,'tictactoe_msgs');
mkdir(packagePath)
mkdir(fullfile(packagePath,'msg'))

% Step 2: Create the message file
fileID = fopen(fullfile(packagePath,'msg','TicTacToeMove.msg'),'w');
fprintf(fileID,'%s\n','int32[9] board_state','string player_symbol','int32 selected_cell','string game_status','string winner');
fclose(fileID);

% Step 3: Generate the message
ros2genmsg(genDir,CreateShareableFile=true);

% Step 4: Verify
ros2message('tictactoe_msgs/TicTacToeMove')