import csv
import pymongo

# Conectarse a la base de datos MongoDB
client = pymongo.MongoClient("mongodb+srv://igna:pHf1471tlvtYcUT0@clustercorreo.ozbrffa.mongodb.net/") 
db = client["Correo"]
collection = db["Ciudades"]

# Consulta la colección Ciudades y recupera los datos
ciudades_data = collection.find({}, {"_id": 1, "nombre": 1, "provincia": 1, "cod_ciudad": 1})

# Nombre del archivo CSV de salida
csv_filename = "datos.csv"

# Abre el archivo CSV en modo escritura
with open(csv_filename, "w", encoding='utf-8', newline='') as csvfile:
    fieldnames = ["_id", "nombre", "provincia", "cod_ciudad"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Escribe el encabezado
    writer.writeheader()

    # Escribe los datos en el archivo CSV
    for ciudad in ciudades_data:
        writer.writerow(ciudad)

print(f"Los datos se han exportado a '{csv_filename}'.")
