import pygame
from settings import * 

class Health:

	def __init__(self, player):

		# Gets font from files
		self.display_surface = pygame.display.get_surface()
		self.player = player
		self.font = pygame.font.Font('C:/Users/faree/Downloads/Images_for_pygame/asteroid_shooter_files/project_4 - Image Text/graphics/subatomic.ttf', 50)
		self.percent = self.player.damage

	def display(self):

		# Sets up scoreboard
		score_text = f'{self.percent}%' # Text format
		text_surf = self.font.render(score_text, True, (255,255,255))
		text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH/6 - 7, WINDOW_HEIGHT - 80))
		self.display_surface.blit(text_surf, text_rect) 
		#pygame.draw.rect(self.display_surface, 'white', text_rect.inflate(10,10), width = 8, border_radius = 5)

	def update(self):

		# Adds 1 point for every meteor blown up
		self.percent = self.player.damage


class Health2:

	def __init__(self, player):

		# Gets font from files
		self.display_surface = pygame.display.get_surface()
		self.player = player
		self.font = pygame.font.Font('C:/Users/faree/Downloads/Images_for_pygame/asteroid_shooter_files/project_4 - Image Text/graphics/subatomic.ttf', 50)
		self.percent = self.player.damage

	def display(self):

		# Sets up scoreboard
		score_text = f'{self.percent}%' # Text format
		text_surf = self.font.render(score_text, True, (255,255,255))
		text_rect = text_surf.get_rect(midbottom = (5*WINDOW_WIDTH/6 + 20, WINDOW_HEIGHT - 80))
		self.display_surface.blit(text_surf, text_rect) 
		#pygame.draw.rect(self.display_surface, 'white', text_rect.inflate(10,10), width = 8, border_radius = 5)

	def update(self):

		# Adds 1 point for every meteor blown up
		self.percent = self.player.damage