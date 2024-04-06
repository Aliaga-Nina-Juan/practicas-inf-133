import requests

url = 'http://localhost:8000/'
#----------------Nuevo paciente----------
ruta_post = url + 'pacientes'
nuevo_paciente = {
    "nombre":"Wendy",
    "apellido":"Calle",
    "edad":21,
    "genero":"femenino",
    "diagnostico":"resfrio",
    "doctor":"Laime",
}
post_response = requests.request(method="POST",url=ruta_post,json=nuevo_paciente)
print("-----------------------------------------------------")
print("\n-------------Se añade un nuevo paciente----------\n")
print("-----------------------------------------------------")
print(post_response.text)

#--------------------Listamos pacientes----------------------
ruta_listar = url + 'pacientes'
listar_response = requests.request(method="GET", url=ruta_listar)
print("-----------------------------------------------------")
print("\n-------------Esta es la lista de estudiantes----------\n")
print("-----------------------------------------------------")
print(listar_response.text)

#--------------------Buscamos paciente por ci--------------
listar_por_ci = requests.request(method="GET", url=url+"pacientes/2")
print("-----------------------------------------------------")
print("\n-------------Paciente con cedula 2-------------\n")
print("-----------------------------------------------------")
print(listar_por_ci.text)

#--------------------Actualizar paciente---------------
ruta_actualizar = url +"pacientes/2"
paciente_actualizado={
    "nombre":"Juan",
    "apellido":"Perez",
    "edad":40,
    "genero":"femenino",
    "diagnostico":"diabetes",
    "doctor":"Luis",
}
put_response = requests.request(method="PUT",
                                url=ruta_actualizar,
                                json=paciente_actualizado)
print("-----------------------------------------------------")
print("\n---------Actualizamos paciente con ci 2-------------\n")
print("-----------------------------------------------------")
print(put_response.text)
#---------------Eliminamos paciente por ID---------------
ruta_eliminar = url+'pacientes/2'
response_delete = requests.request(method="DELETE",url=ruta_eliminar)
print("-----------------------------------------------------")
print("\n-----------Eliminamos al paciente 2---------------------\n")
print("-----------------------------------------------------")
print(response_delete.text)

#-------------------------Filtradno por query params----------------------
ruta_get = url + "pacientes?diagnostico=cancer"
get_response_diagnostico = requests.request(method="GET",url= ruta_get)
print("-----------------------------------------------------")
print("\n---------------Buscando paciente por diagnostico-----------------\n")
print("-----------------------------------------------------")
print(get_response_diagnostico.text)

#----------------Buscamos al paciente por el doctor que lo atendio---------
ruta_get1 = url + "pacientes?doctor=Laime"
get_response_diagnostico1 = requests.request(method="GET",url= ruta_get1)
print("-----------------------------------------------------")
print("\n----------Buscando paciente por el doctor que lo atendio--------------------\n")
print("-----------------------------------------------------")
print(get_response_diagnostico1.text)