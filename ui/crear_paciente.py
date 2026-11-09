from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QPushButton, QDateEdit, QComboBox, QMessageBox, QLabel, QFrame
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont, QCursor

from dao.paciente_dao import PacienteDAO


class CrearPaciente(QWidget):
    def __init__(self, volver_al_menu):
        super().__init__()
        self.dao = PacienteDAO()
        self.volver_al_menu = volver_al_menu
        self.id_editando = None 
        self.init_ui()
        self.cargar_tipos_sangre()

    def init_ui(self):
        # Layout principal de la pestaña
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # Encabezado dinámico
        self.lbl_titulo = QLabel("Registro de Paciente")
        self.lbl_titulo.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.lbl_titulo.setStyleSheet("color: #1E2A38;")
        layout_principal.addWidget(self.lbl_titulo)

        # --- Tarjeta del Formulario ---
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjetaForm")
        tarjeta.setStyleSheet("""
            QFrame#tarjetaForm {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E6ED;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2C3E50;
                border: none;
            }
            QLineEdit, QDateEdit, QComboBox {
                border: 2px solid #E0E6ED;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background: #F8FAFC;
                color: #1E2A38;
                min-height: 25px;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border: 2px solid #0F62FE;
                background: #FFFFFF;
            }
            
            /* --- SOLUCIÓN TIPO DE SANGRE (Opciones del ComboBox) --- */
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #1E2A38;
                selection-background-color: #0F62FE;
                selection-color: #FFFFFF;
                border: 1px solid #E0E6ED;
                border-radius: 4px;
                outline: none;
            }""")

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(30, 30, 30, 30)
        layout_tarjeta.setSpacing(20)

        # Formulario
        form = QFormLayout()
        form.setSpacing(15)

        self.input_nombres = QLineEdit()
        self.input_nombres.setPlaceholderText("Ej: Juan Carlos")
        
        self.input_apellidos = QLineEdit()
        self.input_apellidos.setPlaceholderText("Ej: Gómez López")
        
        self.input_fecha_nac = QDateEdit()
        self.input_fecha_nac.setCalendarPopup(True)
        self.input_fecha_nac.setDate(QDate.currentDate())
        
        self.combo_tipo_sangre = QComboBox()
        self.combo_tipo_sangre.addItem("Sin especificar", None)
        self.combo_tipo_sangre.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.input_alergias = QLineEdit()
        self.input_alergias.setPlaceholderText("Ej: penicilina, polen (separadas por coma)")

        form.addRow("Nombres:", self.input_nombres)
        form.addRow("Apellidos:", self.input_apellidos)
        form.addRow("Fecha de nacimiento:", self.input_fecha_nac)
        form.addRow("Tipo de sangre:", self.combo_tipo_sangre)
        form.addRow("Alergias conocidas:", self.input_alergias)
        
        layout_tarjeta.addLayout(form)

        # Espaciador antes de los botones
        layout_tarjeta.addSpacing(10)

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(15)

        self.btn_volver = QPushButton("Cancelar / Volver")
        self.btn_volver.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #F8FAFC;
                color: #2C3E50;
                border: 2px solid #E0E6ED;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E0E6ED; }
            QPushButton:pressed { background-color: #CBD5E1; }
        """)

        self.btn_guardar = QPushButton("Guardar Paciente")
        self.btn_guardar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #0F62FE;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0050E6; }
            QPushButton:pressed { background-color: #1E2A38; }
        """)

        self.btn_volver.clicked.connect(self.cancelar_edicion)
        self.btn_guardar.clicked.connect(self.guardar_paciente)

        # Añadir botones al layout (alineados a la derecha)
        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_volver)
        botones_layout.addWidget(self.btn_guardar)

        layout_tarjeta.addLayout(botones_layout)
        
        # Añadir tarjeta al layout principal y empujar hacia arriba
        layout_principal.addWidget(tarjeta)
        layout_principal.addStretch()

    def cargar_tipos_sangre(self):
        tipos = self.dao.listar_tipos_sangre()
        for id_tipo, nombre in tipos:
            self.combo_tipo_sangre.addItem(nombre, id_tipo)

    def cancelar_edicion(self):
        """Limpia el formulario y vuelve al menú."""
        self.limpiar_formulario()
        self.volver_al_menu()

    def cargar_paciente(self, id_paciente):
        """Carga los datos de un paciente para editarlo y cambia el título."""
        datos = self.dao.obtener_paciente(id_paciente)
        if datos is None:
            QMessageBox.warning(self, "Error", "No se encontró el paciente.")
            return
        
        self.id_editando = datos[0]
        self.lbl_titulo.setText("Editar Paciente")
        self.btn_guardar.setText("Actualizar Paciente")
        
        self.input_nombres.setText(datos[1])
        self.input_apellidos.setText(datos[2])
        self.input_fecha_nac.setDate(QDate.fromString(str(datos[3]), "yyyy-MM-dd"))

        # Selecciona el tipo de sangre en el combo
        index = self.combo_tipo_sangre.findText(datos[4])
        if index >= 0:
            self.combo_tipo_sangre.setCurrentIndex(index)
        else:
            self.combo_tipo_sangre.setCurrentIndex(0)

        # Carga las alergias
        alergias = datos[5]
        if alergias == "Sin alergias":
            self.input_alergias.clear()
        else:
            self.input_alergias.setText(alergias)

    def guardar_paciente(self):
        if not self.input_nombres.text().strip() or not self.input_apellidos.text().strip():
            QMessageBox.warning(self, "Validación", "Nombres y apellidos son obligatorios.")
            return

        id_tipo_sangre = self.combo_tipo_sangre.currentData()

        if self.id_editando is not None:
            # MODO EDICION
            exito, error = self.dao.actualizar(
                self.id_editando,
                self.input_nombres.text().strip(),
                self.input_apellidos.text().strip(),
                self.input_fecha_nac.date().toString("yyyy-MM-dd"),
                id_tipo_sangre
            )
            if not exito:
                QMessageBox.critical(self, "Error de validación", error)
                return
            self.procesar_alergias(self.id_editando)
            QMessageBox.information(self, "Éxito", "Paciente actualizado correctamente.")
        else:
            # MODO CREACION
            id_paciente, error = self.dao.insertar(
                self.input_nombres.text().strip(),
                self.input_apellidos.text().strip(),
                self.input_fecha_nac.date().toString("yyyy-MM-dd"),
                id_tipo_sangre
            )
            if id_paciente is None:
                QMessageBox.critical(self, "Error de validación", error)
                return
            self.procesar_alergias(id_paciente)
            QMessageBox.information(self, "Éxito", "Paciente guardado correctamente.")

        self.limpiar_formulario()

    def procesar_alergias(self, id_paciente):
        texto = self.input_alergias.text().strip()
        alergias_actuales = self.dao.listar_alergias(id_paciente)
        alergias_nuevas = [a.strip().lower() for a in texto.split(",") if a.strip()]

        for nombre in alergias_actuales:
            if nombre not in alergias_nuevas:
                id_alergia = self.dao.buscar_o_crear_alergia(nombre)
                if id_alergia is not None:
                    self.dao.desvincular_alergia(id_paciente, id_alergia)

        for nombre in alergias_nuevas:
            id_alergia = self.dao.buscar_o_crear_alergia(nombre)
            if id_alergia is not None:
                self.dao.vincular_alergia(id_paciente, id_alergia)
                
    def limpiar_formulario(self):
        self.id_editando = None 
        self.lbl_titulo.setText("Registro de Paciente")
        self.btn_guardar.setText("Guardar Paciente")
        self.input_nombres.clear()
        self.input_apellidos.clear()
        self.input_fecha_nac.setDate(QDate.currentDate())
        self.combo_tipo_sangre.setCurrentIndex(0)
        self.input_alergias.clear()