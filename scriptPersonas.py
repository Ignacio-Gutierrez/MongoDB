import csv
from faker import Faker
import random
from datosCarga.listasCiudades import provincias_codigos_postales

# Crear una instancia de Faker
fake = Faker()

# Número de personas a generar
num_personas = 80000

# Lista para almacenar los datos
personas = []

# Conjuntos para rastrear teléfonos, correos electrónicos y DNIs generados
telefonos_generados = set()
emails_generados = set()
dnis_generados = set()

# Función para generar un número de DNI único
def generar_dni():
    while True:
        dni = str(random.randint(10000000, 40000000))
        if dni not in dnis_generados:
            dnis_generados.add(dni)
            return dni

# Cargar ciudades desde el archivo CSV "datos.csv" y mapear _id a ciudad y provincia
ciudades = {}
with open('datos.csv', 'r', encoding='utf-8', newline='') as ciudades_file:
    reader = csv.DictReader(ciudades_file)
    for row in reader:
        ciudades[row["_id"]] = {"ciudad": row["nombre"], "provincia": row["provincia"]}

# Generar datos y almacenarlos en la lista
for _ in range(num_personas):
    nombre = fake.first_name()
    apellido = fake.last_name()
    direccion = fake.street_name()  # Generar solo el nombre de la calle sin números
    departamento = random.randint(1, 18)  # Generar un número aleatorio entre 1 y 18
    numero_casa = fake.building_number()
    
    # Generar teléfono único
    while True:
        telefono = fake.phone_number()
        if telefono not in telefonos_generados:
            telefonos_generados.add(telefono)
            break
    
    # Generar correo electrónico único
    while True:
        email = fake.email()
        if email not in emails_generados:
            emails_generados.add(email)
            break
    
    ciudad_id = random.choice(list(ciudades.keys()))  # Seleccionar un _id de ciudad aleatorio
    ciudad = ciudad_id  # Utilizar el _id de ciudad en lugar del nombre
    provincia = ciudades[ciudad_id]["provincia"]
    
    # Obtener el primer dígito del código postal de la provincia
    primer_dígito_provincia = provincias_codigos_postales.get(provincia, "0")
    
    # Generar tres dígitos aleatorios
    tres_digitos_aleatorios = str(random.randint(100, 999))
    
    codPostal = primer_dígito_provincia + tres_digitos_aleatorios
    
    dni = generar_dni()  # Generar un número de DNI único
    personas.append([nombre, apellido, direccion, departamento, numero_casa, telefono, email, ciudad, codPostal, dni])

# Guardar los datos en un archivo CSV
with open('personas.csv', 'w', encoding='utf-8',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Nombre", "Apellido", "Dirección", "Departamento", "Número de Casa", "Teléfono", "Email", "Ciudad", "CodPostal", "DNI"])
    for persona in personas:
        writer.writerow(persona)

print(f"Se han generado y guardado {num_personas} personas en el archivo personas.csv")
