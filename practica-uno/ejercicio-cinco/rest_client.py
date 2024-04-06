import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los animales por la ruta /animales
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print("-----------------------------------------------------")
print("\n---------Listamos a los animales-------------\n")
print("-----------------------------------------------------")
print(get_response.text)


# POST agrega un nuevo animal por la ruta /animales
ruta_post = url + "animales"
nuevo_animal = {
        "nombre":"guepardo",
        "especie":"terrestre",
        "genero":"hembra",
        "edad":"2",
        "peso":"90",
    }
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print("-----------------------------------------------------")
print("\n---------Agregamos un nuevo animal-------------\n")
print("-----------------------------------------------------")
print(post_response.text)


# GET obtener a todos los animales por la ruta /animales{especie}
ruta_get = url + "animales?especie=felino"
get_response = requests.request(method="GET", url=ruta_get)
print("-----------------------------------------------------")
print("\n---------Listamos animal por especie-------------\n")
print("-----------------------------------------------------")
print(get_response.text)


# GET obtener a todos los animales por la ruta /animales{genero}
ruta_get = url + "animales?genero=hembra"
get_response = requests.request(method="GET", url=ruta_get)
print("-----------------------------------------------------")
print("\n---------Listamos animal por genero-------------\n")
print("-----------------------------------------------------")
print(get_response.text)


# PUT actualiza un animal por la ruta /animales
ruta_actualizar = url + "animales/2"
animal_actualizado = {
        "nombre":"Gato",
        "especie":"felino",
        "genero":"hembra",
        "edad":"1",
        "peso":"2",
    }
put_response = requests.request(
    method="PUT", url=ruta_actualizar, 
    json=animal_actualizado
)
print("-----------------------------------------------------")
print("\n---------Actualizamos animal con id 2-------------\n")
print("-----------------------------------------------------")
print(put_response.text)


#DELETE elimina un animal por la ruta /animales{id}
ruta_eliminar = url + "animales/1"
delete_response = requests.request(method="DELETE", url=ruta_eliminar)
print("-----------------------------------------------------")
print("\n---------Elimina animal con id 1-------------\n")
print("-----------------------------------------------------")
print(delete_response.text)

