#!/usr/bin/env python3
"""Dependency diagnostic script for PyChessBot."""

import sys
import subprocess
import os


def check_python_packages():
    """Check if required Python packages are available."""
    print("🔍 Checking Python packages...")
    
    packages = {
        'chess': 'python-chess',
        'stockfish': 'stockfish',
        'pygame': 'pygame',
        'pytest': 'pytest'
    }
    
    available = {}
    
    for import_name, package_name in packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name} - Available")
            available[import_name] = True
        except ImportError:
            print(f"❌ {package_name} - Missing")
            available[import_name] = False
    
    return available


def check_stockfish_binary():
    """Check if Stockfish binary is available."""
    print("\n🔍 Checking Stockfish binary...")
    
    # Common Stockfish locations
    locations = [
        'stockfish',
        '/usr/bin/stockfish',
        '/usr/local/bin/stockfish',
        'C:\\Programs\\stockfish\\stockfish.exe',
        'C:\\stockfish\\stockfish.exe'
    ]
    
    for location in locations:
        try:
            result = subprocess.run([location], capture_output=True, text=True, timeout=2)
            print(f"✅ Stockfish found at: {location}")
            return location
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            print(f"✅ Stockfish found at: {location} (responsive)")
            return location
        except Exception as e:
            print(f"⚠️  Error testing {location}: {e}")
    
    print("❌ Stockfish binary not found")
    return None


def check_alternative_implementations():
    """Check if alternative implementations work."""
    print("\n🔍 Checking alternative implementations...")
    
    try:
        # Add the src directory to Python path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(script_dir, '..', 'src')
        sys.path.insert(0, src_dir)
        
        from alternatives.random_ai import RandomChessAI
        ai = RandomChessAI()
        ai.initialize()
        print("✅ Random AI - Working")
        
        from alternatives.simple_validator import SimpleChessValidator
        validator = SimpleChessValidator()
        result = validator.validate_move(None, "e4")
        print("✅ Simple Validator - Working")
        
        from alternatives.simple_board import SimpleBoardState
        board_state = SimpleBoardState()
        board = board_state.create_initial_board()
        print("✅ Simple Board State - Working")
        
    except Exception as e:
        print(f"❌ Alternative implementations failed: {e}")


def test_logging():
    """Test logging system."""
    print("\n🔍 Testing logging system...")
    
    try:
        from utils.logger import get_main_logger, configure_logging
        configure_logging()
        logger = get_main_logger()
        logger.info("Test log message")
        print("✅ Logging system - Working")
    except Exception as e:
        print(f"❌ Logging system failed: {e}")


def provide_recommendations(available_packages, stockfish_path):
    """Provide installation recommendations."""
    print("\n💡 Recommendations:")
    
    if not any(available_packages.values()):
        print("❗ No required packages found. This appears to be a minimal Python environment.")
        print("   To use PyChessBot with full features, install:")
        print("   pip install python-chess stockfish pygame pytest")
        print()
        print("   To use with basic functionality only:")
        print("   python main.py --ai-engine random --validator simple --board-engine simple")
        
    elif not available_packages.get('chess', False):
        print("❗ python-chess missing - core chess functionality unavailable")
        print("   Install with: pip install python-chess")
        print("   Or use: --validator simple --board-engine simple")
        
    elif not available_packages.get('stockfish', False):
        print("❗ stockfish package missing - AI functionality limited")
        print("   Install with: pip install stockfish")
        print("   Or use: --ai-engine random")
        
    if not stockfish_path:
        print("❗ Stockfish binary missing - Install Stockfish engine")
        print("   Ubuntu/Debian: sudo apt-get install stockfish")
        print("   Windows: Download from https://stockfishchess.org/download/")
        print("   Or use: --ai-engine random")


def main():
    """Run dependency diagnosis."""
    print("🚀 PyChessBot Dependency Diagnostics")
    print("=" * 50)
    
    available_packages = check_python_packages()
    stockfish_path = check_stockfish_binary()
    check_alternative_implementations()
    test_logging()
    
    print("\n" + "=" * 50)
    provide_recommendations(available_packages, stockfish_path)


if __name__ == "__main__":
    main()