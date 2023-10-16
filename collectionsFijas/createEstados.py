import pymongo

mongo_uri = "mongodb+srv://igna:pHf1471tlvtYcUT0@clustercorreo.ozbrffa.mongodb.net/"

client = pymongo.MongoClient(mongo_uri)

db = client["Correo"]

estados_collection = db["Estados"]

estados_collection.delete_many({})

# Define los estados y sus descripciones
estados = [
    {"nombre": "Paquete Registrado", "descripcion": "El paquete ha sido registrado y está listo para ser enviado."},
    {"nombre": "Salió del Centro de Distribución De Origen", "descripcion": "El paquete ha salido del centro de distribución de origen."},
    {"nombre": "En Viaje", "descripcion": "El paquete está en camino hacia su destino."},
    {"nombre": "Llegó al Centro de Distribución De Destino", "descripcion": "El paquete ha llegado al centro de distribución de destino."},
    {"nombre": "Entregado", "descripcion": "El paquete ha sido entregado con éxito."},
    {"nombre": "En Sucursal a la Espera de ser Retirado", "descripcion": "El paquete se encuentra en la sucursal y está listo para ser retirado por el destinatario."}
]

# Inserta los estados en la colección "Estados"
estados_collection.insert_many(estados)

client.close()
