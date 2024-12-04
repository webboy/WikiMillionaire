import pygame
import os

class SoundService:
    def __init__(self):
        """
        Initialize the SoundService and pygame mixer.
        """
        pygame.mixer.init()  # Initialize pygame mixer for sound playback
        # Use os.path.join for cross-platform path handling
        self.folder = os.path.join(os.path.dirname(__file__), '..', 'media')

        self.answer_sound = os.path.join(self.folder, 'answer_sound.mp3')
        self.end_sound = os.path.join(self.folder, 'end_sound.mp3')
        self.opening_sound = os.path.join(self.folder, 'opening_sound.mp3')
        self.background_sound = os.path.join(self.folder, 'background_sound.mp3')

        self.is_enabled = True

    def enable_sound(self):
        self.is_enabled = True

    def disable_sound(self):
        self.is_enabled = False
        pygame.mixer.music.stop()

    def play_background_music(self):
        """
        Play background music in a loop.
        """
        if self.is_enabled:
            pygame.mixer.music.load(self.background_sound)
            pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    def stop_background_music(self):
        """
        Stop the background music.
        """
        pygame.mixer.music.stop()

    def play_sound_effect(self, sound_file):
        """
        Play a sound effect.
        :param sound_file: The path to the sound file to be played.
        """
        if self.is_enabled:
            try:
                sound = pygame.mixer.Sound(sound_file)
                sound.play()
            except pygame.error as e:
                print(f"Error playing sound {sound_file}: {e}")

    def play_answer_sound(self):
        """
        Play the answer sound effect.
        """
        self.play_sound_effect(self.answer_sound)

    def play_end_sound(self):
        """
        Play the end game sound effect.
        """
        self.play_sound_effect(self.end_sound)

    def play_opening_sound(self):
        """
        Play the opening sound effect.
        """
        self.play_sound_effect(self.opening_sound)

