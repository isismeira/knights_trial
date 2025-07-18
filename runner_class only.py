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
		
		scale_factor = screen_height / 400  
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

# Dicionário de sprites por fase
OBSTACLE_SPRITES = {
    'phase1': {
        'fly': ['graphics/fly/fly1.png', 'graphics/fly/fly2.png'],
        'snail': ['graphics/snail/snail1.png', 'graphics/snail/snail2.png']
    },
    'phase2': {
        'fly': ['graphics/fly/Fly3.png', 'graphics/fly/Fly4.png'],
        'snail': ['graphics/snail/snail3.png', 'graphics/snail/snail4.png']
    },
    'phase3': {
        'fly': ['graphics/fly/Fly5.png', 'graphics/fly/Fly6.png'],
        'snail': ['graphics/snail/snail5.png', 'graphics/snail/snail6.png']
    }
}

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, screen_width, screen_height, phase):
        super().__init__()
        scale_factor = screen_height / 400
        ground_y = int(screen_height * 0.75)
        # Selecionar sprites conforme a fase
        sprites = OBSTACLE_SPRITES[phase][type]
        img1 = pygame.image.load(sprites[0]).convert_alpha()
        img2 = pygame.image.load(sprites[1]).convert_alpha()
        img1_scaled = pygame.transform.scale(img1, (int(img1.get_width() * scale_factor), int(img1.get_height() * scale_factor)))
        img2_scaled = pygame.transform.scale(img2, (int(img2.get_width() * scale_factor), int(img2.get_height() * scale_factor)))
        self.frames = [img1_scaled, img2_scaled]
        y_pos = int(screen_height * 0.525) if type == 'fly' else ground_y
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        spawn_x = randint(int(screen_width * 1.125), int(screen_width * 1.375))
        self.rect = self.image.get_rect(midbottom = (spawn_x, y_pos))
        self.speed = int(6 * (screen_width / 800))
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

# Controle de fases e cutscenes
# Possíveis valores: 'menu', 'cutscene1', 'phase1', 'cutscene2', 'phase2', 'cutscene3', 'phase3', 'cutscene4', 'game_over'
game_stage = 'menu'
# Para controlar o tempo de cada fase/cutscene
game_stage_start_time = 0
# Para controlar o tempo do próximo spawn de obstáculo após cada fase
next_obstacle_time = 0
# Para controlar o tempo de exibição do game over
game_over_time = 0

# Carregar imagens das cutscenes
def load_cutscene(path):
    img = pygame.image.load(path).convert()
    return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

cutscene1_img = load_cutscene('graphics/cutscene_1.jpeg')
cutscene2_img = load_cutscene('graphics/cutscene_2.jpeg')
cutscene3_img = load_cutscene('graphics/cutscene_3.jpeg')
cutscene4_img = load_cutscene('graphics/cutscene_4.jpeg')

game_over_img = load_cutscene('graphics/game_over.jpeg')

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player(SCREEN_WIDTH, SCREEN_HEIGHT))

obstacle_group = pygame.sprite.Group()

# Carregar e ajustar imagens de fundo para dimensões específicas
original_sky = pygame.image.load('graphics/florestabg.png').convert()
original_ground = pygame.image.load('graphics/ground_1.jpeg').convert()
original_menubg = pygame.image.load('graphics/menubgsky.png').convert()

# Carregar backgrounds e chãos específicos para cada fase
sky_2 = pygame.image.load('graphics/sky_2.png').convert()
sky_3 = pygame.image.load('graphics/sky_3.png').convert()
ground_2 = pygame.image.load('graphics/ground_2.jpeg').convert()
ground_3 = pygame.image.load('graphics/ground_3.jpeg').convert()

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
menubg_surface = pygame.transform.scale(original_menubg, (new_width, new_height))

# Escalar os backgrounds e chãos específicos para cada fase
sky_2_surface = pygame.transform.scale(sky_2, (new_width, new_height))
sky_3_surface = pygame.transform.scale(sky_3, (new_width, new_height))

# Escalar o chão para cobrir toda a largura da tela
ground_height = int(SCREEN_HEIGHT * 0.25)
ground_surface = pygame.transform.scale(original_ground, (SCREEN_WIDTH, ground_height))
ground_2_surface = pygame.transform.scale(ground_2, (SCREEN_WIDTH, ground_height))
ground_3_surface = pygame.transform.scale(ground_3, (SCREEN_WIDTH, ground_height))

# Intro screen
logo = pygame.image.load('graphics/logo.png').convert_alpha()
logo_rect = logo.get_rect(center = (SCREEN_WIDTH//2, int(SCREEN_HEIGHT * 0.5)))

game_message = test_font.render('Press space to run',False,(0,0,0))
game_message_rect = game_message.get_rect(center = (SCREEN_WIDTH//2, int(SCREEN_HEIGHT * 0.825)))

# Timer - ajustar baseado na velocidade proporcional
# Facilitar: aumentar o intervalo base para 3000 ms
EASY_TIMER_BASE = 3000
obstacle_timer = pygame.USEREVENT + 1
timer_interval = int(EASY_TIMER_BASE * (800 / SCREEN_WIDTH))
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

		if game_stage == 'phase1' or game_stage == 'phase2' or game_stage == 'phase3':
			if event.type == obstacle_timer:
				# Só permitir spawn de obstáculos após o delay inicial da fase
				if pygame.time.get_ticks() >= next_obstacle_time:
					# Passar a fase correta para o obstáculo
					obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail']), SCREEN_WIDTH, SCREEN_HEIGHT, game_stage))
		elif game_stage == 'menu':
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_stage = 'cutscene1'
				game_stage_start_time = pygame.time.get_ticks()
				# Remover a definição do start_time aqui
				# Resetar score e grupos
				obstacle_group.empty()
				player.sprite.rect.bottom = player.sprite.ground_y
				player.sprite.gravity = 0
				score = 0
		elif game_stage == 'game_over':
			# Permitir que o jogador pressione espaço para voltar ao menu imediatamente
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_stage = 'menu'
				game_stage_start_time = pygame.time.get_ticks()

	# Controle de fases/cutscenes
	now = pygame.time.get_ticks()
	if game_stage == 'cutscene1':
		screen.blit(cutscene1_img, (0, 0))
		if now - game_stage_start_time >= 5000:
			game_stage = 'phase1'
			game_stage_start_time = now
			start_time = pygame.time.get_ticks() // 1000  # Definir start_time quando a fase 1 começa
			obstacle_group.empty()  # Limpar obstáculos
			next_obstacle_time = now + 2000  # 2 segundos de delay
	elif game_stage == 'cutscene1' and now - game_stage_start_time == 1:
		# Garante que o timer seja atualizado ao entrar na fase
		pygame.time.set_timer(obstacle_timer, timer_interval)
	elif game_stage == 'phase1':
		# Gameplay normal (primeira fase)
		sky_x = (SCREEN_WIDTH - new_width) // 2
		sky_y = (SCREEN_HEIGHT - new_height) // 2
		screen.blit(sky_surface, (sky_x, sky_y))
		ground_y = int(SCREEN_HEIGHT * 0.75)
		screen.blit(ground_surface, (0, ground_y))
		score = display_score(screen, test_font, start_time, SCREEN_WIDTH, SCREEN_HEIGHT)
		player.draw(screen)
		player.update()
		obstacle_group.draw(screen)
		obstacle_group.update()
		if not collision_sprite(player, obstacle_group):
			game_stage = 'game_over'
			game_over_time = now
		elif now - game_stage_start_time >= 30000:
			game_stage = 'cutscene2'
			game_stage_start_time = now
	elif game_stage == 'cutscene2':
		screen.blit(cutscene2_img, (0, 0))
		if now - game_stage_start_time >= 5000:
			game_stage = 'phase2'
			game_stage_start_time = now
			obstacle_group.empty()  # Limpar obstáculos
			next_obstacle_time = now + 2000  # 2 segundos de delay
	elif game_stage == 'cutscene2' and now - game_stage_start_time == 1:
		pygame.time.set_timer(obstacle_timer, timer_interval)
	elif game_stage == 'phase2':
		# Gameplay segunda fase
		sky_x = (SCREEN_WIDTH - new_width) // 2
		sky_y = (SCREEN_HEIGHT - new_height) // 2
		screen.blit(sky_2_surface, (sky_x, sky_y))
		ground_y = int(SCREEN_HEIGHT * 0.75)
		screen.blit(ground_2_surface, (0, ground_y))
		score = display_score(screen, test_font, start_time, SCREEN_WIDTH, SCREEN_HEIGHT)
		player.draw(screen)
		player.update()
		obstacle_group.draw(screen)
		obstacle_group.update()
		if not collision_sprite(player, obstacle_group):
			game_stage = 'game_over'
			game_over_time = now
		elif now - game_stage_start_time >= 30000:
			game_stage = 'cutscene3'
			game_stage_start_time = now
	elif game_stage == 'cutscene3':
		screen.blit(cutscene3_img, (0, 0))
		if now - game_stage_start_time >= 5000:
			game_stage = 'phase3'
			game_stage_start_time = now
			obstacle_group.empty()  # Limpar obstáculos
			next_obstacle_time = now + 2000  # 2 segundos de delay
	elif game_stage == 'cutscene3' and now - game_stage_start_time == 1:
		pygame.time.set_timer(obstacle_timer, timer_interval)
	elif game_stage == 'phase3':
		# Gameplay terceira fase
		sky_x = (SCREEN_WIDTH - new_width) // 2
		sky_y = (SCREEN_HEIGHT - new_height) // 2
		screen.blit(sky_3_surface, (sky_x, sky_y))
		ground_y = int(SCREEN_HEIGHT * 0.75)
		screen.blit(ground_3_surface, (0, ground_y))
		score = display_score(screen, test_font, start_time, SCREEN_WIDTH, SCREEN_HEIGHT)
		player.draw(screen)
		player.update()
		obstacle_group.draw(screen)
		obstacle_group.update()
		if not collision_sprite(player, obstacle_group):
			game_stage = 'game_over'
			game_over_time = now
		elif now - game_stage_start_time >= 30000:
			game_stage = 'cutscene4'
			game_stage_start_time = now
	elif game_stage == 'cutscene4':
		screen.blit(cutscene4_img, (0, 0))
		if now - game_stage_start_time >= 5000:
			game_stage = 'menu'
			game_stage_start_time = now
	elif game_stage == 'game_over':
		screen.blit(game_over_img, (0, 0))
		# Removida a mensagem de texto na tela de game over
		# O retorno ao menu agora ocorre apenas ao pressionar espaço
	else:
		# Menu
		sky_x = (SCREEN_WIDTH - new_width) // 2
		sky_y = (SCREEN_HEIGHT - new_height) // 2
		screen.blit(menubg_surface, (sky_x, sky_y))
		screen.blit(logo,logo_rect)
		score_message = test_font.render(f'Your score: {score}',False,(0,0,0))
		score_message_rect = score_message.get_rect(center = (SCREEN_WIDTH//2, int(SCREEN_HEIGHT * 0.825)))
		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)