import requests

#Definir la consulta GraphQL
query_actualizar = """
mutation{
        actualizarPlanta(id: 2,nombre: "frutilla", especie: "Fregaria",edad: 6,altura: 50,frutos:false){
            planta{
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""
# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

#Solicitud POST al servidor GraphQL
response = requests.post(url,json={'query':query_actualizar})
print(response.text)

query_listar = """
{
    plantas{
        id
        nombre
        especie
        edad 
        altura
        frutos
    }
}
"""

response_listar = requests.post(url,json={'query':query_listar})
print(response_listar.text)