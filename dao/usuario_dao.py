import bcrypt
from db.conexion import Conexion


class UsuarioDAO:
    def __init__(self):
        self.conexion = Conexion()

    def validar_login(self, nombre_usuario, contrasena):
        conn = self.conexion.conectar()
        if conn is None:
            return None, None, "No se pudo conectar a la base de datos"
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT u.id_usuario, u.id_personal, u.password_hash, u.activo, "
                "r.nombre_rol "
                "FROM usuario u "
                "LEFT JOIN personal_rol pr ON u.id_personal = pr.id_personal "
                "LEFT JOIN rol r ON pr.id_rol = r.id_rol "
                "WHERE u.nombre_usuario = %s",
                (nombre_usuario,)
            )
            resultado = cursor.fetchone()

            if resultado is None:
                return None, None, "Usuario o contrasena incorrectos"

            id_usuario, id_personal, password_hash, activo, rol = resultado

            if not activo:
                return None, None, "Usuario inactivo. Contacta al administrador."

            if password_hash is None:
                return None, None, "PRIMER_INGRESO"

            if bcrypt.checkpw(
                contrasena.encode('utf-8'),
                password_hash.encode('utf-8')
            ):
                return id_personal, rol, None
            else:
                return None, None, "Usuario o contrasena incorrectos"
        finally:
            cursor.close()
            conn.close()
    def configurar_password(self, nombre_usuario, contrasena):
        """Hashea y guarda la contrasena en el primer ingreso.
        Devuelve (exito, mensaje_error)."""
        conn = self.conexion.conectar()
        if conn is None:
            return False, "No se pudo conectar a la base de datos"
        cursor = conn.cursor()
        try:
            hash_bytes = bcrypt.hashpw(
                contrasena.encode('utf-8'),
                bcrypt.gensalt()
            )
            cursor.execute(
                "UPDATE usuario SET password_hash = %s "
                "WHERE nombre_usuario = %s AND password_hash IS NULL",
                (hash_bytes.decode('utf-8'), nombre_usuario)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return False, "No se encontro un usuario pendiente de configuracion."
            return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()