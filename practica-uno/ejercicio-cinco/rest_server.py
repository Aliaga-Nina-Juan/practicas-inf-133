from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse,parse_qs

animales = [
    {
        "id":1,
        "nombre":"ballena",
        "especie":"acuatico",
        "genero":"macho",
        "edad":"4",
        "peso":"56",
    },
    {
        "id":2,
        "nombre":"leon",
        "especie":"felino",
        "genero":"macho",
        "edad":"4",
        "peso":"56",
    },
]


class RESTRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    
    def find_animal(self, id):
        return next(
            (animal for animal in animales if animal["id"] == id),
            None,
        )
    
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if self.path == "/animales":
            self.response_handler(200, animales)
        elif self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = self.find_animal(id)
            if animal:
                self.response_handler(200, [animal])
            else:
                self.response_handler(204, [])
        elif parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_filtrados = [
                    animal
                    for animal in animales
                    if animal["especie"]==especie
                ]
                if animales_filtrados != []:
                    self.response_handler(200,animales_filtrados)
                else:
                    self.response_handler(204,[])
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales_filtrados = [
                    animal
                    for animal in animales
                    if animal["genero"]==genero
                ]
                if animales_filtrados != []:
                    self.response_handler(200,animales_filtrados)
                else:
                    self.response_handler(204,[])
            else:
                self.response_handler(200,{"Error":"No se encontro al animal"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            data["id"] = len(animales) + 1
            animales.append(data)
            self.response_handler(201, animales)

        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = self.find_animal(id)
            data = self.read_data()
            if animal:
                animal.update(data)
                self.response_handler(200, [animales])
            else:
                self.response_handler(404, {"Error": "animal no encontrado"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path == "/animales":
            animales.clear()
            self.response_handler(200, animales)
        elif self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = self.find_animal(id)
            if animal:
                animales.remove(animal)
                self.response_handler(200, animales)
            else:
                self.response_handler(404, {"Error": "animal no encontrado"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()