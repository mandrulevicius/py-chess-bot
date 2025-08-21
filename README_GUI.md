# PyChessBot GUI Documentation

## GUI Features Overview

PyChessBot includes a professional PyGame-based GUI interface that provides an intuitive chess playing experience with smart move highlighting, adaptive board orientation, and visual feedback.

## Features

### ✨ **Visual Interface**
- **800x800 pixel window** with professional layout
- **Interactive game setup screen** with difficulty slider and color selection
- **Professional PNG chess pieces** with Unicode fallback
- **Adaptive board orientation** - automatically flips when playing as black
- **Chessboard rendering** with alternating light/dark squares  
- **File/rank coordinates** (a-h, 1-8) dynamically adjusted for orientation
- **Status bar** showing current turn, check status, and game result

### 🎮 **Interactive Controls** 
- **Smart piece selection** - only current player's pieces can be selected
- **Legal move highlighting** - white semi-transparent overlay on valid destination squares
- **Yellow piece highlighting** for currently selected piece
- **Click-to-move** for intuitive move input
- **Intelligent game flow** - board loads first, then AI makes moves
- **Setup screen controls** - slider for difficulty, buttons for color selection

### 🤖 **AI Integration**
- **Full AI support** with all 21 difficulty levels (0-20)
- **Seamless turn management** between human and AI players
- **Real-time updates** as AI calculates and makes moves
- **Clean shutdown** with proper resource cleanup

### 🔄 **Dual Interface Support**
- **Console mode** (default): Traditional text-based interface
- **GUI mode** (--gui flag): Modern graphical interface  
- **Same game logic** powers both interfaces
- **All features available** in both modes

## Usage

### Command Line Options
```bash
# Console interface (original)
python main.py
python main.py --difficulty 15 --color black

# PyGame GUI interface (recommended)
python main.py --gui
python main.py --gui --difficulty 10 --color white
python main.py -g -d 20 -c black
```

### Game Setup Screen
When launching with `--gui` (and no specific difficulty/color), you'll see an interactive setup screen:
- **Difficulty Slider**: Choose AI strength from 0 (random) to 20 (maximum)
- **Color Selection**: Click White or Black buttons
- **Keyboard Support**: Arrow keys for difficulty, Space for color, Enter to start

### GUI Controls
1. **Start a game**: Run with `--gui` flag or use setup screen
2. **Select a piece**: Click on any of your pieces (shows yellow highlight)
3. **See legal moves**: Valid destination squares show white semi-transparent overlay
4. **Make a move**: Click on any highlighted destination square
5. **Deselect**: Click the same piece again or an invalid square
6. **Board orientation**: Automatically adjusts - your pieces always at bottom
7. **Quit**: Close the window or press Alt+F4

## Architecture

### Component Structure
- **`GameSetup`**: Interactive setup screen with difficulty and color selection
- **`ChessboardRenderer`**: Handles board, coordinates, highlighting, and board flipping
- **`PieceAssets`**: Manages chess piece rendering (PNG images with Unicode fallback)
- **`MouseHandler`**: Converts mouse clicks to chess coordinates (supports board flipping)
- **`GameGUI`**: Main coordination class integrating with game logic

### Integration Design
- **Preserves existing architecture**: No changes to game logic
- **Clean separation**: UI and game logic remain independent
- **Reuses components**: Move validation, AI, and board state unchanged
- **Extensible**: Easy to add new GUI features without affecting console mode

## Technical Details

### Chess Piece Rendering
- **Professional PNG graphics** loaded from `assets/pieces/` directory
- **Unicode chess symbols fallback** (♔♕♖♗♘♙ ♚♛♜♝♞♟) if PNG loading fails
- **Font fallback system** for cross-platform compatibility
- **Shadow effects** for better visibility on light/dark squares
- **Automatic scaling** to fit board squares perfectly

### Coordinate System
- **Screen coordinates** converted to chess notation (a1-h8)
- **Adaptive orientation** - coordinate mapping adjusts when board is flipped
- **Row/column mapping** with proper file/rank orientation
- **Click detection** within board boundaries
- **Algebraic notation conversion** for game logic integration
- **Smart legal move filtering** using python-chess move validation

### Performance
- **60 FPS rendering** for smooth visual experience
- **Efficient redraws** only when game state changes
- **Minimal resource usage** when idle
- **Clean memory management** with proper pygame cleanup

## Future Enhancements

### Near-term Improvements
- **Drag-and-drop** piece movement
- **Move animation** for piece transitions
- **Sound effects** for moves, captures, check
- **Captured pieces display** on the side
- **Game history panel** with move notation

### Advanced Features  
- **Analysis mode** showing AI evaluation
- **Move hints** for learning players
- **Custom piece sets** and board themes
- **Resize support** for different screen sizes
- **Full-screen mode** option

## Testing

The GUI implementation includes comprehensive tests:
- **72+ total tests passing** (15 GUI tests + 57+ existing)
- **Mouse interaction testing** for coordinate conversion (normal and flipped)
- **Component initialization** and state management
- **Board flipping and orientation testing**
- **Legal move detection and highlighting**
- **Error handling** and edge cases
- **Integration testing** with existing game logic

## Requirements

- **Python 3.7+** 
- **pygame 2.0+** (install with `pip install pygame`)
- **All existing dependencies** (python-chess, stockfish)

The console interface remains available even if pygame is not installed.