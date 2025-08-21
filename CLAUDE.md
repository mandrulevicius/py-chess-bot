# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyChessBot is a Python-based chess game designed for human vs AI gameplay with educational purposes. The project aims to create a playable chess implementation with a simple but effective AI opponent.

## Core Requirements (from docs/initialDoc.md)

The project prototype requires:
- Notation-based move tracking
- Move restrictions for both humans and AIs  
- Decoupled UI for humans
- Chess AI - free, simple to implement, but not completely stupid

## Development Methodology

This project follows **Test Driven Development (TDD)** with red-green-refactor cycles:

### TDD Workflow
1. **Red**: Write a failing test for the feature
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Clean up code while keeping tests green

### Development Process
1. **Before implementing each feature**: Define tests (where they make sense)
2. **Make tests pass**: Add implementation to satisfy tests
3. **Commit**: Once tests pass, commit the working code
4. **Tidy up**: Do basic cleanup and refactoring
5. **Test again**: Run tests after cleanup
6. **Commit**: If tests still pass, commit improvements
7. **Before new features**: Consider refactoring existing structure

### Key Principles
- **Make the change easy, then make the easy change**
- **Prefer procedural over class-based approach** when it makes sense
- **Red-Green-Refactor**: Make it work, make it right, make it fast

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (primary development command)
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=src

# Run a single test file
python -m pytest tests/test_filename.py

# Run specific test
python -m pytest tests/test_filename.py::test_function_name

# Run the main game
python main.py

# Run the main game with sound options
python main.py --gui --sound          # GUI with sounds (default)
python main.py --no-sound             # Console without sounds
python main.py --volume 0.3           # Custom volume level

# Test sound system
python test_sound.py

# Generate new sound effects (if needed)
python scripts/generate_sounds.py

# Code formatting
black .

# Linting
flake8 .
pylint src/

# Type checking
mypy .
```

## Recommended Project Structure

Based on the requirements, the codebase should be organized with these key components:

### Core Game Engine
- **Board representation**: Track piece positions and game state
- **Move validation**: Implement chess rules and legal move checking
- **Game logic**: Handle turn management, check/checkmate detection

### AI Component
- **Search algorithm**: Minimax with alpha-beta pruning recommended
- **Evaluation function**: Position scoring for AI decision making
- **Move generation**: Efficient legal move enumeration

### User Interface Layer
- **Input handling**: Parse human moves (algebraic notation)
- **Display system**: Board visualization (console or GUI)
- **Game controller**: Coordinate between UI, game engine, and AI

### Move Notation System
- Support standard algebraic notation (SAN)
- Move history tracking and replay capability
- FEN (Forsyth-Edwards Notation) for position serialization

## Key Architecture Principles

- **Decoupled design**: UI should be separate from game logic to allow multiple interfaces
- **Testable components**: Each module should be independently testable
- **Extensible AI**: AI system should allow for different difficulty levels and algorithms

## Testing Strategy

- Unit tests for game rules and move validation
- Integration tests for AI vs AI games
- UI testing for human input parsing
- Performance tests for AI response time

## Sound System Implementation

**Status**: ✅ IMPLEMENTED (Commit: a8d274c)

The project now includes a comprehensive sound effects system:

### Sound Features
- **9 sound effects**: move, capture, check, checkmate, castle, promotion, error, game_start, game_end
- **Smart priority system**: checkmate > check > castle > promotion > capture > move
- **Volume control**: Adjustable sound levels (0.0-1.0)
- **Graceful degradation**: Works without sound hardware/files
- **Cross-platform**: Uses pygame.mixer for compatibility

### Command-Line Options
```bash
python main.py --gui --sound          # Enable sounds (default)
python main.py --no-sound            # Disable sounds  
python main.py --volume 0.5          # Custom volume (0.0-1.0)
```

### Key Files
- `src/ui/sound_manager.py`: Core sound management system
- `src/game/move_analyzer.py`: Chess move analysis for sound selection
- `assets/sounds/`: 9 generated WAV sound files
- `scripts/generate_sounds.py`: Sound generation utility
- `test_sound.py`: Sound system testing script

### Testing
- 27 new sound-related tests (100 total tests passing)
- Sound integration tested in both GUI and console modes
- Comprehensive test coverage for SoundManager and MoveAnalyzer classes

### Usage Notes
- Sounds are enabled by default
- System automatically detects and handles missing sound files
- Move analysis determines appropriate sound based on chess rules
- Both GUI and console interfaces support sound effects

## Dependencies to Consider

Common Python chess libraries that might be useful:
- `python-chess`: Comprehensive chess library ✅ USED
- `pygame`: For GUI implementation ✅ USED (also for sound)
- `numpy`: For position evaluation arrays (used in sound generation)
- `pytest`: For testing framework ✅ USED