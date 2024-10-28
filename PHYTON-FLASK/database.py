from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://samuelgodoy140202:m4O9OB10s8eF3Xx0@cluster0.pvylw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
ca = certifi.where()

def dbConnection():
  try:
    client = MongoClient(MONGO_URI, tlsCAFile=ca)  # Eliminado el .connect
    db = client["dbb_products_app"]
    return db
  except ConnectionError:
    print('Error de conexión con la base de datos')
    return None
