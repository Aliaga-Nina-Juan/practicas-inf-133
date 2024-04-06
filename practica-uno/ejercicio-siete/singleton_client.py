import requests

url = "http://localhost:8000/"

print("--------------------------------------------------")
print("----------------SE AÑADE UNA PARTIDA--------------")
print("--------------------------------------------------")
response = requests.request(
    method="POST", url=url + "partidas", json={"elemento": "piedra"}
)
print(response.text)


response = requests.request(
    method="GET",url=url+"partidas"
)
print("--------------------------------------------------")
print("-----------SE MUESTRAN LAS PARTIDAS--------------")
print("--------------------------------------------------")
print(response.text)

ruta_resultados = url + "partidas?resultado=empate"
response = requests.request(
    method="GET",url=ruta_resultados
)
print("--------------------------------------------------")
print("------SE MUESTRAN LAS PARTIDAS que DAN EMPATE------")
print("--------------------------------------------------")
print(response.text)