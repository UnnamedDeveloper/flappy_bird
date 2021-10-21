import esper
import pygame

from .actor import Actor
from .system import *

class Scene (object):
	def __init__(self, surface: pygame.Surface, name: str = "unnamed"):
		self.world = esper.World()
		self.surface = surface

		self.add_system(RenderSystem(False))
		self.add_system(MovementSystem())
		self.add_system(InputSystem())
		self.add_system(CollitionSystem())
		self.add_system(ScriptSystem())

		self.last_t = pygame.time.get_ticks()
		self.next_scene = self

		print(f"Loaded {name} scene")

	def update(self):
		t = pygame.time.get_ticks()
		delta = (t - self.last_t) / 1000.0
		self.last_t = t

		self.world.process(delta)

		return self.next_scene

	def load_scene(self, scene):
		self.next_scene = scene

	def add_system(self, system):
		self.world.add_processor(system)

	def add_actor(self) -> Actor:
		return Actor(self.world)

	def remove_actor(self, actor: Actor):
		actor.delete()

	def stop(self):
		pass
