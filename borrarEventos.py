import pymongo
from bson import ObjectId

# Establece la conexión a la base de datos MongoDB
client = pymongo.MongoClient("mongodb+srv://igna:pHf1471tlvtYcUT0@clustercorreo.ozbrffa.mongodb.net/")  # Cambia la URL y el puerto según tu configuración

db = client["Correo"]
paquetes_collection = db["Paquetes"]
eventos_collection = db["Eventos"]

# Obtén todos los ObjectIds de eventos en la colección "Eventos"
eventos_ids = set(evento["_id"] for evento in eventos_collection.find({}, {"_id": 1}))

# Obtén todos los ObjectIds de eventos referenciados en los paquetes
eventos_referenciados = set()
for paquete in paquetes_collection.find({"Eventos": {"$exists": True}}):
    eventos_referenciados.update(paquete["Eventos"])

# Encuentra los eventos que no están referenciados en ningún paquete
eventos_no_referenciados = [evento_id for evento_id in eventos_ids if evento_id not in eventos_referenciados]

# Elimina los eventos no referenciados
for evento_id in eventos_no_referenciados:
    eventos_collection.delete_one({"_id": evento_id})
    print(f"Evento con ID {evento_id} ha sido eliminado.")

# Cierra la conexión a la base de datos
client.close()