# PyChessBot GUI Design Documentation

## Architecture Overview

PyChessBot includes a professional PyGame-based GUI interface that provides an intuitive chess playing experience with smart move highlighting, adaptive board orientation, and visual feedback.

## Component Structure

### Core Components

- **`GameSetup`**: Interactive setup screen with difficulty slider and color selection
- **`ChessboardRenderer`**: Handles board, coordinates, highlighting, and board flipping
- **`PieceAssets`**: Manages chess piece rendering (PNG images with Unicode fallback)
- **`MouseHandler`**: Converts mouse clicks to chess coordinates (supports board flipping)
- **`GameGUI`**: Main coordination class integrating with game logic

### Integration Design

- **Preserves existing architecture**: No changes to core game logic
- **Clean separation**: UI and game logic remain independent
- **Reuses components**: Move validation, AI, and board state unchanged
- **Extensible**: Easy to add new GUI features without affecting console mode

## Technical Implementation

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

### Threading Architecture (Dual Mode)

**Problem**: Pygame is not thread-safe, especially `pygame.event.get()`

**Solution**:
- **Main thread**: Handles ALL pygame events + console input (thread-safe)
- **Background thread**: Pure rendering ONLY, zero event handling
- **Communication**: Thread-safe shared state with mutex locks

### Performance

- **30+ FPS rendering** for smooth visual experience
- **Efficient redraws** only when game state changes
- **Minimal resource usage** when idle
- **Clean memory management** with proper pygame cleanup

## Future Enhancements

### Near-term Improvements
- **Drag-and-drop** piece movement
- **Move animation** for piece transitions
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