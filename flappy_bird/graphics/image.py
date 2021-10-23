import os
import sys
import pathlib

import pygame

def load_image(path: str) -> pygame.Surface:
	root_dir = pathlib.Path(sys.argv[0]).parent.resolve()
	return pygame.image.load(os.path.join(root_dir, "assets", "sprites", path))
