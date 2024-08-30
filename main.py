import pygame, sys
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from settings import * 
from tiles import Tile, CollisionTile
from player import Player
from player2 import Player2
from projectile import Projectile
from slash import Slash
from overlay import Overlay, Overlay2
from health import Health, Health2

class AllSprites(pygame.sprite.Group):

	def __init__(self):

		super().__init__()

		# Display setup
		self.display_surface = pygame.display.get_surface()
		self.offset = vector()

		# Sky setup
		self.sky = pygame.image.load('../Graphics/Background.png').convert_alpha()

		# Map import
		tmx_map = load_pygame('../Map.tmx')


		# Dimensions
		self.sky_width = self.sky.get_width()
		self.padding = WINDOW_WIDTH/2  # padding for how much space there should be between the right and left of the window 
		map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
		self.sky_num = int(map_width // self.sky_width) # Number of times you need to blit the sky

	def custom_draw(self, player, player2):

		# change the offset vector
		self.offset.x = (player.rect.centerx + player2.rect.centerx)/2 - WINDOW_WIDTH/2
		self.offset.y = (player.rect.centery + player2.rect.centery)/2 - WINDOW_HEIGHT/2 - 100

		for x in range(self.sky_num): # Blits the sky x amounts of time so it covers the whole screen

			x_pos = -self.padding + (x * self.sky_width)
			self.display_surface.blit(self.sky, (x_pos - self.offset.x / 2.5, -self.offset.y / 2.5))

		for sprite in self.sprites():
				
			offset_rect = sprite.image.get_rect(center = sprite.rect.center)  #gets the offset position for each sprite
			offset_rect.center -= self.offset
			self.display_surface.blit(sprite.image, offset_rect) #blits the offsetted image to the screen, making it look like a camera view for the game


class Main:

	def __init__(self):

		# Display setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Smash Brawl')
		self.clock = pygame.time.Clock()

		self.y_offset = 220

		# groups
		self.all_sprites = AllSprites()
		self.collision_sprites = pygame.sprite.Group()
		self.player_group = pygame.sprite.Group()
		self.projectile_sprites1 = pygame.sprite.Group()
		self.projectile_sprites2 = pygame.sprite.Group()
		self.slash_sprites1 = pygame.sprite.Group()
		self.slash_sprites2 = pygame.sprite.Group()

		# Projectile Setup
		self.kunai = pygame.image.load('../Graphics/ninja/Kunai/0.png').convert_alpha()
		self.kunai = pygame.transform.scale_by(self.kunai, 0.2)

		self.fire = pygame.image.load('../Graphics/robot/Objects/0.png').convert_alpha()
		self.fire = pygame.transform.scale_by(self.fire, 0.2)

		self.ninja_slash = pygame.image.load('../Graphics/slash/ninja.png').convert_alpha()
		self.ninja_slash = pygame.transform.scale_by(self.ninja_slash, 0.2)
		self.ninja_slash = pygame.transform.rotate(self.ninja_slash, 20)

		self.robot_slash = pygame.image.load('../Graphics/slash/robot.png').convert_alpha()
		self.robot_slash = pygame.transform.scale_by(self.robot_slash, 0.3)

		self.setup()
		self.overlay = Overlay(self.player)
		self.overlay2 = Overlay2(self.player2)

		#Ninja Damage

		self.ninjadamage = Health(self.player)
		self.robotdamage = Health2(self.player2)




	def setup(self):

		# Gets map
		tmx_map = load_pygame('../Map.tmx')


		# Imports layers from Tiled file
		for x, y, surf in tmx_map.get_layer_by_name('bg trees').tiles():
				size = vector(surf.get_size()) * 0.5
				surface = pygame.transform.scale(surf, size)
				Tile((x*32, y*32 - self.y_offset), surface, self.all_sprites, True)


		for x, y, surf in tmx_map.get_layer_by_name('props').tiles():
				size = vector(surf.get_size()) * 0.5
				surface = pygame.transform.scale(surf, size)
				Tile((x*32, y*32 - 90), surface, self.all_sprites, True)


		for x, y, surf in tmx_map.get_layer_by_name('Platform').tiles(): # Imports 'Platform' layer from Tiles
			size = vector(surf.get_size()) * 0.5
			surface = pygame.transform.scale(surf, size)
			CollisionTile((x*32, y*32), surface, [self.all_sprites, self.collision_sprites])

		# Creates the players
		self.player = Player((418, 1000), self.all_sprites, self.collision_sprites, '../Graphics/ninja', self.shoot, self.projectile_sprites1, self.slash1, self.slash_sprites1)
		self.player2 = Player2((1500, 1000), self.all_sprites, self.collision_sprites, '../Graphics/robot', self.shoot2, self.projectile_sprites2, self.slash2, self.slash_sprites2) 

	def shoot(self, pos, direction, entity):
		# Creates kunai animation
		Projectile(
			pos = pos, 
			surf = self.kunai, 
			direction = direction, 
			groups = [self.all_sprites, self.projectile_sprites2])

	def shoot2(self, pos, direction, entity):
		# Creates fire animation
		Projectile(
			pos = pos, 
			surf = self.fire, 
			direction = direction, 
			groups = [self.all_sprites, self.projectile_sprites1])

	def slash1(self, pos, direction, entity):
		# Creates kunai animation
		Slash(
			pos = pos, 
			surf = self.ninja_slash, 
			direction = direction, 
			groups = [self.all_sprites, self.slash_sprites2])

	def slash2(self, pos, direction, entity):
		# Creates fire animation
		Slash(
			pos = pos, 
			surf = self.robot_slash, 
			direction = direction, 
			groups = [self.all_sprites, self.slash_sprites1])

	def run(self):

		while True: 

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
								
 
			dt = self.clock.tick() / 1000
			self.display_surface.fill((42,217,223))


			self.all_sprites.update(dt)

			
			
			
			self.all_sprites.custom_draw(self.player, self.player2)
			self.overlay.display()
			self.overlay2.display()
			self.ninjadamage.update()
			self.ninjadamage.display()
			self.robotdamage.update()
			self.robotdamage.display()
			
			pygame.display.update()


if __name__ == '__main__':
	main = Main()
	main.run()