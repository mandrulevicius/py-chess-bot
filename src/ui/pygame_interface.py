"""PyGame GUI interface for chess game."""

import pygame
import sys
import os
from typing import Optional, Tuple, List
from ..game.game_loop import get_current_player, get_game_status, get_legal_moves
from ..game.board_state import get_board_fen
from .sound_manager import get_sound_manager
from .learning_gui import EvaluationDisplay, SoloModeIndicator, HelpDisplay, LearningButtonPanel


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

# Setup UI Colors
SETUP_BACKGROUND = (40, 40, 40)
SETUP_PANEL = (60, 60, 60)
BUTTON_COLOR = (80, 80, 80)
BUTTON_HOVER = (100, 100, 100)
BUTTON_ACTIVE = (120, 120, 120)
SLIDER_TRACK = (70, 70, 70)
SLIDER_HANDLE = (150, 150, 150)
ACCENT_COLOR = (100, 149, 237)  # Cornflower blue


class ChessboardRenderer:
    """Handles rendering the chess board and visual elements."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.selected_square = None
        self.legal_moves = []
        self.flipped = False  # Whether board should be flipped (black at bottom)
    
    def draw_board(self):
        """Draw the chess board squares."""
        for row in range(8):
            for col in range(8):
                # Calculate square position
                display_row = 7 - row if self.flipped else row
                x = BOARD_OFFSET_X + col * SQUARE_SIZE
                y = BOARD_OFFSET_Y + display_row * SQUARE_SIZE
                
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
            if self.flipped:
                rank_number = str(row + 1)  # When flipped, show 1-8 from top to bottom
            else:
                rank_number = str(8 - row)  # Normal: 8-1 from top to bottom
            x = BOARD_OFFSET_X - 20
            y = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
            
            text = font.render(rank_number, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
    
    def draw_selection_highlight(self):
        """Draw highlight for selected square."""
        if self.selected_square:
            row, col = self.selected_square
            display_row = 7 - row if self.flipped else row
            x = BOARD_OFFSET_X + col * SQUARE_SIZE
            y = BOARD_OFFSET_Y + display_row * SQUARE_SIZE
            
            # Create a surface with alpha for transparency
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(SELECTED_SQUARE)
            self.screen.blit(highlight_surface, (x, y))
    
    def draw_legal_move_highlights(self):
        """Draw highlights for legal moves from selected square."""
        for move_square in self.legal_moves:
            row, col = move_square
            display_row = 7 - row if self.flipped else row
            x = BOARD_OFFSET_X + col * SQUARE_SIZE
            y = BOARD_OFFSET_Y + display_row * SQUARE_SIZE
            
            # Draw a semi-transparent white highlight over the entire square
            # Create a surface with alpha for transparency
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill((255, 255, 255, 100))  # White with transparency
            self.screen.blit(highlight_surface, (x, y))
    
    def set_selected_square(self, square: Optional[Tuple[int, int]]):
        """Set the currently selected square."""
        self.selected_square = square
    
    def set_legal_moves(self, moves: List[Tuple[int, int]]):
        """Set the list of legal move squares to highlight."""
        self.legal_moves = moves
    
    def set_flipped(self, flipped: bool):
        """Set whether the board should be flipped (black at bottom)."""
        self.flipped = flipped


class PieceAssets:
    """Manages loading and rendering chess pieces."""
    
    def __init__(self):
        self.pieces = {}
        self.load_pieces()
    
    def load_pieces(self):
        """Load piece images from assets directory or create text-based fallback."""
        import os
        
        # Try to load PNG images first
        if self._load_png_pieces():
            print("Loaded PNG chess pieces successfully")
            return
        
        # Fallback to Unicode symbols if image loading fails
        print("PNG pieces not found, using Unicode fallback")
        self._load_unicode_pieces()
    
    def _load_png_pieces(self) -> bool:
        """Load chess pieces from PNG files. Returns True if successful."""
        try:
            import os
            
            # Get the path to assets directory
            assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'pieces')
            
            # If running from different directory, try alternative paths
            if not os.path.exists(assets_dir):
                assets_dir = os.path.join('assets', 'pieces')
            if not os.path.exists(assets_dir):
                assets_dir = os.path.join('..', 'assets', 'pieces')
            if not os.path.exists(assets_dir):
                return False
            
            # Define piece mappings
            piece_files = {
                'white': {
                    'king': 'white_king.png',
                    'queen': 'white_queen.png', 
                    'rook': 'white_rook.png',
                    'bishop': 'white_bishop.png',
                    'knight': 'white_knight.png',
                    'pawn': 'white_pawn.png'
                },
                'black': {
                    'king': 'black_king.png',
                    'queen': 'black_queen.png',
                    'rook': 'black_rook.png', 
                    'bishop': 'black_bishop.png',
                    'knight': 'black_knight.png',
                    'pawn': 'black_pawn.png'
                }
            }
            
            # Load each piece
            for color, pieces_dict in piece_files.items():
                self.pieces[color] = {}
                for piece_type, filename in pieces_dict.items():
                    filepath = os.path.join(assets_dir, filename)
                    
                    if not os.path.exists(filepath):
                        print(f"Missing piece file: {filepath}")
                        return False
                    
                    # Load and scale the image
                    piece_surface = pygame.image.load(filepath).convert_alpha()
                    
                    # Scale to fit square size (with some padding)
                    target_size = int(SQUARE_SIZE * 0.8)  # 80% of square size
                    piece_surface = pygame.transform.smoothscale(piece_surface, (target_size, target_size))
                    
                    self.pieces[color][piece_type] = piece_surface
            
            return True
            
        except Exception as e:
            print(f"Error loading PNG pieces: {e}")
            return False
    
    def _load_unicode_pieces(self):
        """Load chess pieces using Unicode symbols as fallback."""
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
        for color, pieces_dict in piece_symbols.items():
            self.pieces[color] = {}
            for piece_type, symbol in pieces_dict.items():
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
    def screen_to_board_coords(mouse_x: int, mouse_y: int, flipped: bool = False) -> Optional[Tuple[int, int]]:
        """Convert screen coordinates to board coordinates (row, col)."""
        # Check if click is within board bounds
        if (BOARD_OFFSET_X <= mouse_x < BOARD_OFFSET_X + BOARD_SIZE and
            BOARD_OFFSET_Y <= mouse_y < BOARD_OFFSET_Y + BOARD_SIZE):
            
            col = (mouse_x - BOARD_OFFSET_X) // SQUARE_SIZE
            display_row = (mouse_y - BOARD_OFFSET_Y) // SQUARE_SIZE
            
            # Convert display row to logical row based on flip state
            row = 7 - display_row if flipped else display_row
            
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


class GameSetup:
    """Handles the game setup screen for difficulty and color selection."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 48)
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 24)
        
        # Setup state
        self.difficulty = 8  # Default medium difficulty
        self.human_color = 'white'  # Default human plays white
        self.difficulty_descriptions = {
            0: "Beginner (Random moves)",
            1: "Very Easy", 2: "Very Easy", 3: "Easy", 4: "Easy",
            5: "Medium-Easy", 6: "Medium-Easy", 7: "Medium", 8: "Medium",
            9: "Medium-Hard", 10: "Medium-Hard", 11: "Hard", 12: "Hard",
            13: "Very Hard", 14: "Very Hard", 15: "Expert", 16: "Expert",
            17: "Master", 18: "Master", 19: "Grandmaster", 20: "Maximum"
        }
        
        # UI elements
        self.slider_rect = pygame.Rect(250, 300, 300, 20)
        self.slider_handle = pygame.Rect(0, 0, 20, 30)
        self.white_button = pygame.Rect(250, 400, 120, 80)
        self.black_button = pygame.Rect(430, 400, 120, 80)
        self.start_button = pygame.Rect(300, 550, 200, 60)
        
        # Interaction state
        self.dragging_slider = False
        self.mouse_pos = (0, 0)
        self.setup_complete = False
        
        self._update_slider_handle()
    
    def _update_slider_handle(self):
        """Update slider handle position based on difficulty value."""
        # Map difficulty (0-20) to slider position
        slider_progress = self.difficulty / 20.0
        handle_x = self.slider_rect.x + int(slider_progress * (self.slider_rect.width - self.slider_handle.width))
        self.slider_handle.x = handle_x
        self.slider_handle.centery = self.slider_rect.centery
    
    def handle_event(self, event) -> bool:
        """Handle setup screen events. Returns True if setup is complete."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.mouse_pos = event.pos
                
                # Check slider
                if self.slider_handle.collidepoint(event.pos):
                    self.dragging_slider = True
                    return False
                
                # Check color buttons
                if self.white_button.collidepoint(event.pos):
                    self.human_color = 'white'
                    return False
                elif self.black_button.collidepoint(event.pos):
                    self.human_color = 'black'
                    return False
                
                # Check start button
                if self.start_button.collidepoint(event.pos):
                    self.setup_complete = True
                    return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging_slider = False
        
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            
            if self.dragging_slider:
                # Update difficulty based on mouse position
                relative_x = event.pos[0] - self.slider_rect.x
                relative_x = max(0, min(relative_x, self.slider_rect.width))
                progress = relative_x / self.slider_rect.width
                self.difficulty = int(progress * 20)
                self._update_slider_handle()
        
        elif event.type == pygame.KEYDOWN:
            # Keyboard controls for accessibility
            if event.key == pygame.K_LEFT and self.difficulty > 0:
                self.difficulty -= 1
                self._update_slider_handle()
            elif event.key == pygame.K_RIGHT and self.difficulty < 20:
                self.difficulty += 1
                self._update_slider_handle()
            elif event.key == pygame.K_SPACE:
                self.human_color = 'black' if self.human_color == 'white' else 'white'
            elif event.key == pygame.K_RETURN:
                self.setup_complete = True
                return True
        
        return False
    
    def _is_mouse_over(self, rect: pygame.Rect) -> bool:
        """Check if mouse is over a rectangle."""
        return rect.collidepoint(self.mouse_pos)
    
    def render(self):
        """Render the setup screen."""
        # Clear screen
        self.screen.fill(SETUP_BACKGROUND)
        
        # Title
        title_text = self.font_title.render("PyChessBot - Game Setup", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(WINDOW_SIZE // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Difficulty section
        diff_title = self.font_large.render("AI Difficulty", True, TEXT_COLOR)
        self.screen.blit(diff_title, (250, 200))
        
        # Difficulty slider track
        pygame.draw.rect(self.screen, SLIDER_TRACK, self.slider_rect)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.slider_rect, 2)
        
        # Difficulty slider handle
        handle_color = SLIDER_HANDLE
        if self._is_mouse_over(self.slider_handle) or self.dragging_slider:
            handle_color = ACCENT_COLOR
        pygame.draw.rect(self.screen, handle_color, self.slider_handle)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.slider_handle, 2)
        
        # Difficulty labels
        easy_label = self.font_small.render("Easy", True, TEXT_COLOR)
        self.screen.blit(easy_label, (250, 330))
        hard_label = self.font_small.render("Hard", True, TEXT_COLOR)
        hard_rect = hard_label.get_rect(topright=(550, 330))
        self.screen.blit(hard_label, hard_rect)
        
        # Current difficulty description
        diff_desc = f"Level {self.difficulty}: {self.difficulty_descriptions[self.difficulty]}"
        desc_text = self.font_medium.render(diff_desc, True, ACCENT_COLOR)
        desc_rect = desc_text.get_rect(center=(WINDOW_SIZE // 2, 360))
        self.screen.blit(desc_text, desc_rect)
        
        # Color selection section
        color_title = self.font_large.render("Your Color", True, TEXT_COLOR)
        self.screen.blit(color_title, (250, 370))
        
        # White button
        white_color = BUTTON_ACTIVE if self.human_color == 'white' else BUTTON_HOVER if self._is_mouse_over(self.white_button) else BUTTON_COLOR
        pygame.draw.rect(self.screen, white_color, self.white_button)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.white_button, 3 if self.human_color == 'white' else 1)
        
        white_text = self.font_medium.render("White", True, TEXT_COLOR)
        white_text_rect = white_text.get_rect(center=self.white_button.center)
        self.screen.blit(white_text, white_text_rect)
        
        # Black button  
        black_color = BUTTON_ACTIVE if self.human_color == 'black' else BUTTON_HOVER if self._is_mouse_over(self.black_button) else BUTTON_COLOR
        pygame.draw.rect(self.screen, black_color, self.black_button)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.black_button, 3 if self.human_color == 'black' else 1)
        
        black_text = self.font_medium.render("Black", True, TEXT_COLOR)
        black_text_rect = black_text.get_rect(center=self.black_button.center)
        self.screen.blit(black_text, black_text_rect)
        
        # Start game button
        start_color = BUTTON_HOVER if self._is_mouse_over(self.start_button) else ACCENT_COLOR
        pygame.draw.rect(self.screen, start_color, self.start_button)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.start_button, 2)
        
        start_text = self.font_large.render("Start Game", True, TEXT_COLOR)
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_text_rect)
        
        # Instructions
        instructions = [
            "Use mouse to adjust difficulty and select color",
            "Keyboard: Arrow keys for difficulty, Space to switch color, Enter to start"
        ]
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, (160, 160, 160))
            inst_rect = inst_text.get_rect(center=(WINDOW_SIZE // 2, 680 + i * 25))
            self.screen.blit(inst_text, inst_rect)
    
    def get_settings(self) -> dict:
        """Get the selected game settings."""
        return {
            'difficulty': self.difficulty,
            'human_color': self.human_color
        }


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
        
        # Learning components
        self.evaluation_display = EvaluationDisplay()
        self.solo_mode_indicator = SoloModeIndicator()
        self.help_display = HelpDisplay()
        self.button_panel = LearningButtonPanel()
        self.auto_evaluation = False  # Toggle for automatic evaluation display
        self._solo_enabled = False  # Track solo mode state for GUI
        
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
                    display_row = 7 - row if self.renderer.flipped else row
                    x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = BOARD_OFFSET_Y + display_row * SQUARE_SIZE + SQUARE_SIZE // 2
                    
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
        board_coords = MouseHandler.screen_to_board_coords(*mouse_pos, self.renderer.flipped)
        
        if board_coords is None:
            return None
        
        row, col = board_coords
        algebraic_pos = MouseHandler.board_coords_to_algebraic(row, col)
        
        if self.selected_square is None:
            # First click - select a square
            # Get legal moves for this square first
            legal_moves = self._get_legal_moves_for_square(game, algebraic_pos)
            
            # Only select the square if it has legal moves
            if legal_moves:
                self.selected_square = board_coords
                self.renderer.set_selected_square(board_coords)
                
                # Convert legal moves to coordinates and highlight them
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
            import chess
            
            # Convert algebraic square to chess square index
            source_square = chess.parse_square(square)
            
            # Get the board from game
            board = game['board']
            
            # Check if there's a piece on this square that belongs to current player
            piece = board.piece_at(source_square)
            if piece is None:
                return []  # No piece on this square
            
            # Check if the piece belongs to the current player
            if piece.color != board.turn:
                return []  # Not current player's piece
            
            # Get all legal moves that start from the specified square
            legal_destination_squares = []
            
            for move in board.legal_moves:
                if move.from_square == source_square:
                    # Convert destination square back to algebraic notation
                    dest_square = chess.square_name(move.to_square)
                    legal_destination_squares.append(dest_square)
            
            return legal_destination_squares
            
        except Exception as e:
            print(f"Error getting legal moves for square {square}: {e}")
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
        board = game['board']
        
        try:
            # Convert to chess library format for processing
            import chess
            
            from_chess_square = chess.parse_square(from_square)
            to_chess_square = chess.parse_square(to_square)
            
            # Create a move object
            move = chess.Move(from_chess_square, to_chess_square)
            
            # Check if the move is legal before converting to SAN
            if move not in board.legal_moves:
                # Return None to indicate invalid move - don't fall back to anything
                return None
            
            # Convert to SAN
            san_move = board.san(move)
            return san_move
            
        except Exception as e:
            # Don't fall back to basic notation - return None for invalid moves
            print(f"Move conversion error: {e}")
            return None
    
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
        
        # Draw learning components
        self.draw_learning_indicators()
        
        # Update display
        pygame.display.flip()
    
    def draw_learning_indicators(self):
        """Draw learning feature indicators (evaluation and solo mode)."""
        # Position evaluation in top right
        eval_x = WINDOW_SIZE - 120
        eval_y = 10
        self.evaluation_display.render(self.screen, eval_x, eval_y)
        
        # Solo mode indicator in top left
        solo_x = 10
        solo_y = 10
        self.solo_mode_indicator.render(self.screen, solo_x, solo_y)
        
        # Keyboard shortcuts info in bottom left (always visible)
        auto_status = " [ON]" if self.auto_evaluation else ""
        shortcuts_text = ["Keyboard shortcuts:", "E/A-eval B-best S-solo", f"U-undo R-redo{auto_status}", "H-help (toggle overlay)"]
        shortcuts_font = pygame.font.Font(None, 16)
        for i, text in enumerate(shortcuts_text):
            color = (180, 180, 180) if i == 0 else (160, 160, 160)
            if auto_status and "redo" in text and self.auto_evaluation:
                color = (100, 255, 100)  # Green when auto-eval is on
            text_surface = shortcuts_font.render(text, True, color)
            self.screen.blit(text_surface, (10, WINDOW_SIZE - 80 + i * 16))
        
        # Learning button panel below chessboard
        button_x = BOARD_OFFSET_X + (BOARD_SIZE - 330) // 2  # Center below board (wider for single row)
        button_y = BOARD_OFFSET_Y + BOARD_SIZE + 40  # Further below the board
        solo_enabled = hasattr(self, '_solo_enabled') and self._solo_enabled
        self.button_panel.render(self.screen, button_x, button_y, self.auto_evaluation, solo_enabled)
        
        # Help display in bottom right
        help_x = WINDOW_SIZE - 220
        help_y = WINDOW_SIZE - 200
        self.help_display.render(self.screen, help_x, help_y)
    
    def set_evaluation(self, evaluation):
        """Set the position evaluation to display."""
        self.evaluation_display.set_evaluation(evaluation)
    
    def set_solo_mode(self, enabled):
        """Set the solo mode status."""
        self.solo_mode_indicator.set_solo_mode(enabled)
    
    def toggle_help(self):
        """Toggle help display."""
        self.help_display.toggle_help()
    
    def toggle_auto_evaluation(self):
        """Toggle automatic evaluation display."""
        self.auto_evaluation = not self.auto_evaluation
        return self.auto_evaluation
    
    def is_auto_evaluation_enabled(self):
        """Check if auto-evaluation is enabled."""
        return self.auto_evaluation
    
    def handle_events(self, game) -> Optional[str]:
        """Handle pygame events and return move if one was made."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check button panel clicks first
                    button_x = BOARD_OFFSET_X + (BOARD_SIZE - 330) // 2
                    button_y = BOARD_OFFSET_Y + BOARD_SIZE + 40
                    button_command = self.button_panel.handle_click(
                        event.pos[0], event.pos[1], button_x, button_y
                    )
                    if button_command:
                        return button_command
                    
                    # Handle chess board clicks
                    return self.handle_click(event.pos, game)
            elif event.type == pygame.KEYDOWN:
                # Handle keyboard shortcuts for learning features
                if event.key == pygame.K_e:  # 'e' for evaluation
                    return "eval"
                elif event.key == pygame.K_b:  # 'b' for best move
                    return "best"
                elif event.key == pygame.K_s:  # 's' for solo mode
                    return "solo"
                elif event.key == pygame.K_u:  # 'u' for undo
                    return "undo"
                elif event.key == pygame.K_r:  # 'r' for redo
                    return "redo"
                elif event.key == pygame.K_h:  # 'h' for help
                    return "help"
                elif event.key == pygame.K_a:  # 'a' for auto-evaluation toggle
                    return "eval"
        
        return None
    
    def is_running(self) -> bool:
        """Check if the GUI should continue running."""
        return self.running
    
    def quit(self):
        """Clean up and quit pygame."""
        pygame.quit()


def run_gui_game_with_setup():
    """Run the chess game with setup screen, then game."""
    from ..game.game_loop import create_game, make_move, get_current_player, get_game_status
    from ..ai.stockfish_ai import create_ai, get_ai_move, cleanup_ai
    
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("PyChessBot - Chess Game")
    clock = pygame.time.Clock()
    
    # Show setup screen
    setup = GameSetup(screen)
    
    print("Showing game setup screen...")
    setup_complete = False
    
    while not setup_complete:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if setup.handle_event(event):
                setup_complete = True
        
        setup.render()
        pygame.display.flip()
        clock.tick(60)
    
    # Get settings from setup
    settings = setup.get_settings()
    print(f"Starting game with difficulty {settings['difficulty']}, human color: {settings['human_color']}")
    
    # Initialize game with selected settings
    try:
        game = create_game()
        ai = create_ai(difficulty=settings['difficulty'])
        
        # Now run the main game
        run_gui_game(game, ai, settings['human_color'], screen, clock)
        
    except Exception as e:
        print(f"Error setting up game: {e}")
        pygame.quit()


def run_gui_game(game, ai, human_color='white', screen=None, clock=None):
    """Run the chess game with PyGame GUI."""
    from ..game.game_loop import make_move, get_current_player, get_game_status
    from ..ai.stockfish_ai import get_ai_move, cleanup_ai
    from ..analysis.position_evaluator import get_position_evaluation, get_best_move_suggestion
    from ..analysis.move_history import GameHistory, can_undo, can_redo, undo_move, redo_move, get_current_position
    from ..analysis.solo_mode import SoloModeState, toggle_solo_mode, should_use_ai, get_solo_mode_status
    
    # Get sound manager (already initialized in main)
    sound_manager = get_sound_manager()
    sound_manager.play_game_start_sound()
    
    # Initialize learning features
    game_history = GameHistory()
    game_history.add_position(game)  # Add starting position
    solo_state = SoloModeState()
    
    # Use provided screen/clock or create new ones
    if screen is None or clock is None:
        gui = GameGUI()
        screen = gui.screen
        clock = gui.clock
    else:
        gui = GameGUI()
        gui.screen = screen
        gui.clock = clock
    
    # Set board orientation based on player color
    gui.renderer.set_flipped(human_color == 'black')
    
    def handle_learning_command(command, current_game):
        """Handle learning commands in GUI mode."""
        if command == 'eval':
            # Toggle auto-evaluation mode
            enabled = gui.toggle_auto_evaluation()
            status = "enabled" if enabled else "disabled"
            print(f"Auto-evaluation {status}")
            if enabled:
                # Show evaluation immediately when enabling
                evaluation = get_position_evaluation(current_game, ai)
                gui.set_evaluation(evaluation)
                print(f"Auto-evaluation: {evaluation.get('score', 0)} centipawns")
            return current_game
        elif command == 'best':
            best_move = get_best_move_suggestion(current_game, ai)
            if best_move:
                print(f"Best move: {best_move}")
            return current_game
        elif command == 'solo':
            toggle_solo_mode(solo_state)
            status = get_solo_mode_status(solo_state)
            gui.set_solo_mode(solo_state.is_solo_enabled())
            gui._solo_enabled = solo_state.is_solo_enabled()  # Track for button display
            print(status)
            return current_game
        elif command == 'undo':
            if can_undo(game_history):
                if undo_move(game_history):
                    updated_game = get_current_position(game_history)
                    print("Move undone")
                    # Auto-evaluate if enabled
                    if gui.is_auto_evaluation_enabled():
                        evaluation = get_position_evaluation(updated_game, ai)
                        gui.set_evaluation(evaluation)
                        print(f"Auto-evaluation: {evaluation.get('score', 0)} centipawns")
                    return updated_game
            print("Cannot undo - no previous moves")
            return current_game
        elif command == 'redo':
            if can_redo(game_history):
                if redo_move(game_history):
                    updated_game = get_current_position(game_history)
                    print("Move redone") 
                    # Auto-evaluate if enabled
                    if gui.is_auto_evaluation_enabled():
                        evaluation = get_position_evaluation(updated_game, ai)
                        gui.set_evaluation(evaluation)
                        print(f"Auto-evaluation: {evaluation.get('score', 0)} centipawns")
                    return updated_game
            print("Cannot redo - no moves to redo")
            return current_game
        elif command == 'help':
            gui.toggle_help()
            print("Toggled help display")
            return current_game
        return current_game
    
    try:
        # Always render the initial position first
        gui.render(game)
        pygame.display.flip()
        
        game_ended_sound_played = False
        
        while gui.is_running():
            # Check if game is over
            game_status = get_game_status(game)
            if not game_status['active']:
                # Play game end sound once
                if not game_ended_sound_played:
                    sound_manager.play_game_end_sound()
                    game_ended_sound_played = True
                
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
            
            # Check if in solo mode or if it's human's turn
            if should_use_ai(solo_state) and current_player != human_color:
                # AI turn (only if not in solo mode)
                # First render current position, then let AI think
                gui.render(game)
                pygame.display.flip()
                
                print("AI is thinking...")
                
                # Handle GUI events (but don't process moves)
                gui_event = gui.handle_events(game)
                if gui_event == "quit":
                    break
                
                # Get AI move with retry logic
                max_retries = 3
                ai_move_successful = False
                
                for retry_count in range(max_retries):
                    try:
                        ai_move_result = get_ai_move(ai, game, time_limit=3.0)
                        
                        if not ai_move_result['success']:
                            print(f"AI error: {ai_move_result['error']}")
                            if retry_count == max_retries - 1:
                                break  # Exit game after max retries
                            continue
                        
                        ai_move = ai_move_result['move']
                        print(f"AI plays: {ai_move}")
                        
                        move_result = make_move(game, ai_move)
                        
                        if move_result['success']:
                            game = move_result['new_game']
                            ai_move_successful = True
                            
                            # Add new position to history
                            game_history.add_position(game)
                            
                            # Auto-evaluate if enabled
                            if gui.is_auto_evaluation_enabled():
                                evaluation = get_position_evaluation(game, ai)
                                gui.set_evaluation(evaluation)
                                print(f"Auto-evaluation: {evaluation.get('score', 0)} centipawns")
                            
                            # Play appropriate sound effect for AI move
                            analysis = move_result.get('move_analysis', {})
                            sound_manager.play_move_sound(
                                is_capture=analysis.get('is_capture', False),
                                is_check=analysis.get('is_check', False),
                                is_checkmate=analysis.get('is_checkmate', False),
                                is_castle=analysis.get('is_castle', False),
                                is_promotion=analysis.get('is_promotion', False)
                            )
                            break
                        else:
                            print(f"AI made invalid move: {move_result['error']}")
                            if retry_count < max_retries - 1:
                                print(f"Retrying AI move... (attempt {retry_count + 2}/{max_retries})")
                            else:
                                print("AI failed to make valid move after maximum retries")
                        
                    except Exception as e:
                        print(f"AI turn failed: {str(e)}")
                        if retry_count < max_retries - 1:
                            print(f"Retrying after error... (attempt {retry_count + 2}/{max_retries})")
                        
                if not ai_move_successful:
                    print("AI unable to make valid move. Game ending.")
                    break
            else:
                # Human turn OR solo mode (human controls both sides)
                move_input = gui.handle_events(game)
                
                if move_input == "quit":
                    break
                elif move_input in ['eval', 'best', 'solo', 'undo', 'redo', 'help']:
                    # Handle learning commands
                    game = handle_learning_command(move_input, game)
                    # Continue to re-render the position
                elif move_input is not None:
                    # Process human move
                    print(f"Human move: {move_input}")
                    move_result = make_move(game, move_input)
                    
                    if move_result['success']:
                        game = move_result['new_game']
                        print(f"Move successful: {move_input}")
                        
                        # Add new position to history
                        game_history.add_position(game)
                        
                        # Auto-evaluate if enabled
                        if gui.is_auto_evaluation_enabled():
                            evaluation = get_position_evaluation(game, ai)
                            gui.set_evaluation(evaluation)
                            print(f"Auto-evaluation: {evaluation.get('score', 0)} centipawns")
                        
                        # Play appropriate sound effect
                        analysis = move_result.get('move_analysis', {})
                        sound_manager.play_move_sound(
                            is_capture=analysis.get('is_capture', False),
                            is_check=analysis.get('is_check', False),
                            is_checkmate=analysis.get('is_checkmate', False),
                            is_castle=analysis.get('is_castle', False),
                            is_promotion=analysis.get('is_promotion', False)
                        )
                    else:
                        print(f"Invalid move: {move_result['error']}")
                        sound_manager.play_error_sound()
            
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


def run_dual_mode_game(game, ai, human_color='white'):
    """Run the chess game in dual mode: console input with GUI visualization."""
    import threading
    import time
    from ..game.game_loop import make_move, get_current_player, get_game_status
    from ..ai.stockfish_ai import get_ai_move, cleanup_ai
    from ..ui.console_interface import (
        display_board, get_user_move, show_message, show_error, 
        clear_screen, show_help, show_move_history, show_legal_moves, show_game_status
    )
    
    # Initialize GUI components
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("PyChessBot - Dual Mode (View Only - Use Console for Input)")
    clock = pygame.time.Clock()
    
    gui = GameGUI()
    gui.screen = screen
    gui.clock = clock
    gui.renderer.set_flipped(human_color == 'black')
    
    # Get sound manager
    sound_manager = get_sound_manager()
    sound_manager.play_game_start_sound()
    
    # Shared state between console and GUI threads with thread safety
    shared_state = {
        'game': game,
        'running': True,
        'game_over': False,
        'updated': True,  # Flag to trigger GUI refresh
        'lock': threading.Lock(),  # Thread safety
        'gui_ready': False  # Flag to indicate GUI is ready to be closed
    }
    
    def gui_thread():
        """GUI thread that ONLY does rendering - NO event handling."""
        game_ended_sound_played = False
        last_game = None
        
        # Mark GUI as ready
        with shared_state['lock']:
            shared_state['gui_ready'] = True
        
        try:
            while True:
                # Check if we should stop (non-blocking)
                with shared_state['lock']:
                    should_run = shared_state['running']
                    if not should_run:
                        break
                
                # DO NOT HANDLE PYGAME EVENTS HERE - NOT THREAD SAFE!
                # All event handling must be done in main thread
                
                # Check if game state was updated (thread-safe)
                current_game = None
                needs_update = False
                
                with shared_state['lock']:
                    if shared_state['updated'] or shared_state['game'] != last_game:
                        current_game = shared_state['game']
                        shared_state['updated'] = False
                        needs_update = True
                        last_game = current_game
                
                if needs_update and current_game:
                    try:
                        # Check if game is over
                        game_status = get_game_status(current_game)
                        if not game_status['active']:
                            if not game_ended_sound_played:
                                sound_manager.play_game_end_sound()
                                game_ended_sound_played = True
                        
                        # Render the current game state
                        gui.render(current_game)
                        
                        # Add visual indicator that this is view-only mode
                        font = pygame.font.Font(None, 24)
                        view_only_text = font.render("VIEW ONLY - Use Console for Input", True, (255, 255, 0))
                        gui.screen.blit(view_only_text, (10, 10))
                        
                        # Force display update
                        pygame.display.flip()
                        
                    except Exception as e:
                        print(f"GUI rendering error: {e}")
                        # Try to clear screen and show error message
                        try:
                            gui.screen.fill((50, 50, 50))  # Dark grey background
                            error_font = pygame.font.Font(None, 48)
                            error_text = error_font.render("Rendering Error - Check Console", True, (255, 255, 255))
                            text_rect = error_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
                            gui.screen.blit(error_text, text_rect)
                            pygame.display.flip()
                        except:
                            pass  # If we can't even render error message, give up gracefully
                
                # Higher FPS since we're not processing events (just rendering)
                clock.tick(30)
                
        except Exception as e:
            print(f"GUI thread error: {e}")
        finally:
            # Clean exit without pygame.quit() - main thread will handle it
            pass
    
    def console_and_events_thread():
        """Main thread that handles console input, pygame events, and game logic."""
        import time
        current_game = shared_state['game']
        
        try:
            while shared_state['running']:
                # Handle pygame events in main thread (THREAD SAFE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        with shared_state['lock']:
                            shared_state['running'] = False
                        print("\nGUI window closed. Exiting game...")
                        return
                    # Consume all other events silently - no processing needed
                
                # Small delay to prevent CPU spinning and allow GUI thread to render
                time.sleep(0.01)
                # Display current position in console
                display_board(current_game)
                
                # Check if game is over
                game_status = get_game_status(current_game)
                if not game_status['active']:
                    show_message("Game Over!")
                    if game_status['result'] == 'checkmate':
                        winner = 'White' if game_status['winner'] == 'white' else 'Black'
                        show_message(f"Checkmate! {winner} wins!")
                    elif game_status['result'] == 'stalemate':
                        show_message("Stalemate! It's a draw!")
                    else:
                        show_message(f"Game ended: {game_status['result']}")
                    break
                
                # Determine whose turn it is
                current_player = get_current_player(current_game)
                
                if current_player == human_color:
                    # Human turn - get console input
                    while True:
                        try:
                            user_input = get_user_move()
                            
                            # Check for special commands
                            command = user_input.lower().strip()
                            if command == 'help':
                                show_help()
                                continue
                            elif command == 'history':
                                show_move_history(current_game)
                                continue
                            elif command == 'legal':
                                show_legal_moves(current_game)
                                continue
                            elif command == 'status':
                                show_game_status(current_game)
                                continue
                            elif command == 'clear':
                                clear_screen()
                                continue
                            elif command in ['quit', 'exit', 'q']:
                                with shared_state['lock']:
                                    shared_state['running'] = False
                                return
                            
                            # Try to make the move
                            move_result = make_move(current_game, user_input)
                            
                            if move_result['success']:
                                current_game = move_result['new_game']
                                # Thread-safe state update
                                with shared_state['lock']:
                                    shared_state['game'] = current_game
                                    shared_state['updated'] = True
                                
                                # Play sound effect
                                analysis = move_result.get('move_analysis', {})
                                sound_manager.play_move_sound(
                                    is_capture=analysis.get('is_capture', False),
                                    is_check=analysis.get('is_check', False),
                                    is_checkmate=analysis.get('is_checkmate', False),
                                    is_castle=analysis.get('is_castle', False),
                                    is_promotion=analysis.get('is_promotion', False)
                                )
                                break
                            else:
                                sound_manager.play_error_sound()
                                show_error(move_result['error'])
                                show_message("Type 'help' for assistance or 'legal' to see valid moves.")
                                
                        except KeyboardInterrupt:
                            show_message("\nGame interrupted. Thanks for playing!")
                            with shared_state['lock']:
                                shared_state['running'] = False
                            return
                else:
                    # AI turn
                    show_message("AI is thinking...")
                    
                    try:
                        ai_move_result = get_ai_move(ai, current_game, time_limit=3.0)
                        
                        if not ai_move_result['success']:
                            show_error(f"AI error: {ai_move_result['error']}")
                            with shared_state['lock']:
                                shared_state['running'] = False
                            return
                        
                        ai_move = ai_move_result['move']
                        show_message(f"AI plays: {ai_move}")
                        
                        move_result = make_move(current_game, ai_move)
                        
                        if not move_result['success']:
                            show_error(f"AI made invalid move: {move_result['error']}")
                            with shared_state['lock']:
                                shared_state['running'] = False
                            return
                        
                        current_game = move_result['new_game']
                        # Thread-safe state update
                        with shared_state['lock']:
                            shared_state['game'] = current_game
                            shared_state['updated'] = True
                        
                        # Play sound effect for AI move
                        analysis = move_result.get('move_analysis', {})
                        sound_manager.play_move_sound(
                            is_capture=analysis.get('is_capture', False),
                            is_check=analysis.get('is_check', False),
                            is_checkmate=analysis.get('is_checkmate', False),
                            is_castle=analysis.get('is_castle', False),
                            is_promotion=analysis.get('is_promotion', False)
                        )
                        
                    except Exception as e:
                        show_error(f"AI turn failed: {str(e)}")
                        with shared_state['lock']:
                            shared_state['running'] = False
                        return
        
        except Exception as e:
            show_error(f"Console thread error: {str(e)}")
            with shared_state['lock']:
                shared_state['running'] = False
        finally:
            cleanup_ai(ai)
    
    # Start GUI in a separate thread (daemon so it exits when main thread exits)
    gui_thread_handle = threading.Thread(target=gui_thread, daemon=True)
    gui_thread_handle.start()
    
    # Wait for GUI to be ready
    max_wait = 50  # 5 seconds max
    wait_count = 0
    while wait_count < max_wait:
        with shared_state['lock']:
            if shared_state['gui_ready']:
                break
        time.sleep(0.1)
        wait_count += 1
    
    if wait_count >= max_wait:
        print("Warning: GUI initialization timeout")
    
    # Render initial position (thread-safe)
    with shared_state['lock']:
        shared_state['updated'] = True
    
    try:
        # Show initial console display
        clear_screen()
        print("=" * 60)
        print("  PyChessBot - Dual Mode")
        print("  Console input + GUI visualization")
        print("=" * 60)
        print()
        print("Instructions:")
        print("- Type moves in this console (e.g., e4, Nf3, O-O)")
        print("- Watch moves appear in the GUI window")
        print("- Type 'help' for available commands")
        print("- Type 'quit' to exit")
        print("- Close GUI window to exit")
        print("- DO NOT click in GUI window (view only)")
        print()
        
        # Run console interface and event handling in main thread  
        console_and_events_thread()
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"Dual mode error: {str(e)}")
    finally:
        # Ensure GUI thread stops
        with shared_state['lock']:
            shared_state['running'] = False
        
        # Give GUI thread a moment to see the shutdown signal
        time.sleep(0.1)
        
        # Since GUI thread is daemon, it will exit automatically
        # Just do pygame cleanup
        try:
            pygame.quit()
        except:
            pass
        
        print("Dual mode cleanup complete.")