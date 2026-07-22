from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tictactoe_game',
            executable='engine',
            name='game_engine',
            output='screen'
        ),
        Node(
            package='tictactoe_game',
            executable='visualizer',
            name='board_visualizer',
            output='screen'
        ),
        ExecuteProcess(
            cmd=['rviz2'],
            output='screen'
        )
    ])
