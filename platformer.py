import pygame
from pygame.locals import *
import sys
import random
import os.path
 
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
 
HEIGHT = 550
WIDTH = 550
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
 
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
		 
		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH
			 
		self.rect.midbottom = self.pos
		self.x = self.pos.x // 50
 
	def jump(self):
		hits = pygame.sprite.spritecollide(self, platforms, False)
		if hits:
			self.vel.y = -10
 
 
	def update(self):
		hits = pygame.sprite.spritecollide(self, platforms, False)
		if self.vel.y > 0:        
			if hits:
				self.vel.y = 0
				self.pos.y = hits[0].rect.top + 1
 
 
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
		self.rect = self.surf.get_rect(midbottom = (x * 50, y * 50))
 
	def move(self):
		pass

class Map:
	def __init__(self):
		self.lines = []
		self.collectable_count = 0

	def import_map(self, filename):
		if (os.path.isfile(filename) == False):
			print("not a real file")
			return
		with open(filename, 'r') as file:
			self.lines = file.readlines()
		line = str(self.lines[0])
		self.width = len(line)
		self.height = len(self.lines)
		self.w = int(WIDTH / (len(line) - 1))
		self.h = int(HEIGHT / len(self.lines))
		for y in range(0, self.height):
			for x in range(0, self.width - 1):
				if self.lines[y][x] == "1":
					wall = platform(x, y)
					platforms.add(wall)			
				if self.lines[y][x] == "P":
					self.player = Player(x, y)
					all_sprites.add(self.player)
		print(self.collectable_count)

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
 
	for sprite in all_sprites:
		if (abs(map.player.x - sprite.x) < 5):
			displaysurface.blit(sprite.surf, sprite.rect)
			sprite.move()
	# displaysurface.blit(map.player.image, (map.player.rect.x, map.player.rect.y))
 
	pygame.display.update()
	FramePerSec.tick(FPS)