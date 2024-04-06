from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from urllib.parse import urlparse,parse_qs

partidas = []

class Player:
    _instance = None

    def __new__(cls, ele,ele2):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.id = 0
            cls._instance.ele = ele
            cls._instance.ele2 = ele2
            cls._instance.result = None
        return cls._instance
    def crear_partida(self,ele):
        self.id = self.id + 1
        opciones = ["piedra","papel","tijera"]
        self.ele2 = random.choice(opciones)
        self.ele = ele
        if ele =="piedra":
            if self.ele2=="piedra":
                self.result = "empate"
            elif self.ele2 == "tijera":
                self.result = "gano"
            elif self.ele2 == "papel":
                self.result = "perdio"
        if ele=="papel":
            if self.ele2=="piedra":
                self.result = "gano"
            elif self.ele2 == "tijera":
                self.result = "perdio"
            elif self.ele2 == "papel":
                self.result = "empate"
        if ele=="tijera":
            if self.ele2=="piedra":
                self.result = "perdio"
            elif self.ele2 == "tijera":
                self.result = "empate"
            elif self.ele2 == "papel":
                self.result = "gano"
        
    
    def to_dict(self):
        return {"Id":self.id,"Elemento del jugador": self.ele, "Elemento del servidor": self.ele2,"resultado":self.result},

class PartidasHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if self.path == "/partidas":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(partidas).encode("utf-8"))
        elif parsed_path.path == "/partidas":
            if "resultado" in query_params:
                Resultado = query_params["resultado"][0]
                partidas_filtradas = [
                    partida
                    for partida in partidas
                    if partida["resultado"]
                ]
                if partidas_filtradas != []:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(partidas_filtradas).encode("utf-8"))
                else:
                    self.send_response(204)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps([]).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/partidas":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            elemento = json.loads(post_data.decode("utf-8"))["elemento"]
            player.crear_partida(elemento)
            self.send_response(201)
            self.end_headers()
            player_data = player.to_dict()
            partidas.append(player_data)
            self.wfile.write(json.dumps(player_data).encode("utf-8"))
            
            #self.wfile.write(player_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def main():
    global player
    player = Player("piedra","papel")

    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PartidasHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()