from db.conexion import Conexion
import mysql.connector


class ConsultaDAO:
    def __init__(self):
        self.conexion = Conexion()

    def listar_pacientes(self):
        """Devuelve (id, nombre_completo) de todos los pacientes."""
        conn = self.conexion.conectar()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_paciente, CONCAT(nombres, ' ', apellidos) "
            "FROM vista_pacientes ORDER BY nombres, apellidos"
        )
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def listar_medicos(self):
        """Devuelve (id, nombre_completo) solo del personal con rol Medico."""
        conn = self.conexion.conectar()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_personal, CONCAT(nombres, ' ', apellidos) "
            "FROM vista_personal "
            "WHERE LOWER(REPLACE(rol, 'á', 'a')) = 'medico' "
            "ORDER BY nombres, apellidos"
        )
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def insertar(self, id_paciente, id_medico, id_recepcion, motivo_visita):
        """Crea una consulta con la fecha/hora actual.
        Devuelve (id_consulta, error)."""
        conn = self.conexion.conectar()
        if conn is None:
            return None, "No se pudo conectar a la base de datos"
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO consulta "
                "(id_paciente, id_medico, id_recepcion, fecha_hora, motivo_visita) "
                "VALUES (%s, %s, %s, NOW(), %s)",
                (id_paciente, id_medico, id_recepcion, motivo_visita)
            )
            conn.commit()
            return cursor.lastrowid, None
        except mysql.connector.Error as e:
            conn.rollback()
            return None, e.msg
        finally:
            cursor.close()
            conn.close()
    def listar_pendientes_medico(self, id_medico):
        """Devuelve las consultas pendientes de un medico, por orden de llegada."""
        conn = self.conexion.conectar()
        if conn is None:
            return []
        cursor = conn.cursor()
        try:
            cursor.callproc('sp_consultas_pendientes', (id_medico,))
            resultados = []
            for result in cursor.stored_results():
                resultados = result.fetchall()
            return resultados
        except mysql.connector.Error as e:
            print(f"Error al llamar al procedimiento: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    def atender_consulta(self, id_consulta, diagnostico, nota, lista_receta):
        conn = self.conexion.conectar()
        if conn is None:
            return False, "No se pudo conectar a la base de datos"
        cursor = conn.cursor()
        
        try:
            # 1. Insertar los detalles de la consulta (diagnostico y nota)
            sql_detalles = """
                INSERT INTO detalles_consulta (id_consulta, diagnostico, nota_medica, fecha_atencion)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(sql_detalles, (id_consulta, diagnostico, nota))
            
            # 2. Si el médico agregó medicamentos, procesamos la receta
            if lista_receta and len(lista_receta) > 0:
                # Crear la cabecera de la receta
                cursor.execute("INSERT INTO receta (id_consulta) VALUES (%s)", (id_consulta,))
                id_receta = cursor.lastrowid # Obtenemos el ID generado
                
                # Procesar cada medicamento ingresado
                for nombre_med, dosis in lista_receta:
                    # Insertamos la receta dejando id_medicamento como NULL 
                    # y guardando el texto en la nueva columna nombre_medicamento
                    sql_detalles_receta = """
                        INSERT INTO detalles_receta (id_receta, id_medicamento, nombre_medicamento, dosis)
                        VALUES (%s, NULL, %s, %s)
                    """
                    cursor.execute(sql_detalles_receta, (id_receta, nombre_med.strip(), dosis.strip()))
                    
            conn.commit()
            return True, None
            
        except Exception as e:
            conn.rollback()
            return False, f"Error al guardar atención médica: {e}"
        finally:
            cursor.close()
            conn.close()
