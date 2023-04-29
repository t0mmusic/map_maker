# Maze generator -- Randomized Prim Algorithm

## Imports
import random
import time

# Init variables
# wall = '1'
# cell = '0'
# unvisited = 'u'
# height = random.randint(5, 20)
# width = random.randint(5, 20)
# maze = []

class random_map:
	def __init__(self):
		self.wall = '1'
		self.cell = '0'
		self.unvisited = 'u'
		self.height = random.randint(25, 50)
		self.width = random.randint(25, 50)
		self.maze = []

## Functions
	def printMaze(self, maze):
		for i in range(0, self.height):
			for j in range(0, self.width):
					print(str(maze[i][j]), end="")
			print('')

	# Find number of surrounding cells
	def surroundingCells(self, r1, r2):
		s_cells = 0
		if (self.maze[r1-1][r2] == '0'):
			s_cells += 1
		if (self.maze[r1+1][r2] == '0'):
			s_cells += 1
		if (self.maze[r1][r2-1] == '0'):
			s_cells +=1
		if (self.maze[r1][r2+1] == '0'):
			s_cells += 1

		return s_cells

	def logic_stuff(self, this):
		# Denote all cells as unvisited
		for i in range(0, self.height):
			line = []
			for j in range(0, self.width):
				line.append(self.unvisited)
			self.maze.append(line)

		# Randomize starting point and set it a cell
		starting_height = int(random.random()*self.height)
		starting_width = int(random.random()*self.width)
		if (starting_height == 0):
			starting_height += 1
		if (starting_height == self.height-1):
			starting_height -= 1
		if (starting_width == 0):
			starting_width += 1
		if (starting_width == self.width-1):
			starting_width -= 1

		# Mark it as cell and add surrounding walls to the list
		self.maze[starting_height][starting_width] = self.cell
		walls = []
		walls.append([starting_height - 1, starting_width])
		walls.append([starting_height, starting_width - 1])
		walls.append([starting_height, starting_width + 1])
		walls.append([starting_height + 1, starting_width])

		# Denote walls in maze
		self.maze[starting_height-1][starting_width] = '1'
		self.maze[starting_height][starting_width - 1] = '1'
		self.maze[starting_height][starting_width + 1] = '1'
		self.maze[starting_height + 1][starting_width] = '1'

	
		while (walls):
			# Pick a random wall
			rand_wall = walls[int(random.random()*len(walls))-1]

			# Check if it is a left wall
			if (rand_wall[1] != 0):
				if (self.maze[rand_wall[0]][rand_wall[1]-1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]+1] == '0'):
					# Find the number of surrounding cells
					s_cells = this.surroundingCells(rand_wall[0], rand_wall[1])

					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_wall[0]][rand_wall[1]] = '0'

						# Mark the new walls
						# Upper cell
						if (rand_wall[0] != 0):
							if (self.maze[rand_wall[0]-1][rand_wall[1]] != '0'):
								self.maze[rand_wall[0]-1][rand_wall[1]] = '1'
							if ([rand_wall[0]-1, rand_wall[1]] not in walls):
								walls.append([rand_wall[0]-1, rand_wall[1]])


						# Bottom cell
						if (rand_wall[0] != self.height-1):
							if (self.maze[rand_wall[0]+1][rand_wall[1]] != '0'):
								self.maze[rand_wall[0]+1][rand_wall[1]] = '1'
							if ([rand_wall[0]+1, rand_wall[1]] not in walls):
								walls.append([rand_wall[0]+1, rand_wall[1]])

						# Leftmost cell
						if (rand_wall[1] != 0):	
							if (self.maze[rand_wall[0]][rand_wall[1]-1] != '0'):
								self.maze[rand_wall[0]][rand_wall[1]-1] = '1'
							if ([rand_wall[0], rand_wall[1]-1] not in walls):
								walls.append([rand_wall[0], rand_wall[1]-1])
					

					# Delete wall
					for wall in walls:
						if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
							walls.remove(wall)

					continue

			# Check if it is an upper wall
			if (rand_wall[0] != 0):
				if (self.maze[rand_wall[0]-1][rand_wall[1]] == 'u' and self.maze[rand_wall[0]+1][rand_wall[1]] == '0'):

					s_cells = this.surroundingCells(rand_wall[0], rand_wall[1])
					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_wall[0]][rand_wall[1]] = '0'

						# Mark the new walls
						# Upper cell
						if (rand_wall[0] != 0):
							if (self.maze[rand_wall[0]-1][rand_wall[1]] != '0'):
								self.maze[rand_wall[0]-1][rand_wall[1]] = '1'
							if ([rand_wall[0]-1, rand_wall[1]] not in walls):
								walls.append([rand_wall[0]-1, rand_wall[1]])

						# Leftmost cell
						if (rand_wall[1] != 0):
							if (self.maze[rand_wall[0]][rand_wall[1]-1] != '0'):
								self.maze[rand_wall[0]][rand_wall[1]-1] = '1'
							if ([rand_wall[0], rand_wall[1]-1] not in walls):
								walls.append([rand_wall[0], rand_wall[1]-1])

						# Rightmost cell
						if (rand_wall[1] != self.width-1):
							if (self.maze[rand_wall[0]][rand_wall[1]+1] != '0'):
								self.maze[rand_wall[0]][rand_wall[1]+1] = '1'
							if ([rand_wall[0], rand_wall[1]+1] not in walls):
								walls.append([rand_wall[0], rand_wall[1]+1])

					# Delete wall
					for wall in walls:
						if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
							walls.remove(wall)

					continue

			# Check the bottom wall
			if (rand_wall[0] != self.height-1):
				if (self.maze[rand_wall[0]+1][rand_wall[1]] == 'u' and self.maze[rand_wall[0]-1][rand_wall[1]] == '0'):

					s_cells = this.surroundingCells(rand_wall[0], rand_wall[1])
					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_wall[0]][rand_wall[1]] = '0'

						# Mark the new walls
						if (rand_wall[0] != self.height-1):
							if (self.maze[rand_wall[0]+1][rand_wall[1]] != '0'):
								self.maze[rand_wall[0]+1][rand_wall[1]] = '1'
							if ([rand_wall[0]+1, rand_wall[1]] not in walls):
								walls.append([rand_wall[0]+1, rand_wall[1]])
						if (rand_wall[1] != 0):
							if (self.maze[rand_wall[0]][rand_wall[1]-1] != '0'):
								self.maze[rand_wall[0]][rand_wall[1]-1] = '1'
							if ([rand_wall[0], rand_wall[1]-1] not in walls):
								walls.append([rand_wall[0], rand_wall[1]-1])
						if (rand_wall[1] != self.width-1):
							if (self.maze[rand_wall[0]][rand_wall[1]+1] != '0'):
								self.maze[rand_wall[0]][rand_wall[1]+1] = '1'
							if ([rand_wall[0], rand_wall[1]+1] not in walls):
								walls.append([rand_wall[0], rand_wall[1]+1])

					# Delete wall
					for wall in walls:
						if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
							walls.remove(wall)
					continue

			# Check the right wall
			if (rand_wall[1] != self.width - 1):
				if (self.maze[rand_wall[0]][rand_wall[1]+1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]-1] == '0'):

					s_cells = this.surroundingCells(rand_wall[0], rand_wall[1])
					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_wall[0]][rand_wall[1]] = '0'

						# Mark the new walls
						if (rand_wall[1] != self.width-1):
							if (self.maze[rand_wall[0]][rand_wall[1]+1] != '0'):
								self.maze[rand_wall[0]][rand_wall[1]+1] = '1'
							if ([rand_wall[0], rand_wall[1]+1] not in walls):
								walls.append([rand_wall[0], rand_wall[1]+1])
						if (rand_wall[0] != self.height-1):
							if (self.maze[rand_wall[0]+1][rand_wall[1]] != '0'):
								self.maze[rand_wall[0]+1][rand_wall[1]] = '1'
							if ([rand_wall[0]+1, rand_wall[1]] not in walls):
								walls.append([rand_wall[0]+1, rand_wall[1]])
						if (rand_wall[0] != 0):	
							if (self.maze[rand_wall[0]-1][rand_wall[1]] != '0'):
								self.maze[rand_wall[0]-1][rand_wall[1]] = '1'
							if ([rand_wall[0]-1, rand_wall[1]] not in walls):
								walls.append([rand_wall[0]-1, rand_wall[1]])

					# Delete wall
					for wall in walls:
						if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
							walls.remove(wall)
					continue

			# Delete the wall from the list anyway
			for wall in walls:
				if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
					walls.remove(wall)
			
		# Mark the remaining unvisited cells as walls
		for i in range(0, self.height):
			for j in range(0, self.width):
				if (self.maze[i][j] == 'u'):
					self.maze[i][j] = '1'

	def place_object(self, obj, count):
		while count > 0:
			x = random.randint(0, self.width - 1)
			y = random.randint(0, self.height - 1)

			if (self.maze[y][x] == "0"):
				self.maze[y][x] = obj
				count -= 1

	def final_touches(self):
		self.place_object("P", 1)
		self.place_object("E", 1)
		self.place_object("C", random.randint(1, 10))

		with open("map.txt", "w") as f:
			for row in self.maze:
				# print(row)
				for tile in row:
					# print(tile)
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
