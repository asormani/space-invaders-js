#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funções utilitárias para o jogo
"""

import pygame
import os

def carregar_imagem(nome, escala=1):
    """Carrega uma imagem a partir de um nome de arquivo
    
    Args:
        nome: O nome do arquivo de imagem
        escala: Fator de escala para redimensionar a imagem
        
    Returns:
        A superfície da imagem carregada
    """
    # Verifica se o arquivo existe
    if not os.path.isfile(nome):
        # Cria uma superfície com cor sólida como fallback
        img = pygame.Surface((30, 30))
        img.fill((255, 255, 255))  # Branco como cor padrão
        return img
    
    try:
        img = pygame.image.load(nome).convert_alpha()
        
        if escala != 1:
            tamanho_original = img.get_size()
            novo_tamanho = (int(tamanho_original[0] * escala), 
                           int(tamanho_original[1] * escala))
            img = pygame.transform.scale(img, novo_tamanho)
        
        return img
    except pygame.error:
        # Cria uma superfície com cor sólida como fallback
        img = pygame.Surface((30, 30))
        img.fill((255, 255, 255))  # Branco como cor padrão
        return img

def criar_texto(texto, fonte, cor):
    """Cria uma superfície de texto
    
    Args:
        texto: O texto a ser renderizado
        fonte: A fonte a ser usada
        cor: A cor do texto
        
    Returns:
        A superfície de texto renderizada
    """
    return fonte.render(texto, True, cor)
