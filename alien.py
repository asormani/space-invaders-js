import pygame
import random
from laser import Laser

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        # Define a imagem com base no tipo de alien
        file_path = 'graphics/' + color + '.png'
        try:
            self.image = pygame.image.load(file_path).convert_alpha()
        except:
            print(f"Erro ao carregar a imagem {file_path}, criando uma imagem básica")
            self.image = pygame.Surface((40, 40))
            # Define cores diferentes baseado no tipo de alien
            if color == 'red':
                self.image.fill((255, 0, 0))  # Vermelho
            elif color == 'green':
                self.image.fill((0, 255, 0))  # Verde
            else:
                self.image.fill((255, 255, 0))  # Amarelo

        self.rect = self.image.get_rect(topleft = (x, y))

        # Define o valor de pontos do alien com base em sua cor
        if color == 'red':
            self.value = 100
        elif color == 'green':
            self.value = 200
        else:
            self.value = 300

    def update(self, direction):
        # Move o alien horizontalmente
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        try:
            self.image = pygame.image.load('graphics/extra.png').convert_alpha()
        except Exception as e:
            print(f"Erro ao carregar imagem da nave extra: {e}")
            # Create a fallback red rectangle
            self.image = pygame.Surface((40, 20), pygame.SRCALPHA)
            self.image.fill((255, 0, 0))

        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x, 80))
        print(f"Nave extra criada na posição ({x}, 80) com velocidade {self.speed}")

    def update(self):
        self.rect.x += self.speed

        # Check if the extra ship has gone off screen in the opposite direction
        if (self.speed < 0 and self.rect.right < 0) or (self.speed > 0 and self.rect.left > 700):
            print(f"Nave extra removida na posição {self.rect.x}")
            self.kill()

class GrupoAliens:
    def __init__(self, imagens_aliens=None, nivel=1, rows=5, cols=9):
        self.aliens = pygame.sprite.Group()
        self.direction = 1
        self.move_down = False
        self.rows = rows
        self.cols = cols
        self.imagens_aliens = imagens_aliens
        self.nivel = nivel
        self.setup_aliens()

        # Som do laser dos aliens
        try:
            self.laser_sound = pygame.mixer.Sound('audio/alien_laser.wav')
            self.laser_sound.set_volume(0.3)

            # Sons de destruição dos aliens
            self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
            self.explosion_sound.set_volume(0.3)
        except:
            print("Erro ao carregar sons dos aliens")
            # Cria um som vazio como fallback
            self.laser_sound = pygame.mixer.Sound(buffer=bytes([]))
            self.explosion_sound = pygame.mixer.Sound(buffer=bytes([]))

        # Lasers dos aliens
        self.lasers = pygame.sprite.Group()

        # Extra alien
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = random.randint(800, 1200)
        self.last_extra_spawn = pygame.time.get_ticks()

    def setup_aliens(self):
        # Configura a grade de aliens
        # Ajusta dificuldade com base no nível
        velocidade_base = 1 + (self.nivel * 0.2)

        # Configura a grade de aliens com base nos parâmetros fornecidos
        if isinstance(self.rows, int):
            # Se rows for int, usa range para criar o número correto de linhas
            rows_to_process = range(self.rows)
        else:
            # Se não, usa a lista diretamente
            rows_to_process = self.rows

        for row_index, row in enumerate(rows_to_process):
            # Se cols for int, usa range, caso contrário usa a lista diretamente
            cols_to_process = range(self.cols) if isinstance(self.cols, int) else self.cols

            for col_index, col in enumerate(cols_to_process):
                x = col_index * 60 + 70
                y = row_index * 48 + 50

                if row_index == 0:
                    alien_color = 'yellow'
                elif row_index <= 2:
                    alien_color = 'green'
                else:
                    alien_color = 'red'

                # Se temos imagens fornecidas, usa-as em vez de carregar por cor
                if self.imagens_aliens:
                    alien = Alien(alien_color, x, y)
                else:
                    alien = Alien(alien_color, x, y)

                self.aliens.add(alien)

    def check_edges(self):
        # Verifica se algum alien atingiu as bordas da tela
        for alien in self.aliens.sprites():
            if alien.rect.right >= 800 or alien.rect.left <= 0:
                self.direction *= -1
                self.move_down = True
                return

    def move_aliens_down(self):
        # Move todos os aliens para baixo
        if self.move_down:
            for alien in self.aliens.sprites():
                alien.rect.y += 4
            self.move_down = False

    def alien_shoot(self):
        # Faz um alien aleatório atirar
        if self.aliens.sprites():
            random_alien = random.choice(self.aliens.sprites())
            laser = Laser(random_alien.rect.center, 6, 600)
            self.lasers.add(laser)
            self.laser_sound.play()

    def check_alien_position(self):
        # Verifica se algum alien chegou na parte inferior da tela
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= 560:
                return True
        return False

    def create_extra_alien(self):
        # Cria um alien extra (bonus) ocasionalmente
        current_time = pygame.time.get_ticks()
        if current_time - self.last_extra_spawn >= self.extra_spawn_time:
            side = random.choice(['right', 'left'])
            self.extra.add(Extra(side, 800))
            self.last_extra_spawn = current_time
            self.extra_spawn_time = random.randint(800, 1200)

    def update(self):
        # Atualiza todos os aliens e seus projéteis
        self.check_edges()
        self.move_aliens_down()
        self.aliens.update(self.direction)
        self.lasers.update()
        self.extra.update()
        self.create_extra_alien()

        # Remove os lasers que saíram da tela
        for laser in self.lasers.copy():
            if laser.rect.top >= 600:
                laser.kill()