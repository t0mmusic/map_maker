import pygame
from pygame.locals import *
import sys
import random
import os.path
import math
 
pygame.init()
vec = pygame.math.Vector2
 
HEIGHT = 550
WIDTH = 1000
TILESIZE = 50
ACC = 0.6
FRIC = -0.12
FPS = 60
GRAVITY = 0.6
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Base class for all moving sprites
class Entity(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.surf = pygame.Surface((TILESIZE, TILESIZE))
		self.surf.fill((255, 0, 0))
		self.rect = self.surf.get_rect(topleft = (x * TILESIZE, y * TILESIZE))
		self.pos = vec((x * TILESIZE, y * TILESIZE))
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)

	def move(self):
		self.rect.topleft = self.pos
		if self.rect.right < -TILESIZE:
			self.kill()

class Finish(Entity):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.surf.fill((255, 0, 255))

class Platform(Entity):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.surf.fill((255, 0, 0))

	def player_hit(self):
		self.kill()

class Player(Entity):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.surf.fill((0,0,255))
		self.pos.y += TILESIZE
 
	def move(self):
		self.acc = vec(0, GRAVITY)
	
		pressed_keys = pygame.key.get_pressed()
				
		if pressed_keys[K_LEFT]:
			self.acc.x = -ACC
		if pressed_keys[K_RIGHT]:
			self.acc.x = ACC
		if pressed_keys[K_SPACE]:
			self.jump()
				 
		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
		 
		if self.pos.x > WIDTH - (TILESIZE / 2): # wrap around left to right
			self.pos.x = WIDTH - (TILESIZE / 2)
		if self.pos.x < TILESIZE / 2:
			self.pos.x = TILESIZE // 2
		if self.pos.y > HEIGHT + TILESIZE:
			self.kill()
			print("DEAD")
			raise SystemExit
			 
		self.rect.midbottom = self.pos
		self.x = self.pos.x // TILESIZE
		self.update()
 
	def jump(self):
		hits = pygame.sprite.spritecollide(self, platforms, False)
		if hits:
			self.vel.y = -15

	def enemy_collision(self):
		hits = pygame.sprite.spritecollide(self, enemies, False)
		for hit in hits:
			top_diff = abs(hit.rect.bottom - self.rect.top)
			bottom_diff = abs(hit.rect.top - self.rect.bottom)
			right_diff = abs(hit.rect.left - self.rect.right)
			left_diff = abs(hit.rect.right - self.rect.left)
			if (top_diff > bottom_diff and top_diff > right_diff and top_diff > left_diff):
				hit.player_hit()
				break
			else:
				self.kill()
				print("DEAD")
				raise SystemExit

	def platform_collision(self):
		hits = pygame.sprite.spritecollide(self, platforms, False)
		for hit in hits: # these should factor current velocity somehow
			top_diff = abs(hit.rect.bottom - self.rect.top)
			bottom_diff = abs(hit.rect.top - self.rect.bottom)
			right_diff = abs(hit.rect.left - self.rect.right)
			left_diff = abs(hit.rect.right - self.rect.left)
			# player has collided with ceiling
			if (bottom_diff > right_diff and bottom_diff > left_diff and bottom_diff > top_diff):
				self.rect.top = hit.rect.bottom
				self.pos.y = self.rect.midbottom[1]
				self.vel.y = 0
				hit.player_hit() # this behaviour should depend on the type of platform
				break
			# player has collided with left wall
			if (right_diff > bottom_diff and right_diff > left_diff and right_diff > top_diff and top_diff < 90):
				self.rect.left = hit.rect.right
				self.pos.x = self.rect.midbottom[0] - self.vel.x
				self.vel.x = 0
				break
			# player has collided with right wall
			if (left_diff > bottom_diff and left_diff > right_diff and left_diff > top_diff):
				self.rect.right = hit.rect.left
				self.pos.x = self.rect.midbottom[0] - self.vel.x
				self.vel.x = 0
				break							
			# player has landed on platform
			if (top_diff > bottom_diff and top_diff > right_diff and top_diff > left_diff):
				if self.vel.y > 0:        
					self.vel.y = 0
					self.pos.y = hit.rect.top + 1
				break

	def update(self):		
		self.platform_collision()
		self.enemy_collision()

# Base enemy (Goomba)
class Enemy(Entity):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.surf.fill((0, 255, 0))
		# self.pos.y += TILESIZE / 2
		self.vel = vec(-1.5, 0)

	def move(self):
		self.acc = vec(0, GRAVITY)
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
		self.rect.midbottom = self.pos
		hits = pygame.sprite.spritecollide(self, platforms, False)
		for hit in hits:
			top_diff = abs(hit.rect.bottom - self.rect.top)
			bottom_diff = abs(hit.rect.top - self.rect.bottom)
			right_diff = abs(hit.rect.left - self.rect.right)
			left_diff = abs(hit.rect.right - self.rect.left)
			if (right_diff > bottom_diff and right_diff > left_diff and right_diff > top_diff):
				self.vel.x = -self.vel.x
				self.pos.x = hit.rect.right + ((TILESIZE / 2) + 2)
				self.pos.y = hit.rect.bottom + 1
				self.rect.midbottom = self.pos
				break
			if (left_diff > bottom_diff and left_diff > right_diff and left_diff > top_diff):
				self.vel.x = -self.vel.x
				self.pos.x = hit.rect.left - ((TILESIZE / 2) + 2)
				self.pos.y = hit.rect.bottom + 1
				self.rect.midbottom = self.pos
				break
			if self.vel.y > 0:        
				self.vel.y = 0
				self.pos.y = hit.rect.top + 1
		if self.rect.right < -TILESIZE:
			self.kill()

	def player_hit(self):
		self.kill()

class Map:
	def __init__(self):
		self.lines = []
		self.collectable_count = 0

	def import_map(self, filename):
		if (os.path.isfile(filename) == False):
			print("not a real file")
			raise SystemExit
		with open(filename, 'r') as file:
			self.lines = file.readlines()
		line = str(self.lines[0])
		self.width = len(line)
		self.height = len(self.lines)
		self.end = False
		self.w = int(WIDTH / (len(line) - 1))
		self.h = int(HEIGHT / len(self.lines))
		for y in range(0, self.height):
			for x in range(0, self.width - 1):
				if self.lines[y][x] == "1":
					wall = Platform(x, y)
					platforms.add(wall)
				if self.lines[y][x] == "E":
					enemy = Enemy(x, y)
					enemies.add(enemy)
				if self.lines[y][x] == "F":
					self.finish = Finish(x, y)
					all_sprites.add(self.finish)
				if self.lines[y][x] == "P":
					self.player = Player(x, y)
					all_sprites.add(self.player)

	def update(self):
		if pygame.Rect.colliderect(self.player.rect, self.finish.rect):
			print("YOUR WINNAR")
			raise SystemExit
		# checks if player is in middle of screen or end of the map
		if (self.end == False and self.player.x > (WIDTH // TILESIZE) / 2):
			dist = 0
			for sprite in all_sprites:
				# checks to see if the last tile has entered the screen
				if (sprite.x == self.width - 2 and sprite.rect.right < WIDTH):
					dist = WIDTH - sprite.rect.right
					self.end = True
					break
				# once the player reaches the center of the screen, it will stop moving right
				# and everything else will start moving left instead
				if (self.player.vel.x > 0):	
					sprite.pos.x -= self.player.vel.x
			if (self.end == True):
				for sprite in all_sprites:
					sprite.rect.right += dist

platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
map = Map()
map.import_map('platforms.txt')

all_sprites.add(platforms)
all_sprites.add(enemies)
 
while True: 
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()
		 
	displaysurface.fill((0,0,0))
	map.update()
 
	for sprite in all_sprites:
		if (sprite.rect.right > 0 and sprite.rect.left < WIDTH):
			displaysurface.blit(sprite.surf, sprite.rect)
		sprite.move()
 
	pygame.display.update()
	FramePerSec.tick(FPS)