# PyChessBot GUI Interface

## Overview
PyChessBot now includes a fully functional PyGame GUI interface alongside the original console interface. The GUI provides an intuitive graphical chess experience while maintaining all the original game functionality.

## Features

### ✨ **Visual Interface**
- **800x800 pixel window** with professional layout
- **Chessboard rendering** with alternating light/dark squares  
- **Unicode chess pieces** with shadow effects for better visibility
- **File/rank coordinates** (a-h, 1-8) around the board
- **Status bar** showing current turn, check status, and game result

### 🎮 **Interactive Controls** 
- **Click-to-select** pieces to see available moves
- **Click-to-move** for intuitive move input
- **Move highlighting** shows legal moves for selected pieces
- **Visual feedback** with square highlighting and move indicators

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

# PyGame GUI interface  
python main.py --gui
python main.py --gui --difficulty 10 --color white
python main.py -g -d 20 -c black
```

### GUI Controls
1. **Start a game**: Run with `--gui` flag
2. **Select a piece**: Click on any of your pieces  
3. **See legal moves**: Valid moves are highlighted in green
4. **Make a move**: Click on a highlighted destination square
5. **Deselect**: Click the same piece again or an invalid square
6. **Quit**: Close the window or press Alt+F4

## Architecture

### Component Structure
- **`ChessboardRenderer`**: Handles board, coordinates, and highlighting
- **`PieceAssets`**: Manages chess piece rendering with Unicode symbols
- **`MouseHandler`**: Converts mouse clicks to chess coordinates
- **`GameGUI`**: Main coordination class integrating with game logic

### Integration Design
- **Preserves existing architecture**: No changes to game logic
- **Clean separation**: UI and game logic remain independent
- **Reuses components**: Move validation, AI, and board state unchanged
- **Extensible**: Easy to add new GUI features without affecting console mode

## Technical Details

### Chess Piece Rendering
- **Unicode chess symbols** (♔♕♖♗♘♙ ♚♛♜♝♞♟)
- **Font fallback system** for cross-platform compatibility
- **Shadow effects** for better visibility on light/dark squares
- **Automatic scaling** to fit board squares

### Coordinate System
- **Screen coordinates** converted to chess notation (a1-h8)
- **Row/column mapping** with proper file/rank orientation
- **Click detection** within board boundaries
- **Algebraic notation conversion** for game logic integration

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
- **67 total tests passing** (10 new GUI tests + 57 existing)
- **Mouse interaction testing** for coordinate conversion
- **Component initialization** and state management
- **Error handling** and edge cases
- **Integration testing** with existing game logic

## Requirements

- **Python 3.7+** 
- **pygame 2.0+** (install with `pip install pygame`)
- **All existing dependencies** (python-chess, stockfish)

The console interface remains available even if pygame is not installed.