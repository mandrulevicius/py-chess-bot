"""Tests for solo mode functionality."""

import pytest
from src.analysis.solo_mode import (
    SoloModeState, is_solo_mode_enabled, toggle_solo_mode, 
    should_use_ai, get_solo_mode_status
)


class TestSoloMode:
    """Test solo mode toggle functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.solo_state = SoloModeState()
    
    def test_create_solo_mode_state(self):
        """Test creating solo mode state."""
        assert self.solo_state is not None
        assert is_solo_mode_enabled(self.solo_state) is False  # Default: AI enabled
        assert should_use_ai(self.solo_state) is True
    
    def test_toggle_solo_mode_on(self):
        """Test turning solo mode on."""
        # Initially AI is enabled
        assert should_use_ai(self.solo_state) is True
        
        # Toggle to solo mode
        result = toggle_solo_mode(self.solo_state)
        assert result is True  # Successfully toggled
        
        # Now solo mode should be enabled (AI disabled)
        assert is_solo_mode_enabled(self.solo_state) is True
        assert should_use_ai(self.solo_state) is False
    
    def test_toggle_solo_mode_off(self):
        """Test turning solo mode off (back to AI mode)."""
        # Start by turning solo mode on
        toggle_solo_mode(self.solo_state)
        assert is_solo_mode_enabled(self.solo_state) is True
        
        # Toggle back to AI mode
        result = toggle_solo_mode(self.solo_state)
        assert result is True
        
        # Should be back to AI mode
        assert is_solo_mode_enabled(self.solo_state) is False
        assert should_use_ai(self.solo_state) is True
    
    def test_multiple_toggles(self):
        """Test multiple toggle operations."""
        # Initially AI is enabled
        assert should_use_ai(self.solo_state) is True
        
        # Toggle multiple times
        for i in range(5):
            toggle_solo_mode(self.solo_state)
            # After odd number of toggles: solo mode (AI disabled = False)
            # After even number of toggles: AI mode (AI enabled = True)
            expected_ai_enabled = (i % 2 == 1)  # i=0: False, i=1: True, i=2: False, etc.
            assert should_use_ai(self.solo_state) == expected_ai_enabled
    
    def test_get_solo_mode_status(self):
        """Test getting solo mode status description."""
        # Test AI mode status
        status = get_solo_mode_status(self.solo_state)
        assert status is not None
        assert isinstance(status, str)
        assert "AI" in status or "ai" in status.lower()
        
        # Test solo mode status
        toggle_solo_mode(self.solo_state)
        status = get_solo_mode_status(self.solo_state)
        assert status is not None
        assert isinstance(status, str)
        assert "solo" in status.lower() or "human" in status.lower()
    
    def test_should_use_ai_for_both_modes(self):
        """Test should_use_ai returns correct values."""
        # AI mode
        assert should_use_ai(self.solo_state) is True
        
        # Solo mode  
        toggle_solo_mode(self.solo_state)
        assert should_use_ai(self.solo_state) is False
        
        # Back to AI mode
        toggle_solo_mode(self.solo_state)
        assert should_use_ai(self.solo_state) is True
    
    def test_solo_mode_persistence(self):
        """Test that solo mode state persists correctly."""
        # Enable solo mode
        toggle_solo_mode(self.solo_state)
        solo_enabled = is_solo_mode_enabled(self.solo_state)
        
        # State should remain consistent across multiple checks
        for _ in range(10):
            assert is_solo_mode_enabled(self.solo_state) == solo_enabled
            assert should_use_ai(self.solo_state) == (not solo_enabled)
    
    def test_independent_solo_mode_instances(self):
        """Test that different solo mode instances are independent."""
        solo_state2 = SoloModeState()
        
        # Toggle first instance
        toggle_solo_mode(self.solo_state)
        
        # Second instance should be unaffected
        assert is_solo_mode_enabled(self.solo_state) is True
        assert is_solo_mode_enabled(solo_state2) is False
        
        # They should behave independently
        toggle_solo_mode(solo_state2)
        assert is_solo_mode_enabled(self.solo_state) is True
        assert is_solo_mode_enabled(solo_state2) is True