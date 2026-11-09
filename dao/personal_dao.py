from db.conexion import Conexion
import mysql.connector


class PersonalDAO:
    def __init__(self):
        self.conexion = Conexion()

    def listar_roles(self):
        conn = self.conexion.conectar()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id_rol, nombre_rol FROM rol ORDER BY nombre_rol")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def insertar(self, nombres, apellidos, id_rol, numero_colegiado=None):
        """Inserta personal, vincula su rol y, si es medico,
        crea y vincula su numero de colegiado.
        Devuelve (id_personal, nombre_usuario, error)."""
        conn = self.conexion.conectar()
        if conn is None:
            return None, None, "No se pudo conectar a la base de datos"
        cursor = conn.cursor()
        try:
            # 1. Insertar personal
            cursor.execute(
                "INSERT INTO personal (nombres, apellidos) VALUES (%s, %s)",
                (nombres, apellidos)
            )
            id_personal = cursor.lastrowid

            # 2. Vincular rol
            cursor.execute(
                "INSERT INTO personal_rol (id_personal, id_rol) VALUES (%s, %s)",
                (id_personal, id_rol)
            )

            # 3. Si es medico, crear y vincular numero de colegiado
            if numero_colegiado is not None:
                cursor.execute(
                    "INSERT INTO numero_colegiado (numero_colegiado) VALUES (%s)",
                    (numero_colegiado,)
                )
                id_colegiado = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO personal_numero_colegiado "
                    "(id_personal, id_numero_colegiado) VALUES (%s, %s)",
                    (id_personal, id_colegiado)
                )

            conn.commit()

            # 4. Obtener el usuario que genero el trigger
            cursor.execute(
                "SELECT nombre_usuario FROM usuario WHERE id_personal = %s",
                (id_personal,)
            )
            resultado = cursor.fetchone()
            nombre_usuario = resultado[0] if resultado else None

            return id_personal, nombre_usuario, None
        except mysql.connector.Error as e:
            conn.rollback()
            return None, None, e.msg
        finally:
            cursor.close()
            conn.close()