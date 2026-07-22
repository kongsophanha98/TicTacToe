# Tic-Tac-Toe ROS2 Project 
# Tic-Tac-Toe ROS 2 Game

A multi-node Tic-Tac-Toe game developed as a ROS 2 application, featuring a game engine, automated/interactive players, and visualizer nodes integrated with RViz2.

## Project Structure

* **`launch/`**: Contains Python launch files (`game.launch.py`) to spin up the entire system.
* **`tictactoe_game/`**: Core Python package containing:
  * `engine.py`: Manages game state, turn-taking, and win/draw condition checks.
  * `player.py`: Handles player logic and move inputs.
  * `visualizer.py`: Publishes board state and visualization markers for RViz2.
* **`resource/`**: Package resource markers.
* **`test/`**: Automated code style and copyright test configurations.

## Prerequisites

* **ROS 2** (Humble / Iron / Rolling / Jazzy)
* **Python 3**
* **RViz2**

## Building and Running

1. Navigate to your workspace directory:
   ```bash
   cd ~/tictactoe_ws
##Colcon building : 
colcon build --packages-select tictactoe_game
##Source your workspace environment:
source install/setup.bash
##Launch the game and RViz2 visualizer:
ros2 launch tictactoe_game game.launch.py
