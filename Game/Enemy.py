import pygame
import math
import random

# --- Globals ---
# Colors
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Set initial speed
speed = 10
x_change = speed
y_change = 0

class Enemy(pygame.sprite.Sprite):
	def	__init__(self, spriteslist, x, y, x_change, y_change):
		# Call the parent's constructor
		pygame.sprite.Sprite.__init__(self)
		
		self.spriteslist = spriteslist
		self.spriteslist.add(self)
		
		# Set height, width
		self.image = pygame.Surface([20, 20])
		pygame.draw.polygon(self.image, red, [(10,0),(0,20),(20,20)], 3)
		#self.image = pygame.image.load("triangle.png")
		#self.image = pygame.transform.scale(self.image, (25, 25))
		
		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
		self.x_change = x_change
		self.y_change = y_change
		
		angle = 0
		if y_change != 0:
			angle = math.degrees(math.atan(x_change / y_change))
		elif x_change < 0:
			angle = 90.0
		else:
			angle = 270.0
		if y_change > 0:
			angle += 180
		self.image = pygame.transform.rotate(self.image, angle)
	def destroy(self):
		self.spriteslist.remove(self)
	def update(self):
		pygame.sprite.Sprite.update(self)
		self.rect.x += self.x_change
		self.rect.y += self.y_change

if __name__ == "__main__":
	# Init
	pygame.init()
	screen = pygame.display.set_mode([800, 600])
	pygame.display.set_caption('Enemy test')
	allspriteslist = pygame.sprite.Group()

	# Variable
	enemys = []
	generate_duration = 2
	last = pygame.time.get_ticks()
	clock = pygame.time.Clock()
	done = False

	while not done:
		x_change = 0
		y_change = 0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
		
		now = pygame.time.get_ticks()
		if now - last >= generate_duration:
			last = now
			appear_x = random.randint(1,799)
			appear_y = random.randint(1,599)
			dir = random.choice(['up', 'down', 'left', 'right'])
			if dir == 'left':
				appear_x = 0
			if dir == 'right':
				appear_x = 800
			if dir == 'up':
				appear_y = 0
			if dir == 'down':
				appear_y = 600
			v = pygame.math.Vector2(400 - appear_x, 300 - appear_y)
			v = 10 * v.normalize()
			enemy = Enemy(allspriteslist, appear_x, appear_y, v.x, v.y)
			enemys.insert(0, enemy)

		# -- Draw everything
		# Clear screen
		screen.fill(black)

		allspriteslist.update()
		allspriteslist.draw(screen)
			  
		# Flip screen
		pygame.display.flip()
	  
		# Pause
		clock.tick(30)
				  
	pygame.quit()