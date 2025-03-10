#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que implementa o jogador
"""

import pygame
from configuracoes import *

class Jogador:
    """Classe que representa a nave do jogador"""
    
    def __init__(self, imagem):
        """Inicializa o jogador com a imagem fornecida"""
        self.imagem = imagem
        self.rect = self.imagem.get_rect()
        
        # Posiciona o jogador na parte inferior central da tela
        self.rect.centerx = LARGURA_TELA // 2
        self.rect.bottom = ALTURA_TELA - 10
        
        # Velocidade do jogador
        self.velocidade = 5
    
    def mover(self, direcao):
        """Move o jogador na direção especificada"""
        self.rect.x += direcao * self.velocidade
        
        # Limita o movimento ao tamanho da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA_TELA:
            self.rect.right = LARGURA_TELA
    
    def atualizar(self):
        """Atualiza o estado do jogador"""
        # No momento, não precisamos de lógica adicional aqui, mas
        # podemos adicionar no futuro (ex: invencibilidade temporária)
        pass
    
    def desenhar(self, tela):
        """Desenha o jogador na tela"""
        tela.blit(self.imagem, self.rect)
