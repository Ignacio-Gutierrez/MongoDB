import pymongo
import csv
import os
from bson import ObjectId
from concurrent.futures import ProcessPoolExecutor

# Configura la conexión a tu base de datos MongoDB
client = pymongo.MongoClient("mongodb+srv://igna:pHf1471tlvtYcUT0@clustercorreo.ozbrffa.mongodb.net/")  # Reemplaza con la URL de tu base de datos

# Selecciona la base de datos y la colección
db = client["Correo"]
collection = db["Usuarios"]

# Función para insertar un registro en MongoDB
def insertar_registro(row, row_number):
    process_pid = os.getpid()  # Obtiene el PID del proceso actual
    print(f"PID {process_pid} - Fila {row_number} insertada.")
    
    filtro = {
        "Email": row["Email"],
        "DNI": row["DNI"],
    }
    nuevos_datos = {
        "$set": {
            "Ciudad": ObjectId(row["Ciudad"]),  # Convierte el valor en ObjectId
            "Paquetes": []  # Define "Paquetes" como un arreglo vacío
        }
    }
    
    # Actualiza los datos en la colección
    collection.update_one(filtro, nuevos_datos)
    print(f"Registro {row_number} actualizado")

# Abre el archivo CSV
with open("usuarios.csv", encoding='utf-8', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    
    # Utiliza ProcessPoolExecutor para paralelizar las actualizaciones
    with ProcessPoolExecutor() as executor:
        for row_number, row in enumerate(csv_reader, start=1):
            executor.submit(insertar_registro, row, row_number)

# Cierra la conexión a la base de datos
client.close()
