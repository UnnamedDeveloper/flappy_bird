import types
from dataclasses import dataclass as component

import pygame

from .actor import Actor

@component
class Position:
	x: float = 0.0
	y: float = 0.0

@component
class Velocity:
	x: float = 0.0
	y: float = 0.0
	x_speed_cap: float = 500
	y_speed_cap: float = 500

@component
class Camera:
	target: pygame.Surface = None
	offset_x: float = 0.0

@component
class Background:
	image: pygame.Surface = None

@component
class Sprite:
	image: pygame.Surface = None
	layer: int = 1
	rotation: float = 0.0

@component
class InputMove:
	key: type(pygame.K_SPACE) = pygame.K_SPACE
	press: bool = True
	move_x: float = 0.0
	move_y: float = 0.0

@component
class InputCallback:
	key: type(pygame.K_ESCAPE) = pygame.K_ESCAPE
	press: bool = True
	callback: types.FunctionType = None

@component
class BoxCollider:
	offset_x: float = 0.0
	offset_y: float = 0.0
	width: float = 10.0
	height: float = 10.0
	on_collition: types.FunctionType = None

@component
class Script:
	update: types.FunctionType = None

