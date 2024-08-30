import pygame, sys
from settings import *
from pygame.math import Vector2 as vector
from os import walk

class Player2(pygame.sprite.Sprite):

	def __init__(self, pos, groups, collision_sprites, path, shoot, projectile_sprites, slash, slash_sprites):

		super().__init__(groups)

		# graphics setup
		self.import_assets(path)
		self.frame_index = 0
		self.status = 'left_'

		# collisions setup
		self.collision_sprites = collision_sprites
		self.projectile_sprites = projectile_sprites
		self.slash_sprites = slash_sprites

		# image setup
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.mask = pygame.mask.from_surface(self.image)

		# float based movement
		self.direction = vector()
		self.pos = vector(self.rect.topleft)
		self.speed = 400

		# vertcal movement
		self.jump_speed = 1300
		self.gravity = 10
		self.on_floor = False # Players only attack while on floor

		# Attack timers
		self.melee = False # If set to False, player can not attack
		self.is_moving = False # If player is moving, player can not attack
		self.can_shoot = True
		self.shoot = shoot
		self.shoot_animate = False
		self.shoot_time = 0

		# slide
		self.slide = False
		self.slide_timer = 0
		self.can_slide = True

		# Damage
		self.damage = 0
		self.is_damage = False
		self.lives = 3

		#Attack
		self.slash = slash

	def import_assets(self, path):

		self.animations = {}

		for index,folder in enumerate(walk(path)):  # Imports assets needed for the entities
			
			if index == 0:
				for name in folder[1]:
					self.animations[name] = [] # Gets folder names for different status (e.g., folder for player attacking)

			else:
				for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])): # gets the contents inside the status folders

					path = folder[0].replace('\\', '/') + '/' + file_name
					surf = pygame.image.load(path).convert_alpha()

					# resize sprites so they fit the screen
					size = vector(surf.get_size()) * 0.2 
					surface = pygame.transform.scale(surf, size)

					key = folder[0].split('\\')[1]
					self.animations[key].append(surface)

	def get_status(self):

		# idle status
		if self.direction.x == 0 and self.on_floor and not self.melee and not self.slide and not self.shoot_animate and not self.is_damage:

			self.status = self.status.split('_')[0] + '_idle'
			self.is_moving = False

		# jump status
		if self.direction.y != 0 and not self.on_floor and not self.slide and not self.shoot_animate and not self.is_damage:

			self.status = self.status.split('_')[0] + '_jump'

		# slide status
		if self.slide and not self.is_damage:

			self.status = self.status.split('_')[0] + '_slide'

		if self.is_damage:

			self.status = self.status.split('_')[0] + '_hit'

	def check_contact(self):

		# Creates a bottom rect that checks if player is on the floor
		bottom_rect = pygame.Rect(0,0,self.rect.width, 2)
		bottom_rect.midtop = self.rect.midbottom

		#If player is in contact with platform, set on_floor to true
		for sprite in self.collision_sprites.sprites(): 
			if sprite.rect.colliderect(bottom_rect):
				if self.direction.y > 0:
					self.on_floor = True

	def animate(self, dt):

		if self.status == 'right_attack' or self.status == 'left_attack':

		 	self.frame_index += 20 * dt

		elif self.status == 'right_shoot' or self.status == 'left_shoot':

			self.frame_index += 15*dt

		elif self.status == 'right_hit' or self.status == 'left_hit':

			self.frame_index += 13*dt

		else:
			self.frame_index += 7*dt


		if self.shoot_animate or self.melee: #If attack animation, executes the frames only once

			if self.frame_index >= len(self.animations[self.status]): 

				self.melee = False
				self.status = self.status.split('_')[0] + '_idle'
				self.frame_index = 0
				self.direction.x = 0

		elif self.is_damage: #If attack animation, executes the frames only once

			if self.frame_index >= len(self.animations[self.status]): 

				
				self.is_damage = False
				self.status = self.status.split('_')[0] + '_idle'
				self.frame_index = 0
				self.direction.x = 0


		elif self.frame_index >= len(self.animations[self.status]): # Ensures the frame index doesnt exceed the amount of frames 
			self.frame_index = 0

		self.image = self.animations[self.status][int(self.frame_index)] #Update image and mask
		self.mask = pygame.mask.from_surface(self.image)

	def input(self):

		keys = pygame.key.get_pressed()

		# Horizontal Movement
		if 0 <= self.rect.centerx <= 1800 and not self.shoot_animate: 
			
			if keys[pygame.K_RIGHT]:
				
				self.direction.x = 1
				self.status = 'right_'

				# Parameters so player does not attack mid movement
				self.melee = False
				self.is_moving = True
				

			elif keys[pygame.K_LEFT]:
				
				self.direction.x = -1
				self.status = 'left_'

				# Parameters so player does not attack mid movement
				self.melee = False
				self.is_moving = True


			elif not self.slide and not self.is_damage:
				self.direction.x = 0

		else:
			if not self.is_damage: 
		 		self.direction.x = 0

		# Ensures player does not move too far off screen
		if self.rect.centerx <= -300:

			self.direction.x = 1

		if self.rect.centerx >= 2100:

			self.direction.x = -1


		if keys[pygame.K_DOWN] and self.can_slide:

				if self.status.split('_')[0] == 'right': 

					self.status = self.status.split('_')[0] + '_slide'
					self.slide = True
					self.direction.x = 2
					self.can_slide = False
					self.slide_timer = pygame.time.get_ticks()

				if self.status.split('_')[0] == 'left': 

					self.status = self.status.split('_')[0] + '_slide'
					self.slide = True
					self.direction.x = -2
					self.can_slide = False
					self.slide_timer = pygame.time.get_ticks()


		# Vertical Movement

		if keys[pygame.K_UP] and self.on_floor:
				
			self.direction.y = -self.jump_speed
			

		# Attack

		# Melee attacks only if player is on a platform and not moving
		if keys[pygame.K_PERIOD] and self.on_floor and not self.is_moving and not self.is_damage:

			self.frame_index = 0
			self.status = self.status.split('_')[0] + '_attack'
			self.melee = True

			# Gets direction for attack depending on where the player is facing
			direction = vector(1,0) if self.status.split('_')[0] == 'right' else vector(-1,0)

			# Gets position for where the slash will spawn
			pos = self.rect.center + direction * 70

			y_offset = vector(50, 0) if self.status.split("_")[0] == 'left' else vector(-50, 0)

			self.slash(pos + y_offset, direction, self)

		if keys[pygame.K_COMMA] and self.can_shoot and not self.slide and not self.melee and not self.is_damage:

			self.frame_index = 0
			self.status = self.status.split('_')[0] + '_shoot'
			self.shoot_animate = True
			# Gets direction for attack depending on where the player is facing
			direction = vector(1,0) if self.status.split('_')[0] == 'right' else vector(-1,0)

			# Gets position for where the bullet will spawn
			pos = self.rect.center + direction * 70

			# offset to make sure bullet aligns with player
			y_offset = vector(0, 10) 

			#Player shoots
			self.shoot(pos + y_offset, direction, self)

			self.can_shoot = False # Initiate cooldown
			self.shoot_time = pygame.time.get_ticks() # gets time player shoots
		
	def slide_duration(self):

		current_time = pygame.time.get_ticks()

		if current_time - self.slide_timer >= 500 and not self.can_slide:
			self.slide = False
	
	def slide_check(self):

		current_time = pygame.time.get_ticks()

		if current_time - self.slide_timer >= 2000 and not self.can_slide:
			self.can_slide = True
	
	def shoot_duration(self):

		current_time = pygame.time.get_ticks()

		if current_time - self.shoot_time >= 350 and not self.can_shoot:
			self.shoot_animate = False
			
	def shoot_timer(self):

		if not self.can_shoot: # timer which checks when the entity is allowed to shoot again after shooting
			current_time = pygame.time.get_ticks()
			if current_time - self.shoot_time > 750:
				self.can_shoot = True

	def collision(self, direction):

		for sprite in self.collision_sprites.sprites():

			if sprite.rect.colliderect(self.rect):
				
				if direction == 'horizontal':

				# left collision
					if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
						self.rect.left = sprite.rect.right


				# right collision
					if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
						self.rect.right = sprite.rect.left

					self.pos.x = self.rect.x

				else:

				# top collision	
					if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
						self.rect.top = sprite.rect.bottom


				# bottom collision
					if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
						self.rect.bottom = sprite.rect.top
						self.on_floor = True

					self.pos.y = self.rect.y
					self.direction.y = 0

		# Checks if player is on floor
		if self.on_floor and self.direction.y != 0:
			self.on_floor = False
	
	def ProjectileCollision(self):

		for items in self.collision_sprites.sprites():
			pygame.sprite.spritecollide(items, self.projectile_sprites, True, pygame.sprite.collide_mask) 


		for sprite in self.projectile_sprites.sprites():

			if sprite.rect.colliderect(self.rect) and not self.slide:

				x = sprite.rect.x
				sprite.kill()


				if self.rect.x >= x:
					self.status = 'left_hit'
					self.is_damage = True
					self.damage += 3
					self.direction.x = round(0.05 * self.damage)
					

				if self.rect.x <= x:
					self.status = 'right_hit'
					self.is_damage = True
					self.damage += 3
					self.direction.x = round(-0.05 * self.damage)

		for sprite in self.slash_sprites.sprites():

			if sprite.rect.colliderect(self.rect) and not self.slide:

				x = sprite.rect.x
				sprite.kill()


				if self.rect.x >= x:
					self.status = 'left_hit'
					self.is_damage = True
					self.damage += 4
					self.direction.x = 0.01 * self.damage
					

				if self.rect.x <= x:
					self.status = 'right_hit'
					self.is_damage = True
					self.damage += 4
					self.direction.x = -0.01 * self.damage				

	def move(self, dt):

		# Horizontal Movement
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)
		self.collision('horizontal')
		

		# Vertical Movement 
		self.direction.y += self.gravity
		self.pos.y += self.direction.y * dt

		self.rect.y = round(self.pos.y)
		self.collision('vertical')

	def check_death(self):

		# Respawns Player
		if self.rect.y > 2000:
			self.damage = 0
			self.lives -= 1
			self.status = 'left_'
			self.pos = vector(1300, 0)

			if self.lives <= 0:
				self.rect.centerx = 1000
				self.rect.centery = 1000
				self.kill()
	
	def update(self, dt):

		self.old_rect = self.rect.copy()
		self.input()
		self.get_status()

		self.ProjectileCollision()
		self.move(dt)
		
		self.slide_duration()
		self.slide_check()
		self.check_contact()
		self.shoot_timer()
		self.shoot_duration()
		self.check_death()
		self.animate(dt)
