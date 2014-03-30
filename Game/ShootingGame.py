""" 
Test simple STG.
Created by shawnsion.
 
"""
  
import pygame
import math
import random
import Actor
import Enemy

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Set the width and height of each snake segment
segment_width = 5
segment_height = 5
# Margin between each segment
segment_margin = 3

# Set initial speed
x_change = segment_width + segment_height
y_change = 0

# Call this function so the Pygame library can initialize itself
pygame.init()
  
# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])
  
# Set the title of the window
pygame.display.set_caption('Shooting Game')
#pygame.display.set_icon(pygame.image.load('triangle.png').convert_alpha())

allspriteslist = pygame.sprite.Group()

actor = Actor.Actor(allspriteslist,400, 300)
enemys = []

clock = pygame.time.Clock()
done = False
down = False
fire = False
last = pygame.time.get_ticks()
generate_duration = 2000

font = pygame.font.Font(None, 36)
font.set_bold(True)
fps = font.render("0.0", 1, white)
fpspos = fps.get_rect()
fpspos.bottomright = [775, 600]

score = 0
scoreboard = font.render(str(score).zfill(8), 1, white)
scoreboardpos = scoreboard.get_rect()
scoreboardpos.x = 0
scoreboardpos.y = 0

bombicon = pygame.Surface([30, 30])
pygame.draw.circle(bombicon, red, [15, 15], 15)
bombiconpos = bombicon.get_rect()
bombiconpos.bottomleft = [0, 600]
bombicontext = font.render("B", 1, black)
bombicontextpos = bombicontext.get_rect()
bombicontextpos.center = [15, 15]
bombicon.blit(bombicontext, bombicontextpos)

bomb = 3
bombboard = font.render(str(" X ") + str(bomb).zfill(2), 1, white)
bombboardpos = bombboard.get_rect()
bombboardpos.bottomleft = [30, 600]

while not done:
	x_change = 0
	y_change = 0
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		x_change += (segment_width + segment_margin) *- 1
	if keys[pygame.K_RIGHT]:
		x_change += (segment_width + segment_margin)
	if keys[pygame.K_UP]:
		y_change += (segment_height + segment_margin) *- 1
	if keys[pygame.K_DOWN]:
		y_change += (segment_height + segment_margin)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				fire = True
			if event.key == pygame.K_z:
				if bomb > 0:
					bomb -= 1
					for enemy in enemys:
						score += 1000
						enemys.remove(enemy)
						enemy.destroy()
		
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				fire = False
	now = pygame.time.get_ticks()
	if now - last >= generate_duration:
		last = now
		generate_duration = generate_duration * 0.9
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
		enemy = Enemy.Enemy(allspriteslist, appear_x, appear_y, v.x, v.y)
		enemys.insert(0, enemy)
		allspriteslist.add(enemy)
	# Figure out where new segment will be
	x = actor.rect.x + x_change
	y = actor.rect.y + y_change
	actor.moveTo(x, y)
	actor.fireEnable(fire)
	actor.update()
	for enemy in enemys:
		enemy.update()
		x = enemy.rect.x
		y = enemy.rect.y
		if pygame.Rect.colliderect(actor.critical_point, enemy.rect):
			print('Game Over')
			done = True
		if x > 800 or x < 0 or y > 600 or y < 0:
			enemys.remove(enemy)
			enemy.destroy()
		for bullet in actor.bullets:
			if pygame.Rect.colliderect(enemy.rect, bullet.rect):
				if enemys.__contains__(enemy):
					score += 1000
					enemys.remove(enemy)
					enemy.destroy()
					
	
	# -- Draw everything
	# Clear screen
	screen.fill(black)
	
	allspriteslist.update()
	allspriteslist.draw(screen)
	
	fps = font.render(str(round(clock.get_fps(), 1)), 1, white)
	screen.blit(fps, fpspos)
	
	score += 1 + len(enemys) * 10
	scoreboard = font.render(str(score).zfill(8), 1, white)
	screen.blit(scoreboard, scoreboardpos)
	
	screen.blit(bombicon, bombiconpos)
	bombboard = font.render(str(" X ") + str(bomb).zfill(2), 1, white)
	screen.blit(bombboard, bombboardpos)
	# Flip screen
	pygame.display.flip()
	  
	# Pause
	clock.tick(30)
				  
pygame.quit()