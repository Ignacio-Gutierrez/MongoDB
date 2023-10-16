import pymongo

mongo_uri = "mongodb+srv://igna:pHf1471tlvtYcUT0@clustercorreo.ozbrffa.mongodb.net/"

# Obtiene la lista de colecciones en la base de datos

client = pymongo.MongoClient(mongo_uri)
db = client["Correo"]

ciudades_collection = db["Ciudades"]

codigo_iata_provincias = {
    "Buenos Aires": "BA",
    "Catamarca": "CT",
    "Chaco": "CC",
    "Chubut": "CH",
    "Córdoba": "CB",
    "Corrientes": "CR",
    "Entre Ríos": "ER",
    "Formosa": "FO",
    "Jujuy": "JY",
    "La Pampa": "LP",
    "La Rioja": "LR",
    "Mendoza": "MZ",
    "Misiones": "MN",
    "Neuquén": "NQ",
    "Río Negro": "RN",
    "Salta": "SA",
    "San Juan": "SJ",
    "San Luis": "SL",
    "Santa Cruz": "SC",
    "Santa Fe": "SF",
    "Santiago del Estero": "SE",
    "Tierra del Fuego": "TF",
    "Tucumán": "TU"
}

ciudades_por_provincia = {
    "Buenos Aires": ["Buenos Aires", "La Plata", "Mar del Plata", "Bahía_Blanca"],
    "Chaco": ["Resistencia", "Barranqueras", "Presidencia Roque Sáenz Peña", "Charata"],
    "Chubut": ["Rawson", "Trelew", "Comodoro Rivadavia", "Puerto Madryn"],
    "Córdoba": ["Córdoba", "Villa María", "Río Cuarto", "San Francisco"],
    "Corrientes": ["Corrientes", "Goya", "Mercedes", "Curuzú Cuatiá"],
    "Entre Ríos": ["Paraná", "Concordia", "Gualeguaychú", "La Paz"],
    "Formosa": ["Formosa", "Clorinda", "Pirané", "Las Lomitas"],
    "Jujuy": ["San Salvador de Jujuy", "Palpalá", "San Pedro", "La Quiaca"],
    "La Pampa": ["Santa Rosa", "General Pico", "Toay", "Realicó"],
    "La Rioja": ["La Rioja", "Chilecito", "Aimogasta", "Chamical"],
    "Mendoza": ["Mendoza", "San Rafael", "Godoy Cruz", "Luján de Cuyo"],
    "Misiones": ["Posadas", "Puerto Iguazú", "Oberá", "Eldorado"],
    "Neuquén": ["Neuquén", "Cutral-Có", "Plottier", "Zapala"],
    "Río Negro": ["Viedma", "General Roca", "Cipolletti", "San Carlos de Bariloche"],
    "Salta": ["Salta", "San Ramón de la Nueva Orán", "Tartagal", "San Salvador de Jujuy"],
    "San Juan": ["San Juan", "Rawson", "Pocito", "Chimbas"],
    "San Luis": ["San Luis", "Villa Mercedes", "La Toma", "Merlo"],
    "Santa Cruz": ["Río Gallegos", "Caleta Olivia", "Pico Truncado", "El Calafate"],
    "Santa Fe": ["Santa Fe", "Rosario", "Venado Tuerto", "San Lorenzo"],
    "Santiago del Estero": ["Santiago del Estero", "La Banda", "Termas de Río Hondo", "Añatuya"],
    "Tierra del Fuego": ["Ushuaia", "Río Grande", "Tolhuin"],
    "Tucumán": ["San Miguel de Tucumán", "Yerba Buena", "Concepción", "Tafí Viejo"],
}



# Inserta las ciudades en la colección "Ciudades" junto con un ID corto que combina el código IATA y el nombre de la ciudad
for provincia, ciudades in ciudades_por_provincia.items():
    codigo_iata = codigo_iata_provincias.get(provincia, "XX")  # Obtiene el código IATA de la provincia
    for ciudad in ciudades:
        # Combina el código IATA de la provincia y una parte del nombre de la ciudad para crear un ID corto
        id_ciudad = f"{codigo_iata}_{ciudad[:3].replace(' ', '_').upper()}"
        ciudad_doc = {
            "nombre": ciudad,
            "provincia": provincia,
            "cod_ciudad": id_ciudad
        }
        ciudades_collection.insert_one(ciudad_doc)

client.close()