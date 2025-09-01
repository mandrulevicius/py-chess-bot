#!/usr/bin/env python3
"""
PyChessBot Project Dependency Graph Data

This file contains the structured dependency graph data for the PyChessBot project,
including file descriptions, dependencies, and git change history for heatmap visualization.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GitStats:
    """Git statistics for a file"""
    commit_count: int
    lines_added: int
    lines_deleted: int
    last_modified: str
    recent_activity: float  # 0-1 score based on recent changes

@dataclass
class FileNode:
    """Represents a file node in the dependency graph"""
    path: str
    short_name: str
    description: str
    category: str  # main, game, ai, ui, analysis, utils, core
    git_stats: Optional[GitStats] = None

@dataclass
class DependencyEdge:
    """Represents a dependency between two files"""
    source: str
    target: str
    reason: str
    edge_type: str  # import, function_call, class_instantiation

# File nodes with descriptions
NODES = [
    FileNode(
        path="main.py",
        short_name="main",
        description="Main application entry point with argument parsing, game setup, and main game loop for console interface",
        category="main"
    ),
    
    # Core Game Logic
    FileNode(
        path="src/game/game_loop.py",
        short_name="game_loop",
        description="Core game state management and turn-based gameplay logic",
        category="game"
    ),
    FileNode(
        path="src/game/board_state.py",
        short_name="board_state",
        description="Chess board state management using python-chess library",
        category="game"
    ),
    FileNode(
        path="src/game/move_validator.py",
        short_name="move_validator",
        description="Move validation combining syntax parsing and board position checking",
        category="game"
    ),
    FileNode(
        path="src/game/move_parser.py",
        short_name="move_parser",
        description="Standard Algebraic Notation (SAN) move parsing and validation",
        category="game"
    ),
    FileNode(
        path="src/game/move_analyzer.py",
        short_name="move_analyzer",
        description="Chess move analysis for sound effects (captures, checks, castling, etc.)",
        category="game"
    ),
    
    # AI Components
    FileNode(
        path="src/ai/stockfish_ai.py",
        short_name="stockfish_ai",
        description="Stockfish engine integration with SafeStockfish wrapper for resource management",
        category="ai"
    ),
    FileNode(
        path="src/alternatives/random_ai.py",
        short_name="random_ai",
        description="Random move AI for testing and fallback purposes",
        category="ai"
    ),
    
    # User Interface
    FileNode(
        path="src/ui/console_interface.py",
        short_name="console_interface",
        description="Console-based user interface for human chess interaction",
        category="ui"
    ),
    FileNode(
        path="src/ui/pygame_interface.py",
        short_name="pygame_interface",
        description="PyGame GUI interface with graphical chess board",
        category="ui"
    ),
    FileNode(
        path="src/ui/sound_manager.py",
        short_name="sound_manager",
        description="Sound effects management using pygame.mixer",
        category="ui"
    ),
    FileNode(
        path="src/ui/learning_gui.py",
        short_name="learning_gui",
        description="GUI components for learning features (evaluation display, etc.)",
        category="ui"
    ),
    
    # Analysis & Learning Features
    FileNode(
        path="src/analysis/position_evaluator.py",
        short_name="position_evaluator",
        description="Position evaluation using Stockfish with caching",
        category="analysis"
    ),
    FileNode(
        path="src/analysis/move_history.py",
        short_name="move_history",
        description="Move history tracking with undo/redo functionality",
        category="analysis"
    ),
    FileNode(
        path="src/analysis/solo_mode.py",
        short_name="solo_mode",
        description="Solo mode state management (human controls both sides)",
        category="analysis"
    ),
    
    # Utilities & Core
    FileNode(
        path="src/utils/logger.py",
        short_name="logger",
        description="Structured logging with colored console output",
        category="utils"
    ),
    FileNode(
        path="src/utils/cache.py",
        short_name="cache",
        description="TTL caching utilities for performance optimization",
        category="utils"
    ),
    FileNode(
        path="src/core/interfaces.py",
        short_name="interfaces",
        description="Abstract interfaces for pluggable architecture",
        category="core"
    ),
]

# Dependency edges
EDGES = [
    # main.py dependencies
    DependencyEdge("main.py", "src/utils/logger.py", "logging functionality", "import"),
    DependencyEdge("main.py", "src/game/game_loop.py", "game state management functions", "import"),
    DependencyEdge("main.py", "src/ai/stockfish_ai.py", "AI engine creation and management", "import"),
    DependencyEdge("main.py", "src/ui/console_interface.py", "console UI functions", "import"),
    DependencyEdge("main.py", "src/ui/sound_manager.py", "sound system initialization", "import"),
    DependencyEdge("main.py", "src/analysis/position_evaluator.py", "position analysis for learning features", "import"),
    DependencyEdge("main.py", "src/analysis/move_history.py", "undo/redo functionality", "import"),
    DependencyEdge("main.py", "src/analysis/solo_mode.py", "solo mode management", "import"),
    DependencyEdge("main.py", "src/alternatives/random_ai.py", "fallback AI engine", "dynamic_import"),
    DependencyEdge("main.py", "src/ui/pygame_interface.py", "GUI interface", "dynamic_import"),
    
    # Game logic dependencies
    DependencyEdge("src/game/game_loop.py", "src/game/board_state.py", "board creation, move application, FEN conversion", "import"),
    DependencyEdge("src/game/game_loop.py", "src/game/move_analyzer.py", "move analysis for sound effects", "import"),
    
    DependencyEdge("src/game/board_state.py", "src/game/move_validator.py", "move validation functionality", "import"),
    
    DependencyEdge("src/game/move_validator.py", "src/game/move_parser.py", "SAN notation parsing", "import"),
    
    # AI dependencies
    DependencyEdge("src/ai/stockfish_ai.py", "src/utils/logger.py", "AI-specific logging", "import"),
    DependencyEdge("src/ai/stockfish_ai.py", "src/game/board_state.py", "FEN position handling", "dynamic_import"),
    
    DependencyEdge("src/alternatives/random_ai.py", "src/core/interfaces.py", "ChessAI interface implementation", "import"),
    
    # UI dependencies
    DependencyEdge("src/ui/console_interface.py", "src/game/game_loop.py", "game state query functions", "import"),
    DependencyEdge("src/ui/console_interface.py", "src/ui/sound_manager.py", "sound effects integration", "import"),
    
    DependencyEdge("src/ui/pygame_interface.py", "src/game/game_loop.py", "game state management", "import"),
    DependencyEdge("src/ui/pygame_interface.py", "src/game/board_state.py", "FEN position handling", "import"),
    DependencyEdge("src/ui/pygame_interface.py", "src/ui/sound_manager.py", "sound effects", "import"),
    DependencyEdge("src/ui/pygame_interface.py", "src/ui/learning_gui.py", "learning feature GUI components", "import"),
    
    # Analysis dependencies
    DependencyEdge("src/analysis/position_evaluator.py", "src/ai/stockfish_ai.py", "AI engine for evaluation", "import"),
    DependencyEdge("src/analysis/position_evaluator.py", "src/utils/cache.py", "caching decorator for performance", "import"),
    DependencyEdge("src/analysis/position_evaluator.py", "src/game/board_state.py", "FEN position handling", "import"),
    
    # Utility dependencies
    DependencyEdge("src/utils/cache.py", "src/game/board_state.py", "FEN-based cache keys", "import"),
]

# Git statistics data (manually extracted from git log analysis)
GIT_STATS = {
    "main.py": GitStats(
        commit_count=8,
        lines_added=320,
        lines_deleted=65,
        last_modified="2025-08-24",
        recent_activity=0.9
    ),
    "src/ai/stockfish_ai.py": GitStats(
        commit_count=6,
        lines_added=284,
        lines_deleted=32,
        last_modified="2025-08-27",
        recent_activity=0.8
    ),
    "src/game/game_loop.py": GitStats(
        commit_count=2,
        lines_added=171,
        lines_deleted=2,
        last_modified="2025-08-21",
        recent_activity=0.6
    ),
    "src/game/board_state.py": GitStats(
        commit_count=1,
        lines_added=95,
        lines_deleted=0,
        last_modified="2025-08-20",
        recent_activity=0.5
    ),
    "src/game/move_validator.py": GitStats(
        commit_count=1,
        lines_added=50,
        lines_deleted=0,
        last_modified="2025-08-20",
        recent_activity=0.5
    ),
    "src/game/move_parser.py": GitStats(
        commit_count=3,
        lines_added=126,
        lines_deleted=36,
        last_modified="2025-08-21",
        recent_activity=0.6
    ),
    "src/game/move_analyzer.py": GitStats(
        commit_count=1,
        lines_added=72,
        lines_deleted=0,
        last_modified="2025-08-21",
        recent_activity=0.6
    ),
    "src/ui/console_interface.py": GitStats(
        commit_count=3,
        lines_added=185,
        lines_deleted=4,
        last_modified="2025-08-24",
        recent_activity=0.7
    ),
    "src/ui/pygame_interface.py": GitStats(
        commit_count=15,
        lines_added=1419,
        lines_deleted=222,
        last_modified="2025-08-23",
        recent_activity=1.0  # Highest activity
    ),
    "src/ui/sound_manager.py": GitStats(
        commit_count=1,
        lines_added=226,
        lines_deleted=0,
        last_modified="2025-08-21",
        recent_activity=0.6
    ),
    "src/ui/learning_gui.py": GitStats(
        commit_count=6,
        lines_added=455,
        lines_deleted=101,
        last_modified="2025-08-23",
        recent_activity=0.9
    ),
    "src/analysis/position_evaluator.py": GitStats(
        commit_count=3,
        lines_added=181,
        lines_deleted=29,
        last_modified="2025-08-24",
        recent_activity=0.8
    ),
    "src/analysis/move_history.py": GitStats(
        commit_count=1,
        lines_added=101,
        lines_deleted=0,
        last_modified="2025-08-21",
        recent_activity=0.6
    ),
    "src/analysis/solo_mode.py": GitStats(
        commit_count=1,
        lines_added=55,
        lines_deleted=0,
        last_modified="2025-08-21",
        recent_activity=0.6
    ),
    "src/utils/logger.py": GitStats(
        commit_count=1,
        lines_added=149,
        lines_deleted=0,
        last_modified="2025-08-24",
        recent_activity=0.7
    ),
    "src/utils/cache.py": GitStats(
        commit_count=2,
        lines_added=101,
        lines_deleted=0,
        last_modified="2025-08-27",
        recent_activity=0.8
    ),
    "src/core/interfaces.py": GitStats(
        commit_count=1,
        lines_added=138,
        lines_deleted=0,
        last_modified="2025-08-24",
        recent_activity=0.7
    ),
    "src/alternatives/random_ai.py": GitStats(
        commit_count=1,
        lines_added=81,
        lines_deleted=0,
        last_modified="2025-08-24",
        recent_activity=0.7
    ),
}

# Add git stats to nodes
for node in NODES:
    if node.path in GIT_STATS:
        node.git_stats = GIT_STATS[node.path]

# Category colors for visualization
CATEGORY_COLORS = {
    "main": "#FF6B6B",      # Red - entry point
    "game": "#4ECDC4",      # Teal - core game logic
    "ai": "#45B7D1",        # Blue - AI components
    "ui": "#96CEB4",        # Green - user interfaces
    "analysis": "#FFEAA7",  # Yellow - learning/analysis
    "utils": "#DDA0DD",     # Purple - utilities
    "core": "#FFB347",      # Orange - core interfaces
}

def get_nodes_by_category() -> Dict[str, List[FileNode]]:
    """Group nodes by category"""
    categories = {}
    for node in NODES:
        if node.category not in categories:
            categories[node.category] = []
        categories[node.category].append(node)
    return categories

def get_high_activity_files(threshold: float = 0.8) -> List[FileNode]:
    """Get files with high recent activity"""
    return [node for node in NODES 
            if node.git_stats and node.git_stats.recent_activity >= threshold]

def get_dependency_graph() -> Tuple[List[FileNode], List[DependencyEdge]]:
    """Get the complete dependency graph"""
    return NODES, EDGES