import pygame
from pygame.math import Vector2 as vector

class Overlay:

	def __init__(self, player):

		# Gets player data, specifically health
		self.player = player

		self.display_surface = pygame.display.get_surface()

		# Gets health image
		self.health_surf = pygame.image.load('../Graphics/ninja_health.png').convert_alpha()
		self.size = vector(self.health_surf.get_size()) * 0.1
		self.stock = pygame.transform.scale(self.health_surf, self.size)

		

	def display(self):

		# For every hp the player has, blit that amount of health images
		for h in range(self.player.lives):
			x = 200 + h * (self.stock.get_width() + 6)
			y = 650
			self.display_surface.blit(self.stock, (x, y))

class Overlay2:

	def __init__(self, player):

		# Gets player data, specifically health
		self.player = player

		self.display_surface = pygame.display.get_surface()

		# Gets health image
		self.health_surf = pygame.image.load('../Graphics/robot_health.png').convert_alpha()
		self.size = vector(self.health_surf.get_size()) * 0.1
		self.stock = pygame.transform.scale(self.health_surf, self.size)

		

	def display(self):

		# For every hp the player has, blit that amount of health images
		for h in range(self.player.lives):
			x = 1200 + h * (self.stock.get_width() - 20)
			y = 635
			self.display_surface.blit(self.stock, (x, y))