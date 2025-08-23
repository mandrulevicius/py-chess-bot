"""Position evaluation functionality using Stockfish engine."""

from typing import Dict, Any, Optional
from ..ai.stockfish_ai import get_ai_move


def get_position_evaluation(game, ai) -> Dict[str, Any]:
    """
    Get position evaluation using Stockfish engine.
    
    Args:
        game: Current game state
        ai: AI instance (Stockfish)
        
    Returns:
        Dictionary with evaluation data
    """
    if not game or not ai:
        return {
            'score': 0,
            'evaluation_type': 'error',
            'error': 'Invalid game or AI instance'
        }
    
    try:
        # Get the chess.Board from the game state
        board = game.get('board')
        if not board:
            return {
                'score': 0,
                'evaluation_type': 'error', 
                'error': 'No board in game state'
            }
        
        # Get Stockfish engine from AI instance
        stockfish = ai.get('_engine')
        if not stockfish:
            return {
                'score': 0,
                'evaluation_type': 'error',
                'error': 'No Stockfish engine available'
            }
        
        # Use Stockfish to evaluate position
        # Set current position
        from ..game.board_state import get_board_fen
        fen = get_board_fen(board)
        stockfish.set_fen_position(fen)
        
        # Get evaluation (centipawns from White's perspective)
        evaluation = stockfish.get_evaluation()
        
        if not evaluation:
            return {
                'score': 0,
                'evaluation_type': 'error',
                'error': 'No evaluation from engine'
            }
        
        # Get best move in UCI format, convert to SAN
        uci_move = stockfish.get_best_move()
        best_move = None
        if uci_move:
            try:
                # Convert UCI to SAN using the board
                import chess
                chess_move = chess.Move.from_uci(uci_move)
                best_move = board.san(chess_move)
            except:
                # Fallback: just return the UCI move if conversion fails
                best_move = uci_move
        
        # Parse evaluation based on Stockfish API
        eval_type = evaluation.get('type')
        eval_value = evaluation.get('value')
        
        # Debug: Add some logging for development  
        # print(f"DEBUG: Stockfish evaluation: {evaluation}")  # Uncomment for debugging
        
        if eval_type == 'mate':
            return {
                'score': 0,
                'mate_in': eval_value,
                'evaluation_type': 'mate',
                'best_move': best_move
            }
        elif eval_type == 'cp':
            return {
                'score': eval_value,  # Centipawns
                'evaluation_type': 'cp',
                'best_move': best_move
            }
        else:
            return {
                'score': 0,
                'evaluation_type': 'error',
                'error': f'Unknown evaluation type: {eval_type}'
            }
            
    except Exception as e:
        # Fallback: use AI move generation as basic evaluation
        try:
            ai_result = get_ai_move(ai, game, time_limit=1.0)
            
            if ai_result and ai_result.get('success'):
                return {
                    'score': 0,  # No evaluation, just best move
                    'evaluation_type': 'cp',
                    'best_move': ai_result.get('move'),
                    'note': 'Basic evaluation (engine analysis failed)'
                }
            else:
                return {
                    'score': 0,
                    'evaluation_type': 'error',
                    'error': f'Engine error: {str(e)}'
                }
                
        except Exception as fallback_error:
            return {
                'score': 0,
                'evaluation_type': 'error',
                'error': f'All evaluation methods failed: {str(e)}'
            }


def get_best_move_suggestion(game, ai) -> Optional[str]:
    """
    Get best move suggestion for current position.
    
    Args:
        game: Current game state
        ai: AI instance
        
    Returns:
        Best move in algebraic notation or None
    """
    evaluation = get_position_evaluation(game, ai)
    best_move = evaluation.get('best_move')
    
    # If no best move from evaluation, fallback to AI move
    if not best_move:
        try:
            ai_result = get_ai_move(ai, game, time_limit=1.0)
            if ai_result and ai_result.get('success'):
                return ai_result.get('move')
        except Exception:
            pass
    
    return best_move