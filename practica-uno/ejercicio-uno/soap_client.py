#-------Instanciando al cliente--------------
from zeep import Client
client = Client('http://localhost:8000')

result = client.service.Suma(number_one=2,number_two=3)
print(result)

result2 = client.service.Resta(number_one=2,number_two=8)
print(result2)

result3 = client.service.Multiplicacion(number_one=2,number_two=8)
print(result3)

result4 = client.service.Division(number_one=27,number_two=3)
print(result4)
