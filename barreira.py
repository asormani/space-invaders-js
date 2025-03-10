#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que implementa as barreiras de proteção
"""

import pygame
from configuracoes import *

class Barreira:
    """Classe que representa uma barreira de proteção"""
    
    def __init__(self, x, y):
        """Inicializa a barreira na posição especificada"""
        self.blocos = []
        self.cor = VERDE
        self.largura_bloco = 10
        self.altura_bloco = 10
        
        # Cria a forma da barreira
        # Uma forma de barreira clássica do Space Invaders
        # em formato aproximado de fortaleza
        forma = [
            "  XXXXX  ",
            " XXXXXXX ",
            "XXXXXXXXX",
            "XXXXXXXXX",
            "XXXXXXXXX",
            "XXX   XXX",
            "XX     XX"
        ]
        
        for linha_idx, linha in enumerate(forma):
            for coluna_idx, char in enumerate(linha):
                if char == 'X':
                    bloco_x = x + coluna_idx * self.largura_bloco
                    bloco_y = y + linha_idx * self.altura_bloco
                    bloco = pygame.Rect(bloco_x, bloco_y, self.largura_bloco, self.altura_bloco)
                    self.blocos.append(bloco)
    
    def verificar_colisao(self, rect):
        """Verifica se um projétil colidiu com a barreira
        
        Args:
            rect: O retângulo do projétil
            
        Returns:
            True se houve colisão, False caso contrário
        """
        for bloco in self.blocos[:]:  # Usamos uma cópia para evitar problemas ao remover
            if bloco.colliderect(rect):
                self.blocos.remove(bloco)
                return True
        return False
    
    def desenhar(self, tela):
        """Desenha a barreira na tela"""
        for bloco in self.blocos:
            pygame.draw.rect(tela, self.cor, bloco)
