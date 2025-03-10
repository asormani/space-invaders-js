
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Inicializador do servidor web para o jogo Space Invaders em JavaScript
"""

import web_server
import time

if __name__ == "__main__":
    print("Iniciando o servidor web do jogo Space Invaders...")
    server_thread = web_server.run_server_thread()
    print("Servidor web iniciado com sucesso!")
    print("Acesse o jogo em: http://0.0.0.0:8000")
    print("Pressione Ctrl+C para encerrar o servidor")
    
    try:
        # Manter o programa em execução até que o usuário o interrompa
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário")
