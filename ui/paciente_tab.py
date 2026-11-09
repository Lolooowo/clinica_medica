from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDateEdit, QComboBox, QLabel
)
from PyQt6.QtCore import QDate

from dao.paciente_dao import PacienteDAO


class PacienteTab(QWidget):
    def __init__(self):
        super().__init__()
        self.dao = PacienteDAO()
        self.id_seleccionado = None
        self.init_ui()
        self.cargar_pacientes()
        self.cargar_tipos_sangre()

    def init_ui(self):
        layout_principal = QHBoxLayout(self)

        # --- Formulario (izquierda) ---
        panel_formulario = QVBoxLayout()
        form = QFormLayout()

        self.input_nombres = QLineEdit()
        self.input_apellidos = QLineEdit()
        self.input_fecha_nac = QDateEdit()
        self.input_fecha_nac.setCalendarPopup(True)
        self.input_fecha_nac.setDate(QDate.currentDate())

        self.combo_tipo_sangre = QComboBox()
        self.combo_tipo_sangre.addItem("Sin especificar", None)

        self.input_alergias = QLineEdit()
        self.input_alergias.setPlaceholderText(
            "Ej: penicilina, polen, lactosa (separadas por coma)"
        )

        form.addRow("Nombres:", self.input_nombres)
        form.addRow("Apellidos:", self.input_apellidos)
        form.addRow("Fecha nacimiento:", self.input_fecha_nac)
        form.addRow("Tipo de sangre:", self.combo_tipo_sangre)
        form.addRow("Alergias:", self.input_alergias)

        panel_formulario.addLayout(form)

        botones = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_limpiar = QPushButton("Limpiar")

        self.btn_guardar.clicked.connect(self.guardar_paciente)
        self.btn_actualizar.clicked.connect(self.actualizar_paciente)
        self.btn_eliminar.clicked.connect(self.eliminar_paciente)
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)

        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_actualizar)
        botones.addWidget(self.btn_eliminar)
        botones.addWidget(self.btn_limpiar)
        panel_formulario.addLayout(botones)

        # --- Busqueda + tabla (derecha) ---
        panel_tabla = QVBoxLayout()
        busqueda_layout = QHBoxLayout()
        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar por nombres o apellidos...")
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_pacientes)
        busqueda_layout.addWidget(self.input_busqueda)
        busqueda_layout.addWidget(self.btn_buscar)
        panel_tabla.addLayout(busqueda_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Nombres", "Apellidos", "Fecha Nac.", "Tipo Sangre"]
        )
        self.tabla.cellClicked.connect(self.seleccionar_fila)
        panel_tabla.addWidget(self.tabla)

        layout_principal.addLayout(panel_formulario, 1)
        layout_principal.addLayout(panel_tabla, 2)

    def cargar_tipos_sangre(self):
        tipos = self.dao.listar_tipos_sangre()
        for id_tipo, nombre in tipos:
            self.combo_tipo_sangre.addItem(nombre, id_tipo)

    def cargar_pacientes(self):
        datos = self.dao.listar_todos()
        self.llenar_tabla(datos)

    def llenar_tabla(self, datos):
        self.tabla.setRowCount(0)
        for fila_idx, fila in enumerate(datos):
            self.tabla.insertRow(fila_idx)
            for col_idx, valor in enumerate(fila):
                self.tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def buscar_pacientes(self):
        texto = self.input_busqueda.text().strip()
        if texto == "":
            self.cargar_pacientes()
        else:
            datos = self.dao.buscar(texto)
            self.llenar_tabla(datos)

    def seleccionar_fila(self, fila, columna):
        self.id_seleccionado = int(self.tabla.item(fila, 0).text())
        self.input_nombres.setText(self.tabla.item(fila, 1).text())
        self.input_apellidos.setText(self.tabla.item(fila, 2).text())
        fecha_texto = self.tabla.item(fila, 3).text()
        self.input_fecha_nac.setDate(QDate.fromString(fecha_texto, "yyyy-MM-dd"))

        # Selecciona el tipo de sangre en el combo si coincide
        tipo_sangre = self.tabla.item(fila, 4).text()
        index = self.combo_tipo_sangre.findText(tipo_sangre)
        if index >= 0:
            self.combo_tipo_sangre.setCurrentIndex(index)
        else:
            self.combo_tipo_sangre.setCurrentIndex(0)

        # Carga las alergias del paciente en el campo de texto
        alergias = self.dao.listar_alergias(self.id_seleccionado)
        self.input_alergias.setText(", ".join(alergias))

    def validar_campos(self):
        if not self.input_nombres.text().strip() or not self.input_apellidos.text().strip():
            QMessageBox.warning(self, "Validacion", "Nombres y apellidos son obligatorios.")
            return False
        return True

    def procesar_alergias(self, id_paciente):
        texto = self.input_alergias.text().strip()
        alergias_actuales = self.dao.listar_alergias(id_paciente)
        alergias_nuevas = [a.strip() for a in texto.split(",") if a.strip()]

        # Eliminar las que ya no estan en el texto
        for nombre in alergias_actuales:
            if nombre not in alergias_nuevas:
                id_alergia = self.dao.buscar_o_crear_alergia(nombre)
                if id_alergia is not None:
                    self.dao.desvincular_alergia(id_paciente, id_alergia)

        # Agregar las nuevas
        for nombre in alergias_nuevas:
            id_alergia = self.dao.buscar_o_crear_alergia(nombre)
            if id_alergia is None:
                return False
            if not self.dao.vincular_alergia(id_paciente, id_alergia):
                return False
        return True

    def guardar_paciente(self):
        if not self.validar_campos():
            return
        id_tipo_sangre = self.combo_tipo_sangre.currentData()
        id_paciente = self.dao.insertar(
            self.input_nombres.text().strip(),
            self.input_apellidos.text().strip(),
            self.input_fecha_nac.date().toString("yyyy-MM-dd"),
            id_tipo_sangre
        )
        if id_paciente is None:
            QMessageBox.critical(self, "Error", "No se pudo guardar el paciente.")
            return
        if not self.procesar_alergias(id_paciente):
            QMessageBox.warning(self, "Aviso", "Paciente guardado, pero hubo un problema con las alergias.")
        else:
            QMessageBox.information(self, "Exito", "Paciente guardado correctamente.")
        self.limpiar_formulario()
        self.cargar_pacientes()

    def actualizar_paciente(self):
        if self.id_seleccionado is None:
            QMessageBox.warning(self, "Seleccion", "Selecciona un paciente de la tabla primero.")
            return
        if not self.validar_campos():
            return
        id_tipo_sangre = self.combo_tipo_sangre.currentData()
        exito = self.dao.actualizar(
            self.id_seleccionado,
            self.input_nombres.text().strip(),
            self.input_apellidos.text().strip(),
            self.input_fecha_nac.date().toString("yyyy-MM-dd"),
            id_tipo_sangre
        )
        if exito:
            if not self.procesar_alergias(self.id_seleccionado):
                QMessageBox.warning(self, "Aviso", "Paciente actualizado, pero hubo un problema con las alergias.")
            else:
                QMessageBox.information(self, "Exito", "Paciente actualizado.")
            self.limpiar_formulario()
            self.cargar_pacientes()
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar el paciente.")

    def eliminar_paciente(self):
        if self.id_seleccionado is None:
            QMessageBox.warning(self, "Seleccion", "Selecciona un paciente de la tabla primero.")
            return
        confirmacion = QMessageBox.question(
            self, "Confirmar", "Seguro que deseas eliminar este paciente?"
        )
        if confirmacion == QMessageBox.StandardButton.Yes:
            exito = self.dao.eliminar(self.id_seleccionado)
            if exito:
                QMessageBox.information(self, "Exito", "Paciente eliminado.")
                self.limpiar_formulario()
                self.cargar_pacientes()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el paciente.")

    def limpiar_formulario(self):
        self.id_seleccionado = None
        self.input_nombres.clear()
        self.input_apellidos.clear()
        self.input_fecha_nac.setDate(QDate.currentDate())
        self.combo_tipo_sangre.setCurrentIndex(0)
        self.input_alergias.clear()