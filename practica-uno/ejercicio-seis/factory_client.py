# Importamos la biblioteca requests para hacer peticiones HTTP
import requests

# Definimos la URL del servicio al que vamos a hacer la petición
url = "http://localhost:8000/animal"

# Definimos los encabezados HTTP que vamos a enviar con la petición
headers = {"Content-Type": "application/json"}

# Definimos el animal
data = {
    "id": 3,
    "especie": "mamifero",
    "nombre": "cocodrilo",
    "genero": "macho",
    "edad": 12,
    "peso": 15,
    }

# Hacemos una petición POST a la URL con los datos y encabezados definidos
response = requests.post(url, json=data, headers=headers)

if response.status_code == 201:
    print(response.text)
else:
    print("Error scheduling animal:", response.text)
