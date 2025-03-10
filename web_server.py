
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web server for the Space Invaders game
"""

import http.server
import socketserver
import threading
import os

class SpaceInvadersServer(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler for serving the Space Invaders game"""
    
    def do_GET(self):
        """Handle GET requests"""
        # Serve index.html by default
        if self.path == '/':
            self.path = '/index.html'
        
        # Verifica se o arquivo solicitado existe
        try:
            # Use os.path para combinar o caminho base e o caminho solicitado
            file_path = os.path.join(os.getcwd(), self.path.lstrip('/'))
            
            # Se o arquivo existe, tente servi-lo
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            
            # Se for solicitado um arquivo de som ou imagem que não existe no caminho raiz,
            # tente encontrá-lo na estrutura de pastas do jogo original
            ext = os.path.splitext(self.path)[1].lower()
            if ext in ['.wav', '.png', '.gif']:
                for folder in ['sons', 'audio', 'graphics']:
                    alt_path = os.path.join(os.getcwd(), folder, os.path.basename(self.path))
                    if os.path.exists(alt_path):
                        with open(alt_path, 'rb') as file:
                            self.send_response(200)
                            self.send_header('Content-type', self.guess_type(alt_path))
                            self.end_headers()
                            self.wfile.write(file.read())
                            return
            
            # Se o arquivo não foi encontrado em nenhum lugar, envie uma página 404
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1><p>The requested file could not be found.</p></body></html>')
        except Exception as e:
            print(f"Erro ao servir arquivo: {e}")
            self.send_error(500, str(e))

def run_web_server():
    """Runs the web server in a separate thread"""
    try:
        PORT = 8000
        Handler = SpaceInvadersServer

        # Bind to all interfaces to make it accessible externally
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            print(f"Web server running at port {PORT}")
            print(f"Acesse o jogo em: http://0.0.0.0:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error in web server: {e}")

def run_server_thread():
    """Start the server in a daemon thread so it doesn't block the main game"""
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    print(f"Web server started on port 8000")
    return server_thread

if __name__ == "__main__":
    server_thread = run_server_thread()
    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("Server stopped")
