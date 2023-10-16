import random
from concurrent.futures import ProcessPoolExecutor
import os
from datetime import datetime, timedelta
import pymongo
from bson import ObjectId
import csv
from datosCarga import listasEventos

data_personas = []

# Abrimos el archivo CSV y lo leemos
with open("personas.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
            
    # Iteramos a través de las filas del CSV y las agregamos a la lista "data"
    for row in reader:
        data_personas.append(row)

def run_script(index):
        pid = os.getpid()
        print(f'Process with PID {pid} is on iteration {index}')

        # Conexión a MongoDB
        mongo_uri = "mongodb+srv://igna:pHf1471tlvtYcUT0@clustercorreo.ozbrffa.mongodb.net/"

        # Obtiene la lista de colecciones en la base de datos

        client = pymongo.MongoClient(mongo_uri)
        db = client["Correo"]




        # Elegir la primera persona al azar
        persona_1 = random.choice(data_personas)

        # Elegir la segunda persona al azar, asegurándote de que sea diferente de la primera
        persona_2 = random.choice(data_personas)
        while persona_2 == persona_1:
            persona_2 = random.choice(data_personas)

        client = pymongo.MongoClient(mongo_uri)
        db = client["Correo"]

        # Recuperar los datos de la tabla "Estados"
        estados_collection = db["Estados"]
        estados_data = estados_collection.find()  # Recupera todos los estados

        # Convertir los datos de estados a una lista de Python
        estados = list(estados_data)

        # Definir la colección "Eventos"
        eventos_collection = db["Eventos"]

        # Definir el rango de fechas
        fecha_inicial_inicio = datetime(2022, 1, 1)
        fecha_inicial_fin = datetime(2022, 12, 23)

        # Generar una fecha inicial aleatoria dentro del rango
        fecha_inicial = fecha_inicial_inicio + timedelta(days=random.randint(0, (fecha_inicial_fin - fecha_inicial_inicio).days))

        # Inicializar una lista para almacenar los datos generados
        datos = []
        horitas = []
        fechitas = []

        # Generar datos para los primeros 4 estados
        for i, estado in enumerate(estados[:4]):
            fecha_aleatoria = fecha_inicial.strftime("%Y-%m-%d")
            hora_aleatoria = "{:02d}:{:02d}".format(random.randint(0, 23), random.randint(0, 59))
            sucursal_aleatoria = random.choice(listasEventos.lista_sucursales)

            dato_evento = {
                "Fecha": datetime.strptime(fecha_aleatoria, "%Y-%m-%d"),
                "Hora": hora_aleatoria,
                "Estado": ObjectId(estado["_id"]),  # Usa ObjectId en lugar de id_estado
                "Sucursal": sucursal_aleatoria
            }

            datos.append(dato_evento)
            horitas.append(hora_aleatoria)
            fechitas.append(fecha_aleatoria)

            # Incrementar la fecha en un día
            fecha_inicial += timedelta(days=1)

        # Generar el quinto evento con un estado 5 o 6 aleatorio
        fecha_aleatoria = fecha_inicial.strftime("%Y-%m-%d")
        hora_aleatoria = "{:02d}:{:02d}".format(random.randint(0, 23), random.randint(0, 59))
        sucursal_aleatoria = random.choice(listasEventos.lista_sucursales)

        estado_final = random.choice(estados[4:6])  # Elige un estado 5 o 6 de manera aleatoria

        dato_evento_final = {
            "Fecha": datetime.strptime(fecha_aleatoria, "%Y-%m-%d"),
            "Hora": hora_aleatoria,
            "Estado": ObjectId(estado_final["_id"]),  # Usa ObjectId en lugar de id_estado
            "Sucursal": sucursal_aleatoria
        }

        datos.append(dato_evento_final)

        # Inicializa una lista para almacenar los IDs de los documentos insertados
        document_ids = []

        for dato in datos:
            inserted_event = eventos_collection.insert_one(dato)
            document_ids.append(inserted_event.inserted_id)

    ################################################################################################
    ################################################################################################

        paquetes_collection = db["Paquetes"]

        dato_paquete = {
            "Destino": {
                "id_ciudad": ObjectId(persona_1[7]),
                "codPostal": persona_1[8],
                "dirección": persona_1[2],
                "nroCasa": persona_1[4],
                "departamento": persona_1[3],
                "sucursal": "Sucursal Destino"
            },
            "Destinatario": {
                "nombre": persona_1[0],
                "apellido": persona_1[1],
                "dni": persona_1[9],
                "mail": persona_1[6],
                "teléfono": persona_1[5]
            },
            "Origen": {
                "id_ciudad": ObjectId(persona_2[7]),
                "codPostal": persona_2[8],
                "dirección": persona_2[2],
                "sucursal": "Sucursal de Origen"
            },
            "Remitente": {
                "nombre": persona_2[0],
                "apellido": persona_2[1],
                "dni": persona_2[9],
                "teléfono": persona_2[5]
            },
            "Peso": round(random.uniform(0.5, 10.0), 1),
            "FechaEnvío": {
                "Fecha": datetime.strptime(fechitas[0], "%Y-%m-%d"),
                "Hora": horitas[0]
            },
            "Dimensiones": {
                "ancho": random.randint(10, 50),
                "alto": random.randint(10, 50),
                "largo": random.randint(30, 100)
            },
            "PrecioEnvío": round(random.uniform(50.0, 200.0), 2),
            "Eventos": [(id) for id in document_ids]
            }
        
        result = paquetes_collection.insert_one(dato_paquete)

        client.close()

if __name__ == "__main__":
    num_processes = os.cpu_count()  # Obtener el número de núcleos de la CPU
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(run_script, range(100000)))