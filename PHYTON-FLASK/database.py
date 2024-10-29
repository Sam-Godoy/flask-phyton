from pymongo import MongoClient
import certifi

# URI de MongoDB: Asegúrate de reemplazar `<tu_contraseña>` con tu contraseña real
MONGO_URI = 'mongodb+srv://samuelgodoy140202:<MogoIvy>@cluster0.12tnq.mongodb.net/dbb_products_app?retryWrites=true&w=majority'
ca = certifi.where()

# Conexión a la base de datos
def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["dbb_products_app"]  # Nombre de la base de datos
        return db
    except ConnectionError:
        print('Error de conexión con la base de datos')
        return None
