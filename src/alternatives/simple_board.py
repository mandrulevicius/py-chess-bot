"""Simple board state implementation - basic chess board without external dependencies."""

from typing import Any, Dict, List, Tuple
from ..core.interfaces import ChessBoardState


class SimpleBoard:
    """
    Simplified chess board representation.
    
    This is a basic implementation for demonstration purposes.
    It doesn't implement full chess rules but provides the interface.
    """
    
    def __init__(self):
        # 8x8 board, None = empty square
        # Pieces represented as strings: 'wK' = white king, 'bq' = black queen, etc.
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.to_move = 'white'
        self.move_count = 0
        self._setup_initial_position()
    
    def _setup_initial_position(self):
        """Set up initial chess position."""
        # White pieces (row 0 and 1)
        pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for col in range(8):
            self.board[0][col] = f'w{pieces[col]}'  # White back rank
            self.board[1][col] = 'wP'  # White pawns
            self.board[6][col] = 'bP'  # Black pawns  
            self.board[7][col] = f'b{pieces[col]}'  # Black back rank
    
    def copy(self):
        """Create a copy of the board."""
        new_board = SimpleBoard()
        new_board.board = [row[:] for row in self.board]
        new_board.to_move = self.to_move
        new_board.move_count = self.move_count
        return new_board
    
    def get_fen(self) -> str:
        """Get FEN representation (simplified)."""
        # This is a very basic FEN implementation
        fen_pieces = []
        
        for row in reversed(self.board):  # FEN starts from rank 8
            empty_count = 0
            row_str = ""
            
            for piece in row:
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0
                    # Convert piece format: 'wK' -> 'K', 'bK' -> 'k'
                    piece_char = piece[1]
                    if piece[0] == 'b':
                        piece_char = piece_char.lower()
                    row_str += piece_char
            
            if empty_count > 0:
                row_str += str(empty_count)
            
            fen_pieces.append(row_str)
        
        board_fen = '/'.join(fen_pieces)
        to_move = 'w' if self.to_move == 'white' else 'b'
        return f"{board_fen} {to_move} - - 0 {self.move_count}"
    
    def _parse_algebraic_move(self, move: str) -> Tuple[int, int, int, int]:
        """Parse algebraic notation to board coordinates (simplified)."""
        # This is a very basic parser - real implementation would be much more complex
        move = move.strip()
        
        if len(move) == 2:  # Pawn move like 'e4'
            col = ord(move[0]) - ord('a')
            row = int(move[1]) - 1
            # Assume pawn move from 2nd/7th rank
            if self.to_move == 'white':
                from_row = 1 if row == 3 else 1  # Simplified
            else:
                from_row = 6 if row == 4 else 6
            return (from_row, col, row, col)
        
        # Default fallback (not a real parser)
        return (1, 4, 3, 4)  # e2-e4


class SimpleBoardState(ChessBoardState):
    """Simple board state implementation."""
    
    def create_initial_board(self) -> Any:
        """Create initial chess board position."""
        return SimpleBoard()
    
    def make_move(self, board: Any, move: str) -> Tuple[Any, Dict[str, Any]]:
        """Make a move and return new board state."""
        if not isinstance(board, SimpleBoard):
            raise ValueError("Invalid board type")
        
        new_board = board.copy()
        
        try:
            # Parse and make move (very simplified)
            from_row, from_col, to_row, to_col = new_board._parse_algebraic_move(move)
            
            # Move the piece
            piece = new_board.board[from_row][from_col]
            new_board.board[to_row][to_col] = piece
            new_board.board[from_row][from_col] = None
            
            # Switch turns
            new_board.to_move = 'black' if new_board.to_move == 'white' else 'white'
            new_board.move_count += 1
            
            move_info = {
                'move': move,
                'valid': True,
                'capture': False,  # Simplified
                'check': False,    # Simplified
                'checkmate': False  # Simplified
            }
            
            return new_board, move_info
        
        except Exception as e:
            return board, {
                'move': move,
                'valid': False,
                'error': str(e)
            }
    
    def get_board_fen(self, board: Any) -> str:
        """Get FEN representation of board."""
        if isinstance(board, SimpleBoard):
            return board.get_fen()
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"  # Starting position
    
    def is_checkmate(self, board: Any) -> bool:
        """Check if position is checkmate (simplified)."""
        return False  # Simplified implementation
    
    def is_stalemate(self, board: Any) -> bool:
        """Check if position is stalemate (simplified)."""
        return False  # Simplified implementation


# Register with factory
from ..core.interfaces import ComponentFactory
ComponentFactory.register_board_state('simple', SimpleBoardState)