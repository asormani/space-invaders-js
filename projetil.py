#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que implementa os projéteis do jogo
"""

import pygame
from configuracoes import *

class Projetil:
    """Classe que representa um projétil"""
    
    def __init__(self, x, y, imagem, velocidade):
        """Inicializa o projétil com a posição, imagem e velocidade"""
        self.imagem = imagem
        self.rect = self.imagem.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocidade = velocidade
    
    def atualizar(self):
        """Atualiza a posição do projétil"""
        self.rect.y += self.velocidade
    
    def desenhar(self, tela):
        """Desenha o projétil na tela"""
        tela.blit(self.imagem, self.rect)
