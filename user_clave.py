import csv
import pymongo
from pymongo import MongoClient
from concurrent.futures import ProcessPoolExecutor

# Función para cargar un usuario en MongoDB
def load_user(user_data, row_number):
    client = MongoClient("mongodb+srv://igna:pHf1471tlvtYcUT0@clustercorreo.ozbrffa.mongodb.net/")  # Cambia la URL de conexión según tu configuración
    db = client.Correo
    collection = db.Usuarios
    collection.insert_one(user_data)
    print(f"Fila {row_number}: Usuario cargado")

# Abre el archivo CSV y carga los datos en paralelo
def main():
    with open('usuarios_modificado.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        user_data_list = []
        for row_number, row in enumerate(csv_reader, 1):  # Utiliza `enumerate` para obtener el número de fila
            user_data = {
                'Nombre': row['Nombre'],
                'Apellido': row['Apellido'],
                'Teléfono': row['Teléfono'],
                'Email': row['Email'],
                'DNI': row['DNI'],
                'Contraseña': row['Contraseña'],
                'Rol': row['Rol'],
                'Paquetes': []  # Paquetes se inicializa como un array vacío
            }
            user_data_list.append(user_data)
        
        with ProcessPoolExecutor() as executor:
            executor.map(load_user, user_data_list, range(1, len(user_data_list) + 1))  # Pasa el número de fila como argumento

    print(f"{len(user_data_list)} usuarios cargados en paralelo en la colección 'Usuarios' en la base de datos 'Correo' de MongoDB.")

if __name__ == "__main__":
    main()
