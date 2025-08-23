"""GUI components for learning features."""

import pygame
from typing import Dict, Any, Optional


class EvaluationDisplay:
    """GUI component for displaying position evaluation."""
    
    def __init__(self):
        """Initialize evaluation display."""
        self.current_evaluation: Optional[Dict[str, Any]] = None
        self.font = None
        self._init_font()
    
    def _init_font(self):
        """Initialize font for evaluation display."""
        try:
            self.font = pygame.font.Font(None, 24)
        except:
            # Fallback if font loading fails
            self.font = None
    
    def set_evaluation(self, evaluation: Dict[str, Any]) -> None:
        """
        Set the current evaluation to display.
        
        Args:
            evaluation: Evaluation dictionary from position evaluator
        """
        self.current_evaluation = evaluation
    
    def get_display_text(self) -> str:
        """
        Get the text to display for current evaluation.
        
        Returns:
            String representation of evaluation
        """
        if not self.current_evaluation:
            return ""
        
        eval_type = self.current_evaluation.get('evaluation_type', 'error')
        
        if eval_type == 'error':
            return "No eval"
        elif eval_type == 'cp':
            score = self.current_evaluation.get('score', 0)
            # Convert centipawns to pawns (divide by 100)
            pawn_score = score / 100.0
            return f"{pawn_score:+.2f}"
        elif eval_type == 'mate':
            mate_in = self.current_evaluation.get('mate_in', 0)
            if mate_in > 0:
                return f"M{mate_in}"  # White mates
            else:
                return f"M{mate_in}"  # Black mates
        
        return ""
    
    def render(self, surface, x: int, y: int) -> None:
        """
        Render the evaluation display on the given surface.
        
        Args:
            surface: Pygame surface to render on
            x: X position
            y: Y position
        """
        if not self.font:
            return
        
        text = self.get_display_text()
        if not text:
            return
        
        # Choose color based on evaluation
        color = (255, 255, 255)  # White default
        if self.current_evaluation:
            eval_type = self.current_evaluation.get('evaluation_type')
            if eval_type == 'cp':
                score = self.current_evaluation.get('score', 0)
                if score > 50:
                    color = (144, 238, 144)  # Light green for positive
                elif score < -50:
                    color = (255, 182, 193)  # Light pink for negative
            elif eval_type == 'mate':
                mate_in = self.current_evaluation.get('mate_in', 0)
                if mate_in > 0:
                    color = (144, 238, 144)  # Green for white mate
                else:
                    color = (255, 182, 193)  # Pink for black mate
        
        # Render the text
        text_surface = self.font.render(text, True, color)
        surface.blit(text_surface, (x, y))


class HelpDisplay:
    """GUI component for showing help text."""
    
    def __init__(self):
        """Initialize help display."""
        self.show_help = False
        self.font = None
        self._init_font()
    
    def _init_font(self):
        """Initialize font for help display."""
        try:
            self.font = pygame.font.Font(None, 18)
        except:
            # Fallback if font loading fails
            self.font = None
    
    def toggle_help(self):
        """Toggle help display on/off."""
        self.show_help = not self.show_help
    
    def set_help_visible(self, visible: bool):
        """Set help visibility."""
        self.show_help = visible
    
    def render(self, surface, x: int, y: int) -> None:
        """
        Render the help display on the given surface.
        
        Args:
            surface: Pygame surface to render on
            x: X position
            y: Y position
        """
        if not self.show_help or not self.font:
            return
        
        help_lines = [
            "Learning Commands:",
            "  E - Position evaluation",
            "  B - Best move suggestion",
            "  S - Toggle solo mode", 
            "  U - Undo last move",
            "  R - Redo move",
            "  H - Toggle this help",
            "",
            "Click pieces to move"
        ]
        
        # Draw semi-transparent background
        help_height = len(help_lines) * 20 + 10
        help_width = 200
        background = pygame.Surface((help_width, help_height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 180))  # Semi-transparent black
        surface.blit(background, (x, y))
        
        # Render each line
        for i, line in enumerate(help_lines):
            color = (255, 255, 255) if line else (200, 200, 200)  # White or gray
            text_surface = self.font.render(line, True, color)
            surface.blit(text_surface, (x + 5, y + 5 + i * 20))


class SoloModeIndicator:
    """GUI component for indicating solo mode status."""
    
    def __init__(self):
        """Initialize solo mode indicator."""
        self.solo_mode_enabled: bool = False
        self.font = None
        self._init_font()
    
    def _init_font(self):
        """Initialize font for solo mode indicator."""
        try:
            self.font = pygame.font.Font(None, 20)
        except:
            # Fallback if font loading fails
            self.font = None
    
    def set_solo_mode(self, enabled: bool) -> None:
        """
        Set solo mode status.
        
        Args:
            enabled: True if solo mode is enabled
        """
        self.solo_mode_enabled = enabled
    
    def get_display_text(self) -> str:
        """
        Get the text to display for current mode.
        
        Returns:
            String representation of current mode
        """
        if self.solo_mode_enabled:
            return "Solo Mode"
        else:
            return "Human vs AI"
    
    def render(self, surface, x: int, y: int) -> None:
        """
        Render the solo mode indicator on the given surface.
        
        Args:
            surface: Pygame surface to render on
            x: X position
            y: Y position
        """
        if not self.font:
            return
        
        text = self.get_display_text()
        
        # Choose color based on mode
        if self.solo_mode_enabled:
            color = (255, 215, 0)  # Gold for solo mode
        else:
            color = (135, 206, 235)  # Sky blue for AI mode
        
        # Render the text
        text_surface = self.font.render(text, True, color)
        surface.blit(text_surface, (x, y))


class HelpDisplay:
    """GUI component for showing help text."""
    
    def __init__(self):
        """Initialize help display."""
        self.show_help = False
        self.font = None
        self._init_font()
    
    def _init_font(self):
        """Initialize font for help display."""
        try:
            self.font = pygame.font.Font(None, 18)
        except:
            # Fallback if font loading fails
            self.font = None
    
    def toggle_help(self):
        """Toggle help display on/off."""
        self.show_help = not self.show_help
    
    def set_help_visible(self, visible: bool):
        """Set help visibility."""
        self.show_help = visible
    
    def render(self, surface, x: int, y: int) -> None:
        """
        Render the help display on the given surface.
        
        Args:
            surface: Pygame surface to render on
            x: X position
            y: Y position
        """
        if not self.show_help or not self.font:
            return
        
        help_lines = [
            "Learning Commands:",
            "  E - Position evaluation",
            "  B - Best move suggestion",
            "  S - Toggle solo mode", 
            "  U - Undo last move",
            "  R - Redo move",
            "  H - Toggle this help",
            "",
            "Click pieces to move"
        ]
        
        # Draw semi-transparent background
        help_height = len(help_lines) * 20 + 10
        help_width = 200
        background = pygame.Surface((help_width, help_height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 180))  # Semi-transparent black
        surface.blit(background, (x, y))
        
        # Render each line
        for i, line in enumerate(help_lines):
            color = (255, 255, 255) if line else (200, 200, 200)  # White or gray
            text_surface = self.font.render(line, True, color)
            surface.blit(text_surface, (x + 5, y + 5 + i * 20))