from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher , SOAPHandler

def suma(number_one,number_two):
    return number_one+number_two
def resta(number_one,number_two):
    return number_one-number_two
def multiplicacion(number_one,number_two):
    return number_one*number_two
def division(number_one,number_two):
    return number_one/number_two

#------------Ruta del servidor SOAP--------------
dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)
#-----------Registramos servicios------------------
dispatcher.register_function(
    "Suma",
    suma,
    returns={"suma":int},
    args={"number_one":int,"number_two":int},
)
dispatcher.register_function(
    "Resta",
    resta,
    returns={"resta":int},
    args={"number_one":int,"number_two":int},
)
dispatcher.register_function(
    "Multiplicacion",
    multiplicacion,
    returns={"multiplicacion":int},
    args={"number_one":int,"number_two":int},
)
dispatcher.register_function(
    "Division",
    division,
    returns={"division":float},
    args={"number_one":int,"number_two":int},
)

#-----------------Iniciamos el servidor HTTP----------------
server = HTTPServer(("0.0.0.0",8000),SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciando en http://localhost:8000/")
server.serve_forever()