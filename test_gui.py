#!/usr/bin/env python3
"""Simple test script for the PyGame GUI."""

import sys

def main():
    """Test the PyGame GUI by running main.py with GUI flag."""
    print("Testing PyGame GUI...")
    print("This will launch the GUI interface. Close the window to exit.")
    print("You can also run: python main.py --gui")
    
    # Import and run main with GUI arguments
    sys.argv = ["main.py", "--gui", "--difficulty", "5"]  # Easy difficulty for testing
    
    from main import main as main_game
    main_game()


if __name__ == "__main__":
    main()