"""Stockfish AI integration for chess engine."""

import atexit
from stockfish import Stockfish
from ..game.board_state import get_board_fen


# Patch the Stockfish destructor to handle the AttributeError gracefully
_original_del = Stockfish.__del__

def _safe_del(self):
    """Safe destructor that handles missing _stockfish attribute."""
    try:
        _original_del(self)
    except AttributeError:
        # Ignore the AttributeError from missing _stockfish
        pass

Stockfish.__del__ = _safe_del


class SafeStockfish:
    """Wrapper around Stockfish that handles cleanup properly."""
    
    def __init__(self, path):
        self._engine = None
        self._path = path
        try:
            self._engine = Stockfish(path=path)
            # Register cleanup on exit
            atexit.register(self._cleanup)
        except Exception:
            self._engine = None
            raise
    
    def _cleanup(self):
        """Clean up the engine properly."""
        if self._engine and hasattr(self._engine, '_stockfish'):
            try:
                if hasattr(self._engine, 'send_quit_command'):
                    self._engine.send_quit_command()
            except:
                pass
            try:
                if self._engine._stockfish and self._engine._stockfish.poll() is None:
                    self._engine._stockfish.terminate()
                    self._engine._stockfish.wait(timeout=1.0)
            except:
                pass
        self._engine = None
    
    def __getattr__(self, name):
        """Delegate all other attributes to the underlying engine."""
        if self._engine is None:
            raise RuntimeError("Stockfish engine is not initialized")
        return getattr(self._engine, name)
    
    def __del__(self):
        """Ensure cleanup on destruction."""
        self._cleanup()


def create_ai(difficulty=8, stockfish_path=None):
    """
    Create a Stockfish AI instance.
    
    Args:
        difficulty (int): Difficulty level 0-20 (0=weakest, 20=strongest)
        stockfish_path (str): Path to Stockfish binary
    
    Returns:
        dict: AI configuration with keys:
            - engine_type: "stockfish"
            - difficulty: difficulty level
            - stockfish_path: path to binary
            - _engine: internal Stockfish instance
    """
    if difficulty < 0 or difficulty > 20:
        difficulty = max(0, min(20, difficulty))  # Clamp to valid range
    
    # Try different Stockfish paths
    possible_paths = [
        stockfish_path,
        "stockfish",
        "c:/programs/stockfish/stockfish-windows-x86-64-avx2.exe",
        "c:/programs/stockfish/stockfish.exe",
        "c:/programs/stockfish/stockfish"
    ] if stockfish_path else [
        "stockfish",
        "c:/programs/stockfish/stockfish-windows-x86-64-avx2.exe",
        "c:/programs/stockfish/stockfish.exe", 
        "c:/programs/stockfish/stockfish"
    ]
    
    engine = None
    last_error = None
    
    for path in possible_paths:
        if path is None:
            continue
        try:
            # Initialize Stockfish engine with safe wrapper
            engine = SafeStockfish(path=path)
            stockfish_path = path
            break
        except Exception as e:
            last_error = e
            engine = None
            continue
    
    if engine is None:
        raise RuntimeError(f"Failed to initialize Stockfish. Tried paths: {possible_paths}. Last error: {str(last_error)}")
    
    try:
        
        # Configure difficulty settings
        engine.set_skill_level(difficulty)
        if difficulty < 20:
            # Add some randomness for lower difficulties
            engine.set_elo_rating(800 + (difficulty * 100))
        
        return {
            "engine_type": "stockfish",
            "difficulty": difficulty,
            "stockfish_path": stockfish_path,
            "_engine": engine
        }
    
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Stockfish: {str(e)}")


def get_ai_move(ai, game, time_limit=3.0):
    """
    Get AI move for current game position.
    
    Args:
        ai (dict): AI instance from create_ai()
        game (dict): Current game state
        time_limit (float): Maximum time in seconds for move calculation
    
    Returns:
        dict: Result with keys:
            - success: True if move was generated successfully
            - move: Move in SAN notation (if successful)
            - error: Error message (if unsuccessful)
    """
    try:
        engine = ai["_engine"]
        
        # Set the current position
        fen = get_board_fen(game["board"])
        engine.set_fen_position(fen)
        
        # Get best move (returns UCI format like 'e2e4')
        uci_move = engine.get_best_move_time(int(time_limit * 1000))  # Convert to milliseconds
        
        if uci_move is None:
            return {
                "success": False,
                "error": "AI could not find a valid move"
            }
        
        # Convert UCI move to SAN notation
        # We'll use python-chess board to convert UCI to SAN
        board = game["board"]
        try:
            import chess
            move_obj = chess.Move.from_uci(uci_move)
            san_move = board.san(move_obj)
            
            return {
                "success": True,
                "move": san_move
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to convert move to SAN: {str(e)}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"AI move generation failed: {str(e)}"
        }


def cleanup_ai(ai):
    """
    Properly clean up AI resources.
    
    Args:
        ai (dict): AI instance to cleanup
    
    Returns:
        dict: Result with keys:
            - success: True if cleanup was successful
            - error: Error message (if unsuccessful)
    """
    try:
        engine = ai.get("_engine")
        if engine and isinstance(engine, SafeStockfish):
            # Use the safe cleanup method
            engine._cleanup()
        
        return {
            "success": True
        }
    
    except Exception as e:
        # Don't raise exceptions during cleanup
        return {
            "success": False,
            "error": f"AI cleanup failed: {str(e)}"
        }


def set_ai_difficulty(ai, new_difficulty):
    """
    Change AI difficulty level (immutable - returns new AI instance).
    
    Args:
        ai (dict): Current AI instance
        new_difficulty (int): New difficulty level 0-20
    
    Returns:
        dict: Result with keys:
            - success: True if difficulty was changed successfully
            - new_ai: New AI instance (if successful)
            - error: Error message (if unsuccessful)
    """
    if new_difficulty < 0 or new_difficulty > 20:
        return {
            "success": False,
            "error": f"Invalid difficulty level: {new_difficulty}. Must be between 0 and 20."
        }
    
    try:
        # Clean up the old AI first
        cleanup_ai(ai)
        
        # Create new AI instance with new difficulty
        new_ai = create_ai(
            difficulty=new_difficulty,
            stockfish_path=ai["stockfish_path"]
        )
        
        return {
            "success": True,
            "new_ai": new_ai
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to change difficulty: {str(e)}"
        }