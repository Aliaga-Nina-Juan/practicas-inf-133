from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType,String,Int,Boolean,List,Schema,Field,Mutation

class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura = Int()
    frutos= Boolean()
#-------------------Query-----------------
class Query(ObjectType):
    plantas = List(Planta)
    planta_por_especie = Field(Planta,especie=String())
    planta_por_frutos = Field(Planta,frutos=Boolean())
    
    def resolve_plantas(root,info):
        return plantas
    def resolve_planta_por_especie(root,info,especie):
        for planta in plantas:
            if planta.especie == especie:
                return planta
        return None
    def resolve_planta_por_frutos(root,info):
        for planta in plantas:
            if planta.frutos == True:
                return planta
        return None
#--------------------------------------
plantas = [
    Planta(
        id = 1,
        nombre = "coca",
        especie = "coca amazonica",
        edad = 3,
        altura = 50,
        frutos= False,
    ),
    Planta(
        id = 2,
        nombre = "bananero",
        especie = "musa",
        edad = 7,
        altura = 120,
        frutos= True,
    ),
]
#------------------Creando una nueva planta------------
class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()
    planta = Field(Planta)
#--------------funcion mutate--------------
    def mutate(root , info , nombre, especie,edad,altura,frutos):
        nueva_planta = Planta(
            id = len(plantas) + 1,
            nombre = nombre,
            especie = especie,
            edad = edad,
            altura = altura,
            frutos = frutos,
        )
        plantas.append(nueva_planta)
        return CrearPlanta(planta=nueva_planta)
#---------------Eliminar planta------------------
class DeletePlanta(Mutation):
    class Arguments:
        id = Int()
    planta = Field(Planta)
#--------------funcion mutate--------------
    def mutate(root ,info,id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None
#----------------Actualizar planta-------------
class ActualizarPlanta(Mutation):
    class Arguments:
        id = Int()
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()
    planta = Field(Planta)
#---------------funcion mutate--------------
    def mutate(root,info,id,nombre,especie,edad,altura,frutos):
        for i,planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                planta_actualizada = Planta(
                    id = i+1,
                    nombre = nombre,
                    especie = especie,
                    edad = edad,
                    altura = altura,
                    frutos = frutos,
                )
                plantas.append(planta_actualizada)
                return ActualizarPlanta(planta=planta_actualizada)
        return None
#----------------Clase Mutations----------------
class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()
    actualizar_planta = ActualizarPlanta.Field()

#----------definiendo el Esquema----------
schema = Schema(query=Query,mutation=Mutations)
#-----------------------------------------
class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self,status,data):
        self.send_response(status)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200,result.data)
        else:
            self.response_handler(404,{"Error":"Ruta no existente"})
#--------------funcion para iniciar servidor--------------
def run_server(port=8000):
    try:
        server_address = ("",port)
        httpd = HTTPServer(server_address,GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()
#---------------------------------------------------------
if __name__ == "__main__":
    run_server()