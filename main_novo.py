import pygame, sys, gif_pygame
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser


class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((screen_width/2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.explosion_player = gif_pygame.load('graphics/explosion.gif')
        self.point = 0

        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('graphics/player.png').convert_alpha()
        self.live_surf = pygame.transform.scale(self.live_surf, [20, 10])
        self.live_x_star_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)
        self.font2 = pygame.font.Font('font/Pixeled.ttf', 10)

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
        self.extra_spawn_time = randint(40, 80)


        #Audio
        music = pygame.mixer.Sound('audio/music.wav')
        music.set_volume(0.2)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)
        self.extra_sound = pygame.mixer.Sound('audio/mysteryentered.wav')
        self.extra_sound.set_volume(0.3)
        self.player_sound = pygame.mixer.Sound('audio/shipexplosion.wav')
        self.player_sound.set_volume(0.3)
        self.extra_explosion_sound = pygame.mixer.Sound('audio/mysterykilled.wav')
        self.extra_explosion_sound.set_volume(0.3)

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
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']), screen_width))
            self.extra_spawn_time = randint(400, 800)
            self.extra_sound.play()

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
                    explosion_rect = self.explosion_player.get_rect(center=(self.player.sprite.rect.x, self.player.sprite.rect.y))
                    self.player_sound.play()
                    self.draw_general()
                    self.explosion_player.render(screen, explosion_rect)
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
        self.extra.draw(screen)


    def alien_mask(self):
        mask = gif_pygame.load('graphics/red2.png')
        mask2 = gif_pygame.load('graphics/green2.png')
        mask3 = gif_pygame.load('graphics/yellow2.png')
        if self.aliens:
            for alien in self.aliens:
                if alien.rect.y == self.line or alien.rect.y + 48 == self.line or alien.rect.y + 96 == self.line:
                    mask.render(screen, (alien.rect.x, alien.rect.y))
                elif alien.rect.y + 240 == self.line:
                    mask3.render(screen, (alien.rect.x, alien.rect.y))
                else:
                    mask2.render(screen, (alien.rect.x, alien.rect.y))
                



    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.alien_lasers.update()
        self.extra_alien_timer()
        self.extra.update()
        self.collision_checks()
        #self.player.sprite.lasers.draw(screen)
        #self.player.draw(screen)
        #self.blocks.draw(screen)
        #self.aliens.draw(screen)
        #self.alien_lasers.draw(screen)
        #self.extra.draw(screen)
        self.draw_general()
        self.display_lives()
        self.display_score()
        self.victory_message()


class CRT:
    def __init__ (self):
        self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

    def creat_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range (line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.creat_crt_lines()
        screen.blit(self.tv, (0, 0))


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30, 30, 30))
        game.run()
        crt.draw()
        pygame.display.flip()
        clock.tick(60)