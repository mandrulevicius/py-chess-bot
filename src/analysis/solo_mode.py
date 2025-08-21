"""Solo mode functionality - allows human to control both sides."""


class SoloModeState:
    """Manages solo mode state (AI enabled/disabled)."""
    
    def __init__(self):
        """Initialize with AI enabled (normal play mode)."""
        self._solo_mode_enabled = False  # False = AI enabled, True = Solo mode
    
    def toggle(self) -> bool:
        """
        Toggle between AI mode and solo mode.
        
        Returns:
            True if operation successful
        """
        self._solo_mode_enabled = not self._solo_mode_enabled
        return True
    
    def is_solo_enabled(self) -> bool:
        """Check if solo mode is enabled."""
        return self._solo_mode_enabled
    
    def should_use_ai(self) -> bool:
        """Check if AI should be used for moves."""
        return not self._solo_mode_enabled
    
    def get_status_message(self) -> str:
        """Get human-readable status message."""
        if self._solo_mode_enabled:
            return "Solo mode: Human controls both sides"
        else:
            return "AI mode: Human vs AI"


# Module-level convenience functions
def is_solo_mode_enabled(solo_state: SoloModeState) -> bool:
    """Check if solo mode is enabled."""
    return solo_state.is_solo_enabled()


def toggle_solo_mode(solo_state: SoloModeState) -> bool:
    """Toggle between AI and solo mode."""
    return solo_state.toggle()


def should_use_ai(solo_state: SoloModeState) -> bool:
    """Check if AI should be used."""
    return solo_state.should_use_ai()


def get_solo_mode_status(solo_state: SoloModeState) -> str:
    """Get solo mode status description."""
    return solo_state.get_status_message()