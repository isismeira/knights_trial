import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self, screen_width, screen_height):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		player_walk_3 = pygame.image.load('graphics/player/player_walk_3.png').convert_alpha()
		player_walk_4 = pygame.image.load('graphics/player/player_walk_4.png').convert_alpha()
		player_walk_5 = pygame.image.load('graphics/player/player_walk_5.png').convert_alpha()
		player_walk_6 = pygame.image.load('graphics/player/player_walk_6.png').convert_alpha()
		player_walk_7 = pygame.image.load('graphics/player/player_walk_7.png').convert_alpha()
		player_walk_8 = pygame.image.load('graphics/player/player_walk_8.png').convert_alpha()
		player_walk_9 = pygame.image.load('graphics/player/player_walk_9.png').convert_alpha()
		player_walk_10 = pygame.image.load('graphics/player/player_walk_10.png').convert_alpha()
		
		# Escalar sprites do player proporcionalmente
		scale_factor = screen_height / 400  # Fator baseado na altura original de 400px
		self.player_walk = []
		for frame in [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, 
		             player_walk_6, player_walk_7, player_walk_8, player_walk_9, player_walk_10]:
			scaled_frame = pygame.transform.scale(frame, 
				(int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
			self.player_walk.append(scaled_frame)
		
		self.player_index = 0
		jump_img = pygame.image.load('graphics/player/jump.png').convert_alpha()
		self.player_jump = pygame.transform.scale(jump_img,
			(int(jump_img.get_width() * scale_factor), int(jump_img.get_height() * scale_factor)))

		self.image = self.player_walk[self.player_index]
		ground_y = int(screen_height * 0.75)  # Chão a 75% da altura da tela
		self.rect = self.image.get_rect(midbottom = (int(screen_width * 0.1), ground_y))
		self.gravity = 0
		self.ground_y = ground_y
		self.screen_width = screen_width
		self.screen_height = screen_height

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= self.ground_y:
			self.gravity = int(-20 * (self.screen_height / 400))  # Escalar força do pulo
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += int(1 * (self.screen_height / 400))  # Escalar gravidade
		self.rect.y += self.gravity
		if self.rect.bottom >= self.ground_y:
			self.rect.bottom = self.ground_y

	def animation_state(self):
		if self.rect.bottom < self.ground_y: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type, screen_width, screen_height):
		super().__init__()
		
		scale_factor = screen_height / 400
		ground_y = int(screen_height * 0.75)
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			# Escalar sprites da mosca
			fly_1_scaled = pygame.transform.scale(fly_1,
				(int(fly_1.get_width() * scale_factor), int(fly_1.get_height() * scale_factor)))
			fly_2_scaled = pygame.transform.scale(fly_2,
				(int(fly_2.get_width() * scale_factor), int(fly_2.get_height() * scale_factor)))
			self.frames = [fly_1_scaled, fly_2_scaled]
			y_pos = int(screen_height * 0.525)  # Proporção equivalente a 210/400
		else:
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			# Escalar sprites do caracol
			snail_1_scaled = pygame.transform.scale(snail_1,
				(int(snail_1.get_width() * scale_factor), int(snail_1.get_height() * scale_factor)))
			snail_2_scaled = pygame.transform.scale(snail_2,
				(int(snail_2.get_width() * scale_factor), int(snail_2.get_height() * scale_factor)))
			self.frames = [snail_1_scaled, snail_2_scaled]
			y_pos = ground_y

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		spawn_x = randint(int(screen_width * 1.125), int(screen_width * 1.375))  # Proporção de 900-1100/800
		self.rect = self.image.get_rect(midbottom = (spawn_x, y_pos))
		self.speed = int(6 * (screen_width / 800))  # Escalar velocidade

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= self.speed
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

def display_score(screen, test_font, start_time, screen_width, screen_height):
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(255,255,255))
	score_rect = score_surf.get_rect(center = (screen_width//2, int(screen_height * 0.125)))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite(player, obstacle_group):
	if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
		obstacle_group.empty()
		return False
	else: return True

pygame.init()

# Detectar resolução da tela
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Criar tela em modo fullscreen com escala
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption('Knight\'s Trial')
clock = pygame.time.Clock()

# Escalar fonte proporcionalmente
font_size = int(50 * (SCREEN_HEIGHT / 400))
test_font = pygame.font.Font('font/Pixeltype.ttf', font_size)

game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player(SCREEN_WIDTH, SCREEN_HEIGHT))

obstacle_group = pygame.sprite.Group()

# Carregar e ajustar imagens de fundo para dimensões específicas
original_sky = pygame.image.load('graphics/Sky.jpeg').convert()
original_ground = pygame.image.load('graphics/ground.jpeg').convert()

# Calcular a proporção da tela
screen_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
sky_ratio = original_sky.get_width() / original_sky.get_height()

# Escalar o céu mantendo a proporção e cobrindo toda a tela
if screen_ratio > sky_ratio:
    # Tela mais larga que a imagem
    new_width = SCREEN_WIDTH
    new_height = int(SCREEN_WIDTH / sky_ratio)
else:
    # Tela mais alta que a imagem
    new_height = SCREEN_HEIGHT
    new_width = int(SCREEN_HEIGHT * sky_ratio)

sky_surface = pygame.transform.scale(original_sky, (new_width, new_height))

# Escalar o chão para cobrir toda a largura da tela
ground_height = int(SCREEN_HEIGHT * 0.25)
ground_surface = pygame.transform.scale(original_ground, (SCREEN_WIDTH, ground_height))

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
stand_scale = (SCREEN_HEIGHT / 400) * 2  # Manter proporção do zoom original
player_stand = pygame.transform.scale(player_stand, 
	(int(player_stand.get_width() * stand_scale), int(player_stand.get_height() * stand_scale)))
player_stand_rect = player_stand.get_rect(center = (SCREEN_WIDTH//2, int(SCREEN_HEIGHT * 0.5)))

game_name = test_font.render('Knight\'s Trial',False,(0,0,0))
game_name_rect = game_name.get_rect(center = (SCREEN_WIDTH//2, int(SCREEN_HEIGHT * 0.2)))

game_message = test_font.render('Press space to run',False,(0,0,0))
game_message_rect = game_message.get_rect(center = (SCREEN_WIDTH//2, int(SCREEN_HEIGHT * 0.825)))

# Timer - ajustar baseado na velocidade proporcional
obstacle_timer = pygame.USEREVENT + 1
timer_interval = int(1500 * (800 / SCREEN_WIDTH))  # Ajustar frequência baseado na largura
pygame.time.set_timer(obstacle_timer, timer_interval)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		# Adicionar ESC para sair do fullscreen
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail']), SCREEN_WIDTH, SCREEN_HEIGHT))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)

	if game_active:
		# Desenhar céu cobrindo toda a tela
		sky_x = (SCREEN_WIDTH - new_width) // 2
		sky_y = (SCREEN_HEIGHT - new_height) // 2
		screen.blit(sky_surface, (sky_x, sky_y))
		
		# Desenhar chão na parte inferior
		ground_y = int(SCREEN_HEIGHT * 0.75)
		screen.blit(ground_surface, (0, ground_y))
		
		score = display_score(screen, test_font, start_time, SCREEN_WIDTH, SCREEN_HEIGHT)
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite(player, obstacle_group)
		
	else:
		screen.fill((25,62,43))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,(0,0,0))
		score_message_rect = score_message.get_rect(center = (SCREEN_WIDTH//2, int(SCREEN_HEIGHT * 0.825)))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)