import pygame
import random_maze

# Define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PINK = (255, 0, 255)
# Define window size
WIDTH = 500
HEIGHT = 500

class	map_class:
	def __init__(self):
		# Create a 2D map
		choice = int(input("1: Random map, 2: draw map: "))
		if (choice == 1):
			random_map = random_maze.random_map()
			random_map.logic_stuff(random_map)
			random_map.final_touches()
			self.map_width = random_map.width
			self.map_height = random_map.height
			self.map_data = random_map.maze
		else:
			self.map_width = int(input("Enter the width of the map: "))
			self.map_height = int(input("Enter the height of the map: "))
			if (self.map_width < 1 or self.map_height < 1):
				print("Map no good!")
				raise SystemExit
			# set all edges to  walls and all other tiles to floor
			self.map_data = [["1" if x == 0 or x == self.map_width - 1 or y == 0 or y == self.map_height - 1 else "0" for x in range(self.map_width)] for y in range(self.map_height)]
		self.tile_width = int(WIDTH / (self.map_width))
		self.tile_height = int(HEIGHT / (self.map_height))
		

	def mouse_click(self, mouse_pos):
		tile_x = mouse_pos[0] // self.tile_width
		tile_y = mouse_pos[1] // self.tile_height
		# Cycle through the different tile types
		if self.map_data[tile_y][tile_x] == "0":
			self.map_data[tile_y][tile_x] = "1"
		elif self.map_data[tile_y][tile_x] == "1":
			self.map_data[tile_y][tile_x] = "P"
		elif self.map_data[tile_y][tile_x] == "P":
			self.map_data[tile_y][tile_x] = "B"
		elif self.map_data[tile_y][tile_x] == "B":
			self.map_data[tile_y][tile_x] = "C"
		elif self.map_data[tile_y][tile_x] == "C":
			self.map_data[tile_y][tile_x] = "E"
		elif self.map_data[tile_y][tile_x] == "E":
			self.map_data[tile_y][tile_x] = "0"

	def mouse_drag(self, mouse_pos):
		tile_x = mouse_pos[0] // self.tile_width
		tile_y = mouse_pos[1] // self.tile_height
		if self.map_data[tile_y][tile_x] != "1":
			self.map_data[tile_y][tile_x] = "1"

	def export_map(self):
		with open("map.txt", "w") as f:
			for row in self.map_data:
				for tile in row:
					if tile == "0":
						f.write("0")
					elif tile == "1":
						f.write("1")
					elif tile == "P":
						f.write("P")
					elif tile == "B":
						f.write("B")
					elif tile == "C":
						f.write("C")
					elif tile == "E":
						f.write("E")
				f.write("\n")

class	pygame_stuff:
	def __init__(self, map):
		pygame.init()
		pygame.display.set_caption("Map Maker")
		# Text init
		pygame.font.init()
		self.my_font = pygame.font.SysFont('ARIAL', int(map.tile_width / 5))
		# Set the size of the screen
		screen_size = (WIDTH, HEIGHT)
		self.screen = pygame.display.set_mode(screen_size)

	def draw_tiles(self, map):
		# Draw the tiles
		for y in range(map.map_height):
			for x in range(map.map_width):
				text = self.my_font.render('', False, (0, 0, 0))
				rect = pygame.Rect(x * map.tile_width, y * map.tile_height, map.tile_width, map.tile_height)
				if map.map_data[y][x] == "0":
					pygame.draw.rect(self.screen, GREEN, rect)
				elif map.map_data[y][x] == "1":
					pygame.draw.rect(self.screen, BLACK, rect)
				elif map.map_data[y][x] == "P":
					pygame.draw.rect(self.screen, PINK, rect)
					text = self.my_font.render('Player', False, (0, 0, 0))
				elif map.map_data[y][x] == "B":
					pygame.draw.rect(self.screen, RED, rect)
					pygame.draw.circle(self.screen, BLACK, (x * map.tile_width + map.tile_width // 2, y * map.tile_height + map.tile_height // 2), map.tile_width // 4)
					text = self.my_font.render('Enemy', False, (0, 0, 0))
				elif map.map_data[y][x] == "C":
					pygame.draw.rect(self.screen, BLUE, rect)
					text = self.my_font.render('Collectable', False, (0, 0, 0))
				elif map.map_data[y][x] == "E":
					pygame.draw.rect(self.screen, CYAN, rect)
					text = self.my_font.render('Exit', False, (0, 0, 0))
				self.screen.blit(text, rect)

map = map_class()
game = pygame_stuff(map)

# Start the game loop
clock = pygame.time.Clock()
done = False

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# Get the tile clicked by the user
			mouse_pos = pygame.mouse.get_pos()
			map.mouse_click(mouse_pos)
		elif event.type == pygame.MOUSEMOTION:
			# Get the tile clicked by the user
			if pygame.mouse.get_pressed()[0]:
				mouse_pos = pygame.mouse.get_pos()
				map.mouse_drag(mouse_pos)

	# Clear the screen
	game.screen.fill(WHITE)
	game.draw_tiles(map)

	# Update the screen
	pygame.display.flip()
	clock.tick(60)

map.export_map()

pygame.quit