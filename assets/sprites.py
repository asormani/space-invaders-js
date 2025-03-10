#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para carregar e gerenciar os sprites do jogo
"""

import pygame
from util import carregar_imagem

def carregar_sprites():
    """Carrega todos os sprites do jogo
    
    Returns:
        Dicionário com todos os sprites carregados
    """
    sprites = {}
    
    # Como não podemos usar imagens diretamente, vamos criar sprites programaticamente
    
    # Sprite do jogador
    jogador = criar_sprite_jogador()
    sprites['jogador'] = jogador
    
    # Sprites dos aliens
    sprites['aliens'] = [
        criar_sprite_alien(0),  # Alien tipo 1 (topo)
        criar_sprite_alien(1),  # Alien tipo 2 (meio)
        criar_sprite_alien(2)   # Alien tipo 3 (baixo)
    ]
    
    # Sprites dos projéteis
    sprites['tiro_jogador'] = criar_sprite_tiro_jogador()
    sprites['tiro_alien'] = criar_sprite_tiro_alien()
    
    return sprites

def criar_sprite_jogador():
    """Cria o sprite da nave do jogador
    
    Returns:
        Superfície com o sprite da nave
    """
    tamanho = (40, 30)
    sprite = pygame.Surface(tamanho, pygame.SRCALPHA)
    
    # Desenha a nave
    pygame.draw.rect(sprite, (0, 255, 0), (10, 15, 20, 15))  # Corpo principal
    pygame.draw.rect(sprite, (0, 255, 0), (19, 5, 2, 10))    # Canhão
    
    return sprite

def criar_sprite_alien(tipo):
    """Cria o sprite de um alien
    
    Args:
        tipo: Tipo do alien (0, 1 ou 2)
        
    Returns:
        Superfície com o sprite do alien
    """
    tamanho = (30, 30)
    sprite = pygame.Surface(tamanho, pygame.SRCALPHA)
    
    cor = (255, 0, 0) if tipo == 0 else ((255, 255, 0) if tipo == 1 else (0, 255, 255))
    
    if tipo == 0:  # Alien tipo 1 (topo)
        # Desenha um alien com forma ovalada e "tentáculos"
        pygame.draw.ellipse(sprite, cor, (5, 5, 20, 15))  # Cabeça
        pygame.draw.rect(sprite, cor, (5, 20, 20, 5))     # Corpo
        
        # Tentáculos
        pygame.draw.rect(sprite, cor, (5, 25, 3, 5))
        pygame.draw.rect(sprite, cor, (12, 25, 3, 5))
        pygame.draw.rect(sprite, cor, (22, 25, 3, 5))
        
    elif tipo == 1:  # Alien tipo 2 (meio)
        # Desenha um alien com forma de caranguejo
        pygame.draw.ellipse(sprite, cor, (5, 5, 20, 15))  # Cabeça
        
        # Pinças/braços
        pygame.draw.rect(sprite, cor, (0, 15, 5, 3))
        pygame.draw.rect(sprite, cor, (25, 15, 5, 3))
        
        # Pernas
        pygame.draw.rect(sprite, cor, (8, 20, 3, 10))
        pygame.draw.rect(sprite, cor, (19, 20, 3, 10))
        
    else:  # Alien tipo 3 (baixo)
        # Desenha um alien com forma de lula
        pygame.draw.ellipse(sprite, cor, (5, 5, 20, 15))  # Cabeça
        
        # Tentáculos
        pygame.draw.rect(sprite, cor, (5, 20, 2, 10))
        pygame.draw.rect(sprite, cor, (10, 20, 2, 7))
        pygame.draw.rect(sprite, cor, (15, 20, 2, 10))
        pygame.draw.rect(sprite, cor, (20, 20, 2, 7))
    
    return sprite

def criar_sprite_tiro_jogador():
    """Cria o sprite do tiro do jogador
    
    Returns:
        Superfície com o sprite do tiro
    """
    tamanho = (3, 15)
    sprite = pygame.Surface(tamanho)
    sprite.fill((255, 255, 255))  # Tiro branco
    
    return sprite

def criar_sprite_tiro_alien():
    """Cria o sprite do tiro do alien
    
    Returns:
        Superfície com o sprite do tiro
    """
    tamanho = (3, 15)
    sprite = pygame.Surface(tamanho)
    sprite.fill((255, 0, 0))  # Tiro vermelho
    
    return sprite
