
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para gerenciar os sons do jogo
"""

import pygame
import os.path

class Sons:
    """Classe para gerenciar os efeitos sonoros do jogo"""
    
    def __init__(self):
        """Inicializa o sistema de sons"""
        pygame.mixer.init()
        self.sons = {}
        self.inicializar_sons()
    
    def inicializar_sons(self):
        """Inicializa os sons do jogo"""
        # Caminho para as possíveis pastas de sons
        pastas_sons = [
            os.path.join(os.path.dirname(__file__), "..", "sons"),
            os.path.join(os.path.dirname(__file__), "..", "audio"),
            "sons",
            "audio"
        ]
        
        print("Procurando arquivos de som nas pastas:")
        for pasta in pastas_sons:
            print(f" - {os.path.abspath(pasta)}")
        
        # Define os sons por tipo e fornece um som vazio como fallback
        som_vazio = pygame.mixer.Sound(buffer=bytes([0] * 44))
        
        # Mapeamento dos sons originais para os nomes que temos disponíveis
        sons_para_carregar = {
            'tiro_jogador': ['tiro_jogador.wav', 'laser.wav'],
            'tiro_alien': ['tiro_alien.wav', 'laser.wav'],
            'explosao_alien': ['explosao_alien.wav', 'explosion.wav'],
            'explosao_jogador': ['explosao_jogador.wav', 'shipexplosion.wav'],
            'game_over': ['game_over.wav', 'shipexplosion.wav'],
            'nave_extra': ['nave_extra.wav', 'mysteryentered.wav'],
            'nave_extra_explosao': ['nave_extra_explosao.wav', 'mysterykilled.wav', 'explosion.wav']
        }
        
        # Carrega os sons ou usa o som vazio se o arquivo não existir
        for nome, arquivos in sons_para_carregar.items():
            self.sons[nome] = som_vazio
            for arquivo in arquivos:
                for pasta in pastas_sons:
                    caminho = os.path.join(pasta, arquivo)
                    try:
                        if os.path.exists(caminho):
                            print(f"Carregando som: {caminho}")
                            self.sons[nome] = pygame.mixer.Sound(caminho)
                            break
                    except Exception as e:
                        print(f"Erro ao carregar som {arquivo}: {e}")
                if self.sons[nome] != som_vazio:
                    break  # Encontrou o som, não precisa continuar procurando
    
    def tocar_som(self, nome):
        """Toca um som pelo nome
        
        Args:
            nome: O nome do som a ser tocado
        """
        if nome in self.sons:
            try:
                self.sons[nome].play()
            except Exception as e:
                print(f"Erro ao tocar som {nome}: {e}")
    
    def tiro_jogador(self):
        """Toca o som de tiro do jogador"""
        self.tocar_som('tiro_jogador')
    
    def tiro_alien(self):
        """Toca o som de tiro do alien"""
        self.tocar_som('tiro_alien')
    
    def explosao_alien(self):
        """Toca o som de explosão do alien"""
        self.tocar_som('explosao_alien')
    
    def explosao_jogador(self):
        """Toca o som de explosão do jogador"""
        self.tocar_som('explosao_jogador')
    
    def game_over(self):
        """Toca o som de game over"""
        self.tocar_som('game_over')
    
    def nave_extra(self):
        """Toca o som da nave extra"""
        self.tocar_som('nave_extra')
    
    def nave_extra_explosao(self):
        """Toca o som de explosão da nave extra"""
        self.tocar_som('nave_extra_explosao')
    
    def musica_jogo(self):
        """Inicia a música de fundo do jogo"""
        try:
            # Tenta carregar a música das várias pastas possíveis
            pastas_musica = [
                os.path.join(os.path.dirname(__file__), "..", "sons"),
                os.path.join(os.path.dirname(__file__), "..", "audio"),
                "sons",
                "audio"
            ]
            
            for pasta in pastas_musica:
                caminho_musica = os.path.join(pasta, "music.wav")
                if os.path.exists(caminho_musica):
                    print(f"Carregando música: {caminho_musica}")
                    musica = pygame.mixer.Sound(caminho_musica)
                    musica.set_volume(0.2)
                    musica.play(loops=-1)
                    print("Música iniciada com sucesso!")
                    return
            
            # Fallback: Batida de coração crescente característica do Space Invaders
            print("Música não encontrada, usando temporizador para efeito sonoro")
            pygame.time.set_timer(pygame.USEREVENT, 1000)  # Evento a cada 1 segundo
        except Exception as e:
            print(f"Erro ao iniciar música: {e}")
            # Fallback silencioso, sem música
            pygame.time.set_timer(pygame.USEREVENT, 1000)
