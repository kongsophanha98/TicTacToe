import rclpy
from rclpy.node import Node
from tictactoe_interfaces.msg import TicTacToeMove
import threading
import os

class PlayerNode(Node):
    def __init__(self):
        super().__init__('player_node')
        self.declare_parameter('symbol', 'X')
        self.symbol = self.get_parameter('symbol').value
        self.publisher_ = self.create_publisher(TicTacToeMove, '/move_requests', 10)
        self.subscription = self.create_subscription(TicTacToeMove, '/game_state', self.render_board, 10)
        self.last_status = "ONGOING"
        self.get_logger().info(f"You are playing as {self.symbol}. Keys 1-9 to move.")
        self.input_thread = threading.Thread(target=self.keyboard_loop, daemon=True)
        self.input_thread.start()

    def render_board(self, msg):
        self.last_status = msg.game_status
        b = msg.board_state
        
        # Clears the terminal so the board stays in one place
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"--- GAME STATUS: {msg.game_status} ---")
        print(f" {b[0]} | {b[1]} | {b[2]} \t 1 | 2 | 3")
        print("---|---|---\t---|---|---")
        print(f" {b[3]} | {b[4]} | {b[5]} \t 4 | 5 | 6")
        print("---|---|---\t---|---|---")
        print(f" {b[6]} | {b[7]} | {b[8]} \t 7 | 8 | 9\n")
        
        if msg.game_status == "WIN":
            print(f">>> {msg.winner} WINS! <<<")
            print("Do you want to continue? (Y/N):")
        elif msg.game_status == "DRAW":
            print(f">>> {msg.winner} <<<")
            print("Do you want to continue? (Y/N):")
        elif msg.game_status == f"CONFIRM_LEAVE_{self.symbol}":
            print("Are you sure you want to leave? (Y/N):")
        elif msg.game_status.startswith("CONFIRM_LEAVE_"):
            print("Waiting for the other player to decide whether they're really leaving...")
        elif msg.game_status == "ENDED":
            print(f">>> {msg.winner} <<<")
            print("Game session closed. Thanks for playing! (Ctrl+C to exit)")
        else:
            if msg.player_symbol == self.symbol:
                print("YOUR TURN! Press 1-9:")
            else:
                print(f"Waiting for Player {msg.player_symbol} to move...")

    def keyboard_loop(self):
        while rclpy.ok():
            try:
                line = input().strip().lower()
                if self.last_status in ("WIN", "DRAW"):
                    if line == 'y':
                        self.send(0)
                    elif line == 'n':
                        self.send(-1)
                elif self.last_status == f"CONFIRM_LEAVE_{self.symbol}":
                    if line == 'y':
                        self.send(-2)
                    elif line == 'n':
                        self.send(-3)
                elif self.last_status.startswith("CONFIRM_LEAVE_"):
                    pass 
                elif self.last_status == "ONGOING":
                    if line.isdigit() and 1 <= int(line) <= 9:
                        self.send(int(line))
            except EOFError:
                break

    def send(self, cell):
        msg = TicTacToeMove()
        msg.player_symbol = self.symbol
        msg.selected_cell = cell
        self.publisher_.publish(msg)

def main():
    rclpy.init()
    node = PlayerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
