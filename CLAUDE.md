# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyChessBot is a Python-based chess game designed for human vs AI gameplay with educational purposes. The project aims to create a playable chess implementation with a simple but effective AI opponent.

## Core Requirements (from initialDoc.md)

The project prototype requires:
- Notation-based move tracking
- Move restrictions for both humans and AIs  
- Decoupled UI for humans
- Chess AI - free, simple to implement, but not completely stupid

## Development Commands

Since this is a Python project, these commands will likely be needed:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main game
python main.py

# Run tests
python -m pytest tests/

# Run a single test file
python -m pytest tests/test_filename.py

# Run specific test
python -m pytest tests/test_filename.py::test_function_name

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

## Dependencies to Consider

Common Python chess libraries that might be useful:
- `python-chess`: Comprehensive chess library
- `pygame`: For GUI implementation
- `numpy`: For position evaluation arrays
- `pytest`: For testing framework