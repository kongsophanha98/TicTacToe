import rclpy
from rclpy.node import Node
from tictactoe_interfaces.msg import TicTacToeMove

class GameEngine(Node):
    def __init__(self):
        super().__init__('game_engine')
        self.publisher_ = self.create_publisher(TicTacToeMove, '/game_state', 10)
        self.subscription = self.create_subscription(TicTacToeMove, '/move_requests', self.handle_move, 10)
        self.board = [' '] * 9
        self.starting_player = 'X'
        self.current_turn = self.starting_player
        self.status = "ONGOING"
        self.winner = ""
        self.score = {'X': 0, 'O': 0, 'DRAW': 0}
        self.pending_responses = {}
        self.pre_confirm_status = None
        self.get_logger().info("Tic-Tac-Toe Engine Started. Waiting for moves...")
        self.publish_state()

    def handle_move(self, msg):
        if self.status in ("WIN", "DRAW") or self.status.startswith("CONFIRM_LEAVE_"):
            self.handle_continue_response(msg)
            return
        if self.status == "ENDED":
            return
        if msg.player_symbol != self.current_turn:
            return
        
        cell = msg.selected_cell - 1
        if cell < 0 or cell > 8 or self.board[cell] != ' ':
            return

        self.board[cell] = msg.player_symbol
        self.check_game_state()

        if self.status == "ONGOING":
            self.current_turn = 'O' if self.current_turn == 'X' else 'X'
        self.publish_state()

    def handle_continue_response(self, msg):
        symbol = msg.player_symbol
        cell = msg.selected_cell

        if self.status in ("WIN", "DRAW"):
            if cell == 0:  
                self.pending_responses[symbol] = 'Y'
                self.check_pending()
            elif cell == -1:  
                self.pre_confirm_status = self.status
                self.status = f"CONFIRM_LEAVE_{symbol}"
                self.publish_state()
            return

        if self.status.startswith("CONFIRM_LEAVE_"):
            confirming_symbol = self.status.split("_")[-1]
            if symbol != confirming_symbol:
                return  
            if cell == -2:  
                self.status = "ENDED"
                self.winner = f"GAME ENDED (Final Score X:{self.score['X']} O:{self.score['O']} D:{self.score['DRAW']})"
                self.publish_state()
            elif cell == -3:  
                self.pending_responses = {}
                self.status = self.pre_confirm_status
                self.pre_confirm_status = None
                self.publish_state()

    def check_pending(self):
        if {'X', 'O'}.issubset(self.pending_responses):
            self.reset_round()

    def reset_round(self):
        self.board = [' '] * 9
        self.starting_player = 'O' if self.starting_player == 'X' else 'X'
        self.current_turn = self.starting_player
        self.status = "ONGOING"
        self.winner = ""
        self.pending_responses = {}
        self.pre_confirm_status = None
        self.publish_state()

    def check_game_state(self):
        win_lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in win_lines:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                self.status = "WIN"
                winner_symbol = self.board[a]
                self.score[winner_symbol] += 1
                self.winner = f"{winner_symbol} (Score X:{self.score['X']} O:{self.score['O']} D:{self.score['DRAW']})"
                return
        if ' ' not in self.board:
            self.status = "DRAW"
            self.score['DRAW'] += 1
            self.winner = f"DRAW (Score X:{self.score['X']} O:{self.score['O']} D:{self.score['DRAW']})"

    def publish_state(self):
        msg = TicTacToeMove()
        msg.board_state = self.board
        msg.player_symbol = self.current_turn
        msg.game_status = self.status
        
        # SCOREBOARD HACK: Send current score string during ONGOING
        if self.status == "ONGOING":
            msg.winner = f"Score -> X: {self.score['X']} | O: {self.score['O']} | Draws: {self.score['DRAW']}"
        elif self.status.startswith("CONFIRM_LEAVE_"):
            msg.winner = "A player is deciding whether to leave..."
        else:
            msg.winner = self.winner
            
        self.publisher_.publish(msg)

def main():
    rclpy.init()
    node = GameEngine()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
