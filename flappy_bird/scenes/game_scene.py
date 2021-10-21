import threading
import sys

import pygame

from .. import audio
from .. import ecs
from .. import graphics as gfx
from .layers import *
from .bird import Bird
from .ground import Ground
from .pipe import PipePair

class GameScene (ecs.Scene):
	def __init__(self, surface: pygame.Surface, bg: pygame.Surface):
		ecs.Scene.__init__(self, surface, name = "Game")
		self.surface = surface

		self.bg = self.add_actor()
		self.bg.add_component(ecs.Background(image = bg))

		self.bird = Bird(self, surface, self.on_bird_death)

		self.pipe_interval = 1.5
		self.pipes = []
		self.timer = None

		self.create_pipe()

		self.ground1 = Ground(self, self.bird)
		self.ground2 = Ground(self, self.bird, 1)

		self.roof = self.add_actor()
		self.roof.add_component(ecs.Position(y = -40))
		self.roof.add_component(ecs.BoxCollider(width = surface.get_rect().w, height = 1))

		self.points = 0
		self.point_sound = audio.load_audio("point.wav")
		self.add_point(0) # to initialize the point display

		self.death_message = None

	def create_pipe(self):
		try:
			# start a timer for the next pipe
			self.timer = threading.Timer(self.pipe_interval, self.create_pipe)
			self.timer.start()

			# create pipe
			pipe_x = self.surface.get_rect().w + self.bird.actor.get_component(ecs.Position).x
			self.pipes.append(PipePair(self, self.surface, self.bird, pipe_x, self.on_pipe_passed))

		except Exception as e:
			print("A fatal error occured in a thread. Aborting")
			print(e)
			self.stop()

	def on_pipe_passed(self, pipe):
		# TODO: Destroy the pipe and remove it from the game
		# NOTE: Do not create new pipes here, do it on a timer
		pipe.delete()
		self.pipes.remove(pipe)
		self.add_point(1)

	def on_bird_death(self, bird):
		self.stop()
		self.death_message = self.add_actor()

		message_x = self.bird.actor.get_component(ecs.Position).x + self.surface.get_rect().w / 2
		message_x += self.bird.actor.get_component(ecs.Camera).offset_x

		self.death_message.add_component(ecs.Position(x = message_x, y = self.surface.get_rect().h / 2))
		self.death_message.add_component(ecs.Sprite(layer = LAYER_UI, image = gfx.load_image("gameover.png")))
		self.death_message.add_component(ecs.InputCallback(key = pygame.K_SPACE, callback = self.on_game_restart))
		# self.death_message.add_component(ecs.InputCallback(key = pygame.K_ESCAPE, callback = self.on_game_quit))

	def add_point(self, amount: int):
		self.points += amount
		if amount > 0:
			audio.play(self.point_sound, channel = 1)

	def on_game_quit(self, delta):
		sys.exit()

	def on_game_restart(self, delta):
		self.restart()

	def restart(self):
		self.load_scene(GameScene(self.surface, self.bg.get_component(ecs.Background).image))

	def stop(self):
		if self.timer != None:
			self.timer.cancel()
