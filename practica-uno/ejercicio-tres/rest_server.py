from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse,parse_qs

pacientes = [
    {
        "ci": 1,
        "nombre":"Jorge",
        "apellido":"Perez",
        "edad":35,
        "genero":"masculino",
        "diagnostico":"cancer",
        "doctor":"Brayan",
    },
    {
        "ci": 2,
        "nombre":"Juan",
        "apellido":"Perez",
        "edad":40,
        "genero":"masculino",
        "diagnostico":"diabetes",
        "doctor":"Luis",
    },
]
#------------------------------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------------------------------
class PacientesService:
    @staticmethod
    def find_paciente(ci):
        return next(
            (paciente for paciente in pacientes if paciente["ci"] == ci),
            None,
        )

    @staticmethod
    def filter_pacientes_by_diagnostico(diagnostico):
        return [
            paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico
        ]

    @staticmethod
    def filter_pacientes_by_doctor(doctor):
        return [
            paciente for paciente in pacientes if paciente["doctor"] == doctor
        ]

    @staticmethod
    def add_paciente(data):
        data["ci"] = len(pacientes)+1
        pacientes.append(data)
        return pacientes

    @staticmethod
    def update_pacientes(ci,data):
        paciente = PacientesService.find_paciente(ci)
        if paciente:
            paciente.update(data)
            return paciente
        else:
            return None

    @staticmethod
    def delete_paciente(paciente):
        if paciente:
            pacientes.remove(paciente)
        return pacientes

    @staticmethod
    def delete_pacientes():
        pacientes.clear()
        return pacientes

class HTTTPResponseHandler:
    @staticmethod
    def handle_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
#---------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------
class RESTRequestHandler(BaseHTTPRequestHandler):
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
#-----------------------------------------------------------------------------------------------
#                                 Inicio de metodo GET
#-----------------------------------------------------------------------------------------------
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if self.path == "/pacientes":
            HTTTPResponseHandler.handle_response(self,200,pacientes)
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = PacientesService.find_paciente(ci)
            if paciente:
                HTTTPResponseHandler.handle_response(self,200,[paciente])
            else:
                HTTTPResponseHandler.handle_response(self,404,{"Error":"Ruta no existente"})
#----------------------------------------------------------------------------------
#                                  Query params
#----------------------------------------------------------------------------------

        elif parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_diagnostico(diagnostico)
                if pacientes_filtrados != []:
                    HTTTPResponseHandler.handle_response(self,200,pacientes_filtrados)
                else:
                    HTTTPResponseHandler.handle_response(self,204,[])
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_doctor(doctor)
                if pacientes_filtrados != []:
                    HTTTPResponseHandler.handle_response(self,200,pacientes_filtrados)
                else:
                    HTTTPResponseHandler.handle_response(self,204,[])
            else:
                HTTTPResponseHandler.handle_response(self,200,pacientes)
#-------------------------------------------------------------------------------
#                                 Metodo POST
#-------------------------------------------------------------------------------
    def do_POST(self):
        if self.path == "/pacientes":
            data=self.read_data()
            pacientes = PacientesService.add_paciente(data)
            HTTTPResponseHandler.handle_response(self,201,pacientes)
        else:
            HTTTPResponseHandler.handle_response(self,404,{"Error":"Ruta no existente"})
#-------------------------------------------------------------------------------
#                                 Metodo PUT
#-------------------------------------------------------------------------------
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            paciente = PacientesService.update_pacientes(ci,data)
            if paciente:
                HTTTPResponseHandler.handle_response(self,200,[paciente])
            else:
                HTTTPResponseHandler.handle_response(self,404,{"Error":"Paciente no encontrado"})
        else:
            HTTTPResponseHandler.handle_response(self,404,{"Error":"Ruta no existente"})
#-------------------------------------------------------------------------------
#                       Metodo DELETE
#-------------------------------------------------------------------------------
    def do_DELETE(self):
        if self.path == "/pacientes":
            pacientes = PacientesService.delete_pacientes()
            HTTTPResponseHandler.handle_response(self,200,pacientes)
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = PacientesService.find_paciente(ci)
            if paciente:
                pacientes = PacientesService.delete_paciente(paciente)
                HTTTPResponseHandler.handle_response(self,200,pacientes)
            else:
                HTTTPResponseHandler.handle_response(self,404,{"Error":"Paciente no encontrado"})
        else:
            HTTTPResponseHandler.handle_response(self,404,{"Error":"Ruta no existenete"})
#-------------------------------------------------------------------------------
#                           Lenvantando el servidor
#-------------------------------------------------------------------------------
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