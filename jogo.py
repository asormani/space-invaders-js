#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo principal do jogo, coordena todos os componentes e a lógica do jogo
"""

import sys
import pygame
import random
from pygame.locals import *

from configuracoes import *
from jogador import Jogador
from alien import Alien, GrupoAliens
from projetil import Projetil
from barreira import Barreira
from assets.sons import Sons
from assets.sprites import carregar_sprites

class Jogo:
    """Classe principal do jogo que gerencia todos os elementos e estados"""
    
    def __init__(self):
        """Inicializa o jogo, configurações e estados iniciais"""
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption('Space Invaders')
        
        # Carrega os sprites e sons
        self.sprites = carregar_sprites()
        self.sons = Sons()
        print("Sons carregados com sucesso!")
        
        # Inicializa o relógio para controle de FPS
        self.relogio = pygame.time.Clock()
        
        # Estado do jogo
        self.estado = 'menu'  # 'menu', 'jogando', 'game_over'
        
        # Inicializa a fonte
        self.fonte_pequena = pygame.font.SysFont('Arial', 20)
        self.fonte_media = pygame.font.SysFont('Arial', 30)
        self.fonte_grande = pygame.font.SysFont('Arial', 50)
        
        # Cria o jogador
        self.jogador = None
        
        # Cria os aliens
        self.grupo_aliens = None
        
        # Cria os projéteis
        self.projeteis_jogador = []
        self.projeteis_aliens = []
        
        # Cria as barreiras
        self.barreiras = []
        
        # Pontuação e vidas
        self.pontuacao = 0
        self.vidas = 3
        self.recorde = self.carregar_recorde()
        
        # Nível atual
        self.nivel = 1
        
        # Tempo para controle do disparo dos aliens
        self.tempo_ultimo_tiro_alien = 0
        
        # Inicializa componentes do jogo
        self.reset_jogo()
    
    def reset_jogo(self):
        """Reinicia os componentes do jogo para um novo jogo"""
        # Reinicia pontuação e vidas
        self.pontuacao = 0
        self.vidas = 3
        self.nivel = 1
        
        # Reinicia o jogador
        self.jogador = Jogador(self.sprites['jogador'])
        
        # Reinicia os aliens
        self.grupo_aliens = GrupoAliens(self.sprites['aliens'], self.nivel)
        
        # Limpa os projéteis
        self.projeteis_jogador = []
        self.projeteis_aliens = []
        
        # Cria as barreiras
        self.criar_barreiras()
    
    def criar_barreiras(self):
        """Cria as barreiras de proteção"""
        self.barreiras = []
        
        posicoes_x = [100, 250, 400, 550]
        for x in posicoes_x:
            self.barreiras.append(Barreira(x, 500))
    
    def carregar_recorde(self):
        """Carrega o recorde atual de um arquivo"""
        try:
            with open("recorde.txt", "r") as arquivo:
                return int(arquivo.read())
        except (FileNotFoundError, ValueError):
            return 0
    
    def salvar_recorde(self):
        """Salva o recorde atual em um arquivo"""
        with open("recorde.txt", "w") as arquivo:
            arquivo.write(str(self.recorde))
    
    def verificar_recorde(self):
        """Verifica se a pontuação atual é um novo recorde"""
        if self.pontuacao > self.recorde:
            self.recorde = self.pontuacao
            self.salvar_recorde()
            return True
        return False
    
    def processar_eventos(self):
        """Processa os eventos do pygame"""
        for evento in pygame.event.get():
            if evento.type == QUIT:
                self.sair()
            
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.sair()
                
                if self.estado == 'menu':
                    if evento.key == K_RETURN:
                        self.estado = 'jogando'
                        self.reset_jogo()
                        self.sons.musica_jogo()
                
                elif self.estado == 'game_over':
                    if evento.key == K_RETURN:
                        self.estado = 'menu'
                
                elif self.estado == 'jogando':
                    if evento.key == K_SPACE:
                        self.jogador_atira()
    
    def jogador_atira(self):
        """Faz o jogador atirar se possível"""
        # Limita o número de projéteis simultâneos
        if len(self.projeteis_jogador) < 3:
            projetil = Projetil(
                self.jogador.rect.centerx,
                self.jogador.rect.top,
                self.sprites['tiro_jogador'],
                -12  # Velocidade negativa para ir para cima (mais rápido)
            )
            self.projeteis_jogador.append(projetil)
            self.sons.tiro_jogador()
    
    def alien_atira(self, alien):
        """Faz um alien atirar"""
        projetil = Projetil(
            alien.rect.centerx,
            alien.rect.bottom,
            self.sprites['tiro_alien'],
            4  # Velocidade positiva reduzida para ir para baixo
        )
        self.projeteis_aliens.append(projetil)
        self.sons.tiro_alien()
    
    def atualizar(self):
        """Atualiza o estado do jogo"""
        if self.estado == 'jogando':
            # Processa as teclas pressionadas para movimentação contínua
            teclas = pygame.key.get_pressed()
            if teclas[K_LEFT]:
                self.jogador.mover(-5)
            if teclas[K_RIGHT]:
                self.jogador.mover(5)
            
            # Atualiza o jogador
            self.jogador.atualizar()
            
            # Atualiza os aliens
            resultado = self.grupo_aliens.atualizar()
            
            # Verifica se os aliens atingiram o limite inferior
            if resultado == 'invasao':
                self.vidas = 0
                self.atualizar_game_over()
                return
            
            # Atualiza os projéteis do jogador
            self.atualizar_projeteis_jogador()
            
            # Atualiza os projéteis dos aliens
            self.atualizar_projeteis_aliens()
            
            # Aliens atiram aleatoriamente
            self.gerenciar_tiros_aliens()
            
            # Verifica se todos os aliens foram eliminados
            if self.grupo_aliens.tamanho() == 0:
                self.avancar_nivel()
    
    def atualizar_projeteis_jogador(self):
        """Atualiza a posição e colisões dos projéteis do jogador"""
        projeteis_a_remover = []
        
        for projetil in self.projeteis_jogador:
            projetil.atualizar()
            
            # Remove o projétil se saiu da tela
            if projetil.rect.bottom < 0:
                projeteis_a_remover.append(projetil)
                continue
            
            # Verifica colisão com aliens
            alien_atingido = self.grupo_aliens.verificar_colisao(projetil.rect)
            if alien_atingido:
                self.pontuacao += alien_atingido.valor
                self.sons.explosao_alien()
                projeteis_a_remover.append(projetil)
                continue
            
            # Verifica colisão com barreiras
            for barreira in self.barreiras:
                if barreira.verificar_colisao(projetil.rect):
                    projeteis_a_remover.append(projetil)
                    break
        
        # Remove os projéteis marcados
        for projetil in projeteis_a_remover:
            if projetil in self.projeteis_jogador:
                self.projeteis_jogador.remove(projetil)
    
    def atualizar_projeteis_aliens(self):
        """Atualiza a posição e colisões dos projéteis dos aliens"""
        projeteis_a_remover = []
        
        for projetil in self.projeteis_aliens:
            projetil.atualizar()
            
            # Remove o projétil se saiu da tela
            if projetil.rect.top > ALTURA_TELA:
                projeteis_a_remover.append(projetil)
                continue
            
            # Verifica colisão com o jogador
            if projetil.rect.colliderect(self.jogador.rect):
                self.vidas -= 1
                projeteis_a_remover.append(projetil)
                self.sons.explosao_jogador()
                
                if self.vidas <= 0:
                    self.atualizar_game_over()
                break
            
            # Verifica colisão com barreiras
            for barreira in self.barreiras:
                if barreira.verificar_colisao(projetil.rect):
                    projeteis_a_remover.append(projetil)
                    break
        
        # Remove os projéteis marcados
        for projetil in projeteis_a_remover:
            if projetil in self.projeteis_aliens:
                self.projeteis_aliens.remove(projetil)
    
    def gerenciar_tiros_aliens(self):
        """Gerencia os tiros dos aliens com base no tempo e aleatoriedade"""
        tempo_atual = pygame.time.get_ticks()
        # Espera um intervalo entre os tiros (aumentado para tornar o jogo mais lento)
        if tempo_atual - self.tempo_ultimo_tiro_alien > 1500 - (self.nivel * 40):
            # Chance de tiro que aumenta com o nível (reduzida para tornar o jogo mais fácil)
            if random.random() < 0.05 + (self.nivel * 0.01):
                # Seleciona um alien aleatório para atirar
                alien = self.grupo_aliens.obter_alien_aleatorio()
                if alien:
                    self.alien_atira(alien)
                    self.tempo_ultimo_tiro_alien = tempo_atual
    
    def avancar_nivel(self):
        """Avança para o próximo nível"""
        self.nivel += 1
        self.grupo_aliens = GrupoAliens(self.sprites['aliens'], self.nivel)
        
        # Reinicia as barreiras a cada 3 níveis
        if self.nivel % 3 == 1:
            self.criar_barreiras()
    
    def atualizar_game_over(self):
        """Atualiza o estado para game over"""
        self.estado = 'game_over'
        self.verificar_recorde()
        self.sons.game_over()
    
    def desenhar_menu(self):
        """Desenha a tela de menu"""
        self.tela.fill(PRETO)
        
        # Título
        titulo = self.fonte_grande.render('SPACE INVADERS', True, BRANCO)
        titulo_rect = titulo.get_rect(center=(LARGURA_TELA // 2, 150))
        self.tela.blit(titulo, titulo_rect)
        
        # Instruções
        instrucao = self.fonte_media.render('Pressione ENTER para iniciar', True, BRANCO)
        instrucao_rect = instrucao.get_rect(center=(LARGURA_TELA // 2, 350))
        self.tela.blit(instrucao, instrucao_rect)
        
        # Controles
        controles1 = self.fonte_pequena.render('Controles:', True, BRANCO)
        controles2 = self.fonte_pequena.render('Setas para mover | Espaço para atirar', True, BRANCO)
        
        self.tela.blit(controles1, (LARGURA_TELA // 2 - 150, 450))
        self.tela.blit(controles2, (LARGURA_TELA // 2 - 150, 480))
        
        # Recorde
        recorde = self.fonte_pequena.render(f'Recorde: {self.recorde}', True, BRANCO)
        self.tela.blit(recorde, (LARGURA_TELA // 2 - 50, 550))
    
    def desenhar_game_over(self):
        """Desenha a tela de fim de jogo"""
        self.tela.fill(PRETO)
        
        # Texto de Game Over
        game_over = self.fonte_grande.render('GAME OVER', True, VERMELHO)
        game_over_rect = game_over.get_rect(center=(LARGURA_TELA // 2, 150))
        self.tela.blit(game_over, game_over_rect)
        
        # Pontuação
        pontuacao = self.fonte_media.render(f'Pontuação: {self.pontuacao}', True, BRANCO)
        pontuacao_rect = pontuacao.get_rect(center=(LARGURA_TELA // 2, 250))
        self.tela.blit(pontuacao, pontuacao_rect)
        
        # Recorde
        recorde = self.fonte_media.render(f'Recorde: {self.recorde}', True, BRANCO)
        recorde_rect = recorde.get_rect(center=(LARGURA_TELA // 2, 300))
        self.tela.blit(recorde, recorde_rect)
        
        # Nível alcançado
        nivel = self.fonte_media.render(f'Nível Alcançado: {self.nivel}', True, BRANCO)
        nivel_rect = nivel.get_rect(center=(LARGURA_TELA // 2, 350))
        self.tela.blit(nivel, nivel_rect)
        
        # Instruções
        instrucao = self.fonte_media.render('Pressione ENTER para voltar ao menu', True, BRANCO)
        instrucao_rect = instrucao.get_rect(center=(LARGURA_TELA // 2, 450))
        self.tela.blit(instrucao, instrucao_rect)
    
    def desenhar_jogo(self):
        """Desenha os elementos do jogo na tela"""
        self.tela.fill(PRETO)
        
        # Desenha o jogador
        self.jogador.desenhar(self.tela)
        
        # Desenha os aliens
        self.grupo_aliens.desenhar(self.tela)
        
        # Desenha os projéteis do jogador
        for projetil in self.projeteis_jogador:
            projetil.desenhar(self.tela)
        
        # Desenha os projéteis dos aliens
        for projetil in self.projeteis_aliens:
            projetil.desenhar(self.tela)
        
        # Desenha as barreiras
        for barreira in self.barreiras:
            barreira.desenhar(self.tela)
        
        # Desenha a pontuação
        texto_pontuacao = self.fonte_pequena.render(f'Pontuação: {self.pontuacao}', True, BRANCO)
        self.tela.blit(texto_pontuacao, (10, 10))
        
        # Desenha as vidas
        texto_vidas = self.fonte_pequena.render(f'Vidas: {self.vidas}', True, BRANCO)
        self.tela.blit(texto_vidas, (LARGURA_TELA - 100, 10))
        
        # Desenha o nível
        texto_nivel = self.fonte_pequena.render(f'Nível: {self.nivel}', True, BRANCO)
        self.tela.blit(texto_nivel, (LARGURA_TELA // 2 - 50, 10))
    
    def desenhar(self):
        """Desenha o estado atual do jogo"""
        if self.estado == 'menu':
            self.desenhar_menu()
        elif self.estado == 'jogando':
            self.desenhar_jogo()
        elif self.estado == 'game_over':
            self.desenhar_game_over()
        
        pygame.display.flip()
    
    def sair(self):
        """Encerra o jogo"""
        pygame.quit()
        sys.exit()
    
    def executar(self):
        """Loop principal do jogo"""
        while True:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(45)  # Limita o jogo a 45 FPS para uma velocidade mais adequada
