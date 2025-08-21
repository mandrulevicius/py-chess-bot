"""Main application for PyChessBot - Human vs AI Chess Game."""

import argparse
import sys
from src.game.game_loop import create_game, make_move, get_current_player, get_game_status
from src.ai.stockfish_ai import create_ai, get_ai_move, cleanup_ai
from src.ui.console_interface import (
    display_welcome, display_board, get_user_move, show_message, 
    show_error, show_help, show_move_history, show_legal_moves, 
    show_game_status, clear_screen
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='PyChessBot - Human vs AI Chess Game')
    parser.add_argument('--difficulty', '-d', type=int, default=8, choices=range(0, 21),
                       help='AI difficulty level (0=weakest, 20=strongest, default=8)')
    parser.add_argument('--color', '-c', dest='human_color', choices=['white', 'black'], 
                       default='white', help='Human player color (default=white)')
    parser.add_argument('--gui', '-g', action='store_true',
                       help='Use PyGame GUI instead of console interface')
    return parser.parse_args()


def setup_game(difficulty=8):
    """
    Set up a new chess game with AI opponent.
    
    Args:
        difficulty (int): AI difficulty level
    
    Returns:
        tuple: (game_state, ai_instance)
    """
    try:
        game = create_game()
        ai = create_ai(difficulty=difficulty)
        return game, ai
    except Exception as e:
        print(f"Error setting up game: {e}")
        print("Make sure Stockfish is installed and accessible.")
        sys.exit(1)


def handle_user_command(user_input, game):
    """
    Handle special user commands.
    
    Args:
        user_input (str): User input string
        game (dict): Current game state
    
    Returns:
        bool or None: True if command handled, False if not a command, None to quit
    """
    command = user_input.lower().strip()
    
    if command == 'help':
        show_help()
        return True
    elif command == 'history':
        show_move_history(game)
        return True
    elif command == 'legal':
        show_legal_moves(game)
        return True
    elif command == 'status':
        show_game_status(game)
        return True
    elif command == 'clear':
        clear_screen()
        return True
    elif command in ['quit', 'exit', 'q']:
        return None
    
    return False  # Not a command


def human_turn(game):
    """
    Execute human player's turn.
    
    Args:
        game (dict): Current game state
    
    Returns:
        dict: Move result with success/error information
    """
    while True:
        try:
            user_input = get_user_move()
            
            # Check for special commands
            command_result = handle_user_command(user_input, game)
            if command_result is None:  # Quit command
                return None  # Return None to signal quit
            elif command_result is True:  # Command handled
                continue
            
            # Try to make the move
            move_result = make_move(game, user_input)
            
            if move_result['success']:
                return move_result
            else:
                show_error(move_result['error'])
                show_message("Type 'help' for assistance or 'legal' to see valid moves.")
                
        except KeyboardInterrupt:
            show_message("\nGame interrupted. Thanks for playing!")
            return None


def ai_turn(game, ai):
    """
    Execute AI player's turn.
    
    Args:
        game (dict): Current game state
        ai (dict): AI instance
    
    Returns:
        dict: Move result with success/error information
    """
    show_message("AI is thinking...")
    
    try:
        ai_move_result = get_ai_move(ai, game, time_limit=3.0)
        
        if not ai_move_result['success']:
            show_error(f"AI error: {ai_move_result['error']}")
            sys.exit(1)
        
        ai_move = ai_move_result['move']
        show_message(f"AI plays: {ai_move}")
        
        move_result = make_move(game, ai_move)
        
        if not move_result['success']:
            show_error(f"AI made invalid move: {move_result['error']}")
            sys.exit(1)
            
        return move_result
        
    except Exception as e:
        show_error(f"AI turn failed: {str(e)}")
        sys.exit(1)


def is_game_over(game):
    """
    Check if the game is over.
    
    Args:
        game (dict): Current game state
    
    Returns:
        bool: True if game is over
    """
    status = get_game_status(game)
    return not status['active']


def show_game_result(game):
    """
    Display the final game result.
    
    Args:
        game (dict): Final game state
    """
    status = get_game_status(game)
    
    print("\n" + "="*50)
    print("           GAME OVER")
    print("="*50)
    print(f"Result: {status['result']}")
    
    if status['winner']:
        if status['winner'] == 'white':
            print("🎉 White wins!")
        else:
            print("🎉 Black wins!")
    else:
        print("🤝 Game drawn!")
    
    print("="*50)
    show_move_history(game)


def main():
    """Main game loop."""
    # Parse command line arguments
    args = parse_args()
    
    # Setup game
    game, ai = setup_game(difficulty=args.difficulty)
    
    if args.gui:
        # Use PyGame GUI
        try:
            from src.ui.pygame_interface import run_gui_game
            print(f"Starting PyChessBot GUI - Difficulty: {args.difficulty}, You are: {args.human_color}")
            run_gui_game(game, ai, human_color=args.human_color)
        except ImportError as e:
            print(f"GUI not available: {e}")
            print("Install pygame with: pip install pygame")
            sys.exit(1)
        except Exception as e:
            print(f"GUI error: {e}")
            sys.exit(1)
    else:
        # Use console interface (original behavior)
        # Display welcome message
        clear_screen()
        display_welcome()
        
        show_message(f"Setting up game with AI difficulty {args.difficulty}...")
        show_message(f"You are playing as {args.human_color}.")
        show_message("Game started! Type 'help' for commands.\n")
        
        # Console game loop
        try:
            while True:
                # Display current position
                display_board(game)
                
                # Check if game is over
                if is_game_over(game):
                    show_game_result(game)
                    break
                
                # Determine whose turn it is
                current_player = get_current_player(game)
                
                if current_player == args.human_color:
                    # Human turn
                    move_result = human_turn(game)
                    if move_result is None:  # User quit
                        cleanup_ai(ai)
                        show_message("Thanks for playing PyChessBot!")
                        break
                    game = move_result['new_game']
                else:
                    # AI turn
                    move_result = ai_turn(game, ai)
                    game = move_result['new_game']
        
        except KeyboardInterrupt:
            cleanup_ai(ai)
            show_message("\nGame interrupted by user. Thanks for playing!")
        except Exception as e:
            cleanup_ai(ai)
            show_error(f"Unexpected error: {str(e)}")
            sys.exit(1)
        finally:
            # Ensure cleanup happens even if we exit normally
            cleanup_ai(ai)


if __name__ == '__main__':
    main()