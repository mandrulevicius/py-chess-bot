# PyChessBot Dependency Issues and Solutions

## Issue Summary

The Stockfish engine fails to initialize due to missing dependencies in the current environment. This is a common issue in minimal Python environments or when dependencies haven't been installed.

## Root Cause Analysis

### 1. Missing Python Packages
- `python-chess` - Core chess library for move validation and board state
- `stockfish` - Python wrapper for Stockfish chess engine
- `pygame` - GUI framework (optional for console mode)
- `pytest` - Testing framework (development only)

### 2. Missing Stockfish Binary
- Stockfish chess engine executable not found in system PATH
- Required for AI move generation and position evaluation

## Diagnostic Results

```
❌ python-chess - Missing
❌ stockfish - Missing  
❌ pygame - Missing
❌ pytest - Missing
❌ Stockfish binary not found
✅ Alternative implementations - Working
✅ Logging system - Working
```

## Solutions

### Option 1: Install Full Dependencies (Recommended)

```bash
# Install Python packages
pip install python-chess stockfish pygame pytest

# Install Stockfish binary
# Ubuntu/Debian:
sudo apt-get install stockfish

# macOS:
brew install stockfish

# Windows:
# Download from https://stockfishchess.org/download/
```

### Option 2: Use Alternative Implementations (No Dependencies)

PyChessBot includes lightweight alternatives that work without external dependencies:

```bash
# Run with all alternative implementations
python main.py --ai-engine random --validator simple --board-engine simple --console

# Run with specific alternatives
python main.py --ai-engine random --console  # Random AI only
python main.py --validator simple --console   # Simple validator only
```

### Option 3: Partial Installation

Install only what you need:

```bash
# For basic chess functionality (no AI)
pip install python-chess

# For AI without GUI
pip install python-chess stockfish

# For full functionality  
pip install python-chess stockfish pygame
```

## Alternative Implementation Features

### Random AI (`--ai-engine random`)
- **Purpose**: Testing and fallback when Stockfish unavailable
- **Features**: Random legal move selection, basic evaluation
- **Performance**: Instant moves, no thinking time
- **Use Case**: Testing, learning, quick games

### Simple Validator (`--validator simple`)  
- **Purpose**: Basic move validation without python-chess
- **Features**: Regex-based algebraic notation parsing
- **Limitations**: Syntax validation only, no chess rule enforcement
- **Use Case**: Basic input validation, testing

### Simple Board (`--board-engine simple`)
- **Purpose**: Lightweight board representation
- **Features**: 8x8 array, basic FEN support, move parsing
- **Limitations**: No full chess rule validation
- **Use Case**: Demonstration, testing, minimal memory usage

## Testing Alternative Implementations

Use the included test script to verify alternatives work:

```bash
python test_alternatives.py
```

Expected output:
```
✅ Random AI - Working
✅ Simple Validator - Working  
✅ Simple Board - Working
🎉 All alternative implementations working!
```

## Production Recommendations

### For Development/Testing
```bash
python main.py --ai-engine random --validator simple --board-engine simple --console --log-level DEBUG
```

### For Full Chess Experience
1. Install all dependencies (Option 1)
2. Run with default settings:
```bash
python main.py --gui
```

### For Minimal Chess Game
```bash
python main.py --ai-engine random --console --no-sound
```

## Troubleshooting

### Common Issues

1. **"No module named 'chess'"**
   - Solution: `pip install python-chess`

2. **"No module named 'stockfish'"**
   - Solution: `pip install stockfish`

3. **"Stockfish binary not found"**
   - Solution: Install Stockfish engine or use `--ai-engine random`

4. **"pygame not available"**
   - Solution: `pip install pygame` or use `--console`

### Environment-Specific Solutions

#### Docker/Containerized Environments
```dockerfile
RUN apt-get update && apt-get install -y stockfish
RUN pip install python-chess stockfish pygame
```

#### GitHub Codespaces/Cloud IDEs
```bash
sudo apt-get update
sudo apt-get install -y stockfish
pip install -r requirements.txt
```

#### Minimal/Restricted Environments
Use alternative implementations only:
```bash
python main.py --ai-engine random --validator simple --board-engine simple --console
```

## Performance Notes

- **Full Implementation**: Best chess experience, requires dependencies
- **Alternative Implementation**: 50-100x faster initialization, minimal features
- **Hybrid Approach**: Use alternatives for testing, full implementation for production

The alternative implementations provide a fallback that ensures PyChessBot can run in any Python 3.6+ environment without external dependencies.