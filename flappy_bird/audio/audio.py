import os

import pygame

audio_queue = []

def load_audio(audio_file: str) -> pygame.mixer.Sound:
	return pygame.mixer.Sound(os.path.join("assets", "audio", audio_file))

def play(sound: pygame.mixer.Sound, channel: int = 0):
	pygame.mixer.Channel(channel).play(sound)
