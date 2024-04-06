import requests

url = "http://localhost:8000/paciente"
headers = {'Content-type': 'application/json'}

mi_pizza = {
    "ci": "Grande",
    "nombre": "Delgada",
    "apellido": "Delgada",
    "edad": "Delgada",
    "genero": "Delgada",
    "diagnostico": "Delgada",
    "doctor": "Delgada"
}
response = requests.post(url, json=mi_pizza, headers=headers)
print(response.json())