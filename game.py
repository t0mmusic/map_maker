import pygame
import os.path

# Define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

pygame.init()

class map_class:
	def __init__(self):
		self.lines = []

	def import_map(self, filename):
		if (os.path.isfile(filename) == False):
			print("not a real file")
		with open('map.txt', 'r') as file:
			self.lines = file.readlines()

	def write_map(self):
		for line in self.lines:
			print(line, end="")

	def draw_map(self):
		line = str(self.lines[0])
		self.w = WIDTH / (len(line) - 1)
		self.h = HEIGHT / len(self.lines)
		surf = pygame.Surface((self.w, self.h))
		h = 0
		for y in self.lines:
			w = 0
			for x in range(0, len(y)):
				if (y[x] == '1'):
					surf.fill(RED)
				elif (y[x] == 'P'):
					surf.fill((255, 0, 255))
				elif (y[x] == 'E'):
					surf.fill(CYAN)
				elif (y[x] == 'C'):
					surf.fill(BLUE)
				else:
					surf.fill(GREEN)
				rect = surf.get_rect()
				screen.blit(surf, (w * self.w, h * self.h))
				w += 1
			h += 1


WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

map = map_class()
map.import_map('map.txt')
map.write_map()

while True:
	# Process player inputs.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			raise SystemExit

	# Do logical updates here.
	# ...

	# screen.fill("purple")  # Fill the display with a solid color

	# Render the graphics here.
	# ...

	map.draw_map()
	pygame.display.flip()  # Refresh on-screen display
	clock.tick(60)         # wait until next frame (at 60 FPS)