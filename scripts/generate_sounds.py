"""Generate basic sound effects for chess game."""

import pygame
import numpy as np
import os
import sys
import wave

def generate_tone(frequency, duration, sample_rate=22050, volume=0.5):
    """Generate a simple sine wave tone."""
    frames = int(duration * sample_rate)
    arr = np.zeros((frames, 2))
    
    for i in range(frames):
        wave = np.sin(2 * np.pi * frequency * i / sample_rate) * volume
        arr[i] = [wave, wave]  # Stereo
    
    return (arr * 32767).astype(np.int16)

def generate_click(duration=0.1, volume=0.3):
    """Generate a click sound for moves."""
    return generate_tone(800, duration, volume=volume)

def generate_capture(duration=0.2, volume=0.4):
    """Generate a sharper sound for captures."""
    # Mix two frequencies for a more distinctive sound
    tone1 = generate_tone(600, duration, volume=volume)
    tone2 = generate_tone(1200, duration/2, volume=volume/2)
    
    # Combine the tones
    result = tone1.copy()
    frames = min(len(tone1), len(tone2))
    result[:frames] += tone2[:frames]
    
    return result

def generate_check(duration=0.3, volume=0.5):
    """Generate a warning sound for check."""
    # Rising tone
    sample_rate = 22050
    frames = int(duration * sample_rate)
    arr = np.zeros((frames, 2))
    
    for i in range(frames):
        # Frequency rises from 400 to 800 Hz
        freq = 400 + (400 * i / frames)
        wave = np.sin(2 * np.pi * freq * i / sample_rate) * volume
        arr[i] = [wave, wave]
    
    return (arr * 32767).astype(np.int16)

def generate_error(duration=0.2, volume=0.3):
    """Generate an error sound."""
    # Low, buzzing sound
    return generate_tone(200, duration, volume=volume)

def save_sound(sound_array, filename):
    """Save sound array as WAV file."""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(22050)  # Sample rate
        wav_file.writeframes(sound_array.tobytes())

def main():
    """Generate all sound effects."""
    
    # Get the sounds directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sounds_dir = os.path.join(script_dir, '..', 'assets', 'sounds')
    sounds_dir = os.path.normpath(sounds_dir)
    
    # Create directory if it doesn't exist
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("Generating sound effects...")
    
    # Generate and save sounds
    sounds_to_generate = {
        'move.wav': generate_click(),
        'capture.wav': generate_capture(),
        'check.wav': generate_check(),
        'error.wav': generate_error(),
        'castle.wav': generate_click(duration=0.15, volume=0.4),
        'promotion.wav': generate_check(duration=0.25, volume=0.4),
        'checkmate.wav': generate_check(duration=0.5, volume=0.6),
        'game_start.wav': generate_tone(523, 0.3, volume=0.4),  # C note
        'game_end.wav': generate_tone(261, 0.5, volume=0.4),    # Lower C note
    }
    
    for filename, sound_data in sounds_to_generate.items():
        filepath = os.path.join(sounds_dir, filename)
        save_sound(sound_data, filepath)
        print(f"Generated: {filename}")
    
    print(f"\nSound effects saved to: {sounds_dir}")
    print("You can replace these with custom sound files later.")

if __name__ == "__main__":
    try:
        import numpy as np
        main()
    except ImportError:
        print("NumPy is required to generate sound effects.")
        print("Install with: pip install numpy")
        print("\nAlternatively, you can:")
        print("1. Skip sound generation and add sound files manually to assets/sounds/")
        print("2. The game will work without sound files (just no audio)")
        sys.exit(1)