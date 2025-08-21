#!/usr/bin/env python3
"""Test script for sound effects."""

import time
from src.ui.sound_manager import initialize_sound_system


def test_sound_effects():
    """Test all sound effects."""
    print("Testing PyChessBot Sound System")
    print("=" * 40)
    
    # Initialize sound system
    sound_manager = initialize_sound_system(enabled=True, volume=0.7)
    
    if not sound_manager.is_enabled():
        print("[ERROR] Sound system failed to initialize")
        print("This might happen if:")
        print("- PyGame mixer is not working")
        print("- Audio device is not available")
        print("- Sound files are missing")
        return
    
    print("[OK] Sound system initialized successfully")
    print(f"Available sounds: {', '.join(sound_manager.get_available_sounds())}")
    print()
    
    # Test individual sounds
    sounds_to_test = [
        ('game_start', 'Game start sound'),
        ('move', 'Normal move sound'),
        ('capture', 'Capture sound'),
        ('check', 'Check sound'),
        ('castle', 'Castling sound'),
        ('promotion', 'Promotion sound'),
        ('checkmate', 'Checkmate sound'),
        ('error', 'Error sound'),
        ('game_end', 'Game end sound')
    ]
    
    print("Playing sound effects (press Ctrl+C to stop):")
    print()
    
    try:
        for sound_type, description in sounds_to_test:
            print(f"[SOUND] Playing {description}...")
            sound_manager.play_sound(sound_type)
            time.sleep(1.5)  # Wait between sounds
        
        print()
        print("[TEST] Testing move sound priority system:")
        
        # Test move sound priorities
        print("  - Normal move...")
        sound_manager.play_move_sound()
        time.sleep(1)
        
        print("  - Capture move...")
        sound_manager.play_move_sound(is_capture=True)
        time.sleep(1)
        
        print("  - Check move...")
        sound_manager.play_move_sound(is_check=True)
        time.sleep(1)
        
        print("  - Checkmate move...")
        sound_manager.play_move_sound(is_checkmate=True)
        time.sleep(1)
        
        print()
        print("[OK] All sound effects tested successfully!")
        print()
        print("Volume control test:")
        for volume in [0.3, 0.7, 1.0]:
            print(f"  [VOLUME] {volume}: ", end="")
            sound_manager.set_volume(volume)
            sound_manager.play_sound('move')
            time.sleep(0.8)
            print("OK")
        
        print()
        print("[SUCCESS] Sound system is working correctly!")
        print()
        print("You can now play PyChessBot with sound effects:")
        print("  python main.py --gui          # With sounds (default)")
        print("  python main.py --no-sound     # Without sounds")
        print("  python main.py --volume 0.5   # Custom volume")
        
    except KeyboardInterrupt:
        print("\n[STOP] Sound test interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Error during sound test: {e}")
    finally:
        # Cleanup
        sound_manager.cleanup()


if __name__ == "__main__":
    test_sound_effects()