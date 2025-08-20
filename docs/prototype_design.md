# PyChessBot - Prototype Design Document

## Prototype Scope

A minimal viable chess game focusing on core functionality: human vs AI gameplay with standard notation, rule enforcement, and basic UI. Implementation details like class structure are deferred to development phase.

## Selected Design Options

### 1. Standard Algebraic Notation (SAN)
- **Input format**: e4, Nf3, O-O, Qxf7#
- **Output format**: Move history displayed as standard chess notation
- **Reasoning**: Most familiar to chess players, widely supported by libraries

### 2. Library-Based Move Restrictions
- **Primary choice**: `python-chess` library
- **Handles**: All chess rules, special moves, check/checkmate detection
- **Benefits**: Battle-tested, comprehensive, allows focus on other components

### 3. UI Implementation
- **PyGame**: Main user interface with graphical board
- **Console**: Development and debug interface - notation only, no ASCII art
- **Console output format**:
  ```
  Turn 1: White plays e4
  Turn 1: Black plays e5
  Turn 2: White plays Nf3
  [DEBUG] Position evaluation: +0.15
  Turn 2: Black plays Nc6
  ```

### 4. Free Chess Engine Libraries

**Available Options:**

#### Stockfish Python Integration
- **Library**: `stockfish` Python wrapper
- **Pros**: World's strongest open-source engine, configurable difficulty
- **Cons**: Requires Stockfish binary installation
- **Use case**: Can provide perfect play at any level

#### Python-chess with Simple AI
- **Library**: `python-chess` + basic minimax
- **Pros**: Pure Python, no external dependencies
- **Cons**: Need to implement evaluation function
- **Use case**: Educational, customizable difficulty

#### Sunfish
- **Library**: Pure Python chess engine
- **Pros**: Lightweight, educational code, no dependencies
- **Cons**: Weaker than Stockfish, fewer features
- **Use case**: Simple opponent, easy to understand/modify

**Recommendation for Prototype**: **Stockfish Python wrapper**
- Provides immediate strong opponent
- Configurable skill levels (0-20)
- No need to implement AI logic initially
- Can be replaced/supplemented with custom AI later

### 5. Move Validation Feedback

**Error Types and Messages**:
- **Invalid notation**: "Move 'Xe4' is not valid notation. Try 'Nxe4' or similar."
- **Illegal move**: "Knight on g1 cannot reach e4. Legal moves: Ne2, Nf3, Nh3"
- **Piece not found**: "No white bishop can reach c4. Check your notation."
- **King in check**: "Move leaves king in check. Must address check first."
- **Ambiguous notation**: "Multiple pieces can reach e4. Use 'Nge4' or 'Nce4'."

## Prototype Architecture

### Core Components
```
Game Loop
├── Input Handler (SAN parsing)
├── Move Validator (python-chess)
├── Game State Manager (board, history)
├── AI Interface (Stockfish wrapper)
├── Display Manager (PyGame + Console)
└── Move Feedback System
```

### Data Flow
1. **Input**: Player enters move in SAN format
2. **Parse**: Convert SAN to internal move representation
3. **Validate**: Check if move is legal in current position
4. **Feedback**: If invalid, show specific error message
5. **Execute**: If valid, apply move to board
6. **Display**: Update both PyGame and console displays
7. **AI Turn**: Get AI response via Stockfish
8. **Repeat**: Continue until game ends

### Core Functions (Implementation-Agnostic)
```python
# Input/Output
get_player_move() -> str
display_board(board_state)
log_move(player, move, turn_number)
show_error(error_type, details)

# Game Logic  
parse_san_move(move_string, board) -> move_object
validate_move(move, board) -> (valid, error_message)
apply_move(move, board) -> new_board_state
check_game_end(board) -> (ended, result)

# AI Integration
get_ai_move(board, difficulty_level) -> move_object
```

## Implementation Priority

### Phase 1: Core Game Loop
- Basic SAN input/output
- Move validation with python-chess
- Console logging for development
- Simple turn alternation

### Phase 2: AI Integration
- Stockfish integration
- Configurable difficulty
- AI move generation and application

### Phase 3: User Interface
- PyGame board display
- Click-to-move or drag-and-drop
- Visual move validation feedback

### Phase 4: Polish
- Better error messages
- Move history display
- Game state persistence

## Technical Dependencies

### Required Python Packages
```
python-chess    # Core chess logic and validation
stockfish      # AI engine wrapper  
pygame         # Graphical user interface
```

### External Requirements
- Stockfish chess engine binary (free download)
- Python 3.7+ for typing support

## Validation Requirements

### Move Input Validation
- **Syntax check**: Valid SAN format
- **Legal move check**: Piece can make the move
- **Game state check**: Move doesn't leave king in check
- **Disambiguation**: Handle cases where multiple pieces can reach same square

### Feedback Clarity
- **Specific errors**: Explain exactly what's wrong
- **Suggested fixes**: Offer correct notation when possible
- **Context-aware**: Different messages for different error types
- **Educational**: Help users learn proper notation

## Success Criteria

### Functional Requirements
- ✅ Accept and validate SAN moves
- ✅ Enforce all chess rules correctly
- ✅ Provide competent AI opponent
- ✅ Clear error messages for invalid moves
- ✅ Both console and graphical interfaces work

### Quality Requirements
- **Response time**: AI moves within 3 seconds
- **Error handling**: No crashes on invalid input
- **User experience**: Clear feedback for all user actions
- **Code quality**: Simple, readable, well-documented

### Deferred Decisions
- Class structure vs functional approach
- Advanced AI features (opening books, endgame tables)
- Network play capabilities
- Advanced UI features (piece animation, sound)

## Next Steps

1. Set up development environment with dependencies
2. Implement basic game loop with console interface
3. Integrate python-chess for move validation
4. Add Stockfish for AI moves
5. Build PyGame interface
6. Iterate on user experience and feedback