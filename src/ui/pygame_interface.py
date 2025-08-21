"""PyGame GUI interface for chess game."""

import pygame
import sys
import os
from typing import Optional, Tuple, List
from ..game.game_loop import get_current_player, get_game_status, get_legal_moves
from ..game.board_state import get_board_fen


# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 640  # Leave space for UI elements
SQUARE_SIZE = BOARD_SIZE // 8
BOARD_OFFSET_X = (WINDOW_SIZE - BOARD_SIZE) // 2
BOARD_OFFSET_Y = 50  # Leave space at top for status

# Colors
WHITE_SQUARE = (240, 217, 181)
BLACK_SQUARE = (181, 136, 99)
SELECTED_SQUARE = (255, 255, 0, 128)  # Yellow with transparency
LEGAL_MOVE_HIGHLIGHT = (0, 255, 0, 128)  # Green with transparency
BACKGROUND = (49, 46, 43)
TEXT_COLOR = (255, 255, 255)


class ChessboardRenderer:
    """Handles rendering the chess board and visual elements."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.selected_square = None
        self.legal_moves = []
    
    def draw_board(self):
        """Draw the chess board squares."""
        for row in range(8):
            for col in range(8):
                # Calculate square position
                x = BOARD_OFFSET_X + col * SQUARE_SIZE
                y = BOARD_OFFSET_Y + row * SQUARE_SIZE
                
                # Determine square color (light/dark)
                is_light_square = (row + col) % 2 == 0
                color = WHITE_SQUARE if is_light_square else BLACK_SQUARE
                
                # Draw square
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
    
    def draw_coordinates(self):
        """Draw file and rank labels around the board."""
        font = pygame.font.Font(None, 24)
        
        # Draw files (a-h) at bottom
        for col in range(8):
            file_letter = chr(ord('a') + col)
            x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = BOARD_OFFSET_Y + BOARD_SIZE + 10
            
            text = font.render(file_letter, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
        
        # Draw ranks (1-8) on left side
        for row in range(8):
            rank_number = str(8 - row)  # Chess board is numbered 8-1 from top to bottom
            x = BOARD_OFFSET_X - 20
            y = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
            
            text = font.render(rank_number, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
    
    def draw_selection_highlight(self):
        """Draw highlight for selected square."""
        if self.selected_square:
            row, col = self.selected_square
            x = BOARD_OFFSET_X + col * SQUARE_SIZE
            y = BOARD_OFFSET_Y + row * SQUARE_SIZE
            
            # Create a surface with alpha for transparency
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(SELECTED_SQUARE)
            self.screen.blit(highlight_surface, (x, y))
    
    def draw_legal_move_highlights(self):
        """Draw highlights for legal moves from selected square."""
        for move_square in self.legal_moves:
            row, col = move_square
            x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
            
            # Draw a small circle to indicate legal move
            pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 10)
    
    def set_selected_square(self, square: Optional[Tuple[int, int]]):
        """Set the currently selected square."""
        self.selected_square = square
    
    def set_legal_moves(self, moves: List[Tuple[int, int]]):
        """Set the list of legal move squares to highlight."""
        self.legal_moves = moves


class PieceAssets:
    """Manages loading and rendering chess pieces."""
    
    def __init__(self):
        self.pieces = {}
        self.load_pieces()
    
    def load_pieces(self):
        """Load piece images from assets directory or create text-based pieces."""
        # Try to load image files first, fall back to Unicode symbols
        piece_symbols = {
            'white': {'king': '♔', 'queen': '♕', 'rook': '♖', 'bishop': '♗', 'knight': '♘', 'pawn': '♙'},
            'black': {'king': '♚', 'queen': '♛', 'rook': '♜', 'bishop': '♝', 'knight': '♞', 'pawn': '♟'}
        }
        
        # Try to find a system font that supports chess symbols
        fonts_to_try = [
            None,  # Default font
            'arial unicode ms',  # Windows
            'noto sans symbols',  # Linux
            'apple symbols',  # macOS
        ]
        
        chess_font = None
        for font_name in fonts_to_try:
            try:
                chess_font = pygame.font.SysFont(font_name, 60) if font_name else pygame.font.Font(None, 60)
                # Test if font can render chess symbols
                test_surface = chess_font.render('♔', True, (0, 0, 0))
                if test_surface.get_width() > 10:  # Valid rendering
                    break
            except:
                continue
        
        if chess_font is None:
            chess_font = pygame.font.Font(None, 60)
        
        # Create piece surfaces
        for color, pieces in piece_symbols.items():
            self.pieces[color] = {}
            for piece_type, symbol in pieces.items():
                # Create piece surface with shadow effect
                piece_color = (255, 255, 255) if color == 'white' else (0, 0, 0)
                shadow_color = (128, 128, 128)
                
                # Create shadow
                shadow_surface = chess_font.render(symbol, True, shadow_color)
                # Create main piece
                piece_surface = chess_font.render(symbol, True, piece_color)
                
                # Combine shadow and piece
                combined_surface = pygame.Surface((piece_surface.get_width() + 2, 
                                                piece_surface.get_height() + 2), 
                                                pygame.SRCALPHA)
                combined_surface.blit(shadow_surface, (2, 2))  # Shadow offset
                combined_surface.blit(piece_surface, (0, 0))   # Main piece
                
                self.pieces[color][piece_type] = combined_surface
    
    def get_piece_surface(self, piece_type: str, color: str) -> Optional[pygame.Surface]:
        """Get the surface for a specific piece."""
        return self.pieces.get(color, {}).get(piece_type)


class MouseHandler:
    """Handles mouse input and converts to chess coordinates."""
    
    @staticmethod
    def screen_to_board_coords(mouse_x: int, mouse_y: int) -> Optional[Tuple[int, int]]:
        """Convert screen coordinates to board coordinates (row, col)."""
        # Check if click is within board bounds
        if (BOARD_OFFSET_X <= mouse_x < BOARD_OFFSET_X + BOARD_SIZE and
            BOARD_OFFSET_Y <= mouse_y < BOARD_OFFSET_Y + BOARD_SIZE):
            
            col = (mouse_x - BOARD_OFFSET_X) // SQUARE_SIZE
            row = (mouse_y - BOARD_OFFSET_Y) // SQUARE_SIZE
            
            # Ensure coordinates are within valid range
            if 0 <= row < 8 and 0 <= col < 8:
                return (row, col)
        
        return None
    
    @staticmethod
    def board_coords_to_algebraic(row: int, col: int) -> str:
        """Convert board coordinates to algebraic notation (e.g., e4)."""
        file = chr(ord('a') + col)
        rank = str(8 - row)
        return file + rank


class GameGUI:
    """Main GUI class that coordinates all components."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("PyChessBot - Chess Game")
        self.clock = pygame.time.Clock()
        
        # Initialize components
        self.renderer = ChessboardRenderer(self.screen)
        self.pieces = PieceAssets()
        self.font = pygame.font.Font(None, 36)
        
        # Game state
        self.running = True
        self.selected_square = None
    
    def draw_status_bar(self, game):
        """Draw game status information at the top."""
        # Clear status area
        status_rect = pygame.Rect(0, 0, WINDOW_SIZE, BOARD_OFFSET_Y)
        pygame.draw.rect(self.screen, BACKGROUND, status_rect)
        
        # Get current game status
        current_player = get_current_player(game)
        game_status = get_game_status(game)
        
        # Create status text
        status_text = f"Turn: {current_player.title()}"
        if not game_status['active']:
            status_text = f"Game Over - {game_status['result']}"
        elif game_status.get('in_check'):
            status_text += " (Check!)"
        
        # Render and display status
        text_surface = self.font.render(status_text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, BOARD_OFFSET_Y // 2))
        self.screen.blit(text_surface, text_rect)
    
    def draw_pieces(self, game):
        """Draw all pieces on the board."""
        # Get board FEN and parse piece positions
        fen = get_board_fen(game['board'])
        board_part = fen.split()[0]  # Get just the piece placement part
        
        row = 0
        col = 0
        
        for char in board_part:
            if char == '/':
                row += 1
                col = 0
            elif char.isdigit():
                col += int(char)  # Skip empty squares
            else:
                # Determine piece type and color
                piece_type = self._get_piece_type(char)
                color = 'white' if char.isupper() else 'black'
                
                # Get piece surface and draw it
                piece_surface = self.pieces.get_piece_surface(piece_type, color)
                if piece_surface:
                    x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                    
                    piece_rect = piece_surface.get_rect(center=(x, y))
                    self.screen.blit(piece_surface, piece_rect)
                
                col += 1
    
    def _get_piece_type(self, fen_char: str) -> str:
        """Convert FEN character to piece type name."""
        piece_map = {
            'k': 'king', 'q': 'queen', 'r': 'rook',
            'b': 'bishop', 'n': 'knight', 'p': 'pawn'
        }
        return piece_map.get(fen_char.lower(), 'pawn')
    
    def handle_click(self, mouse_pos: Tuple[int, int], game) -> Optional[str]:
        """Handle mouse click and return move in SAN notation if valid."""
        board_coords = MouseHandler.screen_to_board_coords(*mouse_pos)
        
        if board_coords is None:
            return None
        
        row, col = board_coords
        algebraic_pos = MouseHandler.board_coords_to_algebraic(row, col)
        
        if self.selected_square is None:
            # First click - select a square
            self.selected_square = board_coords
            self.renderer.set_selected_square(board_coords)
            
            # Get legal moves for this square and highlight them
            legal_moves = self._get_legal_moves_for_square(game, algebraic_pos)
            legal_move_coords = []
            for move in legal_moves:
                move_row, move_col = self._algebraic_to_coords(move)
                legal_move_coords.append((move_row, move_col))
            
            self.renderer.set_legal_moves(legal_move_coords)
            return None
        else:
            # Second click - attempt to make a move
            from_square = MouseHandler.board_coords_to_algebraic(*self.selected_square)
            to_square = algebraic_pos
            
            # Clear selection
            self.selected_square = None
            self.renderer.set_selected_square(None)
            self.renderer.set_legal_moves([])
            
            # Check if this is the same square (deselect)
            if from_square == to_square:
                return None
            
            # Convert move to SAN notation using existing game logic
            return self._coords_to_san_move(game, from_square, to_square)
    
    def _get_legal_moves_for_square(self, game, square: str) -> List[str]:
        """Get legal moves from a specific square."""
        try:
            # Get all legal moves from the game
            legal_moves = get_legal_moves(game)
            
            # Filter moves that start from the specified square
            # This is a simplified approach - we'd need to enhance this
            # to properly parse SAN moves and identify source squares
            square_moves = []
            
            # For now, return empty list - this needs proper implementation
            # with SAN move parsing to identify source squares
            return square_moves
            
        except Exception:
            return []
    
    def _algebraic_to_coords(self, algebraic: str) -> Tuple[int, int]:
        """Convert algebraic notation to board coordinates."""
        if len(algebraic) >= 2:
            file = algebraic[0]
            rank = algebraic[1]
            col = ord(file) - ord('a')
            row = 8 - int(rank)
            return (row, col)
        return (0, 0)
    
    def _coords_to_san_move(self, game, from_square: str, to_square: str) -> str:
        """Convert coordinate move to SAN notation."""
        # For now, we'll try basic moves and let the existing validation handle it
        # This is a simplified approach that works for basic moves
        
        # Get the piece at the from_square
        board = game['board']
        
        try:
            # Convert to chess library format for processing
            import chess
            
            from_chess_square = chess.parse_square(from_square)
            to_chess_square = chess.parse_square(to_square)
            
            # Create a move object
            move = chess.Move(from_chess_square, to_chess_square)
            
            # Convert to SAN
            san_move = board.san(move)
            return san_move
            
        except Exception:
            # Fallback to basic move notation
            return to_square
    
    def render(self, game):
        """Render the complete game state."""
        # Clear screen
        self.screen.fill(BACKGROUND)
        
        # Draw all components
        self.draw_status_bar(game)
        self.renderer.draw_board()
        self.renderer.draw_coordinates()
        self.draw_pieces(game)
        self.renderer.draw_selection_highlight()
        self.renderer.draw_legal_move_highlights()
        
        # Update display
        pygame.display.flip()
    
    def handle_events(self, game) -> Optional[str]:
        """Handle pygame events and return move if one was made."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    return self.handle_click(event.pos, game)
        
        return None
    
    def is_running(self) -> bool:
        """Check if the GUI should continue running."""
        return self.running
    
    def quit(self):
        """Clean up and quit pygame."""
        pygame.quit()


def run_gui_game(game, ai, human_color='white'):
    """Run the chess game with PyGame GUI."""
    from ..game.game_loop import make_move, get_current_player, get_game_status
    from ..ai.stockfish_ai import get_ai_move, cleanup_ai
    
    gui = GameGUI()
    
    try:
        while gui.is_running():
            # Check if game is over
            game_status = get_game_status(game)
            if not game_status['active']:
                # Game is over, just render and wait for quit
                gui.render(game)
                gui.clock.tick(60)
                
                # Handle events (mainly quit)
                move_input = gui.handle_events(game)
                if move_input == "quit":
                    break
                continue
            
            # Determine whose turn it is
            current_player = get_current_player(game)
            
            if current_player == human_color:
                # Human turn - handle GUI events
                move_input = gui.handle_events(game)
                
                if move_input == "quit":
                    break
                elif move_input:
                    # Process human move
                    print(f"Human move: {move_input}")
                    move_result = make_move(game, move_input)
                    
                    if move_result['success']:
                        game = move_result['new_game']
                        print(f"Move successful: {move_input}")
                    else:
                        print(f"Invalid move: {move_result['error']}")
            else:
                # AI turn
                print("AI is thinking...")
                
                # Handle GUI events (but don't process moves)
                gui_event = gui.handle_events(game)
                if gui_event == "quit":
                    break
                
                # Get AI move
                try:
                    ai_move_result = get_ai_move(ai, game, time_limit=3.0)
                    
                    if ai_move_result['success']:
                        ai_move = ai_move_result['move']
                        print(f"AI plays: {ai_move}")
                        
                        move_result = make_move(game, ai_move)
                        
                        if move_result['success']:
                            game = move_result['new_game']
                        else:
                            print(f"AI made invalid move: {move_result['error']}")
                            break
                    else:
                        print(f"AI error: {ai_move_result['error']}")
                        break
                        
                except Exception as e:
                    print(f"AI turn failed: {str(e)}")
                    break
            
            # Render current state
            gui.render(game)
            gui.clock.tick(60)  # 60 FPS
    
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        cleanup_ai(ai)
        gui.quit()