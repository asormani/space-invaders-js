import pygame
import time
import os

class GIFImage:
    def __init__(self, filename):
        self.filename = filename
        self.frames = []
        self.current_frame = 0
        self.last_update = 0
        self.frame_duration = 100  # Default frame duration in ms
        self.loop = True
        self.load_frames()

    def load_frames(self):
        try:
            base_img = pygame.image.load(self.filename).convert_alpha()
            self.frames.append(base_img)
            # For a real GIF, we would load all frames here
            # But for simplicity, we'll just use the single image
        except Exception as e:
            print(f"Erro ao carregar frames de {self.filename}, usando uma imagem estática")
            # Create a fallback empty surface
            self.frames = [pygame.Surface((32, 32), pygame.SRCALPHA)]

    def get_rect(self, **kwargs):
        return self.frames[0].get_rect(**kwargs)

    def get_current_frame(self):
        return self.frames[self.current_frame]

    def render(self, surface, position):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = current_time
        surface.blit(self.frames[self.current_frame], position)

class StaticImage:
    def __init__(self, filename):
        try:
            self.image = pygame.image.load(filename).convert_alpha()
        except Exception as e:
            print(f"Erro ao carregar imagem estática {filename}, criando superfície vazia")
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA)

    def get_rect(self, **kwargs):
        return self.image.get_rect(**kwargs)

    def get_current_frame(self):
        return self.image

    def render(self, surface, position):
        surface.blit(self.image, position)

def load(filename):
    """Load an image file and return appropriate handler based on extension"""
    if not os.path.exists(filename):
        print(f"Arquivo não encontrado: {filename}")
        return StaticImage('graphics/player.png')

    if filename.lower().endswith('.gif'):
        return GIFImage(filename)
    else:
        return StaticImage(filename)