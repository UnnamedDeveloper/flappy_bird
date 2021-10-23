import os
import sys
import pathlib

import pygame

def load_font(fontname: str, fontsize: int) -> pygame.font.Font:
	root_dir = pathlib.Path(sys.argv[0]).parent.resolve()
	return pygame.font.Font(os.path.join(root_dir, "assets", "fonts", fontname), fontsize)