import os
import sys
import pathlib

import pygame

audio_queue = []

def load_audio(audio_file: str) -> pygame.mixer.Sound:
	root_dir = pathlib.Path(sys.argv[0]).parent.resolve()
	return pygame.mixer.Sound(os.path.join(root_dir, "assets", "audio", audio_file))

def play(sound: pygame.mixer.Sound, channel: int = 0):
	pygame.mixer.Channel(channel).play(sound)
