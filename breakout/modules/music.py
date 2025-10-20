import numpy as np
import pygame

def generate_music():
    samplerate = 44100
    freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
    note_duration = 0.2

    music = np.array([], dtype=np.int16)

    for _ in range(4):
        for freq in freqs:
            t = np.linspace(0., note_duration, int(samplerate * note_duration), False)
            note = np.sin(freq * 2. * np.pi * t)

            # Fade in and out
            fade_len = int(samplerate * 0.01)
            fade_in = np.linspace(0., 1., fade_len)
            fade_out = np.linspace(1., 0., fade_len)

            note[:fade_len] *= fade_in
            note[-fade_len:] *= fade_out

            audio = note * 32767  # Volume
            music = np.concatenate((music, audio.astype(np.int16)))

    # Convert to a stereo sound
    stereo_music = np.zeros((len(music), 2), dtype=np.int16)
    stereo_music[:, 0] = music
    stereo_music[:, 1] = music

    sound = pygame.sndarray.make_sound(stereo_music)
    return sound
