import rclpy
from rclpy.node import Node
from tictactoe_interfaces.msg import TicTacToeMove
from visualization_msgs.msg import Marker, MarkerArray
import math

class BoardVisualizer(Node):
    def __init__(self):
        super().__init__('board_visualizer')
        self.subscription = self.create_subscription(
            TicTacToeMove, '/game_state', self.state_callback, 10)
        self.publisher = self.create_publisher(MarkerArray, '/visualization_marker_array', 10)
        self.get_logger().info('3D Visualizer Node Started (Flat Scoreboard)')

    def state_callback(self, msg):
        marker_array = MarkerArray()
        
        # 1. Thick Wooden Board Base
        board = Marker()
        board.header.frame_id = "map"
        board.header.stamp = self.get_clock().now().to_msg()
        board.ns = "board"
        board.id = 99
        board.type = Marker.CUBE
        board.action = Marker.ADD
        board.pose.position.x = 0.0
        board.pose.position.y = 0.0
        board.pose.position.z = -0.2  
        board.scale.x = 3.2
        board.scale.y = 3.2
        board.scale.z = 0.4   
        board.color.r = 0.55  
        board.color.g = 0.27
        board.color.b = 0.07
        board.color.a = 1.0
        marker_array.markers.append(board)

        # 2. Draw the 3x3 Grid Lines
        lines_coords = [
            (0.0, 0.5, 3.2, 0.05),   
            (0.0, -0.5, 3.2, 0.05),  
            (0.5, 0.0, 0.05, 3.2),   
            (-0.5, 0.0, 0.05, 3.2)   
        ]
        for idx, (lx, ly, sx, sy) in enumerate(lines_coords):
            line = Marker()
            line.header.frame_id = "map"
            line.header.stamp = self.get_clock().now().to_msg()
            line.ns = "grid_lines"
            line.id = 100 + idx
            line.type = Marker.CUBE
            line.action = Marker.ADD
            line.pose.position.x = lx
            line.pose.position.y = ly
            line.pose.position.z = 0.01  
            line.scale.x = sx
            line.scale.y = sy
            line.scale.z = 0.02
            line.color.r = 0.15 
            line.color.g = 0.08
            line.color.b = 0.02
            line.color.a = 1.0
            marker_array.markers.append(line)

        # 3. Game Pieces
        coords = [
            (-1, 1),  (0, 1),  (1, 1),
            (-1, 0),  (0, 0),  (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]
        
        for i, cell in enumerate(msg.board_state):
            m1 = Marker()
            m1.header.frame_id = "map"
            m1.header.stamp = self.get_clock().now().to_msg()
            m1.ns = "pieces"
            m1.id = i
            
            m2 = Marker()
            m2.header.frame_id = "map"
            m2.header.stamp = self.get_clock().now().to_msg()
            m2.ns = "pieces_extra"
            m2.id = i + 20 
            
            if cell == 'X':
                m1.action = Marker.ADD
                m1.type = Marker.CUBE
                m1.pose.position.x = float(coords[i][0])
                m1.pose.position.y = float(coords[i][1])
                m1.pose.position.z = 0.15  
                m1.pose.orientation.z = math.sin(math.pi / 8) 
                m1.pose.orientation.w = math.cos(math.pi / 8)
                m1.scale.x = 0.7
                m1.scale.y = 0.15
                m1.scale.z = 0.3  
                m1.color.r, m1.color.g, m1.color.b, m1.color.a = 0.0, 0.5, 1.0, 1.0

                m2.action = Marker.ADD
                m2.type = Marker.CUBE
                m2.pose.position.x = float(coords[i][0])
                m2.pose.position.y = float(coords[i][1])
                m2.pose.position.z = 0.15
                m2.pose.orientation.z = math.sin(-math.pi / 8)
                m2.pose.orientation.w = math.cos(-math.pi / 8)
                m2.scale.x = 0.7
                m2.scale.y = 0.15
                m2.scale.z = 0.3
                m2.color.r, m2.color.g, m2.color.b, m2.color.a = 0.0, 0.5, 1.0, 1.0
                
                marker_array.markers.append(m1)
                marker_array.markers.append(m2)

            elif cell == 'O':
                m1.action = Marker.ADD
                m1.type = Marker.CYLINDER
                m1.pose.position.x = float(coords[i][0])
                m1.pose.position.y = float(coords[i][1])
                m1.pose.position.z = 0.15  
                m1.scale.x = 0.7
                m1.scale.y = 0.7
                m1.scale.z = 0.3  
                m1.color.r, m1.color.g, m1.color.b, m1.color.a = 1.0, 0.0, 0.0, 1.0
                
                m2.action = Marker.DELETE 
                marker_array.markers.append(m1)
                marker_array.markers.append(m2)
                
            else:
                m1.action = Marker.DELETE
                m2.action = Marker.DELETE
                marker_array.markers.append(m1)
                marker_array.markers.append(m2)
                
        # 4. Scoreboard (Flat on the table, parallel to the board)
        
        # Jumbotron Base Plate (Dark screen)
        screen = Marker()
        screen.header.frame_id = "map"
        screen.header.stamp = self.get_clock().now().to_msg()
        screen.ns = "scoreboard_base"
        screen.id = 50
        screen.type = Marker.CUBE
        screen.action = Marker.ADD
        screen.pose.position.x = 0.0
        screen.pose.position.y = 3.0   # Placed directly behind the board
        screen.pose.position.z = -0.05 # Laying flat, flush with the table
        screen.scale.x = 11.0  # Width
        screen.scale.y = 2.0   # Depth
        screen.scale.z = 0.1   # Thickness (flat)
        screen.color.r, screen.color.g, screen.color.b, screen.color.a = 0.1, 0.1, 0.15, 1.0
        marker_array.markers.append(screen)

        # Jumbotron Gold Frame
        frame = Marker()
        frame.header.frame_id = "map"
        frame.header.stamp = self.get_clock().now().to_msg()
        frame.ns = "scoreboard_base"
        frame.id = 51
        frame.type = Marker.CUBE
        frame.action = Marker.ADD
        frame.pose.position.x = 0.0
        frame.pose.position.y = 3.0   
        frame.pose.position.z = -0.08  
        frame.scale.x = 11.3  # Width 
        frame.scale.y = 2.3   # Depth
        frame.scale.z = 0.1   # Thickness (flat)
        frame.color.r, frame.color.g, frame.color.b, frame.color.a = 0.8, 0.6, 0.0, 1.0 
        marker_array.markers.append(frame)

        # Turn Indicator Text
        turn_text = Marker()
        turn_text.header.frame_id = "map"
        turn_text.header.stamp = self.get_clock().now().to_msg()
        turn_text.ns = "scoreboard_text"
        turn_text.id = 52
        turn_text.type = Marker.TEXT_VIEW_FACING
        turn_text.action = Marker.ADD
        turn_text.pose.position.x = 0.0
        turn_text.pose.position.y = 3.4  # Spaced further back
        turn_text.pose.position.z = 0.3  # High enough to NEVER clip into the floor
        turn_text.scale.z = 0.45 
        
        # Score Tracker Text
        score_text = Marker()
        score_text.header.frame_id = "map"
        score_text.header.stamp = self.get_clock().now().to_msg()
        score_text.ns = "scoreboard_text"
        score_text.id = 53
        score_text.type = Marker.TEXT_VIEW_FACING
        score_text.action = Marker.ADD
        score_text.pose.position.x = 0.0
        score_text.pose.position.y = 2.6  # Spaced closer to the board
        score_text.pose.position.z = 0.3  # High enough to NEVER clip into the floor
        score_text.scale.z = 0.35 

        # Style text based on game state
        if msg.game_status == "ONGOING":
            turn_text.text = f"<<< Player {msg.player_symbol}'s Turn >>>"
            turn_text.color.r, turn_text.color.g, turn_text.color.b, turn_text.color.a = 1.0, 0.8, 0.0, 1.0 # Gold
            
            score_text.text = msg.winner 
            score_text.color.r, score_text.color.g, score_text.color.b, score_text.color.a = 0.0, 1.0, 1.0, 1.0 # Cyan
            
        elif msg.game_status in ("WIN", "DRAW"):
            turn_text.text = f"*** {msg.game_status}! ***"
            turn_text.color.r, turn_text.color.g, turn_text.color.b, turn_text.color.a = 0.0, 1.0, 0.0, 1.0 # Neon Green
            
            score_text.text = msg.winner
            score_text.color.r, score_text.color.g, score_text.color.b, score_text.color.a = 1.0, 1.0, 1.0, 1.0 # White
        else:
            turn_text.text = "System Message"
            turn_text.color.r, turn_text.color.g, turn_text.color.b, turn_text.color.a = 1.0, 0.5, 0.0, 1.0 # Orange
            
            score_text.text = msg.winner
            score_text.color.r, score_text.color.g, score_text.color.b, score_text.color.a = 1.0, 1.0, 1.0, 1.0

        marker_array.markers.append(turn_text)
        marker_array.markers.append(score_text)

        self.publisher.publish(marker_array)

def main():
    rclpy.init()
    node = BoardVisualizer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
