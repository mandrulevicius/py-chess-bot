# PyChessBot - Architecture Overview for Claude Code

> **Essential project understanding for AI development sessions**

## 🎯 **Project Summary**
**PyChessBot** - Advanced educational chess learning platform with AI opponent. Built using TDD methodology with comprehensive test coverage (142+ tests).

**Current Status**: Production-ready learning application with GUI and console interfaces.

## 🏗️ **Architecture Overview**

### **Component Structure** (18 files, 7 categories)
```
MAIN (1)     : main.py - Central orchestrator with CLI and game setup
GAME (5)     : Chess logic, move parsing, validation, board state
AI (2)       : Stockfish + random AI with pluggable interfaces  
UI (4)       : Console + GUI + sound + learning components
ANALYSIS (3) : Position evaluation, move history, solo mode
UTILS (2)    : Logging, caching utilities
CORE (1)     : Abstract interfaces for pluggable architecture
```

### **Critical Dependency Flow**
```
main.py (entry point)
├── game_loop.py (game management)
│   └── board_state.py ← CORE (5 dependents)
├── pygame_interface.py ← HIGH ACTIVITY (GUI)
├── stockfish_ai.py (primary AI)
└── analysis/* (learning features)
```

### **Key Architectural Patterns**
- ✅ **Layered architecture**: UI → Game Logic → AI → Utils
- ✅ **No circular dependencies**: Clean dependency flow
- ✅ **Dependency injection**: Pluggable AI engines via interfaces
- ✅ **Immutable game state**: Copy semantics for state management
- ✅ **TDD methodology**: Test-first development with comprehensive coverage

## 🔥 **Development Context**

### **High Activity Files** (Recent development focus)
- **pygame_interface.py** (1.0 activity) - 15 commits, primary GUI development
- **main.py** (0.9 activity) - 8 commits, core orchestration improvements  
- **learning_gui.py** (0.9 activity) - 6 commits, learning feature components
- **stockfish_ai.py** (0.8 activity) - 6 commits, AI engine improvements

### **Stable Core Components**
- **board_state.py** - Foundation component (5 dependents), stable chess logic
- **move_parser.py** - Chess notation parsing, stable
- **move_validator.py** - Rule validation, stable
- **game_loop.py** - Game orchestration hub, stable

## 🎯 **Key Files by Importance**

### **Start Here** (Essential understanding)
1. **`main.py`** - Entry point, orchestrates all subsystems
2. **`src/game/board_state.py`** - Core chess state (5 dependents)
3. **`src/game/game_loop.py`** - Game management hub
4. **`src/ui/pygame_interface.py`** - Primary user interface

### **Core Game Logic**
- **`src/game/move_parser.py`** - SAN notation parsing
- **`src/game/move_validator.py`** - Chess rules validation
- **`src/game/move_analyzer.py`** - Move analysis for sound effects

### **AI & Learning**
- **`src/ai/stockfish_ai.py`** - Primary AI engine (Stockfish integration)
- **`src/analysis/position_evaluator.py`** - Learning features
- **`src/analysis/move_history.py`** - Undo/redo system

### **Infrastructure**
- **`src/utils/logger.py`** - Structured logging
- **`src/core/interfaces.py`** - Pluggable architecture

## ⚠️ **Critical Considerations**

### **High-Impact Components** (Change carefully)
- **`board_state.py`** - 5 dependents, affects core game logic
- **`game_loop.py`** - 3 dependents, central coordination
- **`main.py`** - Entry point, affects initialization

### **Current Development Focus**
- **GUI enhancements** - pygame_interface.py active development
- **Learning features** - analysis package expansion
- **Core stability** - foundation components are stable

## 🛠️ **Development Commands**

### **Running the Application**
```bash
# Primary mode - GUI with sound
python main.py --gui --sound

# Console mode for debugging
python main.py --console --no-sound

# Custom difficulty and settings
python main.py --gui --difficulty 15 --color black
```

### **Development Workflow**
```bash
# Run all tests (primary development command)
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/game/ -v        # Core game logic
python -m pytest tests/ui/ -v          # User interfaces  
python -m pytest tests/analysis/ -v    # Learning features

# Code quality checks
python -m pytest tests/ --cov=src      # Coverage report
```

## 📚 **External Dependencies**

### **Required**
- **`python-chess`** - Core chess logic, board representation, rule validation
- **`pytest`** - Testing framework (TDD methodology)

### **Optional** (with graceful fallback)
- **`stockfish`** - Chess engine (falls back to random AI)
- **`pygame`** - GUI and sound (console mode available)

## 🎯 **Development Philosophy**

### **TDD Approach**
1. **Red**: Write failing test for feature
2. **Green**: Write minimal code to pass test  
3. **Refactor**: Clean up while keeping tests green

### **Key Principles**
- **Make the change easy, then make the easy change**
- **Prefer procedural over class-based** when appropriate
- **Comprehensive testing** - 142+ tests ensure reliability
- **Educational focus** - prioritize learning over competitive strength

## 🚀 **For New Development Sessions**

### **Understanding Codebase**
1. **Read this document** for architectural context
2. **Start with `main.py`** - understand entry point and flow
3. **Examine `src/game/board_state.py`** - core chess logic
4. **Check recent commits** in high-activity files for context

### **Making Changes**
- **Follow TDD methodology** - tests first, then implementation
- **Respect layered architecture** - UI → Game → AI → Utils
- **Test thoroughly** - especially changes to high-impact components
- **Maintain pluggable design** - use interfaces for extensibility

---

**Bottom Line**: PyChessBot is a mature, well-architected educational chess platform with clean separation of concerns, comprehensive testing, and active GUI development. Changes should respect existing patterns and TDD approach.