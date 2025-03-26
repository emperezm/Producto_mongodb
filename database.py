#from pymongo import MongoClient

# URL de conexión para MongoDB en tu PC (localhost en el puerto 27017)
#MONGO_URI = "mongodb://localhost:27017/"

#def dbConnection():
    #try:
        # Crear la conexión con MongoDB
         #client = MongoClient(MONGO_URI)
        #db = client["dbb_producto"]  # Nombre de tu base de datos
        #print("✅ Conexión exitosa a MongoDB")
        #return db
    #except Exception as e:
        #print(f"❌ Error al conectar a MongoDB: {e}")
        #return None

import pyodbc

# Configurar la conexión a la base de datos SQL Server
def dbConnection():
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"  # Nombre del servidor correcto
        "DATABASE=Productos;"  # Nombre de la base de datos correcto
        "Trusted_Connection=yes;"  # Conexión segura sin usuario/contraseña
    )
    return conn

# Comprobar conexión
if __name__ == '__main__':
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print("Conectado a:", row[0])
    conn.close()