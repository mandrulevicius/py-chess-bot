"""Tests for learning features GUI integration."""

import pytest
from unittest.mock import patch, MagicMock
from src.ui.learning_gui import EvaluationDisplay, SoloModeIndicator, HelpDisplay, LearningButtonPanel


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


class TestLearningButtonPanel:
    """Test GUI learning button panel functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.button_panel = LearningButtonPanel()
    
    def test_create_button_panel(self):
        """Test creating button panel."""
        assert self.button_panel is not None
        assert hasattr(self.button_panel, 'buttons')
        assert hasattr(self.button_panel, 'handle_click')
        assert len(self.button_panel.buttons) == 5  # Eval, Best, Solo, Undo, Redo
    
    def test_button_definitions(self):
        """Test button definitions are correct."""
        button_commands = [btn[1] for btn in self.button_panel.buttons]
        expected_commands = ['eval', 'best', 'solo', 'undo', 'redo']
        
        assert button_commands == expected_commands
    
    def test_handle_click_no_button(self):
        """Test click outside button area."""
        result = self.button_panel.handle_click(0, 0, 100, 100)
        assert result is None
    
    def test_handle_click_on_button(self):
        """Test click on button area."""
        # Test click on first button (eval) - approximate position (no header offset now)
        panel_x, panel_y = 100, 100
        # First button should be at (panel_x, panel_y) with size (60, 30)
        button_x = panel_x + 30  # Center of button
        button_y = panel_y + 15  # Center of button
        
        result = self.button_panel.handle_click(button_x, button_y, panel_x, panel_y)
        assert result == 'eval'