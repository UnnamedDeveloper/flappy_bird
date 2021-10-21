import os

import pygame

def load_image(path: str) -> pygame.Surface:
	return pygame.image.load(os.path.join("assets", "sprites", path))
