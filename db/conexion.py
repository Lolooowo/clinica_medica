import mysql.connector
from mysql.connector import Error


class Conexion:
    def __init__(self):
        self.host = "localhost"
        self.usuario = "root"
        self.password = "root"
        self.base_datos = "clinica_medica"

    def conectar(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.password,
                database=self.base_datos
            )
            return conn
        except Error as e:
            print(f"Error de conexion: {e}")
            return None

    def probar_conexion(self):
        conn = self.conectar()
        if conn and conn.is_connected():
            conn.close()
            return True
        return False