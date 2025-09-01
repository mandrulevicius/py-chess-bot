# PyChessBot - Relevant Documentation

> **Streamlined documentation for Claude Code development sessions**

This folder contains the **essential documentation** that Claude Code needs to understand and work with the PyChessBot project effectively. The documentation has been consolidated and cleaned to avoid information overload.

## 📚 **Essential Reading Order**

### **1. Start Here** ⭐
**`ARCHITECTURE_OVERVIEW.md`** - Complete architectural understanding
- Project structure and dependencies
- Key files and their roles
- Development hotspots and stable components
- Critical considerations for changes

### **2. Development Process** ⭐  
**`DEVELOPMENT_GUIDE.md`** - Practical development guidance
- TDD methodology and workflow
- Essential commands and testing
- Code style and patterns
- Common development tasks

### **3. Project Background**
**`PROJECT_CONTEXT.md`** - Goals, decisions, and current state
- Project purpose and evolution
- Technology choices and rationale
- Current capabilities and features
- Future enhancement opportunities

## 🎯 **Documentation Philosophy**

### **What's Included**
- ✅ **Architectural insights** - Essential for understanding codebase
- ✅ **Development workflow** - TDD methodology and commands
- ✅ **Current context** - Active development areas and stable components
- ✅ **Practical guidance** - What files to read, how to make changes

### **What's Excluded**
- ❌ **Visualization tools** - Moved to `docs/overview/` (non-essential)
- ❌ **Historical design docs** - Outdated architecture discussions  
- ❌ **Dependency troubleshooting** - Environment-specific issues
- ❌ **Redundant information** - Consolidated into essential docs

## 🏗️ **Quick Project Understanding**

### **What PyChessBot Is**
Educational chess learning platform with AI opponent, built using TDD methodology. Features professional GUI, real-time position analysis, and comprehensive learning tools.

### **Current Development Focus**
- **GUI enhancements** - Primary interface development
- **Learning features** - Educational tools and analysis  
- **Core stability** - Foundation components are stable

### **Key Architecture Points**
- **18 files, 7 component categories** with clean layered design
- **No circular dependencies** - proper separation of concerns
- **TDD methodology** - 142+ tests ensure reliability
- **Pluggable design** - Abstract interfaces for extensibility

## 📖 **Full Documentation Structure**

### **Essential (This Folder)**
- **`ARCHITECTURE_OVERVIEW.md`** - Complete architectural guide ⭐
- **`DEVELOPMENT_GUIDE.md`** - TDD workflow and practical guidance ⭐  
- **`PROJECT_CONTEXT.md`** - Background, goals, and current state
- **`README.md`** - This overview file

### **Detailed Analysis** (`docs/overview/`)
- Comprehensive dependency analysis with visualizations
- Git activity heatmaps and development metrics
- Multiple export formats for external tools
- Analysis scripts and data generation tools

### **Historical** (`docs/` - original files)
- Legacy design documents and specifications
- Development history and decision records
- Environment-specific troubleshooting guides
- Outdated architectural discussions

## 🎯 **For Claude Code Sessions**

### **Quick Start**
1. **Read `ARCHITECTURE_OVERVIEW.md`** - Understand the codebase structure
2. **Read `DEVELOPMENT_GUIDE.md`** - Learn TDD workflow and commands
3. **Check `PROJECT_CONTEXT.md`** - Understand goals and current state

### **Before Making Changes**
- **Check high-impact files** - `board_state.py`, `game_loop.py`, `main.py`
- **Follow TDD workflow** - Tests first, then implementation
- **Run comprehensive tests** - `python -m pytest tests/ -v`
- **Respect layered architecture** - UI → Game → AI → Utils

### **Key Development Commands**
```bash
# Primary development command - run all tests
python -m pytest tests/ -v

# Run the application
python main.py --gui --sound

# Test specific components
python -m pytest tests/game/ -v      # Core game logic
python -m pytest tests/ui/ -v        # User interfaces
```

---

## 💡 **Documentation Maintenance**

This documentation is **optimized for AI consumption** and should be updated when:
- **Architecture changes** significantly
- **New high-impact components** are added  
- **Development focus** shifts to new areas
- **Testing strategy** or methodology changes

The goal is to provide Claude Code with **just enough context** to be highly effective without information overload.