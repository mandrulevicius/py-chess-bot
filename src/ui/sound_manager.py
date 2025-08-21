"""Sound manager for chess game audio effects."""

import pygame
import os
import logging
from typing import Dict, Optional


class SoundManager:
    """Manages sound effects for the chess game."""
    
    def __init__(self, enabled: bool = True, volume: float = 0.7):
        """
        Initialize the sound manager.
        
        Args:
            enabled: Whether sound effects are enabled
            volume: Default volume level (0.0 to 1.0)
        """
        self.enabled = enabled
        self.volume = max(0.0, min(1.0, volume))
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.initialized = False
        
        if self.enabled:
            self._initialize_pygame_mixer()
            self._load_sounds()
    
    def _initialize_pygame_mixer(self):
        """Initialize pygame mixer for sound playback."""
        try:
            # Initialize mixer with reasonable defaults
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            self.initialized = True
            logging.info("Sound system initialized successfully")
        except pygame.error as e:
            logging.warning(f"Failed to initialize sound system: {e}")
            self.enabled = False
    
    def _load_sounds(self):
        """Load sound effect files."""
        if not self.initialized:
            return
            
        # Define sound files and their paths
        sound_files = {
            'move': 'move.wav',
            'capture': 'capture.wav', 
            'check': 'check.wav',
            'checkmate': 'checkmate.wav',
            'castle': 'castle.wav',
            'promotion': 'promotion.wav',
            'error': 'error.wav',
            'game_start': 'game_start.wav',
            'game_end': 'game_end.wav'
        }
        
        # Get the sound assets directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sounds_dir = os.path.join(current_dir, '..', '..', 'assets', 'sounds')
        sounds_dir = os.path.normpath(sounds_dir)
        
        # Load available sound files
        for sound_name, filename in sound_files.items():
            sound_path = os.path.join(sounds_dir, filename)
            
            if os.path.exists(sound_path):
                try:
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(self.volume)
                    self.sounds[sound_name] = sound
                    logging.debug(f"Loaded sound: {sound_name}")
                except pygame.error as e:
                    logging.warning(f"Failed to load sound {sound_name}: {e}")
            else:
                logging.debug(f"Sound file not found: {sound_path}")
    
    def play_sound(self, sound_type: str, volume: Optional[float] = None):
        """
        Play a sound effect.
        
        Args:
            sound_type: Type of sound to play ('move', 'capture', 'check', etc.)
            volume: Override volume for this sound (0.0 to 1.0)
        """
        if not self.enabled or not self.initialized:
            return
            
        if sound_type not in self.sounds:
            logging.debug(f"Sound not available: {sound_type}")
            return
            
        try:
            sound = self.sounds[sound_type]
            
            # Set volume if specified
            if volume is not None:
                sound.set_volume(max(0.0, min(1.0, volume)))
            else:
                sound.set_volume(self.volume)
            
            # Play the sound
            sound.play()
            logging.debug(f"Played sound: {sound_type}")
            
        except pygame.error as e:
            logging.warning(f"Failed to play sound {sound_type}: {e}")
    
    def play_move_sound(self, is_capture: bool = False, is_check: bool = False, 
                       is_checkmate: bool = False, is_castle: bool = False,
                       is_promotion: bool = False):
        """
        Play appropriate sound for a chess move.
        
        Args:
            is_capture: Whether the move captures a piece
            is_check: Whether the move puts opponent in check
            is_checkmate: Whether the move is checkmate
            is_castle: Whether the move is castling
            is_promotion: Whether the move is pawn promotion
        """
        # Priority order: checkmate > check > castle > promotion > capture > move
        if is_checkmate:
            self.play_sound('checkmate')
        elif is_check:
            self.play_sound('check')
        elif is_castle:
            self.play_sound('castle')
        elif is_promotion:
            self.play_sound('promotion')
        elif is_capture:
            self.play_sound('capture')
        else:
            self.play_sound('move')
    
    def play_error_sound(self):
        """Play error sound for invalid moves."""
        self.play_sound('error')
    
    def play_game_start_sound(self):
        """Play sound when game starts."""
        self.play_sound('game_start')
    
    def play_game_end_sound(self):
        """Play sound when game ends."""
        self.play_sound('game_end')
    
    def set_volume(self, volume: float):
        """
        Set the master volume for all sounds.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        
        # Update volume for all loaded sounds
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
    
    def set_enabled(self, enabled: bool):
        """
        Enable or disable sound effects.
        
        Args:
            enabled: Whether to enable sound effects
        """
        self.enabled = enabled
        
        if enabled and not self.initialized:
            self._initialize_pygame_mixer()
            self._load_sounds()
    
    def is_enabled(self) -> bool:
        """Check if sound effects are enabled and working."""
        return self.enabled and self.initialized
    
    def get_available_sounds(self) -> list:
        """Get list of available sound effects."""
        return list(self.sounds.keys())
    
    def cleanup(self):
        """Clean up sound resources."""
        if self.initialized:
            try:
                pygame.mixer.quit()
                logging.debug("Sound system cleaned up")
            except pygame.error as e:
                logging.warning(f"Error during sound cleanup: {e}")


# Global sound manager instance
_sound_manager: Optional[SoundManager] = None


def get_sound_manager() -> SoundManager:
    """Get the global sound manager instance."""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager


def initialize_sound_system(enabled: bool = True, volume: float = 0.7) -> SoundManager:
    """
    Initialize the global sound system.
    
    Args:
        enabled: Whether sound effects should be enabled
        volume: Default volume level (0.0 to 1.0)
        
    Returns:
        The initialized sound manager
    """
    global _sound_manager
    _sound_manager = SoundManager(enabled=enabled, volume=volume)
    return _sound_manager


def cleanup_sound_system():
    """Clean up the global sound system."""
    global _sound_manager
    if _sound_manager is not None:
        _sound_manager.cleanup()
        _sound_manager = None