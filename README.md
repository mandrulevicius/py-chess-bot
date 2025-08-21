# PyChessBot

A Python-based chess game featuring human vs AI gameplay, built for educational purposes with clean, maintainable code following Test-Driven Development (TDD) principles.

## 🎯 Features

- **Human vs AI Chess Gameplay** - Play against configurable Stockfish AI
- **Dual Interface Support** - Both Console and PyGame GUI interfaces
- **Interactive GUI** - Professional chess board with piece graphics and game setup screen
- **Move Highlighting** - Visual indicators for legal moves when pieces are selected
- **Standard Chess Notation** - Full SAN (Standard Algebraic Notation) support  
- **Comprehensive Rule Engine** - All chess rules including castling, en passant, promotion
- **Configurable AI Difficulty** - 21 levels from beginner to grandmaster strength
- **Test Coverage** - 72+ passing tests ensuring reliability

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+**
- **Stockfish Chess Engine** - Download from [stockfishchess.org](https://stockfishchess.org/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mandrulevicius/py-chess-bot.git
   cd py-chess-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Stockfish** (if not already installed)
   - Download from [stockfishchess.org](https://stockfishchess.org/)
   - Add to PATH or place in `c:/programs/stockfish/` (Windows)

### Run the Game

**GUI Mode (Default):**
```bash
python main.py
```

**Console Mode:**
```bash
python main.py --console
```

**Command line options:**
```bash
python main.py --difficulty 15 --color black
python main.py --console --no-sound --volume 0.5
```

- `--gui` / `-g`: Use PyGame GUI interface (default)
- `--console` / `-c`: Use console interface instead of GUI
- `--difficulty` / `-d`: AI difficulty level (0-20, default: 8)
- `--color`: Your color (white/black, default: white)
- `--sound` / `-s`: Enable sound effects (default)
- `--no-sound`: Disable sound effects
- `--volume` / `-v`: Sound volume (0.0-1.0, default: 0.7)

## 🎮 How to Play

### GUI Mode (PyGame Interface)

**Game Setup:**
- Use the interactive setup screen to select AI difficulty (0-20) and your color
- Board automatically orients with your pieces at the bottom
- Click "Start Game" to begin

**Playing:**
- Click on a piece to select it (shows yellow highlight)
- Legal destination squares are highlighted with semi-transparent white
- Click on a highlighted square to move the piece there
- The game shows whose turn it is at the top

### Console Mode

**Starting the Game:**
```
==================================================
      Welcome to PyChessBot!
      Human vs AI Chess Game
==================================================

Instructions:
- Enter moves in standard algebraic notation (e.g., e4, Nf3, O-O)
- Type 'help' for available commands
- Type 'quit' to exit the game
```

### Chess Notation Examples
- `e4` - Pawn to e4
- `Nf3` - Knight to f3  
- `Bxc5` - Bishop captures on c5
- `O-O` - Kingside castling
- `O-O-O` - Queenside castling
- `e8=Q` - Pawn promotion to Queen
- `Qh5+` - Queen to h5 with check
- `Nf7#` - Knight to f7, checkmate

### In-Game Commands
- `help` - Show help and notation examples
- `history` - Display move history
- `legal` - Show all legal moves
- `status` - Show current game status
- `clear` - Clear screen
- `quit` - Exit game

## 🏗️ Architecture

The project follows clean architecture principles with clear separation of concerns:

```
src/
├── game/           # Core chess logic
│   ├── move_parser.py      # SAN notation parsing
│   ├── move_validator.py   # Move validation with position awareness
│   ├── board_state.py      # Immutable board state management
│   └── game_loop.py        # Game flow and turn management
├── ai/             # AI integration
│   └── stockfish_ai.py     # Stockfish engine wrapper
└── ui/             # User interface
    ├── console_interface.py # Console I/O and display
    └── pygame_interface.py  # PyGame GUI with interactive chess board
```

### Key Design Principles

- **Immutable State** - All game operations return new state objects
- **Functional Programming** - Preferred over classes where appropriate
- **Validation Layers** - Educational parser + position-aware validation
- **Problem Domain Separation** - Clear boundaries between game/AI/UI
- **Test-Driven Development** - RED-GREEN-REFACTOR cycles throughout

## 🧪 Testing

Run the comprehensive test suite:

```bash
# All tests
python -m pytest tests/ -v

# Specific component
python -m pytest tests/game/ -v          # Game engine tests
python -m pytest tests/ai/ -v            # AI integration tests  
python -m pytest tests/ui/ -v            # Interface tests

# With coverage
python -m pytest tests/ --cov=src
```

**Test Coverage:**
- 72+ total tests across all components
- Move parsing and validation (13 tests)
- Board state management (7 tests)
- Game loop functionality (7 tests)
- Stockfish AI integration (8 tests)
- Console interface (12 tests)
- PyGame GUI interface (15 tests)
- Main application (10+ tests)

## 🔧 Development

### Project Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run linting
black .
flake8 .

# Run type checking
mypy .
```

### TDD Workflow

This project follows strict Test-Driven Development:

1. **RED**: Write failing test for new feature
2. **GREEN**: Write minimal code to pass test  
3. **REFACTOR**: Clean up while keeping tests green
4. **COMMIT**: Commit working implementation

See [`CLAUDE.md`](CLAUDE.md) for detailed development guidelines and [`docs/`](docs/) for design documents.

## 📁 Project Structure

```
PyChessBot/
├── src/                    # Source code
│   ├── game/              # Chess engine
│   ├── ai/                # AI integration  
│   └── ui/                # User interfaces (console + GUI)
├── tests/                 # Comprehensive test suite (72+ tests)
├── docs/                  # Design documents and development history
├── assets/                # Game assets (chess piece images)
│   └── pieces/           # Professional PNG chess pieces
├── main.py               # Main application entry point
├── requirements.txt      # Python dependencies
├── CLAUDE.md            # Development guidelines
└── README.md            # This file
```

## 📋 Requirements

- **Python**: 3.7 or higher
- **Stockfish**: Chess engine binary
- **Dependencies**: Listed in `requirements.txt`
  - `python-chess>=1.999` - Chess logic and validation
  - `stockfish>=3.28.0` - AI engine wrapper
  - `pygame>=2.1.0` - GUI framework (future use)
  - `pytest>=7.0.0` - Testing framework

## 🐛 Troubleshooting

### "Stockfish not found" Error
- Ensure Stockfish is installed and in PATH
- Or place binary in `c:/programs/stockfish/` (Windows)
- Check binary name matches your system (e.g., `stockfish-windows-x86-64-avx2.exe`)

### Import Errors
- Verify Python 3.7+ is installed
- Run `pip install -r requirements.txt`
- Check virtual environment activation

### Performance Issues
- Lower AI difficulty level (`--difficulty 5`)
- Ensure Stockfish binary matches your CPU architecture

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **Test-Driven Development**
- **Tidy first**
- **Clean Architecture**

