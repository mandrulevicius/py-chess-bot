# PyChessBot - Development Guide

> **Practical guidance for Claude Code development sessions**

## 🎯 **Project Type & Methodology**

**PyChessBot** is an educational chess learning platform built with **Test Driven Development (TDD)**:
- **Red-Green-Refactor** cycle for all features
- **142+ comprehensive tests** ensure reliability
- **Procedural over class-based** approach when appropriate
- **Educational focus** - prioritize learning over competitive strength

## 🛠️ **Essential Development Commands**

### **Primary Commands** (Use these frequently)
```bash
# Run all tests - PRIMARY DEVELOPMENT COMMAND
python -m pytest tests/ -v

# Run the application (recommended mode)
python main.py --gui --sound

# Run console mode (good for debugging)
python main.py --console --no-sound
```

### **Specific Testing**
```bash
# Test core game logic
python -m pytest tests/game/ -v

# Test user interfaces
python -m pytest tests/ui/ -v

# Test learning features  
python -m pytest tests/analysis/ -v

# Test specific file
python -m pytest tests/game/test_board_state.py -v

# Coverage report
python -m pytest tests/ --cov=src
```

### **Application Options**
```bash
# Custom difficulty (0-20)
python main.py --gui --difficulty 15

# Play as black
python main.py --gui --color black

# Custom volume
python main.py --gui --volume 0.3

# Console without sound
python main.py --console --no-sound
```

## 🏗️ **TDD Workflow** (CRITICAL)

### **Before Each Feature**
1. **Write failing test** - Define expected behavior
2. **Run test** - Confirm it fails (RED)
3. **Write minimal code** - Make test pass (GREEN)  
4. **Run tests** - Confirm all pass
5. **Refactor** - Clean up code while keeping tests green
6. **Run tests again** - Ensure nothing broke

### **Example TDD Flow**
```bash
# 1. Write test in appropriate test file
# 2. Run specific test to see it fail
python -m pytest tests/game/test_new_feature.py::test_specific_case -v

# 3. Implement minimal feature
# 4. Run test to see it pass  
python -m pytest tests/game/test_new_feature.py::test_specific_case -v

# 5. Run all tests to ensure no regressions
python -m pytest tests/ -v

# 6. Refactor and test again
python -m pytest tests/ -v
```

## 📁 **Key Files for Development**

### **Always Start Here**
- **`main.py`** - Entry point, understand CLI and game setup
- **`src/game/board_state.py`** - Core chess logic (5 dependents)
- **`CLAUDE.md`** - Project instructions and methodology

### **Core Game Engine** 
- **`src/game/game_loop.py`** - Game state management
- **`src/game/move_validator.py`** - Chess rules validation
- **`src/game/move_parser.py`** - SAN notation parsing

### **User Interfaces**
- **`src/ui/pygame_interface.py`** - Primary GUI (high activity)
- **`src/ui/console_interface.py`** - Console interface
- **`src/ui/learning_gui.py`** - Learning feature components

### **AI & Analysis**
- **`src/ai/stockfish_ai.py`** - Primary AI engine
- **`src/analysis/position_evaluator.py`** - Learning features
- **`src/analysis/move_history.py`** - Undo/redo system

## ⚠️ **High-Impact Files** (Change with care)

### **Foundation Components** (5+ dependents)
- **`src/game/board_state.py`** - Core chess state, affects many files
- **`src/game/game_loop.py`** - Game coordination hub
- **`src/ui/sound_manager.py`** - Audio system integration

### **When Changing These Files**
1. **Run comprehensive tests** before and after
2. **Check all dependents** - use overview dependency data
3. **Test integration thoroughly** - UI, AI, analysis systems
4. **Verify no regressions** in core functionality

## 🎨 **Code Style & Patterns**

### **Follow Existing Patterns**
- **Import structure**: Check neighboring files for conventions
- **Error handling**: Use existing patterns for consistency
- **Logging**: Use `src/utils/logger.py` - avoid print statements
- **Testing**: Follow existing test structure and naming

### **Architecture Principles**
- **Layered design**: UI → Game Logic → AI → Utils
- **Dependency injection**: Use interfaces for pluggable components
- **Immutable state**: Copy game state rather than mutating
- **Clean separation**: UI independent from game logic

## 🧪 **Testing Guidelines**

### **Test Organization**
```
tests/
├── game/           # Core chess logic tests
├── ai/             # AI engine tests  
├── ui/             # Interface tests
├── analysis/       # Learning feature tests
└── integration/    # Cross-component tests
```

### **Test Types**
- **Unit tests**: Test individual functions/classes
- **Integration tests**: Test component interactions
- **Game flow tests**: Test complete game scenarios

### **Writing Good Tests**
- **Descriptive names**: `test_castling_kingside_updates_board_correctly`
- **Clear arrange-act-assert** structure
- **Test edge cases** - invalid moves, game endings, etc.
- **Mock external dependencies** - Stockfish, pygame, etc.

## 🚀 **Common Development Tasks**

### **Adding New Features**
1. **Write tests first** (TDD approach)
2. **Implement minimal version**
3. **Integrate with existing systems** (UI, game loop, etc.)
4. **Add comprehensive tests**
5. **Update documentation** if architecture changes

### **Debugging Issues**
1. **Run specific tests** to isolate problem
2. **Use console mode** for easier debugging
3. **Check logs** - structured logging available
4. **Test individual components** before integration

### **GUI Development**
- **Focus on `pygame_interface.py`** - primary GUI file
- **Test mouse and keyboard input**
- **Verify board flipping** and visual feedback
- **Integrate with learning features** via `learning_gui.py`

### **AI Development** 
- **Use pluggable interface** - `src/core/interfaces.py`
- **Test with different difficulty levels**
- **Ensure graceful fallback** if engine unavailable
- **Performance test** - AI should respond within 2-3 seconds

## 🎯 **Current Development Focus**

### **Active Areas** (High activity files)
- **GUI enhancements** - `pygame_interface.py` primary focus
- **Learning features** - `learning_gui.py`, `position_evaluator.py`
- **Core stability** - `main.py` orchestration improvements

### **Stable Areas** (Lower priority)
- **Chess logic** - `board_state.py`, `move_parser.py` are stable
- **Console interface** - mature and working well
- **Sound system** - complete implementation

## 💡 **Best Practices**

### **Before Making Changes**
- **Read existing code** to understand patterns
- **Check test coverage** for the area you're modifying
- **Understand dependencies** - what depends on your changes?

### **During Development**
- **Follow TDD cycle** religiously
- **Run tests frequently** - after each small change
- **Keep changes small** - easier to debug and review

### **After Changes**
- **Run full test suite** - ensure no regressions
- **Test integration** - does it work with UI, AI, etc.?
- **Update documentation** if needed
- **Check performance** - especially for core game logic

---

**Remember**: PyChessBot follows TDD methodology strictly. **Always write tests before implementation**, and respect the existing layered architecture!