import pygame
import math

# --- Globals ---
# Colors
black = (0, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Set initial speed
speed = 10

x_change = speed
y_change = 0

class Bullet(pygame.sprite.Sprite):
	def __init__(self, spriteslist, x, y, x_change, y_change):
		pygame.sprite.Sprite.__init__(self)
		
		self.spriteslist = spriteslist
		self.spriteslist.add(self)
		
		self.image = pygame.Surface([6, 6])
		pygame.draw.circle(self.image, white, [3, 3], 3)
		
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.x_change = x_change
		self.y_change = y_change
		self.create_time = pygame.time.get_ticks()
	def destroy(self):
		self.spriteslist.remove(self)
	def update(self):
		pygame.sprite.Sprite.update(self)
		self.rect.x += self.x_change
		self.rect.y += self.y_change

class Actor(pygame.sprite.Sprite):
	""" Class to represent actor. """
	# -- Methods
	# Constructor function
	def __init__(self, spriteslist, x, y):
		# Call the parent's constructor
		pygame.sprite.Sprite.__init__(self)
		
		self.spriteslist = spriteslist
		self.spriteslist.add(self)
		
		# Set height, width
		self.image = pygame.Surface([50, 50])
		pygame.draw.polygon(self.image, blue, [(25, 0), (0, 50), (50,50)])
		
		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
		# Custom initialize
		self.origin_image = self.image
		self.angle = 0.0
		self.last = pygame.time.get_ticks()
		self.cooldown = 200
		self.bullets = []
		self.face_x = 0
		self.face_y = -8
		self.critical_point = pygame.Rect(self.rect.centerx - 15, self.rect.centery - 15, 30, 30)

	def moveTo(self, x, y):
		dx = x - self.rect.x
		dy = y - self.rect.y
		tmp_angle = 0
		if dy != 0:
			tmp_angle = math.degrees(math.atan(dx / dy))
		elif dx < 0:
			tmp_angle = 90.0
		elif dx > 0:
			tmp_angle = 270.0
		else:
			tmp_angle = self.angle
		if dy > 0:
			tmp_angle += 180
		angle = tmp_angle
		self.rect.x = x
		self.rect.y = y
		self.critical_point = pygame.Rect(self.rect.centerx - 15, self.rect.centery - 15, 30, 30)
		dangle = math.fabs((self.angle - angle) % 360)
		if dangle > 10:
			if dangle >= 180:
				self.angle = (self.angle + 10) % 360
			else:
				self.angle = (self.angle - 10) % 360
		else:
			self.angle = angle
		self.image = pygame.transform.rotate(self.origin_image, self.angle)
		if dangle > 0:
			self.face_x = speed * math.sin(math.radians(self.angle) - math.pi)
			self.face_y = speed * math.cos(math.radians(self.angle) - math.pi)
	def fireEnable(self, fire):
		now = pygame.time.get_ticks()
		if fire and now - self.last >= self.cooldown:
			self.last = now
			bullet = Bullet(self.spriteslist, self.rect.centerx - self.face_y, self.rect.centery + self.face_x, self.face_x * 4, self.face_y * 4)
			self.bullets.insert(0, bullet)
			bullet = Bullet(self.spriteslist, self.rect.centerx + self.face_y, self.rect.centery - self.face_x, self.face_x * 4, self.face_y * 4)
			self.bullets.insert(0, bullet)	

	def update(self):
		now = pygame.time.get_ticks()
		pygame.sprite.Sprite.update(self)
		for bullet in self.bullets:
			if now - bullet.create_time >= 2000:
				self.bullets.remove(bullet)
				bullet.destroy()

if __name__ == "__main__":
	# Init
	pygame.init()
	screen = pygame.display.set_mode([800, 600])
	pygame.display.set_caption('Actor test')
	allspriteslist = pygame.sprite.Group()

	#Variable
	actor = Actor(allspriteslist,400, 300)
	clock = pygame.time.Clock()	
	done = False
	down = False
	fire = False

	while not done:
		x_change = 0
		y_change = 0
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			x_change += speed *- 1
		if keys[pygame.K_RIGHT]:
			x_change += speed
		if keys[pygame.K_UP]:
			y_change += speed *- 1
		if keys[pygame.K_DOWN]:
			y_change += speed
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					fire = True
		
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					fire = False
				
		# Figure out where new segment will be
		x = actor.rect.x + x_change
		y = actor.rect.y + y_change
		actor.moveTo(x, y)
		actor.fireEnable(fire)
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