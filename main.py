#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Space Invaders Clone
Um clone do clássico jogo Space Invaders utilizando Pygame
"""

import pygame
import sys
import gif_pygame
from player import Player
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
import obstacle

class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((screen_width/2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
        # Tenta carregar a imagem de explosão, se falhar, cria uma imagem estática
        try:
            self.explosion_player = gif_pygame.load('graphics/explosion.gif')
        except:
            print("Erro ao carregar a imagem de explosão")
            self.explosion_player = gif_pygame.StaticImage('graphics/player.png')
        
        self.point = 0

        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('graphics/player.png').convert_alpha()
        self.live_surf = pygame.transform.scale(self.live_surf, (20, 10))
        self.live_x_star_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        
        # Tenta carregar a fonte, se falhar, usa a fonte padrão
        try:
            self.font = pygame.font.Font('font/Pixeled.ttf', 20)
            self.font2 = pygame.font.Font('font/Pixeled.ttf', 10)
        except:
            print("Erro ao carregar as fontes, usando fontes padrão")
            self.font = pygame.font.SysFont('Arial', 20)
            self.font2 = pygame.font.SysFont('Arial', 10)

        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4 #numero de obstaculos
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=screen_width / 15, y_start = 480)

        # alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1
        self.line = 340

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)  # Increased for better gameplay

        # Audio - usando a classe Sons para gerenciar os sons
        from assets.sons import Sons
        self.sons = Sons()
        self.sons.musica_jogo()
        
        # Referências para compatibilidade com o código existente
        empty_buffer = bytes([0] * 44)
        self.laser_sound = pygame.mixer.Sound(buffer=empty_buffer)
        self.explosion_sound = pygame.mixer.Sound(buffer=empty_buffer)
        self.extra_sound = pygame.mixer.Sound(buffer=empty_buffer)
        self.player_sound = pygame.mixer.Sound(buffer=empty_buffer)
        self.extra_explosion_sound = pygame.mixer.Sound(buffer=empty_buffer)
        
        # Substitui os sons vazios pelos sons carregados, se existirem
        if 'tiro_jogador' in self.sons.sons:
            self.laser_sound = self.sons.sons['tiro_jogador']
            self.laser_sound.set_volume(0.5)
        if 'explosao_alien' in self.sons.sons:
            self.explosion_sound = self.sons.sons['explosao_alien']
            self.explosion_sound.set_volume(0.3)
        if 'nave_extra' in self.sons.sons:
            self.extra_sound = self.sons.sons['nave_extra']
            self.extra_sound.set_volume(0.3)
        if 'explosao_jogador' in self.sons.sons:
            self.player_sound = self.sons.sons['explosao_jogador']
            self.player_sound.set_volume(0.3)
        if 'nave_extra_explosao' in self.sons.sons:
            self.extra_explosion_sound = self.sons.sons['nave_extra_explosao']
            self.extra_explosion_sound.set_volume(0.4)
        
        print("Sistema de sons inicializado")

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    alien_sprite = Alien('yellow',x,y)
                elif 1 <= row_index <=2:
                    alien_sprite = Alien('green',x,y)
                else:
                    alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
                self.line += 2
            elif alien.rect.left < 0:
                self.alien_direction = 1
                self.alien_move_down(2)
                self.line += 2

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens:
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        # Diminuir o timer para controlar o aparecimento da nave extra
        self.extra_spawn_time -= 1
        
        if self.extra_spawn_time <= 0:
            # Força a direção para alternar entre direita e esquerda
            if not hasattr(self, 'last_extra_direction'):
                self.last_extra_direction = 'right'
            else:
                self.last_extra_direction = 'left' if self.last_extra_direction == 'right' else 'right'
                
            print(f"Criando nave extra vindo da {self.last_extra_direction}")
            
            # Adiciona a nave extra e verifica se foi adicionada corretamente
            try:
                extra_alien = Extra(self.last_extra_direction, screen_width)
                self.extra.add(extra_alien)
                
                # Verifica se a nave foi adicionada ao grupo
                if self.extra.sprite:
                    print(f"Nave extra adicionada com sucesso ao grupo. Posição: {self.extra.sprite.rect.x}, {self.extra.sprite.rect.y}")
                else:
                    print("ERRO: Nave extra não foi adicionada ao grupo!")
            except Exception as e:
                print(f"Erro ao criar nave extra: {e}")
                
            # Timer para o próximo spawn
            self.extra_spawn_time = randint(400, 800)
            
            try:
                self.extra_sound.play()
            except Exception as e:
                print(f"Erro ao tocar som da nave extra: {e}")

    def collision_checks(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # aliens collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                # extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()
                    self.extra_explosion_sound.play()
                    self.draw_general()
                    point_extra_surf = self.font2.render('500 PTS', False, 'white')
                    screen.blit(point_extra_surf, (laser.rect.x, 40))
                    pygame.display.flip()
                    pygame.time.wait(500)

        # alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                #  player collisions
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    explosion_rect = pygame.Rect(0, 0, 32, 32)
                    explosion_rect.center = (self.player.sprite.rect.centerx, self.player.sprite.rect.centery)
                    self.player_sound.play()
                    self.draw_general()
                    
                    # Use try/except to handle potential explosion rendering issues
                    try:
                        screen.blit(self.explosion_player.get_current_frame(), explosion_rect)
                    except Exception as e:
                        print(f"Erro ao renderizar explosão: {e}")
                    
                    pygame.display.flip()
                    pygame.time.wait(300)
                    self.lives -= 1
                    if self.lives <= 0:
                        self.final_end()

        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)
                if pygame.sprite.spritecollide(alien, self.player, True):
                    self.final_end()

    def final_end(self):
        over_surf = self.font.render('GAME OVER', False, 'white')
        over_rect = over_surf.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(over_surf, over_rect)
        pygame.display.flip()
        pygame.time.wait(4000)
        pygame.quit()
        sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_star_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(0, 0))
        screen.blit(score_surf, score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You won', False, 'white')
            victory_rect = victory_surf.get_rect(center=(screen_width/2, screen_height/2))
            screen.blit(victory_surf, victory_rect)
            pygame.display.flip()
            pygame.time.wait(5000)
            pygame.quit()
            sys.exit()

    def draw_general(self):
        self.point += .05
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        if (int(self.point % 2) == 0):
            self.aliens.draw(screen)
        else:
            self.alien_mask()
        self.alien_lasers.draw(screen)
        
        # Desenha a nave extra
        self.extra.draw(screen)

    def alien_mask(self):
        # Fallback para o caso de não encontrar as imagens
        try:
            mask = gif_pygame.load('graphics/red2.png')
            mask2 = gif_pygame.load('graphics/green2.png')
            mask3 = gif_pygame.load('graphics/yellow2.png')
        except:
            print("Erro ao carregar as máscaras dos aliens")
            # Usa as imagens normais como fallback
            mask = gif_pygame.load('graphics/red.png')
            mask2 = gif_pygame.load('graphics/green.png')
            mask3 = gif_pygame.load('graphics/yellow.png')
            
        if self.aliens:
            for alien in self.aliens:
                if alien.rect.y == self.line or alien.rect.y + 48 == self.line or alien.rect.y + 96 == self.line:
                    screen.blit(mask.get_current_frame(), alien.rect)
                elif alien.rect.y + 240 == self.line:
                    screen.blit(mask3.get_current_frame(), alien.rect)
                else:
                    screen.blit(mask2.get_current_frame(), alien.rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.alien_lasers.update()
        self.extra_alien_timer()
        self.extra.update()
        self.collision_checks()
        self.draw_general()
        self.display_lives()
        self.display_score()
        self.victory_message()

class CRT:
    def __init__(self):
        # Tenta carregar a imagem da TV, se falhar, cria uma superfície semitransparente
        try:
            self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
            self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))
        except:
            print("Erro ao carregar a imagem da TV, criando efeito alternativo")
            self.tv = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            self.tv.fill((0, 0, 0, 100))  # Preto semitransparente

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

    def draw(self):
        try:
            self.tv.set_alpha(randint(75, 90))
            self.create_crt_lines()
            screen.blit(self.tv, (0, 0))
        except:
            # Método alternativo de desenho se set_alpha não funcionar
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(25)
            screen.blit(overlay, (0, 0))
            
            # Desenha algumas linhas horizontais para simular o efeito de escaneamento CRT
            for i in range(0, screen_height, 3):
                pygame.draw.line(screen, (0, 0, 0, 50), (0, i), (screen_width, i), 1)

def main():
    """Função principal que inicia o jogo"""
    global screen, screen_width, screen_height
    
    # Inicializa o Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Inicia o servidor web em uma thread separada
    try:
        import web_server
        web_server.run_server_thread()
    except Exception as e:
        print(f"Failed to start web server: {e}")
    
    # Configurações da tela
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Invaders")
    
    # Configurar para ser acessível externamente
    import os
    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
    os.environ['SDL_VIDEO_X11_VISUALID'] = ''
    
    # Inicializa o jogo
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()
    
    # Configuração do timer para disparos dos aliens
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)
    
    # Loop principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()
                
        # Também permite disparos baseados em tempo em vez de eventos
        current_time = pygame.time.get_ticks()
        if hasattr(game, 'last_alien_shot'):
            if current_time - game.last_alien_shot > 1000:  # dispara a cada 1 segundo
                game.alien_shoot()
                game.last_alien_shot = current_time
        else:
            game.last_alien_shot = current_time
        
        # Atualiza e renderiza o jogo
        screen.fill((30, 30, 30))
        game.run()
        crt.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
