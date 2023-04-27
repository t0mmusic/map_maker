import pygame
import os.path

from pygame.locals import (
	RLEACCEL,
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	KEYDOWN,
	QUIT,
)

# Define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PINK = (255, 0, 255)

ACC = 0.5
FRIC = -0.12

pygame.init()
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
	def __init__(self, map):
		x = map.w / 2
		y = map.h / 2
		super(Player, self).__init__()
		self.surf = pygame.Surface((x, y))
		self.surf.fill(PINK)
		self.rect = pygame.Rect(map.player_position[0] + x / 2, map.player_position[1] + y / 2, x, y)
		self.pos = vec((map.player_position[0] + x, map.player_position[1] + y))
		self.vel = vec(0,0)
		self.acc = vec(0,0)

	def collision_check(self, map):
		hits = pygame.sprite.spritecollide(self, walls, False)
		for hit in hits:
			top = self.rect.top - hit.rect.bottom
			bottom = self.rect.bottom - hit.rect.top
			left = self.rect.left - hit.rect.right
			right = self.rect.right - hit.rect.left

			if top < 0 and bottom > 0:
				print("top, bottom", top - bottom)
				self.vel.y = -self.vel.y
				self.acc.y = -self.acc.y
			if left < 0 and right > 0:
				print("left, right", left - right)
				self.vel.x = -self.vel.x
				self.acc.x = -self.acc.x
			self.pos += self.vel + 0.5 * self.acc
			self.rect.midbottom = self.pos
		c = pygame.sprite.spritecollideany(self, collectables)
		if c:
			c.kill()
			map.collectable_count -= 1
			print(map.collectable_count)
		if map.collectable_count == 0 and pygame.sprite.spritecollideany(self, exits):
			print("YOUR WINNAR")
			running = False

	def update(self, pressed_keys, map):
		self.acc = vec(0,0)
		if pressed_keys[K_UP]:
			self.acc.y = -ACC
		if pressed_keys[K_DOWN]:
			self.acc.y = ACC
		if pressed_keys[K_LEFT]:
			self.acc.x = -ACC
		if pressed_keys[K_RIGHT]:
			self.acc.x = ACC
		self.acc.x += self.vel.x * FRIC
		self.acc.y += self.vel.y * FRIC
		self.vel.x += self.acc.x
		self.vel.y += self.acc.y
		self.pos += self.vel + 0.5 * self.acc
		self.rect.midbottom = self.pos
		self.collision_check(map)
		# Prevent player from exiting screen
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= HEIGHT:
			self.rect.bottom = HEIGHT

	def check_exit(self, event):
		if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			return False
		return True

class Wall(pygame.sprite.Sprite):
	def __init__(self, map, x, y):
		super(Wall, self).__init__()
		self.surf = pygame.Surface((map.w, map.h))
		self.surf.fill(BLACK)
		self.rect = pygame.Rect(x * map.w, y * map.h, map.w, map.h)

class Collectable(pygame.sprite.Sprite):
	def __init__(self, map, x, y):
		super(Collectable, self).__init__()
		self.surf = pygame.Surface((map.w, map.h))
		self.surf.fill(BLUE)
		self.rect = pygame.Rect(x * map.w, y * map.h, map.w, map.h)

	def remove(self, map):
		if self.rect.right - player.rect.right < 5:
			self.kill()

class Exit(pygame.sprite.Sprite):
	def __init__(self, map, x, y):
		super(Exit, self).__init__()
		self.surf = pygame.Surface((map.w, map.h))
		self.surf.fill(CYAN)
		self.rect = pygame.Rect(x * map.w, y * map.h, map.w, map.h)

class map_class:
	def __init__(self):
		self.lines = []
		self.collectable_count = 0

	def import_map(self, filename):
		if (os.path.isfile(filename) == False):
			print("not a real file")
			return
		with open('map.txt', 'r') as file:
			self.lines = file.readlines()
		line = str(self.lines[0])
		self.width = len(line)
		self.height = len(self.lines)
		self.w = int(WIDTH / (len(line) - 1))
		self.h = int(HEIGHT / len(self.lines))
		for y in range(0, self.height):
			for x in range(0, self.width):
				if self.lines[y][x] == "1":
					wall = Wall(self, x, y)
					walls.add(wall)
				if self.lines[y][x] == "C":
					collectable = Collectable(self, x, y)
					collectables.add(collectable)
					self.collectable_count += 1
				if self.lines[y][x] == "E":
					exit = Exit(self, x, y)
					exits.add(exit)					
				if self.lines[y][x] == "P":
					self.player_position = (x * self.w, y * self.h, self.w, self.h)
		print(self.collectable_count)

	def write_map(self):
		for line in self.lines:
			print(line, end="")

WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

map = map_class()
map.write_map()

walls = pygame.sprite.Group()
collectables = pygame.sprite.Group()
exits = pygame.sprite.Group()
map.import_map('map.txt')
player = Player(map)

all_sprites = pygame.sprite.Group()
all_sprites.add(walls)
all_sprites.add(collectables)
all_sprites.add(exits)
all_sprites.add(player)

running = True

while running:
	# Process player inputs.
	for event in pygame.event.get():
		running = player.check_exit(event)

	# Do logical updates here.
	# ...
	pressed_keys = pygame.key.get_pressed()
	player.update(pressed_keys, map)

	# Render the graphics here.
	# ...
	screen.fill(GREEN)
	for sprite in all_sprites:
		screen.blit(sprite.surf, sprite.rect)
	pygame.display.flip()  # Refresh on-screen display
	clock.tick(60)         # wait until next frame (at 60 FPS)

pygame.quit()