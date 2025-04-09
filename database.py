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