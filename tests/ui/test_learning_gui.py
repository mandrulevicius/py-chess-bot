"""Tests for learning features GUI integration."""

import pytest
from unittest.mock import patch, MagicMock
from src.ui.learning_gui import EvaluationDisplay, SoloModeIndicator, HelpDisplay


class TestEvaluationDisplay:
    """Test GUI evaluation display functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.display = EvaluationDisplay()
    
    def test_create_evaluation_display(self):
        """Test creating evaluation display."""
        assert self.display is not None
        assert hasattr(self.display, 'set_evaluation')
        assert hasattr(self.display, 'render')
    
    def test_set_centipawn_evaluation(self):
        """Test setting centipawn evaluation."""
        evaluation = {
            'score': 150,
            'evaluation_type': 'cp',
            'best_move': 'e4'
        }
        
        self.display.set_evaluation(evaluation)
        
        # Should store the evaluation
        assert self.display.current_evaluation == evaluation
    
    def test_set_mate_evaluation(self):
        """Test setting mate evaluation."""
        evaluation = {
            'mate_in': 3,
            'evaluation_type': 'mate',
            'best_move': 'Qh7#'
        }
        
        self.display.set_evaluation(evaluation)
        
        # Should store the evaluation
        assert self.display.current_evaluation == evaluation
    
    def test_set_error_evaluation(self):
        """Test handling error evaluation."""
        evaluation = {
            'evaluation_type': 'error',
            'error': 'Engine not available'
        }
        
        self.display.set_evaluation(evaluation)
        
        # Should handle error gracefully
        assert self.display.current_evaluation == evaluation
    
    def test_get_display_text_centipawns(self):
        """Test getting display text for centipawn evaluation."""
        evaluation = {
            'score': 75,
            'evaluation_type': 'cp'
        }
        self.display.set_evaluation(evaluation)
        
        text = self.display.get_display_text()
        assert '+0.75' in text  # 75 centipawns = +0.75
    
    def test_get_display_text_mate(self):
        """Test getting display text for mate evaluation."""
        evaluation = {
            'mate_in': -2,
            'evaluation_type': 'mate'
        }
        self.display.set_evaluation(evaluation)
        
        text = self.display.get_display_text()
        assert 'M-2' in text or 'Mate' in text
    
    def test_get_display_text_no_evaluation(self):
        """Test display text when no evaluation set."""
        text = self.display.get_display_text()
        assert text == "" or "No eval" in text


class TestSoloModeIndicator:
    """Test GUI solo mode indicator functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.indicator = SoloModeIndicator()
    
    def test_create_solo_mode_indicator(self):
        """Test creating solo mode indicator."""
        assert self.indicator is not None
        assert hasattr(self.indicator, 'set_solo_mode')
        assert hasattr(self.indicator, 'render')
    
    def test_set_ai_mode(self):
        """Test setting AI mode."""
        self.indicator.set_solo_mode(False)
        
        assert self.indicator.solo_mode_enabled is False
    
    def test_set_solo_mode(self):
        """Test setting solo mode."""
        self.indicator.set_solo_mode(True)
        
        assert self.indicator.solo_mode_enabled is True
    
    def test_get_display_text_ai_mode(self):
        """Test display text for AI mode."""
        self.indicator.set_solo_mode(False)
        
        text = self.indicator.get_display_text()
        assert 'AI' in text or 'Human vs AI' in text
    
    def test_get_display_text_solo_mode(self):
        """Test display text for solo mode."""
        self.indicator.set_solo_mode(True)
        
        text = self.indicator.get_display_text()
        assert 'Solo' in text or 'Study' in text


class TestHelpDisplay:
    """Test GUI help display functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.help_display = HelpDisplay()
    
    def test_create_help_display(self):
        """Test creating help display."""
        assert self.help_display is not None
        assert self.help_display.show_help == False
    
    def test_toggle_help(self):
        """Test toggling help display."""
        assert self.help_display.show_help == False
        
        self.help_display.toggle_help()
        assert self.help_display.show_help == True
        
        self.help_display.toggle_help()
        assert self.help_display.show_help == False
    
    def test_set_help_visible(self):
        """Test setting help visibility."""
        self.help_display.set_help_visible(True)
        assert self.help_display.show_help == True
        
        self.help_display.set_help_visible(False)
        assert self.help_display.show_help == False