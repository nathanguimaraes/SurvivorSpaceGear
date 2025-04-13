import random
import math
import time  # Usado para controle do tempo no jogo

# Dimensões da tela e parâmetros do jogo
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 64
PLAYER_SPEED = 3
ENEMY_SPEED = 1.5
BULLET_SPEED_BASE = 4
INVINCIBILITY_TIME = 60  # Frames de invencibilidade após levar dano

# Estados do jogo
MENU = 0
PLAYING = 1
PAUSED = 2
game_state = MENU

# Controle de áudio
music_muted = False
music_volume = 0.5

# Controle de tempo
game_start_time = 0
record_time = 0  # Armazena o tempo recorde do jogador

# Classe das estrelas animadas do fundo do menu
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = random.randint(1, 3)
        self.speed = random.uniform(0.2, 1.0)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:  # Reposiciona no topo quando sai da tela
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, (255, 255, 255))

NUM_STARS = 50
stars = [Star() for _ in range(NUM_STARS)]  # Cria várias estrelas

# Classe base para personagens (jogador e inimigos)
class Character:
    def __init__(self, x, y, image, speed):
        self.actor = Actor(image, (x, y))
        self.target_x = x
        self.target_y = y
        self.speed = speed
        self.size = self.actor.width // 2

    def update(self):
        # Move gradualmente para o destino (target_x, target_y)
        dx = self.target_x - self.actor.x
        dy = self.target_y - self.actor.y
        distance = math.hypot(dx, dy)
        if distance > 2:
            dx /= distance
            dy /= distance
            self.actor.x += dx * self.speed
            self.actor.y += dy * self.speed
            angle = math.degrees(math.atan2(dy, -dx)) + 90
            self.actor.angle = angle  # Rotação visual

    def draw(self):
        self.actor.draw()

# Inimigos se movimentam aleatoriamente e atiram
class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 'enemy', ENEMY_SPEED)
        self.wander_timer = 0
        self.wander_radius = TILE_SIZE * 3
        self.shoot_timer = random.randint(30, 90)  # Tempo até atirar

    def update(self):
        super().update()
        # Movimentação aleatória ("wander")
        self.wander_timer -= 1
        if self.wander_timer <= 0:
            self.wander_timer = random.randint(60, 180)
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, self.wander_radius)
            margin = self.size
            self.target_x = min(max(self.actor.x + math.cos(angle) * distance, margin), WIDTH - margin)
            self.target_y = min(max(self.actor.y + math.sin(angle) * distance, margin), HEIGHT - margin)

        # Controle de disparo
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(60, 120)
            shoot_at_player(self)

# Jogador controlável
class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 'navemae', PLAYER_SPEED)
        self.health = 100
        self.invincible = 0  # Contador de invencibilidade

    def move_to(self, x, y):
        self.target_x = x
        self.target_y = y

    def update(self):
        super().update()
        if self.invincible > 0:
            self.invincible -= 1  # Diminui tempo de invencibilidade

    def draw(self):
        # Desenha efeito de movimento e piscar quando invencível
        dx = self.target_x - self.actor.x
        dy = self.target_y - self.actor.y
        distance = math.hypot(dx, dy)
        if distance > 2 and self.invincible % 10 < 5:
            angle_rad = math.radians(self.actor.angle + -90)
            offset_x = math.cos(angle_rad) * 35
            offset_y = -math.sin(angle_rad) * 35
            effect = Actor('effect_purple')
            effect.pos = (self.actor.x + offset_x, self.actor.y + offset_y)
            effect.angle = self.actor.angle
            effect.draw()
        if self.invincible % 10 < 5:
            self.actor.draw()

# Tiro inimigo
class Bullet:
    def __init__(self, x, y, dx, dy, speed):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.radius = 5

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, 'yellow')

    def collides_with(self, target):
        # Checa colisão com um personagem
        distance = math.hypot(self.x - target.actor.x, self.y - target.actor.y)
        return distance < target.size

# Inimigo atira mirando o jogador
def shoot_at_player(enemy):
    elapsed = time.time() - game_start_time
    bullet_speed = BULLET_SPEED_BASE + int(elapsed / 50)  # Aumenta a dificuldade com o tempo
    dx = player.actor.x - enemy.actor.x
    dy = player.actor.y - enemy.actor.y
    dist = math.hypot(dx, dy)
    if dist != 0:
        dx /= dist
        dy /= dist
    bullets.append(Bullet(enemy.actor.x, enemy.actor.y, dx, dy, bullet_speed))
    sounds.laser1.play()

# Desenha a tela
def draw():
    screen.clear()

    if game_state in (MENU, PAUSED):
        screen.fill((10, 10, 30))  # Fundo escuro
        for star in stars:
            star.draw()
        screen.draw.text("Survivor SpaceGear", center=(WIDTH // 2, HEIGHT // 4), fontsize=50)
        if game_state == MENU:
            screen.draw.text("Clique em qualquer lugar para iniciar o jogo", center=(WIDTH // 2, HEIGHT // 2), fontsize=30)
        else:
            screen.draw.text("Jogo Pausado - Pressione 'P' para continuar", center=(WIDTH // 2, HEIGHT // 2), fontsize=30)

        # Informações de música
        if music_muted:
            screen.draw.text("Musica: Mudo (M para ativar)", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=25)
        else:
            screen.draw.text(f"Musica: Volume {int(music_volume * 100)}% (M para mutar)", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=25)
            screen.draw.text("Use as setas do teclado para ajustar volume", center=(WIDTH // 2, HEIGHT // 2 + 80), fontsize=20)

    elif game_state == PLAYING:
        screen.fill((20, 20, 40))  # Fundo de jogo
        # Linhas do grid
        for x in range(0, WIDTH, TILE_SIZE):
            screen.draw.line((x, 0), (x, HEIGHT), (40, 40, 60))
        for y in range(0, HEIGHT, TILE_SIZE):
            screen.draw.line((0, y), (WIDTH, y), (40, 40, 60))

        for enemy in enemies:
            enemy.draw()
        for bullet in bullets:
            bullet.draw()
        player.draw()

        # HUD com informações
        elapsed = int(time.time() - game_start_time)
        screen.draw.text(f"Tempo: {elapsed}s", (WIDTH - 150, 10), fontsize=25)
        screen.draw.text(f"Recorde: {int(record_time)}s", (WIDTH - 150, 40), fontsize=25)
        screen.draw.text(f"Vida: {int(player.health)}", (10, 10), fontsize=30)

# Atualização do jogo
def update():
    global game_state, record_time

    for star in stars:
        star.update()

    if game_state != PLAYING:
        return

    player.update()
    for enemy in enemies:
        enemy.update()

    for bullet in bullets[:]:
        bullet.update()
        if bullet.collides_with(player):
            if player.invincible == 0:
                player.health -= 10
                player.invincible = INVINCIBILITY_TIME
                sounds.spacetrash1.play()
            bullets.remove(bullet)
        elif bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)

    # Colisão corpo a corpo com inimigos
    for enemy in enemies:
        dx = player.actor.x - enemy.actor.x
        dy = player.actor.y - enemy.actor.y
        distance = math.hypot(dx, dy)
        if distance < (player.size + enemy.size):
            if player.invincible == 0:
                player.health -= 0.5
                player.invincible = INVINCIBILITY_TIME

    if player.health <= 0:
        elapsed = time.time() - game_start_time
        if elapsed > record_time:
            record_time = elapsed
        reset_game()
        game_state = MENU

# Clique do mouse
def on_mouse_down(pos):
    global game_state, game_start_time
    if game_state == MENU:
        game_state = PLAYING
        reset_game()
        game_start_time = time.time()
        if not music_muted:
            music.play('topgearvegas')
            music.set_volume(music_volume)
    elif game_state == PLAYING:
        player.move_to(pos[0], pos[1])  # Move o jogador ao clicar

# Entrada de teclado
def on_key_down(key):
    global music_muted, music_volume, game_state

    if key == keys.P:
        if game_state == PLAYING:
            game_state = PAUSED
        elif game_state == PAUSED:
            game_state = PLAYING

    elif key == keys.M:
        music_muted = not music_muted
        if music_muted:
            music.set_volume(0)
        else:
            music.set_volume(music_volume)
            music.play('topgearvegas')

    elif key == keys.UP:
        if not music_muted and music_volume < 1.0:
            music_volume = min(1.0, music_volume + 0.1)
            music.set_volume(music_volume)

    elif key == keys.DOWN:
        if not music_muted and music_volume > 0.0:
            music_volume = max(0.0, music_volume - 0.1)
            music.set_volume(music_volume)

# Reinicia o jogo
def reset_game():
    global player, enemies, bullets
    player = Player(WIDTH // 2, HEIGHT // 2)
    enemies = [
        Enemy(WIDTH // 4, HEIGHT // 4),
        Enemy(WIDTH * 3 // 4, HEIGHT // 4),
        Enemy(WIDTH // 4, HEIGHT * 3 // 4),
        Enemy(WIDTH * 3 // 4, HEIGHT * 3 // 4)
    ]
    bullets = []
    if not music_muted:
        music.play('topgearvegas')
        music.set_volume(music_volume)

# Inicialização do jogo
player = Player(WIDTH // 2, HEIGHT // 2)
enemies = []
bullets = []
