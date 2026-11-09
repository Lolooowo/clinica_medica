from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QComboBox, QDateTimeEdit, QTextEdit, QPushButton,
    QMessageBox, QLabel, QCompleter, QFrame
)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont, QCursor

from dao.consulta_dao import ConsultaDAO


class CrearConsulta(QWidget):
    def __init__(self, volver_al_menu, ventana):
        super().__init__()
        self.dao = ConsultaDAO()
        self.volver_al_menu = volver_al_menu
        self.ventana = ventana
        self.init_ui()
        self.cargar_pacientes()
        self.cargar_medicos()

    def init_ui(self):
        # Layout principal de la pestaña
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # Encabezado
        self.lbl_titulo = QLabel("Registro de Consulta")
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
            /* Se incluye QLineEdit para el combo editable del paciente */
            QComboBox, QDateTimeEdit, QTextEdit, QLineEdit {
                border: 2px solid #E0E6ED;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background: #F8FAFC;
                color: #1E2A38;
                min-height: 25px;
            }
            QComboBox:focus, QDateTimeEdit:focus, QTextEdit:focus, QLineEdit:focus {
                border: 2px solid #0F62FE;
                background: #FFFFFF;
            }
            /* Corrección de colores en las listas desplegables */
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #1E2A38;
                selection-background-color: #0F62FE;
                selection-color: #FFFFFF;
                border: 1px solid #E0E6ED;
                border-radius: 4px;
                outline: none;
            }
        """)

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(30, 30, 30, 30)
        layout_tarjeta.setSpacing(20)

        # Formulario
        form = QFormLayout()
        form.setSpacing(15)

        # Paciente: combo editable con autocompletado
        self.combo_paciente = QComboBox()
        self.combo_paciente.setEditable(True)
        self.combo_paciente.lineEdit().setPlaceholderText("Escribe para buscar un paciente...")
        self.combo_paciente.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.combo_paciente.setCompleter(self.completer)

        # Médico
        self.combo_medico = QComboBox()
        self.combo_medico.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Fecha y hora
        self.input_fecha_hora = QDateTimeEdit(QDateTime.currentDateTime())
        self.input_fecha_hora.setCalendarPopup(True)
        self.input_fecha_hora.setDisplayFormat("dd/MM/yyyy hh:mm")
        self.input_fecha_hora.setEnabled(False) # Sigue en modo lectura

        # Motivo de visita
        self.texto_motivo = QTextEdit()
        self.texto_motivo.setPlaceholderText(
            "Describe de forma breve el motivo por el que el paciente acude a la clínica..."
        )
        self.texto_motivo.setMaximumHeight(120)

        form.addRow("Paciente:", self.combo_paciente)
        form.addRow("Médico asignado:", self.combo_medico)
        form.addRow("Fecha y hora:", self.input_fecha_hora)
        form.addRow("Motivo de visita:", self.texto_motivo)
        
        layout_tarjeta.addLayout(form)

        # Espaciador antes de los botones
        layout_tarjeta.addSpacing(10)

        # --- Botones ---
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

        self.btn_guardar = QPushButton("Guardar Consulta")
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

        self.btn_volver.clicked.connect(self.cancelar_creacion)
        self.btn_guardar.clicked.connect(self.guardar_consulta)

        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_volver)
        botones_layout.addWidget(self.btn_guardar)

        layout_tarjeta.addLayout(botones_layout)
        
        # Añadir tarjeta al layout principal
        layout_principal.addWidget(tarjeta)
        layout_principal.addStretch()

    # =========================================================
    # LÓGICA DEL NEGOCIO (Intacta)
    # =========================================================
    def cargar_pacientes(self):
        pacientes = self.dao.listar_pacientes()
        for id_paciente, nombre in pacientes:
            self.combo_paciente.addItem(nombre, id_paciente)
        self.completer.setModel(self.combo_paciente.model())

    def cargar_medicos(self):
        medicos = self.dao.listar_medicos()
        for id_medico, nombre in medicos:
            self.combo_medico.addItem(nombre, id_medico)

    def cancelar_creacion(self):
        self.limpiar_formulario()
        self.volver_al_menu()

    def guardar_consulta(self):
        # Valida que el paciente escrito exista en la lista
        index = self.combo_paciente.findText(
            self.combo_paciente.currentText(),
            Qt.MatchFlag.MatchExactly
        )
        if index == -1:
            QMessageBox.warning(self, "Validación",
                "Selecciona un paciente válido de la lista desplegable.")
            return
            
        id_paciente = self.combo_paciente.itemData(index)
        id_medico = self.combo_medico.currentData()
        motivo = self.texto_motivo.toPlainText().strip()

        if id_medico is None:
            QMessageBox.warning(self, "Validación", "Selecciona un médico.")
            return
        if motivo == "":
            QMessageBox.warning(self, "Validación", "El motivo de visita es obligatorio.")
            return

        id_recepcion = self.ventana.id_personal_sesion
        if id_recepcion is None:
            QMessageBox.warning(self, "Sesión",
                "No hay un usuario logueado. Inicia sesión primero.")
            return

        id_consulta, error = self.dao.insertar(
            id_paciente,
            id_medico,
            id_recepcion,
            motivo
        )
        if id_consulta is None:
            QMessageBox.critical(self, "Error", error)
            return

        QMessageBox.information(
            self, "Consulta Creada",
            f"Consulta registrada correctamente con el ID #{id_consulta}.\n"
            f"El paciente será atendido por orden de llegada."
        )
        self.limpiar_formulario()
        self.volver_al_menu() # Regresamos automáticamente tras guardar exitosamente

    def limpiar_formulario(self):
        self.combo_paciente.setCurrentIndex(-1)
        self.combo_paciente.clearEditText()
        self.combo_medico.setCurrentIndex(0)
        self.input_fecha_hora.setDateTime(QDateTime.currentDateTime())
        self.texto_motivo.clear()