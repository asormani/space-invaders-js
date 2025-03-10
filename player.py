import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        # Carrega a imagem do jogador, ou cria uma imagem básica se não encontrar
        try:
            self.image = pygame.image.load('graphics/player.png').convert_alpha()
        except FileNotFoundError:
            print("Erro ao carregar a imagem do jogador, criando uma imagem básica")
            self.image = pygame.Surface((60, 30))
            self.image.fill((0, 255, 0))  # Verde para o jogador
            
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600  # Tempo de espera para atirar novamente (em milissegundos)
        
        # Lasers
        self.lasers = pygame.sprite.Group()
        try:
            self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
            self.laser_sound.set_volume(0.5)
        except:
            print("Erro ao carregar o som do laser")
            self.laser_sound = pygame.mixer.Sound(buffer=bytes([]))
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal - suporte para setas e também J/K para compatibilidade
        if keys[pygame.K_RIGHT] or keys[pygame.K_k]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_j]:
            self.rect.x -= self.speed
            
        # Atirar com espaço ou W (para mais compatibilidade)
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()
            
    def recharge(self):
        # Controla o recarregamento do laser
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True
    
    def constraint(self):
        # Impede que o jogador saia da tela
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
            
    def shoot_laser(self):
        # Cria um novo laser
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))
    
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()