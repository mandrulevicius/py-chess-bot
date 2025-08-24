#!/usr/bin/env python3
"""Test the fixes for Stockfish initialization and random AI fallback."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_stockfish_imports():
    """Test if Stockfish imports work."""
    print("🔍 Testing Stockfish imports...")
    try:
        from ai.stockfish_ai import create_ai, get_ai_move, cleanup_ai, STOCKFISH_AVAILABLE
        print(f"✅ Stockfish imports successful, STOCKFISH_AVAILABLE = {STOCKFISH_AVAILABLE}")
        return True
    except Exception as e:
        print(f"❌ Stockfish import failed: {e}")
        return False

def test_random_ai_import():
    """Test if Random AI imports work."""
    print("\n🤖 Testing Random AI import...")
    try:
        from alternatives.random_ai import RandomChessAI
        ai = RandomChessAI()
        ai.initialize()
        move = ai.get_best_move()
        print(f"✅ Random AI working, sample move: {move}")
        return True
    except Exception as e:
        print(f"❌ Random AI import failed: {e}")
        return False

def test_logging():
    """Test logging system."""
    print("\n📝 Testing logging system...")
    try:
        from utils.logger import configure_logging, get_main_logger
        configure_logging()
        logger = get_main_logger()
        logger.info("Test log message")
        print("✅ Logging system working")
        return True
    except Exception as e:
        print(f"❌ Logging failed: {e}")
        return False

def test_ai_creation():
    """Test AI creation with fallback."""
    print("\n🎯 Testing AI creation with fallback...")
    try:
        from ai.stockfish_ai import create_ai
        
        # Try creating Stockfish AI (should fail)
        try:
            ai = create_ai(difficulty=5)
            print("⚠️  Stockfish AI creation succeeded (unexpected)")
        except Exception as e:
            print(f"✅ Stockfish AI creation failed as expected: {e}")
        
        # Test manual random AI creation
        from alternatives.random_ai import RandomChessAI
        ai_instance = RandomChessAI()
        ai_instance.initialize(difficulty=5)
        ai = {
            "engine_type": "random",
            "difficulty": 5,
            "_engine": ai_instance
        }
        
        # Test get_ai_move with random AI
        from ai.stockfish_ai import get_ai_move
        fake_game = {"board": None}  # Minimal game state for testing
        result = get_ai_move(ai, fake_game, time_limit=1.0)
        
        if result['success']:
            print(f"✅ Random AI move generation successful: {result['move']}")
        else:
            print(f"❌ Random AI move generation failed: {result['error']}")
        
        return result['success']
        
    except Exception as e:
        print(f"❌ AI creation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing PyChessBot Fixes")
    print("=" * 50)
    
    results = []
    results.append(test_stockfish_imports())
    results.append(test_random_ai_import())
    results.append(test_logging())
    results.append(test_ai_creation())
    
    print("\n" + "=" * 50)
    success_count = sum(results)
    total_count = len(results)
    
    if success_count == total_count:
        print(f"🎉 All tests passed ({success_count}/{total_count})")
        print("\nYou can now run:")
        print("python main.py --ai-engine random --console --log-level DEBUG --log-file debug.log")
    else:
        print(f"⚠️  {success_count}/{total_count} tests passed")

if __name__ == "__main__":
    main()