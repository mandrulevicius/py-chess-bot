"""Tests for sound manager."""

import pytest
import pygame
import os
from unittest.mock import Mock, patch, call
from src.ui.sound_manager import SoundManager, get_sound_manager, initialize_sound_system


class TestSoundManager:
    """Test the SoundManager class."""
    
    def test_sound_manager_initialization_disabled(self):
        """Test sound manager initialization when disabled."""
        sound_manager = SoundManager(enabled=False)
        
        assert not sound_manager.enabled
        assert not sound_manager.initialized
        assert sound_manager.sounds == {}
    
    @patch('pygame.mixer.init')
    @patch('pygame.mixer.pre_init')
    def test_sound_manager_initialization_enabled(self, mock_pre_init, mock_init):
        """Test sound manager initialization when enabled."""
        sound_manager = SoundManager(enabled=True)
        
        mock_pre_init.assert_called_once()
        mock_init.assert_called_once()
        assert sound_manager.enabled
        assert sound_manager.initialized
    
    @patch('pygame.mixer.init', side_effect=pygame.error("Mixer init failed"))
    @patch('pygame.mixer.pre_init')
    def test_sound_manager_initialization_failure(self, mock_pre_init, mock_init):
        """Test sound manager handles pygame initialization failure gracefully."""
        sound_manager = SoundManager(enabled=True)
        
        assert not sound_manager.enabled  # Should be disabled after failure
        assert not sound_manager.initialized
    
    def test_set_volume(self):
        """Test volume setting."""
        sound_manager = SoundManager(enabled=False)
        
        sound_manager.set_volume(0.5)
        assert sound_manager.volume == 0.5
        
        # Test clamping
        sound_manager.set_volume(1.5)
        assert sound_manager.volume == 1.0
        
        sound_manager.set_volume(-0.5)
        assert sound_manager.volume == 0.0
    
    def test_play_sound_disabled(self):
        """Test playing sound when disabled."""
        sound_manager = SoundManager(enabled=False)
        
        # Should not raise any errors
        sound_manager.play_sound('move')
        sound_manager.play_move_sound()
        sound_manager.play_error_sound()
    
    @patch('pygame.mixer.Sound')
    @patch('pygame.mixer.init')
    @patch('pygame.mixer.pre_init')
    @patch('os.path.exists', return_value=True)
    def test_load_sounds(self, mock_exists, mock_pre_init, mock_init, mock_sound_class):
        """Test sound loading."""
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound
        
        sound_manager = SoundManager(enabled=True)
        
        # Should have attempted to load sounds
        assert mock_sound_class.call_count > 0
        mock_sound.set_volume.assert_called()
    
    @patch('pygame.mixer.Sound')
    @patch('pygame.mixer.init')
    @patch('pygame.mixer.pre_init')
    @patch('os.path.exists', return_value=True)
    def test_play_sound_enabled(self, mock_exists, mock_pre_init, mock_init, mock_sound_class):
        """Test playing sound when enabled."""
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound
        
        sound_manager = SoundManager(enabled=True)
        sound_manager.sounds['move'] = mock_sound
        
        sound_manager.play_sound('move')
        
        mock_sound.set_volume.assert_called()
        mock_sound.play.assert_called_once()
    
    def test_play_move_sound_priorities(self):
        """Test move sound priority logic."""
        sound_manager = SoundManager(enabled=False)
        
        with patch.object(sound_manager, 'play_sound') as mock_play:
            # Test checkmate (highest priority)
            sound_manager.play_move_sound(is_checkmate=True, is_check=True, is_capture=True)
            mock_play.assert_called_with('checkmate')
            
            # Test check
            mock_play.reset_mock()
            sound_manager.play_move_sound(is_check=True, is_capture=True)
            mock_play.assert_called_with('check')
            
            # Test castle
            mock_play.reset_mock()
            sound_manager.play_move_sound(is_castle=True, is_capture=True)
            mock_play.assert_called_with('castle')
            
            # Test promotion
            mock_play.reset_mock()
            sound_manager.play_move_sound(is_promotion=True, is_capture=True)
            mock_play.assert_called_with('promotion')
            
            # Test capture
            mock_play.reset_mock()
            sound_manager.play_move_sound(is_capture=True)
            mock_play.assert_called_with('capture')
            
            # Test normal move
            mock_play.reset_mock()
            sound_manager.play_move_sound()
            mock_play.assert_called_with('move')
    
    def test_convenience_methods(self):
        """Test convenience sound methods."""
        sound_manager = SoundManager(enabled=False)
        
        with patch.object(sound_manager, 'play_sound') as mock_play:
            sound_manager.play_error_sound()
            mock_play.assert_called_with('error')
            
            sound_manager.play_game_start_sound()
            mock_play.assert_called_with('game_start')
            
            sound_manager.play_game_end_sound()
            mock_play.assert_called_with('game_end')
    
    def test_is_enabled(self):
        """Test enabled status check."""
        sound_manager = SoundManager(enabled=False)
        assert not sound_manager.is_enabled()
        
        sound_manager.enabled = True
        sound_manager.initialized = True
        assert sound_manager.is_enabled()
    
    def test_get_available_sounds(self):
        """Test getting available sounds list."""
        sound_manager = SoundManager(enabled=False)
        sound_manager.sounds = {'move': Mock(), 'capture': Mock()}
        
        available = sound_manager.get_available_sounds()
        assert 'move' in available
        assert 'capture' in available


class TestSoundManagerGlobal:
    """Test global sound manager functions."""
    
    def test_get_sound_manager_singleton(self):
        """Test that get_sound_manager returns the same instance."""
        # Clear any existing instance
        import src.ui.sound_manager
        src.ui.sound_manager._sound_manager = None
        
        manager1 = get_sound_manager()
        manager2 = get_sound_manager()
        
        assert manager1 is manager2
    
    def test_initialize_sound_system(self):
        """Test initialize_sound_system function."""
        # Clear any existing instance
        import src.ui.sound_manager
        src.ui.sound_manager._sound_manager = None
        
        manager = initialize_sound_system(enabled=False, volume=0.5)
        
        assert manager.volume == 0.5
        assert not manager.enabled


class TestSoundFiles:
    """Test sound file generation and existence."""
    
    def test_sound_files_exist(self):
        """Test that generated sound files exist."""
        sounds_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'sounds')
        sounds_dir = os.path.normpath(sounds_dir)
        
        expected_files = [
            'move.wav',
            'capture.wav', 
            'check.wav',
            'checkmate.wav',
            'castle.wav',
            'promotion.wav',
            'error.wav',
            'game_start.wav',
            'game_end.wav'
        ]
        
        for filename in expected_files:
            filepath = os.path.join(sounds_dir, filename)
            assert os.path.exists(filepath), f"Sound file {filename} should exist"
            
            # Check file is not empty
            assert os.path.getsize(filepath) > 0, f"Sound file {filename} should not be empty"


class TestSoundIntegration:
    """Integration tests for sound system."""
    
    @patch('pygame.mixer.init')
    @patch('pygame.mixer.pre_init')
    def test_sound_system_with_pygame_available(self, mock_pre_init, mock_init):
        """Test sound system when pygame is available."""
        manager = SoundManager(enabled=True)
        
        assert manager.initialized
        mock_pre_init.assert_called_once()
        mock_init.assert_called_once()
    
    def test_sound_system_graceful_degradation(self):
        """Test that sound system fails gracefully without pygame sounds."""
        # This test runs without mocking to ensure real behavior
        manager = SoundManager(enabled=True)
        
        # Should not raise exceptions even if some sounds are missing
        manager.play_sound('nonexistent_sound')
        manager.play_move_sound()
        manager.play_error_sound()
        
        # These should always work
        manager.set_volume(0.5)
        manager.set_enabled(False)
        available_sounds = manager.get_available_sounds()
        assert isinstance(available_sounds, list)