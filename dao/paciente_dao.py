from db.conexion import Conexion
import mysql.connector


class PacienteDAO:
    def __init__(self):
        self.conexion = Conexion()

    # ---------- Tipos de sangre ----------
    def listar_tipos_sangre(self):
        conn = self.conexion.conectar()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id_tipo_sangre, tipo_sangre FROM tipo_sangre ORDER BY tipo_sangre")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    # ---------- Alergias ----------
    def buscar_o_crear_alergia(self, nombre_alergia):
        """Busca la alergia en el catalogo; si no existe, la crea.
        Devuelve el id_alergia o None si falla."""
        conn = self.conexion.conectar()
        if conn is None:
            return None
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id_alergia FROM alergia WHERE nombre_alergia = %s",
                (nombre_alergia,)
            )
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            cursor.execute(
                "INSERT INTO alergia (nombre_alergia) VALUES (%s)",
                (nombre_alergia,)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al buscar/crear alergia: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def vincular_alergia(self, id_paciente, id_alergia):
        conn = self.conexion.conectar()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            # Evita duplicados
            cursor.execute(
                "SELECT id_alergia_paciente FROM alergia_paciente "
                "WHERE id_paciente=%s AND id_alergia=%s",
                (id_paciente, id_alergia)
            )
            if cursor.fetchone():
                return True
            cursor.execute(
                "INSERT INTO alergia_paciente (id_paciente, id_alergia) VALUES (%s, %s)",
                (id_paciente, id_alergia)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al vincular alergia: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    # ---------- Pacientes ----------
    def listar_todos(self):
        conn = self.conexion.conectar()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM vista_pacientes ORDER BY apellidos, nombres"
        )
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def buscar(self, texto):
        conn = self.conexion.conectar()
        if conn is None:
            return None, "No se pudo conectar a la base de datos"
        cursor = conn.cursor()
        
        try:
            # 1. Si el texto tiene coma (viene del autocompletado)
            if "," in texto:
                partes = texto.split(",")
                nombres = partes[0].strip()
                apellidos = partes[1].strip()
                
                # Buscamos en tu vista exigiendo que coincidan ambos campos
                sql = "SELECT * FROM vista_pacientes WHERE nombres LIKE %s AND apellidos LIKE %s"
                cursor.execute(sql, (f"%{nombres}%", f"%{apellidos}%"))
                
            # 2. Si el usuario escribe libremente sin coma
            else:
                sql = "SELECT * FROM vista_pacientes WHERE nombres LIKE %s OR apellidos LIKE %s"
                cursor.execute(sql, (f"%{texto}%", f"%{texto}%"))
                
            return cursor.fetchall()
            
        except mysql.connector.Error as e:
            print(f"Error al buscar paciente: {e}")
            return None, "Error al buscar paciente: " + str(e)
        finally:
            cursor.close()
            conn.close()

    def insertar(self, nombres, apellidos, fecha_nacimiento, id_tipo_sangre=None):
        conn = self.conexion.conectar()
        if conn is None:
            return None, "No se pudo conectar a la base de datos"
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO paciente (nombres, apellidos, fecha_nacimiento) "
                "VALUES (%s, %s, %s)",
                (nombres, apellidos, fecha_nacimiento)
            )
            id_paciente = cursor.lastrowid
            if id_tipo_sangre is not None:
                cursor.execute(
                    "INSERT INTO paciente_sangre (id_paciente, id_tipo_sangre) VALUES (%s, %s)",
                    (id_paciente, id_tipo_sangre)
                )
            conn.commit()
            return id_paciente, None
        except mysql.connector.Error as e:
            conn.rollback()
            return None, e.msg
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, id_paciente, nombres, apellidos, fecha_nacimiento, id_tipo_sangre=None):
        conn = self.conexion.conectar()
        if conn is None:
            return False, "No se pudo conectar a la base de datos"
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE paciente SET nombres=%s, apellidos=%s, fecha_nacimiento=%s "
                "WHERE id_paciente=%s",
                (nombres, apellidos, fecha_nacimiento, id_paciente)
            )
            if id_tipo_sangre is not None:
                cursor.execute(
                    "SELECT id_paciente_sangre FROM paciente_sangre WHERE id_paciente=%s",
                    (id_paciente,)
                )
                if cursor.fetchone():
                    cursor.execute(
                        "UPDATE paciente_sangre SET id_tipo_sangre=%s WHERE id_paciente=%s",
                        (id_tipo_sangre, id_paciente)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO paciente_sangre (id_paciente, id_tipo_sangre) "
                        "VALUES (%s, %s)",
                        (id_paciente, id_tipo_sangre)
                    )
            conn.commit()
            return True, None
        except mysql.connector.Error as e:
            conn.rollback()
            # Aqui llega el error del trigger (SIGNAL 45000, errno 1644)
            return False, e.msg
        finally:
            cursor.close()
            conn.close()

    def eliminar(self, id_paciente):
        conn = self.conexion.conectar()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM paciente WHERE id_paciente=%s", (id_paciente,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    def listar_alergias(self, id_paciente):
        conn = self.conexion.conectar()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute(
            "SELECT a.nombre_alergia "
            "FROM alergia_paciente ap "
            "JOIN alergia a ON ap.id_alergia = a.id_alergia "
            "WHERE ap.id_paciente = %s "
            "ORDER BY a.nombre_alergia",
            (id_paciente,)
        )
        resultados = [fila[0] for fila in cursor.fetchall()]
        cursor.close()
        conn.close()
        return resultados
    def desvincular_alergia(self, id_paciente, id_alergia):
        conn = self.conexion.conectar()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM alergia_paciente "
                "WHERE id_paciente=%s AND id_alergia=%s",
                (id_paciente, id_alergia)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al desvincular alergia: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    def obtener_paciente(self, id_paciente):
        conn = self.conexion.conectar()
        if conn is None:
            return None
        cursor = conn.cursor()
        cursor.execute(
            "SELECT *"
            "FROM vista_pacientes "
            "WHERE id_paciente = %s",
            (id_paciente,)
        )
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado

    def obtener_historial(self, id_paciente):
        conn = self.conexion.conectar()
        if conn is None:
            return None, "No se pudo conectar a la base de datos"
        cursor = conn.cursor()
        try:
            # Consultamos tu vista y ordenamos de la consulta más reciente a la más antigua
            sql = "SELECT * FROM vista_historial_paciente WHERE id_paciente = %s ORDER BY fecha_consulta DESC"
            cursor.execute(sql, (id_paciente,))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener el historial médico: {e}")
            return []
        finally:
            cursor.close()
            conn.close()