import pygame
from settings import *
from pygame.math import Vector2 as vector

class Slash(pygame.sprite.Sprite):

	def __init__(self, pos, surf, direction, groups):

		super().__init__(groups)

		self.image = surf

		# If facing left direction, flip bullet image
		if direction.x < 0:
			self.image = pygame.transform.flip(self.image, True, False)

		self.rect = self.image.get_rect(center = pos)
		
		# float based movement

		self.direction = direction
		self.pos = vector(self.rect.center)
		self.speed = 75

		# Timer and mask for bullet
		self.start_time = pygame.time.get_ticks()
		self.mask = pygame.mask.from_surface(self.image)

	

	def update(self, dt):

		# Constantly updates the bullet to make it appear as if it is shot
		self.pos += self.direction * self.speed * dt
		self.rect.center = (round(self.pos.x), round(self.pos.y))

		if pygame.time.get_ticks() - self.start_time > 100: # Kills bullet sprite if it moves offscreen
			self.kill()

		