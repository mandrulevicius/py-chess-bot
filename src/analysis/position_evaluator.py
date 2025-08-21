"""Position evaluation functionality using existing Stockfish AI."""

from typing import Dict, Any, Optional
from ..ai.stockfish_ai import get_ai_move


def get_position_evaluation(game, ai) -> Dict[str, Any]:
    """
    Get position evaluation using existing Stockfish AI.
    
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
        # Use existing AI to get a move and basic evaluation
        # This is a minimal implementation - just check if AI can analyze
        ai_result = get_ai_move(ai, game, time_limit=1.0)  # Quick evaluation
        
        if ai_result and ai_result.get('success'):
            # For now, return a basic evaluation
            # In a real implementation, we'd extract more detailed evaluation from Stockfish
            return {
                'score': 0,  # Placeholder - equal position
                'evaluation_type': 'cp',
                'best_move': ai_result.get('move')
            }
        else:
            return {
                'score': 0,
                'evaluation_type': 'error',
                'error': 'AI analysis failed'
            }
            
    except Exception as e:
        return {
            'score': 0,
            'evaluation_type': 'error',
            'error': str(e)
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
    if not game or not ai:
        return None
        
    try:
        ai_result = get_ai_move(ai, game, time_limit=1.0)
        
        if ai_result and ai_result.get('success'):
            return ai_result.get('move')
        else:
            return None
            
    except Exception as e:
        return None