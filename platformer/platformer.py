import pygame
from pygame.locals import *
import sys
import random
import os.path
import math
 
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
 
HEIGHT = 550
WIDTH = 550
TILESIZE = 50
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

flag = True

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.x = x
		self.y = y
		# self.image = pygame.image.load("character.png")
		self.surf = pygame.Surface((50, 50))
		self.surf.fill((0,0,255))
		self.rect = self.surf.get_rect()
   
		self.pos = vec((x * 50, y * 50))
		self.vel = vec(0,0)
		self.acc = vec(0,0)
 
	def move(self):
		self.acc = vec(0,0.5)
	
		pressed_keys = pygame.key.get_pressed()
				
		if pressed_keys[K_LEFT]:
			self.acc.x = -ACC
		if pressed_keys[K_RIGHT]:
			self.acc.x = ACC
				 
		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
		 
		if self.pos.x > WIDTH: # wrap around left to right
			self.pos.x = 0
		if self.pos.x < TILESIZE / 2: # prevent player from going left of the screen
			self.pos.x = TILESIZE // 2
			 
		self.rect.midbottom = self.pos
		self.x = self.pos.x // TILESIZE
 
	def jump(self):
		hits = pygame.sprite.spritecollide(self, platforms, False)
		if hits:
			self.vel.y = -10
 
 
	def update(self):		
		hits = pygame.sprite.spritecollide(self, platforms, False)
		for hit in hits:
			top_diff = abs(hit.rect.bottom - self.rect.top)
			bottom_diff = abs(hit.rect.top - self.rect.bottom)
			right_diff = abs(hit.rect.left - self.rect.right)
			left_diff = abs(hit.rect.right - self.rect.left)
			# player has collided with ceiling
			if (bottom_diff > right_diff and bottom_diff > left_diff and bottom_diff > top_diff):
				print("bottom")
				self.rect.top = hit.rect.bottom
				self.pos[1] = self.rect.midbottom[1]
				self.vel.y = -self.vel.y
				self.acc.y = -self.acc.y
				break
			# player has collided with left wall
			if (right_diff > bottom_diff and right_diff > left_diff and right_diff > top_diff):
				print("right")
				self.rect.left = hit.rect.right
				self.pos[0] = self.rect.midbottom[0]
				self.vel.x = -self.vel.x
				self.acc.x = -self.acc.x
				break
			# player has collided with right wall
			if (left_diff > bottom_diff and left_diff > right_diff and left_diff > top_diff):
				print("left")
				self.rect.right = hit.rect.left
				self.pos[0] = self.rect.midbottom[0]
				self.vel.x = -self.vel.x
				self.acc.x = -self.acc.x
				break							
			# player has landed on platform
			if (top_diff > bottom_diff and top_diff > right_diff and top_diff > left_diff):
				if self.vel.y > 0:        
					self.vel.y = 0
					self.pos.y = hit.rect.top + 1
				break
 
 
class platform(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf = pygame.Surface((WIDTH, 20))
		self.surf.fill((255,0,0))
		self.rect = self.surf.get_rect(midbottom = (WIDTH/2, HEIGHT - 10))

	def __init__(self, x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.surf = pygame.Surface((50, 50))
		self.surf.fill((255, 0, 0))
		self.rect = self.surf.get_rect(topleft = (x * 50, y * 50))
 
	def move(self):
		if self.rect.right < -TILESIZE:
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
		self.w = int(WIDTH / (len(line) - 1))
		self.h = int(HEIGHT / len(self.lines))
		print(self.width, self.w)
		for y in range(0, self.height):
			for x in range(0, self.width - 1):
				if self.lines[y][x] == "1":
					wall = platform(x, y)
					platforms.add(wall)			
				if self.lines[y][x] == "P":
					self.player = Player(x, y)
					self.player_pos = self.player.x
					all_sprites.add(self.player)

	def update(self):
		global flag
		dist = 0
		if (self.player.x > 6 and flag):
			for sprite in platforms:
				if (sprite.x == self.width - 2 and sprite.rect.right < WIDTH):
					dist = WIDTH - sprite.rect.right
					flag = False
				if (self.player.vel[0] > 0):	
					sprite.rect.right -= self.player.vel[0]
			self.player.pos[0] -= self.player.vel[0]
		if (dist):
			for sprite in all_sprites:
				sprite.rect.right += dist

platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
map = Map()
map.import_map('platforms.txt')

all_sprites.add(platforms)
 
while True: 
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:    
			if event.key == pygame.K_SPACE:
				map.player.jump()
		 
	displaysurface.fill((0,0,0))
	map.player.update()
	map.update()
 
	for sprite in all_sprites:
		# if (abs(map.player.x - sprite.x) < 5):
		displaysurface.blit(sprite.surf, sprite.rect)
		sprite.move()
	# displaysurface.blit(map.player.image, (map.player.rect.x, map.player.rect.y))
 
	pygame.display.update()
	FramePerSec.tick(FPS)