from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class Animal:
    def __init__(self, id,nombre,especie,genero,edad,peso):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.genero = genero 
        self.edad = edad
        self.peso = peso

#`Mamífero`, `Ave`, `Reptil`, `Anfibio` o `Pez`.


class Mamifero(Animal):
    def __init__(self,id,nombre,genero,edad,peso):
        super().__init__(id,nombre,"mamifero",genero,edad,peso)

class Ave(Animal):
    def __init__(self,id,nombre,genero,edad,peso):
        super().__init__(id,nombre,"ave",genero,edad,peso)

class Reptil(Animal):
    def __init__(self,id,nombre,genero,edad,peso):
        super().__init__(id,nombre,"reptil",genero,edad,peso)

class Anfibio(Animal):
    def __init__(self,id,nombre,genero,edad,peso):
        super().__init__(id,nombre,"anfibio",genero,edad,peso)

class Pez(Animal):
    def __init__(self,id,nombre,genero,edad,peso):
        super().__init__(id,nombre,"pez",genero,edad,peso)
        
class AnimalFactory:
    def create_especie_animal(self,especie,id,nombre,genero,edad,peso):
        if especie == "mamifero":
            return Mamifero(id,nombre,genero,edad,peso)
        elif especie == "ave":
            return Ave(id,nombre,genero,edad,peso)
        elif especie == "reptil":
            return Reptil(id,nombre,genero,edad,peso)
        elif especie == "anfibio":
            return Anfibio()
        elif especie == "pez":
            return Pez(id,nombre,genero,edad,peso)
        else:
            raise ValueError("Tipo de animal no válido")


class AnimalRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/animal":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode("utf-8"))
            

            id = request_data.get("id")
            nombre = request_data.get("nombre")
            genero = request_data.get("genero")
            edad = request_data.get("edad")
            peso = request_data.get("peso")
            especie = request_data.get("especie")
            animal_factory = AnimalFactory()
            animal_factory.create_especie_animal(especie,id,nombre,genero,edad,peso)

            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(request_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada")


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, AnimalRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()