import os

import pygame

def load_font(fontname: str, fontsize: int) -> pygame.font.Font:
	return pygame.font.Font(os.path.join("assets", "fonts", fontname), fontsize)